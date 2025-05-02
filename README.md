# 🧹 Organizador de Arquivos Automático (Linux Python Script)

![Language](https://img.shields.io/badge/Python_3-blue?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Linux-lightgrey?style=flat-square&logo=linux&logoColor=black)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT) 

Um script Python para Linux que organiza arquivos de múltiplos diretórios de origem (ex: Downloads, Área de Trabalho), movendo-os para pastas categorizadas (Imagens, Documentos, Vídeos, etc.) com base na extensão do arquivo. Lê configurações de um arquivo `config.json`, registra logs detalhados e suporta argumentos de linha de comando. Projetado para ser executado manualmente ou agendado via `cron`.



---

## ✨ Funcionalidades Principais

* 📂 **Múltiplas Origens:** Verifica um ou mais diretórios de origem definidos no `config.json`.
* 🔍 **Busca Recursiva:** Encontra arquivos dentro dos diretórios de origem e suas subpastas.
* 🏷️ **Categorização Flexível:** Organiza arquivos por tipo conforme mapeamento extensão -> categoria no `config.json`.
* 🛡️ **Proteção de Destino:** Evita processar/mover arquivos que já estão nas pastas de destino ou na pasta de scripts.
* 🚫 **Filtro Inteligente:** Ignora arquivos conforme lista de extensões no `config.json`, além de arquivos ocultos (iniciados por `.`) ou sem extensão. Também ignora lançadores `.desktop` na Área de Trabalho.
* ⏩ **Não Sobrescreve:** Avisa no log e não move arquivos se um com o mesmo nome já existir no destino (comportamento atual).
* 📝 **Log Detalhado:** Registra todas as ações (início, fim, arquivos verificados, movidos, ignorados, erros) em um arquivo de log (caminho definido no `config.json`) com data e hora.
* ⏰ **Agendamento Fácil:** Pode ser facilmente configurado para execução automática via `cron`.
* ⚙️ **Altamente Configurável:** Todas as pastas, mapeamentos e listas de ignorados são gerenciados externamente pelo arquivo `config.json`.
* ▶️ **Argumentos CLI:** Suporta `--dry-run` (ou `-n`) para simular a execução sem mover arquivos, e `--config` (ou `-c`) para usar um arquivo de configuração alternativo.

---

## 💻 Requisitos

* 🐧 Ambiente Linux.
* ✅ **Python 3.x** (Python 3.6 ou superior recomendado para `pathlib`, geralmente já instalado em distros modernas como Mint).

---

## 🛠️ Instalação e Configuração

1.  **Clone ou Baixe:**
    * Se estiver usando Git: `git clone https://github.com/SEU_USUARIO/linux-organizer.git && cd linux-organizer` (Substitua pela URL real do seu repo!)
    * Ou apenas baixe os arquivos `organizador_py.py`, `config.example.json`, `.gitignore` e `README.md`.
2.  **Posicione os Arquivos:** Coloque os arquivos em um local adequado (ex: `~/Scripts/linux-organizer`).
3.  **Dê Permissão de Execução ao Script:**
    ```bash
    chmod +x ~/Scripts/linux-organizer/organizador_py.py
    ```
4.  **Crie e Edite seu Arquivo de Configuração (**⚠️ IMPORTANTE**):**
    * **Copie o exemplo:** Dentro da pasta do projeto, execute:
        ```bash
        cp config.example.json config.json
        ```
    * **Edite `config.json`:** Abra `config.json` no VSCode ou seu editor preferido.
    * **Ajuste os caminhos:** Modifique **TODOS** os valores de caminhos em `source_directories`, `destination_directories`, e `log_file_path` para refletir **as suas pastas reais**. Use `~/` para indicar seu diretório home (ex: `"~/Documentos"`). Ajuste também `desktop_dir_name` se necessário.
    * **(Opcional)** Revise `extension_map` e `ignored_extensions` e personalize conforme sua necessidade.
    * **Nota:** O arquivo `config.json` está listado no `.gitignore`, portanto, suas configurações pessoais **não serão enviadas** para o repositório Git. Apenas o `config.example.json` é versionado.
5.  **Agendamento (Opcional - via Cron):**
    * Abra a configuração do cron: `crontab -e`
    * Adicione a linha de agendamento no final (substitua `/home/SEU_USUARIO/` pelo caminho real completo):
        * *Ex: Todo dia às 3h da manhã:*
            ```crontab
            0 3 * * * /usr/bin/python3 /home/SEU_USUARIO/Scripts/linux-organizer/organizador_py.py
            ```
            *(Usar o caminho completo para `python3` (verifique com `which python3`) e para o script é mais seguro no cron).*
    * Salve e feche.

---

## ▶️ Como Usar

Execute os comandos a partir da pasta onde o script está localizado (ex: `~/Scripts/linux-organizer`).

* **Execução Padrão:** Usa `config.json` encontrado na pasta.
    ```bash
    python3 organizador_py.py
    # OU
    ./organizador_py.py
    ```
* **Modo Simulação (Dry Run):** Mostra o que seria feito, sem mover arquivos. Ideal para testar mudanças na configuração!
    ```bash
    python3 organizador_py.py --dry-run
    # OU
    python3 organizador_py.py -n
    ```
* **Usando Configuração Alternativa:**
    ```bash
    python3 organizador_py.py --config /caminho/para/outro_config.json
    # OU
    python3 organizador_py.py -c ../configs/config_teste.json
    ```
* **Verificar o Log:** As ações são registradas no arquivo definido em `log_file_path` no seu `config.json`.
    ```bash
    tail ~/Scripts/linux-organizer/organizador_py.log # Ver o final
    less ~/Scripts/linux-organizer/organizador_py.log # Ver completo
    tail -f ~/Scripts/linux-organizer/organizador_py.log # Ver em tempo real
    ```

---

## 🎨 Customização

* **Adicionar Tipos de Arquivo / Mudar Pastas / Ignorar Extensões:** Edite **diretamente o arquivo `config.json`**. Não é necessário mexer no código Python para essas customizações comuns.
* **Alterar Lógica:** Modifique o arquivo `organizador_py.py` para mudar o comportamento fundamental (ex: adicionar renomeação em colisões, implementar outros filtros).

---

## 📜 Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
*Script desenvolvido como parte de um aprendizado em Python Scripting no Linux. Sinta-se à vontade para usar e modificar.*

---