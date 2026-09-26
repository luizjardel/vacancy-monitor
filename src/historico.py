import sqlite3
from pathlib import Path

CAMINHO_DB = Path(__file__).parent.parent / "data" / "vagas.db"

def _conectar():
    CAMINHO_DB.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(CAMINHO_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vagas_notificadas (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            empresa TEXT,
            url TEXT,
            data_notificacao TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn
def ja_notificada(vaga_id: str) -> bool:
    """Verifica se uma vaga ja foi notificada antes."""
    conn =  _conectar()
    cursor = conn.execute(
        "SELECT 1 FROM vagas_notificadas WHERE id = ?", (vaga_id,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def marcar_como_notificada(vaga_id: str, titulo: str, empresa: str, url: str):
    """Registra uma vaga como ja notificada."""
    conn = _conectar()
    conn.execute(
        "INSERT OR IGNORE INTO vagas_notificadas (id, titulo, empresa, url) VALUES (?, ?, ?, ?)",
        (vaga_id, titulo, empresa, url),
    )
    conn.commit()
    conn.close()