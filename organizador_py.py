#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organizador de Arquivos Automático v1.4.1 (Python)

Organiza arquivos lendo config JSON. Inclui logging.
Ignora arquivos .desktop na Área de trabalho (usando samefile()).
NÃO renomeia em caso de colisão (apenas avisa).
Aceita argumentos de linha de comando (--config, --dry-run).
"""

import shutil
import logging
from pathlib import Path
from datetime import datetime
import json
import argparse # Importa o módulo argparse

# --- Constantes e Configuração Inicial ---
HOME_DIR = Path.home()
# O nome padrão do arquivo de configuração
DEFAULT_CONFIG_FILENAME = "config.json"
# Caminho padrão para procurar config (primeiro ao lado do script, depois em ~/Scripts)
# Usa Path(__file__) para referência relativa ao local do script
try:
    script_path = Path(__file__).resolve()
    DEFAULT_CONFIG_PATH = script_path.parent / DEFAULT_CONFIG_FILENAME
    if not DEFAULT_CONFIG_PATH.is_file():
        DEFAULT_CONFIG_PATH = HOME_DIR / "Scripts" / DEFAULT_CONFIG_FILENAME
except NameError:
    # Fallback se __file__ não estiver definido (ex: execução interativa)
    DEFAULT_CONFIG_PATH = HOME_DIR / "Scripts" / DEFAULT_CONFIG_FILENAME


# --- Funções ---

def load_config(config_path: Path) -> dict | None:
    """Carrega e valida minimamente as configurações do arquivo JSON."""
    # Log inicial para console caso logger não esteja pronto
    print(f"INFO: Tentando carregar configuração de '{config_path}'...")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        required_keys = [
            "source_directories", "destination_directories", "extension_map",
            "ignored_extensions", "log_file_path", "desktop_dir_name"
        ]
        if not all(key in config_data for key in required_keys):
            print(f"ERRO: Arquivo de configuração '{config_path}' está incompleto.")
            return None
        print(f"INFO: Configuração carregada com sucesso de '{config_path}'")
        return config_data
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo de configuração '{config_path}' não encontrado!")
        return None
    except json.JSONDecodeError as e:
        print(f"ERRO CRÍTICO: Falha ao decodificar JSON em '{config_path}'. Erro: {e}")
        return None
    except Exception as e:
        print(f"ERRO inesperado ao carregar config de '{config_path}': {e}")
        return None

def resolve_path(path_str: str) -> Path:
    """Resolve um caminho string para um objeto Path absoluto (expandindo ~)."""
    return Path(path_str).expanduser().resolve(strict=False)

def setup_logging(log_file_path_str: str) -> logging.Logger | None:
    """Configura o logging para arquivo e console."""
    try:
        log_file_path = resolve_path(log_file_path_str)
        log_file_path.parent.mkdir(parents=True, exist_ok=True) # Garante que dir do log existe

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_level = logging.INFO # Mantenha INFO ou mude para DEBUG para mais detalhes

        logger = logging.getLogger()
        logger.setLevel(log_level)
        if logger.hasHandlers():
            logger.handlers.clear()

        # Handler para o arquivo
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

        # Handler para o console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)

        # Não logar aqui, pois pode ser chamado antes do processamento da config principal
        # logger.info(f"Logging configurado. Arquivo de log: '{log_file_path}'")
        return logger
    except Exception as e:
        print(f"ERRO CRÍTICO AO CONFIGURAR LOGGING para '{log_file_path_str}': {e}")
        return None

def check_if_in_dest_dir(file_path: Path, dest_dirs_paths: list, scripts_dir: Path) -> bool:
    """Verifica se o arquivo já está dentro de algum dos diretórios de destino ou scripts."""
    try:
        file_parent_resolved = file_path.parent.resolve()
        for dest_path in dest_dirs_paths:
            # Usa samefile() para comparação robusta
            if file_parent_resolved.samefile(dest_path):
                return True
        # Verifica também se está na pasta de scripts
        if file_parent_resolved.samefile(scripts_dir):
             return True
    except FileNotFoundError:
        # Se um diretório não existe, samefile() falha
        pass
    except Exception as e:
        # print(f"Debug: Erro não crítico ao verificar parentesco de '{file_path}': {e}")
        pass
    return False


# --- Lógica Principal ---
if __name__ == "__main__":
    # --- Configuração do Argument Parser ---
    parser = argparse.ArgumentParser(
        description="Organiza arquivos baseado em extensões, lendo config JSON.",
        epilog="Exemplo: python3 organizador_py.py -c minha_config.json -n"
    )
    parser.add_argument(
        "-c", "--config",
        type=str,
        default=None,
        help=f"Caminho para o arquivo de configuração JSON. Padrão: procura '{DEFAULT_CONFIG_FILENAME}' ao lado do script ou em ~/Scripts/"
    )
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Modo de simulação (Dry Run). Mostra o que seria feito, mas não move arquivos."
    )
    # --- Processa os Argumentos ---
    args = parser.parse_args()

    # --- Determina o Caminho do Arquivo de Configuração ---
    config_to_load = DEFAULT_CONFIG_PATH
    if args.config:
        config_to_load = resolve_path(args.config)
        # Log inicial via print pois o logger depende da config
        print(f"INFO: Usando arquivo de configuração especificado via argumento: '{config_to_load}'")

    # --- Carrega Configuração ---
    config = load_config(config_to_load)
    if config is None:
        exit(1)

    # --- Configura Logging Definitivo ---
    logger = setup_logging(config["log_file_path"])
    if logger is None:
        exit(1)

    # --- Processa Configurações ---
    try:
        SOURCE_DIRS = [resolve_path(p) for p in config["source_directories"]]
        DEST_DIRS = {cat: resolve_path(p) for cat, p in config["destination_directories"].items()}
        EXT_MAP = {ext.lower(): cat for ext, cat in config["extension_map"].items()}
        IGNORED_EXTENSIONS = {ext.lower() for ext in config["ignored_extensions"]}
        DESKTOP_DIR_NAME = config["desktop_dir_name"]
        desktop_path = resolve_path(f"~/{DESKTOP_DIR_NAME}")
        # Tenta obter scripts_dir do destino 'Scripts', senão do log_file
        if "Scripts" in DEST_DIRS:
            scripts_dir = DEST_DIRS["Scripts"]
        else:
             scripts_dir = resolve_path(Path(config["log_file_path"]).parent)
    except KeyError as e:
        logger.error(f"Erro: Chave de configuração faltando: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Erro ao processar dados da configuração: {e}")
        exit(1)

    # --- Início da Execução ---
    logger.info("==============================================")
    logger.info(f"--- Iniciando Script Organizador Python v1.4.1 ---") # Versão Atualizada
    logger.info(f"Usando configuração de: '{config_to_load}'")
    logger.info(f"Argumentos recebidos: {args}")
    if args.dry_run:
        logger.warning("### MODO DE SIMULAÇÃO (DRY RUN) ATIVADO - NENHUM ARQUIVO SERÁ MOVIDO ###")
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
    dest_dir_paths = list(DEST_DIRS.values())

    # Loop pelos diretórios de origem
    for source_dir_path in SOURCE_DIRS:
        if not source_dir_path.is_dir():
            logger.warning(f"Diretório de origem não encontrado ou inválido: '{source_dir_path}'. Pulando.")
            continue
        logger.info(f"--- Verificando diretório: '{source_dir_path}' ---")

        for file_path in source_dir_path.rglob('*'):
            try:
                if not file_path.is_file():
                    continue

                # Verifica se é .desktop na Área de Trabalho (usando samefile)
                try:
                    # *** A CORREÇÃO ESTÁ AQUI ***
                    if file_path.parent.samefile(desktop_path) and file_path.suffix.lower() == '.desktop':
                        logger.info(f"  -> Ignorando (App Fixo/Desktop): '{file_path.name}'")
                        skipped_files += 1
                        continue
                except FileNotFoundError:
                     # Se o desktop_path não existir por algum motivo, loga aviso mas continua
                     logger.warning(f"Diretório da área de trabalho '{desktop_path}' não encontrado ao verificar {file_path.name}")
                     pass

                # Ignora ocultos
                if file_path.name.startswith('.'):
                    logger.debug(f"Ignorando arquivo oculto: {file_path.name}")
                    skipped_files += 1
                    continue

                # Ignora arquivos já no destino ou scripts
                if check_if_in_dest_dir(file_path, dest_dir_paths, scripts_dir):
                    logger.debug(f"Ignorando arquivo já no destino/scripts: {file_path.name}")
                    continue

                processed_files += 1
                logger.debug(f"Processando: '{file_path.name}' (em '{file_path.parent}')")
                ext = file_path.suffix.lower()

                # Ignora sem extensão ou na lista de ignorados
                if not ext:
                    logger.info(f"  -> Ignorando (sem extensão): '{file_path.name}'")
                    skipped_files += 1
                    continue
                if ext in IGNORED_EXTENSIONS:
                    logger.info(f"  -> Ignorando (extensão na lista): '{file_path.name}'")
                    skipped_files += 1
                    continue

                # Determina o destino
                category = EXT_MAP.get(ext, "Outros")
                target_dir = DEST_DIRS[category]
                target_path = target_dir / file_path.name

                # Lógica de mover (considerando --dry-run)
                if target_path.exists():
                    logger.warning(f"  -> ATENÇÃO: Arquivo '{target_path.name}' já existe em '{target_dir}'. '{file_path.name}' NÃO foi movido.")
                    skipped_files += 1
                else:
                    if args.dry_run:
                        logger.info(f"  -> [DRY RUN] Moveria '{file_path.name}' para '{target_dir}'")
                        # moved_files não é incrementado em dry run
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

    # --- Finalização ---
    logger.info("==============================================")
    logger.info("--- Script Organizador Python Concluído ---")
    logger.info(f"Resumo: {processed_files} arquivos verificados, {moved_files} movidos, {skipped_files} ignorados/colisões/desktop, {error_files} erros.")
    logger.info("==============================================")