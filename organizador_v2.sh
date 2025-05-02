#!/bin/bash

# --- Script Organizador de Arquivos V2 ---
# Organiza arquivos de múltiplos diretórios de origem, recursivamente.

# --- Diretórios ---
# Define os diretórios de *destino*
IMAGE_DIR="$HOME/Imagens"
DOC_DIR="$HOME/Documentos"
VIDEO_DIR="$HOME/Videos"
MUSIC_DIR="$HOME/Musicas"
CODING_DIR="$HOME/Scripts" # Diretório adicionado pelo usuário
OTHER_DIR="$HOME/Outros"   # Para onde vai o que não for reconhecido

# Cria os diretórios de destino se não existirem
mkdir -p "$IMAGE_DIR" "$DOC_DIR" "$VIDEO_DIR" "$MUSIC_DIR" "$CODING_DIR" "$OTHER_DIR"

# --- Diretórios de ORIGEM ---
# Edite esta lista para incluir as pastas onde você quer procurar por arquivos.
# CUIDADO: Não coloque os diretórios de DESTINO aqui!
SOURCE_DIRS=(
    "$HOME/Downloads"
    "$HOME/Área de trabalho"
    # Adicione outros diretórios aqui se desejar, por exemplo:
    # "$HOME/Documentos_Temporarios"
)

echo "=============================================="
echo "Iniciando organização recursiva..."
echo "=============================================="

# Loop através de cada diretório de origem definido na lista SOURCE_DIRS
for source_dir in "${SOURCE_DIRS[@]}"; do
    echo # Linha em branco para separar seções
    echo "--- Verificando diretório: '$source_dir' ---"

    # Verifica se o diretório de origem realmente existe
    if [ ! -d "$source_dir" ]; then
      echo "Aviso: Diretório de origem '$source_dir' não encontrado. Pulando."
      continue # Pula para o próximo diretório na lista SOURCE_DIRS
    fi

    # Loop para encontrar apenas ARQUIVOS (-type f) dentro do diretório de origem ATUAL, recursivamente
    # Usamos -print0 e read -d $'\0' para lidar corretamente com nomes de arquivo complexos (com espaços, etc.)
    find "$source_dir" -type f -print0 | while IFS= read -r -d $'\0' file; do
        filename=$(basename "$file")
        current_dir=$(dirname "$file") # Diretório onde o arquivo está atualmente

        # --- VERIFICAÇÃO DE SEGURANÇA ---
        # Ignora arquivos que já estão nos diretórios de destino ou no diretório de scripts
        is_in_target_or_scripts=false
        # Verifica se o diretório atual começa com algum dos diretórios de destino/scripts
        # Usamos %/* para remover o nome do arquivo e comparar apenas diretórios
        # Adicionamos / ao final dos DIRS para garantir comparação de diretório completo
        # Ex: evitar que /home/user/Documentos_Backup seja confundido com /home/user/Documentos
        if [[ "$current_dir/" == "$IMAGE_DIR/"* || \
              "$current_dir/" == "$DOC_DIR/"* || \
              "$current_dir/" == "$VIDEO_DIR/"* || \
              "$current_dir/" == "$MUSIC_DIR/"* || \
              "$current_dir/" == "$CODING_DIR/"* || \
              "$current_dir/" == "$OTHER_DIR/"* ]]; then
             is_in_target_or_scripts=true
             # echo "  -> Ignorando '$filename' (em '$current_dir'). Já está em dir. destino/scripts." # Descomente para depurar
        fi

        # Só processa o arquivo se ele NÃO estiver em um diretório de destino/scripts
        if ! $is_in_target_or_scripts; then
            extension="${filename##*.}"
            # Verifica se realmente há uma extensão (evita arquivos como '.bashrc')
            if [[ "$filename" == *"."* && "$filename" != "."* ]]; then
                extension_lower="${extension,,}"
            else
                extension_lower="" # Sem extensão ou arquivo oculto
            fi

            echo "Processando: '$filename' (em '$current_dir' - Ext: .$extension_lower)"

            target_dir="" # Resetar diretório alvo para cada arquivo

            case "$extension_lower" in
                sh|py)
                    target_dir="$CODING_DIR"
                    ;;
                jpg|jpeg|png|gif|bmp|svg|webp|heic|avif)
                    target_dir="$IMAGE_DIR"
                    ;;
                pdf|doc|docx|txt|odt|rtf|md|epub)
                    target_dir="$DOC_DIR"
                    ;;
                xls|xlsx|ods|csv)
                    target_dir="$DOC_DIR"
                    ;;
                ppt|pptx|odp)
                    target_dir="$DOC_DIR"
                    ;;
                mp4|avi|mkv|mov|wmv|flv|webm)
                    target_dir="$VIDEO_DIR"
                    ;;
                mp3|wav|flac|ogg|aac|m4a)
                    target_dir="$MUSIC_DIR"
                    ;;
                zip|rar|tar|gz|7z|bz2|iso|img)
                    echo "  -> Ignorando arquivo compactado/imagem: '$filename'"
                    continue # Pula para o próximo arquivo
                    ;;
                 deb|appimage)
                    echo "  -> Ignorando arquivo instalador: '$filename'"
                    continue # Pula para o próximo arquivo
                    ;;
                 "" ) # Arquivos sem extensão ou ocultos (extensão vazia após tratamento)
                    echo "  -> Ignorando arquivo sem extensão ou oculto: '$filename'"
                    continue # Pula para o próximo arquivo
                    ;;
                 *) # Extensão não reconhecida E não vazia/oculta
                    target_dir="$OTHER_DIR"
                    ;;
            esac

            # Se um diretório de destino foi definido, move o arquivo
            if [ -n "$target_dir" ]; then
                 # Cria o diretório de destino (redundante se já criado no início, mas seguro)
                 mkdir -p "$target_dir"
                # Tenta mover o arquivo
                mv -n "$file" "$target_dir/"
                if [ $? -eq 0 ]; then
                    echo "  -> Movido para '$target_dir'"
                else
                    echo "  -> ERRO ao mover '$filename' para '$target_dir'. Talvez já exista?"
                fi
            fi
        fi # Fim do if ! is_in_target_or_scripts
    done # Fim do loop while read file
done # Fim do loop for source_dir

echo "=============================================="
echo "Organização concluída!"
echo "=============================================="
