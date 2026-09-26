
import os
import requests


def enviar_telegram(mensagem: str) -> bool:

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([token, chat_id]):
        print("[ERRO] Faltam variaveis de ambiente. Confira seu arquivo .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown",
    }

    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print("[OK] Mensagem enviada com sucesso!")
        return True
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao enviar mensagem via Telegram: {e}")
        return False


if __name__ == "__main__":
    
    from dotenv import load_dotenv
    load_dotenv()
    enviar_telegram("Teste do seu Assistente Pessoal de Monitoramento! 🤖")