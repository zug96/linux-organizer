#!/bin/bash

# --- Script Organizador de Arquivos V3 ---
# Organiza arquivos de múltiplos diretórios de origem, recursivamente, com LOGGING.

# --- Configurações ---
# Arquivo de Log (será criado em ~/Scripts/organizador.log)
LOG_FILE="$HOME/Scripts/organizador.log"

# Define os diretórios de *destino*
IMAGE_DIR="$HOME/Imagens"
DOC_DIR="$HOME/Documentos"
VIDEO_DIR="$HOME/Videos"
MUSIC_DIR="$HOME/Musicas"
SCRIPT_DIR="$HOME/Scripts"
OTHER_DIR="$HOME/Outros"

# Define os diretórios de *origem* a serem verificados
SOURCE_DIRS=(
    "$HOME/Downloads"
    "$HOME/Área de trabalho"
    # Adicione outros diretórios aqui se desejar
)

# --- Funções ---
# Função para registrar mensagens no arquivo de log com data/hora
log_message() {
    # Formato do Timestamp: YYYY-MM-DD HH:MM:SS
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# --- Início do Script ---

# Cria os diretórios de destino se não existirem
mkdir -p "$IMAGE_DIR" "$DOC_DIR" "$VIDEO_DIR" "$MUSIC_DIR" "$SCRIPT_DIR" "$OTHER_DIR"

# Cria o arquivo de log se não existir (apenas para garantir) e registra o início
touch "$LOG_FILE"
echo "" >> "$LOG_FILE" # Linha em branco para separar execuções no log
log_message "=============================================="
log_message "Iniciando execução do script organizador..."
log_message "Diretórios de origem: ${SOURCE_DIRS[*]}"
log_message "Arquivo de log: $LOG_FILE"
log_message "=============================================="


# Loop através de cada diretório de origem
for source_dir in "${SOURCE_DIRS[@]}"; do
    log_message "--- Verificando diretório: '$source_dir' ---"

    if [ ! -d "$source_dir" ]; then
      log_message "AVISO: Diretório de origem '$source_dir' não encontrado. Pulando."
      continue
    fi

    # Loop para encontrar arquivos recursivamente
    find "$source_dir" -type f -print0 | while IFS= read -r -d $'\0' file; do
        filename=$(basename "$file")
        current_dir=$(dirname "$file")

        # --- VERIFICAÇÃO DE SEGURANÇA (Já estava no V2) ---
        is_in_target_or_scripts=false
        if [[ "$current_dir/" == "$IMAGE_DIR/"* || \
              "$current_dir/" == "$DOC_DIR/"* || \
              "$current_dir/" == "$VIDEO_DIR/"* || \
              "$current_dir/" == "$MUSIC_DIR/"* || \
              "$current_dir/" == "$SCRIPT_DIR/"* || \
              "$current_dir/" == "$OTHER_DIR/"* ]]; then
             is_in_target_or_scripts=true
        fi

        if ! $is_in_target_or_scripts; then
            extension="${filename##*.}"
            if [[ "$filename" == *"."* && "$filename" != "."* ]]; then
                extension_lower="${extension,,}"
            else
                extension_lower=""
            fi

            log_message "Processando: '$filename' (Local: '$current_dir')" # Ação principal registrada

            target_dir=""

            case "$extension_lower" in
                sh|py) target_dir="$SCRIPT_DIR" ;;
                jpg|jpeg|png|gif|bmp|svg|webp|heic|avif) target_dir="$IMAGE_DIR" ;;
                pdf|doc|docx|txt|odt|rtf|md|epub) target_dir="$DOC_DIR" ;;
                xls|xlsx|ods|csv) target_dir="$DOC_DIR" ;;
                ppt|pptx|odp) target_dir="$DOC_DIR" ;;
                mp4|avi|mkv|mov|wmv|flv|webm) target_dir="$VIDEO_DIR" ;;
                mp3|wav|flac|ogg|aac|m4a) target_dir="$MUSIC_DIR" ;;
                zip|rar|tar|gz|7z|bz2|iso|img) log_message "  -> IGNORANDO: Arquivo compactado/imagem '$filename'"; continue ;;
                deb|appimage) log_message "  -> IGNORANDO: Arquivo instalador '$filename'"; continue ;;
                "") log_message "  -> IGNORANDO: Arquivo sem extensão ou oculto '$filename'"; continue ;;
                 *) target_dir="$OTHER_DIR" ;;
            esac

            if [ -n "$target_dir" ]; then
                 mkdir -p "$target_dir"
                 # Tenta mover o arquivo (-n não sobrescreve)
                 mv -n "$file" "$target_dir/"
                 if [ $? -eq 0 ]; then # Verifica se o 'mv' deu certo (exit code 0)
                     log_message "  -> SUCESSO: Movido '$filename' de '$current_dir' para '$target_dir'"
                 else
                     log_message "  -> ERRO: Falha ao mover '$filename' para '$target_dir'. Arquivo já existe no destino ou permissão negada?"
                 fi
            fi
        # else # Opcional: Logar arquivos ignorados por estarem no destino
             # log_message "Ignorando: '$filename' (já está em dir. destino/scripts)."
        fi # Fim do if ! is_in_target_or_scripts
    done # Fim do loop while read file
done # Fim do loop for source_dir

log_message "=============================================="
log_message "Execução do script concluída."
log_message "=============================================="

exit 0 # Termina o script com sucesso
