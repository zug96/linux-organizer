#!/bin/bash

# --- Script Organizador de Arquivos V1 ---

# Define os diretórios
# Usamos "$HOME" para pegar o diretório pessoal do usuário atual
SOURCE_DIR="$HOME/Downloads"
IMAGE_DIR="$HOME/Imagens"
DOC_DIR="$HOME/Documentos"
VIDEO_DIR="$HOME/Videos"
MUSIC_DIR="$HOME/Musicas"
CODING_DIR="$HOME/Scripts"
OTHER_DIR="$HOME/Outros" # Para onde vai o que não for reconhecido

echo "-------------------------------------------"
echo "Iniciando organização da pasta $SOURCE_DIR..."
echo "-------------------------------------------"

# Verifica se o diretório de origem existe
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Erro: Diretório de origem '$SOURCE_DIR' não encontrado."
  exit 1
fi

# Loop para encontrar apenas ARQUIVOS (-type f) diretamente dentro de SOURCE_DIR
# -maxdepth 1 evita que ele entre em subpastas dentro de Downloads
find "$SOURCE_DIR" -maxdepth 1 -type f | while read -r file; do
    # Pega apenas o nome do arquivo (sem o caminho)
    filename=$(basename "$file")
    # Pega a extensão do arquivo
    extension="${filename##*.}"
    # Converte a extensão para minúsculas para facilitar a comparação (requer Bash 4+)
    extension_lower="${extension,,}"

    echo "Processando: '$filename' (Extensão: .$extension_lower)"

    # Move o arquivo baseado na extensão
    target_dir="" # Variável para guardar o diretório de destino

    case "$extension_lower" in
        jpg|jpeg|png|gif|bmp|svg|webp|heic|avif)
            target_dir="$IMAGE_DIR"
            ;;
        pdf|doc|docx|txt|odt|rtf|md|epub)
            target_dir="$DOC_DIR"
            ;;
        xls|xlsx|ods|csv)
            target_dir="$DOC_DIR" # Planilhas também vão para Documentos
             ;;
        ppt|pptx|odp)
            target_dir="$DOC_DIR" # Apresentações também vão para Documentos
            ;;
        mp4|avi|mkv|mov|wmv|flv|webm)
            target_dir="$VIDEO_DIR"
            ;;
        mp3|wav|flac|ogg|aac|m4a)
            target_dir="$MUSIC_DIR"
            ;;
        sh|py)
            target_dir="$CODING_DIR"
            ;;
        zip|rar|tar|gz|7z|bz2|iso|img)
             # Arquivos compactados ou imagens de disco podem ir para Outros ou Downloads mesmo
             # target_dir="$OTHER_DIR"
             echo "  -> Ignorando arquivo compactado/imagem: '$filename'"
             continue # Pula para o próximo arquivo no loop
             ;;
         deb|appimage)
             # Instaladores podem ir para Outros ou Downloads
             # target_dir="$OTHER_DIR"
             echo "  -> Ignorando arquivo instalador: '$filename'"
             continue # Pula para o próximo arquivo no loop
             ;;
        *) # Caso não se encaixe em nenhuma das extensões acima
            target_dir="$OTHER_DIR"
            ;;
    esac

    # Se um diretório de destino foi definido, tenta mover
    if [ -n "$target_dir" ]; then
        # Cria o diretório de destino se ele não existir (caso tenha sido apagado)
         mkdir -p "$target_dir"
        # Tenta mover o arquivo
        mv -n "$file" "$target_dir/" # O -n evita sobrescrever arquivos com mesmo nome no destino
        if [ $? -eq 0 ]; then # Verifica se o comando mv foi bem sucedido
            echo "  -> Movido para '$target_dir'"
        else
            echo "  -> ERRO ao mover '$filename' para '$target_dir'. Talvez já exista?"
        fi
    fi

done

echo "-------------------------------------------"
echo "Organização concluída!"
echo "-------------------------------------------"
