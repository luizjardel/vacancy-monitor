import os
import requests


def enviar_telegram(mensagem: str) -> bool:
    """
    Envia uma mensagem via Telegram usando o bot configurado.
    Retorna True se enviou com sucesso, False caso contrario.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not all([token, chat_id]):
        print("[ERRO] Faltam variaveis de ambiente. Confira seu arquivo .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
    }

    try:
        resposta = requests.post(url, json=payload, timeout=10)
        resposta.raise_for_status()
        print("[OK] Mensagem enviada com sucesso!")
        return True
    except requests.RequestException as e:
        detalhe = ""
        if e.response is not None:
            detalhe = f" | Resposta da API: {e.response.text}"
        print(f"[ERRO] Falha ao enviar mensagem via Telegram: {e}{detalhe}")
        return False


if __name__ == "__main__":
    
    from dotenv import load_dotenv
    load_dotenv()
    enviar_telegram("Teste do seu Assistente Pessoal de Monitoramento! 🤖")