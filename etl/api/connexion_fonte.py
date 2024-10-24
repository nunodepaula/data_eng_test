"""Dependencias necessárias para conexão ao Banco de Dados Fonte.

@Author: Nuno de Paula
@date: 23-10-2024
"""

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

host = os.getenv("FONTE_HOST", "")
port = os.getenv("FONTE_PORT", "")
database = os.getenv("FONTE_NAME", "")
user = os.getenv("FONTE_USER", "")
password = os.getenv("FONTE_PASSWORD", "")

if not all([host, port, database, user, password]):
    msg = "Incomplete credentials configuration. Check sample.env file and create a .env file with the credentials."
    raise ValueError(msg)

URL_FONTE = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(URL_FONTE, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Fábrica de sessões para conexão ao Banco Fonte."""


def get_fonte() -> Generator[Session, None, None]:
    """Cria uma sessão de acesso ao Banco de dados fonte a cada requisição.

    Yields:
        SessionLocal: Sessão local criada para cada requisição.
    """
    fonte = SessionLocal()
    try:
        yield fonte
    finally:
        fonte.close()
