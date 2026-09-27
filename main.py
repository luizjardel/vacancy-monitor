import os
import time
import schedule
from dotenv import load_dotenv

from src.buscador_vagas import (
    buscar_todas_as_vagas,
    filtrar_por_palavras_chave,
    filtrar_vagas_latam_brasil,
)
from src.historico import ja_notificada, marcar_como_notificada
from src.notifier import enviar_telegram

load_dotenv()


def filtrar_vagas_relevantes(vagas: list[dict], palavras_chave: list[str]) -> list[dict]:
    vagas_tecnicas = filtrar_por_palavras_chave(vagas, palavras_chave)
    vagas_regiao = filtrar_vagas_latam_brasil(vagas)

    ids_regiao = {v["id"] for v in vagas_regiao}
    return [v for v in vagas_tecnicas if v["id"] in ids_regiao]


def rodar_verificacao():
    print("\n=== Iniciando verificacao de vagas ===")

    palavras_chave = os.getenv("KEYWORDS", "").split(",")
    if not palavras_chave or palavras_chave == [""]:
        print("[AVISO] Nenhuma palavra-chave configurada no .env (KEYWORDS)")
        return

    print("Buscando em todas as fontes:")
    vagas = buscar_todas_as_vagas()
    print(f"Total de vagas encontradas: {len(vagas)}")

    vagas_relevantes = filtrar_vagas_relevantes(vagas, palavras_chave)
    print(f"Vagas relevantes (tecnica E regiao): {len(vagas_relevantes)}")

    novas_vagas = [v for v in vagas_relevantes if not ja_notificada(v["id"])]
    print(f"Vagas novas (ainda nao notificadas): {len(novas_vagas)}")

    for vaga in novas_vagas:
        mensagem = (
            f"🎯 Nova vaga encontrada! ({vaga['fonte']})\n\n"
            f"{vaga['titulo']}\n"
            f"Empresa: {vaga['empresa']}\n"
            f"Localizacao: {vaga['localizacao'] or 'Nao informada'}\n\n"
            f"{vaga['descricao']}\n\n"
            f"Link: {vaga['url']}"
        )
        enviado = enviar_telegram(mensagem)
        if enviado:
            marcar_como_notificada(vaga["id"], vaga["titulo"], vaga["empresa"], vaga["url"])
        time.sleep(1)

    print("=== Verificacao concluida ===\n")


if __name__ == "__main__":
    rodar_verificacao()
    schedule.every(3).hours.do(rodar_verificacao)

    print("Assistente rodando. Verificando vagas a cada 3 horas...")
    print("Pressione Ctrl+C para parar.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)