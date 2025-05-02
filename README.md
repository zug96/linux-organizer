## 🧹 Organizador de Arquivos Automático (Linux Bash Script)

![Language](https://img.shields.io/badge/Bash-blue?style=flat-square&logo=gnu-bash&logoColor=white)
![Platform](https://img.shields.io/badge/Linux-lightgrey?style=flat-square&logo=linux&logoColor=black)

Um script Bash para Linux que organiza arquivos de múltiplos diretórios de origem (ex: Downloads, Área de Trabalho), movendo-os para pastas categorizadas (Imagens, Documentos, Vídeos, etc.) com base na extensão do arquivo. Projetado para ser executado manualmente ou agendado via `cron`.

---

## ✨ Funcionalidades Principais

* 📂 **Múltiplas Origens:** Verifica um ou mais diretórios de origem definidos pelo usuário.
* 🔍 **Busca Recursiva:** Encontra arquivos dentro dos diretórios de origem e suas subpastas.
* 🏷️ **Categorização:** Organiza arquivos por tipo (Imagens, Documentos, Vídeos, Músicas, Scripts, Outros).
* 🛡️ **Proteção de Destino:** Evita processar arquivos que já estão nas pastas de destino ou na pasta de scripts.
* 🚫 **Filtro Inteligente:** Ignora arquivos compactados, instaladores, ocultos (iniciados por `.`) ou sem extensão.
* ⏩ **Segurança Contra Sobrescrita:** Não sobrescreve arquivos com o mesmo nome que já existam no destino (usa `mv -n`).
* 📝 **Log Detalhado:** Registra todas as ações (início, fim, arquivos verificados, movidos, ignorados, erros) em um arquivo de log (`organizador.log`) com data e hora.
* ⏰ **Agendamento Fácil:** Pode ser facilmente configurado para execução automática via `cron`.

---

## 💻 Requisitos

* 🐧 Ambiente Linux com **Bash** (versão 4+ recomendada).
* ✅ Comandos padrão: `find`, `basename`, `dirname`, `mkdir`, `mv`, `date`, `touch`.

---

## 🛠️ Instalação e Configuração

1.  **Clone ou Baixe:**
    * Se estiver usando Git: `git clone <URL_DO_REPOSITORIO>`
    * Ou apenas salve o código do script (ex: `organizador_v3.log.sh`).
2.  **Posicione o Script:** Coloque o arquivo em um local adequado (ex: `~/Scripts`).
3.  **Dê Permissão de Execução:**
    ```bash
    chmod +x ~/Scripts/organizador_v3.log.sh
    ```
4.  **Configure o Script (**⚠️ IMPORTANTE**):**
    * Abra `organizador_v3.log.sh` no VSCode ou seu editor preferido.
    * **Ajuste `SOURCE_DIRS`:** Defina os diretórios a serem monitorados. Use caminhos completos e aspas.
        ```bash
        SOURCE_DIRS=(
            "$HOME/Downloads"
            "$HOME/Área de Trabalho"
            # Adicione mais pastas aqui, se necessário
        )
        ```
    * **(Opcional)** Verifique e ajuste os diretórios de destino (`IMAGE_DIR`, `DOC_DIR`, etc.) e o `LOG_FILE` conforme sua preferência.
5.  **Agendamento (Opcional - via Cron):**
    * Abra a configuração do cron: `crontab -e`
    * Adicione a linha de agendamento no final (substitua `/home/SEU_USUARIO/` pelo caminho real):
        * *Ex: Todo dia às 2h da manhã:*
            ```crontab
            0 2 * * * /home/SEU_USUARIO/Scripts/organizador_v3.log.sh
            ```
    * Salve e feche o editor (`Ctrl+O`, Enter, `Ctrl+X` no nano).

---

## ▶️ Como Usar

* **Execução Manual:**
    ```bash
    ~/Scripts/organizador_v3.log.sh
    ```
* **Verificar o Log:** O arquivo `~/Scripts/organizador.log` contém o histórico de execuções.
    ```bash
    # Ver as últimas linhas do log
    tail ~/Scripts/organizador.log

    # Ver o log completo de forma paginada (use 'q' para sair)
    less ~/Scripts/organizador.log

    # Acompanhar o log em tempo real (Ctrl+C para sair)
    tail -f ~/Scripts/organizador.log
    ```

---

## 🎨 Customização

* **Adicionar Tipos de Arquivo:** Modifique a estrutura `case "$extension_lower" in` no script para incluir novas extensões e definir para qual `target_dir` elas devem ir.
* **Mudar Diretórios:** Edite as variáveis de caminho (`SOURCE_DIRS`, `IMAGE_DIR`, `LOG_FILE`, etc.) no início do script.

---

*Script desenvolvido como parte de um aprendizado em Bash Scripting. Sinta-se à vontade para usar e modificar.*