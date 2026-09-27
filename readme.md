# 🎯 Vacancy Monitor

> ⚠️ **Repositório educacional** — projeto criado como exercício prático de
> aprendizado em Python (primeira linguagem após experiência prévia com
> Java/Spring Boot). Não é um produto ou serviço comercial.
>
> ⚠️ **Educational repository** — built as a hands-on learning exercise in
> Python (first project after prior experience with Java/Spring Boot). Not a
> commercial product or service.

---

## 🇧🇷 Português

Assistente pessoal em Python que monitora vagas de emprego automaticamente
e avisa via Telegram quando encontra uma vaga técnica com chance real de
aceitar candidatos do Brasil/LATAM — sem precisar ficar checando sites de
vaga manualmente.

### Como funciona

1. Busca vagas em duas fontes públicas (RemoteOK e Remotive), sem precisar de chave de API
2. Filtra por palavras-chave técnicas configuráveis (ex: "java", "spring boot")
3. Cruza esse filtro com a localização da vaga, mantendo só as que mencionam Brasil, LATAM ou "remoto"
4. Guarda um histórico em SQLite para nunca notificar a mesma vaga duas vezes
5. Envia a notificação direto para o Telegram, com título, empresa, localização, descrição e link
6. Roda sozinho, de graça, na nuvem via GitHub Actions, a cada 3 horas — mesmo com o computador desligado

### Tecnologias utilizadas

- **Python 3.12**
- **Requests** — consumo das APIs de vagas e envio de mensagens
- **SQLite** (`sqlite3`, nativo do Python) — controle de duplicatas
- **python-dotenv** — gerenciamento de variáveis de ambiente
- **schedule** — agendamento de execução local
- **GitHub Actions** — execução automática na nuvem, gratuita
- **API do Telegram** (via bot) — canal de notificação

### Estrutura do projeto

```
vacancy-monitor/
├── main.py                    # Orquestrador principal (uso local, com loop)
├── run_once.py                # Executa uma unica verificacao (usado pelo GitHub Actions)
├── requirements.txt
├── .env.example                # Modelo de variaveis de ambiente
├── .gitignore
├── .github/
│   └── workflows/
│       └── monitor.yml         # Workflow do GitHub Actions
├── data/
│   └── vagas.db                 # Criado automaticamente (historico local)
└── src/
    ├── buscador_vagas.py        # Busca e filtra vagas (RemoteOK + Remotive)
    ├── historico.py              # Controle de duplicatas via SQLite
    └── notifier.py                # Envio de notificacao via Telegram
```

### Como rodar localmente

**1. Clonar o repositório e instalar as dependências**

```bash
git clone https://github.com/SEU_USUARIO/vacancy-monitor.git
cd vacancy-monitor
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows (PowerShell)
pip install -r requirements.txt
```

**2. Criar um bot no Telegram**

1. No Telegram, procure por **@BotFather** e envie `/newbot`
2. Escolha um nome e um username (precisa terminar em `bot`)
3. Guarde o **token** que ele te enviar
4. Procure por **@userinfobot**, converse com ele e guarde o seu **Chat ID**
5. Envie `/start` (ou qualquer mensagem) para o seu próprio bot, para liberar o envio de mensagens

**3. Configurar as variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o `.env` com `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` e `KEYWORDS` (palavras-chave separadas por vírgula).

**4. Testar o envio e rodar o assistente**

```bash
python src/notifier.py    # testa se a notificacao chega no Telegram
python main.py             # roda o assistente completo
```

### Rodando 24/7 de graça (GitHub Actions)

O projeto já inclui um workflow que executa `run_once.py` automaticamente a
cada 3 horas, direto nos servidores do GitHub, sem depender do computador
estar ligado.

1. Vá em **Settings → Secrets and variables → Actions**
2. Crie os secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` e `KEYWORDS`
3. Vá na aba **Actions** e rode manualmente com **"Run workflow"** para testar

### Próximos passos (ideias futuras)

- Adicionar scraping de sites de vaga brasileiros (Gupy, Programathor)
- Gerar relatórios semanais com `pandas`
- Permitir múltiplos usuários/chats recebendo notificações diferentes

---

## 🇬🇧 English

A personal Python assistant that automatically monitors job listings and
notifies you via Telegram when it finds a technical vacancy that is likely
to accept candidates from Brazil/LATAM — no need to manually check job
boards every day.

### How it works

1. Fetches jobs from two public sources (RemoteOK and Remotive), no API key required
2. Filters by configurable technical keywords (e.g. "java", "spring boot")
3. Cross-references that with the job's location, keeping only listings mentioning Brazil, LATAM, or "remote"
4. Keeps a SQLite history to avoid notifying the same job twice
5. Sends the notification straight to Telegram, with title, company, location, description, and link
6. Runs by itself, for free, in the cloud via GitHub Actions, every 3 hours — even with your computer turned off

### Tech stack

- **Python 3.12**
- **Requests** — consuming job APIs and sending messages
- **SQLite** (`sqlite3`, built into Python) — duplicate control
- **python-dotenv** — environment variable management
- **schedule** — local execution scheduling
- **GitHub Actions** — free automated cloud execution
- **Telegram Bot API** — notification channel

### Project structure

```
vacancy-monitor/
├── main.py                    # Main orchestrator (local use, with loop)
├── run_once.py                # Runs a single check (used by GitHub Actions)
├── requirements.txt
├── .env.example                # Environment variable template
├── .gitignore
├── .github/
│   └── workflows/
│       └── monitor.yml         # GitHub Actions workflow
├── data/
│   └── vagas.db                 # Created automatically (local history)
└── src/
    ├── buscador_vagas.py        # Job search and filtering (RemoteOK + Remotive)
    ├── historico.py              # Duplicate control via SQLite
    └── notifier.py                # Telegram notification sending
```

### Running locally

**1. Clone the repository and install dependencies**

```bash
git clone https://github.com/YOUR_USERNAME/vacancy-monitor.git
cd vacancy-monitor
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows (PowerShell)
pip install -r requirements.txt
```

**2. Create a Telegram bot**

1. On Telegram, search for **@BotFather** and send `/newbot`
2. Choose a name and a username (must end with `bot`)
3. Save the **token** it gives you
4. Search for **@userinfobot**, message it, and save your **Chat ID**
5. Send `/start` (or any message) to your own bot to allow it to message you

**3. Set up environment variables**

```bash
cp .env.example .env
```

Fill in `.env` with `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and `KEYWORDS` (comma-separated).

**4. Test sending and run the assistant**

```bash
python src/notifier.py    # tests if the notification reaches Telegram
python main.py             # runs the full assistant
```

### Running 24/7 for free (GitHub Actions)

The project already includes a workflow that runs `run_once.py`
automatically every 3 hours, directly on GitHub's servers, with no
dependency on your computer being on.

1. Go to **Settings → Secrets and variables → Actions**
2. Create the secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and `KEYWORDS`
3. Go to the **Actions** tab and run it manually with **"Run workflow"** to test

### Future ideas

- Add scraping of Brazilian job boards (Gupy, Programathor)
- Generate weekly reports with `pandas`
- Support multiple users/chats receiving different notifications

---

Projeto desenvolvido como exercício prático de automação em Python.
*Built as a hands-on Python automation learning exercise.*