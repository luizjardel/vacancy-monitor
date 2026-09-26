import re
import requests

URL_REMOTEOK = "https://remoteok.com/api"
URL_REMOTIVE = "https://remotive.com/api/remote-jobs"


def _limpar_html(texto: str, limite: int = 250) -> str:
    """Remove tags HTML de um texto e corta ele num tamanho legivel."""
    texto_limpo = re.sub(r"<[^>]+>", " ", texto)
    texto_limpo = re.sub(r"\s+", " ", texto_limpo).strip()
    if len(texto_limpo) > limite:
        texto_limpo = texto_limpo[:limite].rsplit(" ", 1)[0] + "..."
    return texto_limpo


def buscar_vagas_remoteok() -> list[dict]:
    
    headers = {"User-Agent": "Mozilla/5.0 (compatible; JobMonitorBot/1.0)"}

    try:
        resposta = requests.get(URL_REMOTEOK, headers=headers, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao buscar vagas no RemoteOK: {e}")
        return []

    vagas_brutas = dados[1:] if len(dados) > 1 else []
    vagas = []
    for vaga in vagas_brutas:
        vagas.append({
            "id": f"remoteok_{vaga.get('id', '')}",
            "titulo": vaga.get("position", "Sem titulo"),
            "empresa": vaga.get("company", "Empresa nao informada"),
            "url": vaga.get("url", ""),
            "tags": [t.lower() for t in vaga.get("tags", [])],
            "descricao": _limpar_html(vaga.get("description", "")),
            "localizacao": vaga.get("location", ""),
            "fonte": "RemoteOK",
        })
    return vagas


def buscar_vagas_remotive() -> list[dict]:
    
    try:
        resposta = requests.get(URL_REMOTIVE, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.RequestException as e:
        print(f"[ERRO] Falha ao buscar vagas no Remotive: {e}")
        return []

    vagas_brutas = dados.get("jobs", [])
    vagas = []
    for vaga in vagas_brutas:
        vagas.append({
            "id": f"remotive_{vaga.get('id', '')}",
            "titulo": vaga.get("title", "Sem titulo"),
            "empresa": vaga.get("company_name", "Empresa nao informada"),
            "url": vaga.get("url", ""),
            "tags": [t.lower() for t in vaga.get("tags", [])],
            "descricao": _limpar_html(vaga.get("description", "")),
            "localizacao": vaga.get("candidate_required_location", ""),
            "fonte": "Remotive",
        })
    return vagas


def buscar_todas_as_vagas() -> list[dict]:
    
    vagas_remoteok = buscar_vagas_remoteok()
    vagas_remotive = buscar_vagas_remotive()
    print(f"  - RemoteOK: {len(vagas_remoteok)} vagas")
    print(f"  - Remotive: {len(vagas_remotive)} vagas")
    return vagas_remoteok + vagas_remotive


def filtrar_por_palavras_chave(vagas: list[dict], palavras_chave: list[str]) -> list[dict]:
    
    palavras_chave = [p.lower().strip() for p in palavras_chave]
    vagas_filtradas = []

    for vaga in vagas:
        texto_busca = " ".join([
            vaga["titulo"].lower(),
            " ".join(vaga["tags"]),
            vaga["descricao"].lower(),
        ])
        if any(palavra in texto_busca for palavra in palavras_chave):
            vagas_filtradas.append(vaga)

    return vagas_filtradas


def filtrar_vagas_latam_brasil(vagas: list[dict]) -> list[dict]:
    
    termos_regiao = ["latam", "remoto", "brazil", "brasil", "latin america"]
    vagas_regiao = []

    for vaga in vagas:
        localizacao = vaga.get("localizacao", "").lower()
        if any(termo in localizacao for termo in termos_regiao):
            vagas_regiao.append(vaga)

    return vagas_regiao