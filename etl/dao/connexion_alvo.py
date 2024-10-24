"""Dependencias necessárias para conexão ao Banco de Dados Alvo.

@Author: Nuno de Paula
@date: 24-10-2024
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

host = os.getenv("ALVO_HOST", "")
port = os.getenv("ALVO_PORT", "")
database = os.getenv("ALVO_NAME", "")
user = os.getenv("ALVO_USER", "")
password = os.getenv("ALVO_PASSWORD", "")

if not all([host, port, database, user, password]):
    msg = "Incomplete credentials configuration. Check sample.env file and create a .env file with the credentials."
    raise ValueError(msg)

URL_ALVO = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(URL_ALVO)
