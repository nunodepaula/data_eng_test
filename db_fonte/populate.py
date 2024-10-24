"""Script principal para criação da tabela data do banco de dados fonte.

@Author: Nuno de Paula
@date: 23-10-2024
"""

import os

import psycopg2
from dotenv import load_dotenv

from db_fonte.create_table import create_table
from db_fonte.parse_basileia import parse_basileia


def populate() -> None:
    """Popular a tabela data do banco de dados fonte."""
    basileia_path = parse_basileia()
    create_table()

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

    with basileia_path.open() as file:
        # Forma mais eficiente para copiar um grande volume de dados ao banco PostgreSQL
        cursor.copy_from(file, "data", ",")

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    populate()
