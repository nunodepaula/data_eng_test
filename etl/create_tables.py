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

    tabelas_alvo = {"data": dao.Data, "signal": dao.Signal}

    for nome in tabelas_alvo.keys() - set(tabelas):
        tabelas_alvo[nome].__table__.create(bind=dao.engine)  # type: ignore[attr-defined] # object é um objeto Base de sqlalchemy
