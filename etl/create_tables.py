"""Helper function para criar as tabelas que ainda não existem na Base de Dados.

@Author: Nuno de Paula
@date: 24-10-2024
"""

from sqlalchemy import inspect

from etl import dao


def create_tables() -> None:
    """Cria as tabelas ainda não existentes do Banco de Dados alvo."""
    inspetor = inspect(dao.engine)

    tabelas = inspetor.get_table_names()

    # Como temos apenas duas tabelas e sinais deve ser criada antes, podemos criar uma por uma. Caso tivessemos mais
    # poderíamos optimizar a criação através de um loop.
    if "signal" not in tabelas:
        dao.Signal.__table__.create(bind=dao.engine)

    if "data" not in tabelas:
        dao.Data.__table__.create(bind=dao.engine)
