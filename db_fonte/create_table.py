"""Função para Criar a tabela data na base de dados fonte.

@Author: Nuno de Paula
@date: 23-10-2024
"""

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


def create_table() -> None:
    """Cria a tabela data na base de dados fonte.

    Raises:
        ValueError: Se não houver um arquivo.env ou se as credenciais estiverem incompletas.

    """
    load_dotenv()

    host = os.getenv("FONTE_HOST", "")
    port = os.getenv("FONTE_PORT", "")
    database = os.getenv("FONTE_NAME", "")
    user = os.getenv("FONTE_USER", "")
    password = os.getenv("FONTE_PASSWORD", "")

    if not all([host, port, database, user, password]):
        msg = "Incomplete credentials configuration. Check sample.env file and create a .env file with the credentials."
        raise ValueError(msg)

    conn = psycopg2.connect(host=host, port=port, dbname=database, user=user, password=password)
    cursor = conn.cursor()

    query_path = Path(__file__).parent / "queries" / "criar_tabela.sql"
    query = query_path.read_text()
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()
