#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organizador de Arquivos Automático v1.1.1 (Python)

Organiza arquivos de diretórios de origem para pastas de destino
categorizadas por tipo de arquivo. Inclui logging e ignora
arquivos .desktop na Área de trabalho (nome corrigido).
"""

import shutil
import logging
from pathlib import Path
from datetime import datetime

# --- Configurações ---

# Diretórios de Origem (use Path para caminhos)
# Pegar o diretório home do usuário atual
HOME_DIR = Path.home()
# *** CORREÇÃO APLICADA AQUI ***
DESKTOP_DIR_NAME = "Área de trabalho" # Nome correto do diretório
SOURCE_DIRS = [
    HOME_DIR / "Downloads",
    HOME_DIR / DESKTOP_DIR_NAME, # Usando a variável com nome correto
    # Adicione outros diretórios aqui se desejar
]

# Diretórios de Destino (Mapeamento Nome Categoria -> Caminho)
DEST_DIRS = {
    "Imagens": HOME_DIR / "Imagens",
    "Documentos": HOME_DIR / "Documentos",
    "Videos": HOME_DIR / "Videos",
    "Musicas": HOME_DIR / "Musicas",
    "Scripts": HOME_DIR / "Scripts",
    "Outros": HOME_DIR / "Outros"
}

# Mapeamento Extensão (minúscula) -> Nome Categoria (chave de DEST_DIRS)
EXT_MAP = {
    # Imagens
    '.jpg': "Imagens", '.jpeg': "Imagens", '.png': "Imagens", '.gif': "Imagens",
    '.bmp': "Imagens", '.svg': "Imagens", '.webp': "Imagens", '.heic': "Imagens",
    '.avif': "Imagens",
    # Documentos
    '.pdf': "Documentos", '.doc': "Documentos", '.docx': "Documentos",
    '.txt': "Documentos", '.odt': "Documentos", '.rtf': "Documentos",
    '.md': "Documentos", '.epub': "Documentos", '.xls': "Documentos",
    '.xlsx': "Documentos", '.ods': "Documentos", '.csv': "Documentos",
    '.ppt': "Documentos", '.pptx': "Documentos", '.odp': "Documentos",
    # Vídeos
    '.mp4': "Videos", '.avi': "Videos", '.mkv': "Videos", '.mov': "Videos",
    '.wmv': "Videos", '.flv': "Videos", '.webm': "Videos",
    # Músicas
    '.mp3': "Musicas", '.wav': "Musicas", '.flac': "Musicas", '.ogg': "Musicas",
    '.aac': "Musicas", '.m4a': "Musicas",
    # Scripts
    '.sh': "Scripts", '.py': "Scripts", '.js': "Scripts", '.rb': "Scripts",
    # Adicione mais extensões e categorias aqui
}

# Extensões a serem IGNORADAS (minúsculas) - Usando um set para eficiência
IGNORED_EXTENSIONS = {
    '.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', # Compactados
    '.iso', '.img',                               # Imagens de disco
    '.deb', '.appimage',                          # Instaladores
    '.part', '.crdownload', '.tmp',               # Arquivos temporários/incompletos
}

# Arquivo de Log
# Cria a pasta Scripts se não existir, antes de definir o LOG_FILE
scripts_dir = HOME_DIR / "Scripts"
scripts_dir.mkdir(parents=True, exist_ok=True)
LOG_FILE = scripts_dir / "organizador_py.log"

# --- Configuração do Logging ---
# Configura para logar tanto no arquivo quanto no console
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_level = logging.INFO # Nível de detalhe (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Handler para o arquivo
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(log_formatter)

# Handler para o console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# Pega o logger raiz e adiciona os handlers
logger = logging.getLogger()
logger.setLevel(log_level)
# Remove handlers antigos (caso o script seja re-executado no mesmo processo)
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# --- Funções Auxiliares ---

def check_if_in_dest_dir(file_path: Path, dest_dirs_paths: list) -> bool:
    """Verifica se o arquivo já está dentro de algum dos diretórios de destino ou scripts."""
    try:
        # Compara o caminho pai do arquivo com os caminhos de destino
        for dest_path in dest_dirs_paths:
             # Usar resolve() para obter caminhos absolutos canônicos pode ajudar na comparação
            if file_path.parent.resolve() == dest_path.resolve() or \
               file_path.parent.resolve().is_relative_to(dest_path.resolve()):
                return True
        # Verifica também se está na pasta de scripts
        if file_path.parent.resolve() == scripts_dir.resolve():
             return True
    except Exception as e:
        logger.debug(f"Erro não crítico ao verificar parentesco de '{file_path}': {e}")
    return False

# --- Lógica Principal ---

if __name__ == "__main__":
    logger.info("==============================================")
    logger.info("--- Iniciando Script Organizador Python v1.1.1 ---")
    logger.info(f"Diretórios de Origem: {[str(d) for d in SOURCE_DIRS]}")
    logger.info("==============================================")

    # Garante que os diretórios de destino existem
    for category, dir_path in DEST_DIRS.items():
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Não foi possível criar/verificar o diretório de destino '{dir_path}'. Erro: {e}")

    processed_files = 0
    moved_files = 0
    skipped_files = 0
    error_files = 0
    dest_dir_paths = list(DEST_DIRS.values()) # Lista de Paths para verificação
    desktop_path = HOME_DIR / DESKTOP_DIR_NAME # Path correto para a área de trabalho

    # Loop pelos diretórios de origem
    for source_dir_path in SOURCE_DIRS:
        # Verifica se o diretório de origem realmente existe ANTES de iterar
        if not source_dir_path.is_dir():
            logger.warning(f"Diretório de origem não encontrado ou inválido: '{source_dir_path}'. Pulando.")
            continue

        logger.info(f"--- Verificando diretório: '{source_dir_path}' ---")

        # Encontra arquivos recursivamente usando rglob('*')
        for file_path in source_dir_path.rglob('*'):
            try:
                # Pula se não for um arquivo (ex: diretório, link simbólico)
                if not file_path.is_file():
                    continue

                # ***** INÍCIO DA VERIFICAÇÃO DE ARQUIVOS .desktop NA ÁREA DE TRABALHO (CORRIGIDO) *****
                # Compara o diretório pai do arquivo com o Path CORRETO da Área de trabalho
                # *** CORREÇÃO APLICADA AQUI ***
                if file_path.parent == desktop_path and file_path.suffix.lower() == '.desktop':
                    logger.info(f"  -> Ignorando (App Fixo/Desktop): '{file_path.name}'")
                    skipped_files += 1
                    continue # Pula para o próximo arquivo no loop rglob
                # ***** FIM DA VERIFICAÇÃO DE ARQUIVOS .desktop NA ÁREA DE TRABALHO *****

                # Pula arquivos ocultos (começam com '.')
                if file_path.name.startswith('.'):
                    logger.debug(f"Ignorando arquivo oculto: {file_path.name}")
                    skipped_files += 1
                    continue

                # Pula arquivos já em diretórios de destino ou scripts
                if check_if_in_dest_dir(file_path, dest_dir_paths):
                    logger.debug(f"Ignorando arquivo já no destino/scripts: {file_path.name}")
                    continue

                processed_files += 1
                logger.debug(f"Processando: '{file_path.name}' (em '{file_path.parent}')")

                # Pega a extensão e converte para minúscula
                ext = file_path.suffix.lower()

                # Pula se não tiver extensão ou for uma extensão ignorada
                if not ext:
                    logger.info(f"  -> Ignorando (sem extensão): '{file_path.name}'")
                    skipped_files += 1
                    continue
                if ext in IGNORED_EXTENSIONS:
                    logger.info(f"  -> Ignorando (extensão na lista): '{file_path.name}'")
                    skipped_files += 1
                    continue

                # Determina a categoria e o diretório de destino
                category = EXT_MAP.get(ext, "Outros") # Usa "Outros" como padrão
                target_dir = DEST_DIRS[category]
                target_path = target_dir / file_path.name

                # Lógica para mover (sem sobrescrever por padrão nesta versão 1.1.1)
                if target_path.exists():
                    logger.warning(f"  -> ATENÇÃO: Arquivo '{target_path.name}' já existe em '{target_dir}'. '{file_path.name}' NÃO foi movido.")
                    skipped_files += 1
                else:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        logger.info(f"  -> SUCESSO: Movido '{file_path.name}' para '{target_dir}'")
                        moved_files += 1
                    except Exception as e:
                        logger.error(f"  -> ERRO: Falha ao mover '{file_path.name}' para '{target_dir}'. Detalhes: {e}")
                        error_files += 1

            except Exception as e:
                logger.error(f"Erro inesperado ao processar o item '{file_path}': {e}")
                error_files += 1


    logger.info("==============================================")
    logger.info("--- Script Organizador Python Concluído ---")
    logger.info(f"Resumo: {processed_files} arquivos verificados, {moved_files} movidos, {skipped_files} ignorados/colisões/desktop, {error_files} erros.")
    logger.info("==============================================")