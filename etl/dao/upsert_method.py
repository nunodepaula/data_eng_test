"""Método de upsert para atualizar valores já existentes no banco de dados.

@Author: Nuno de Paula
@date: 24-10-2024
"""

import typing

import pandas as pd
from sqlalchemy.dialects.postgresql import insert


def upsert_data_method(
    table: pd.io.sql.SQLTable,
    conn: typing.Any,  # noqa: ANN401 # Any is expected by pandas syntax
    keys: list[str],
    data_iter: typing.Iterable,
) -> int:
    """Upsert method para atualizar valores já existentes na tabela data do Banco Alvo.

    Args:
        table (pd.io.sql.SQLTable): tabela a atualizar (tabela data).
        conn (Engine | Connection): Conexão ao Banco de dados
        keys (list[str]): Lista de colunas do banco
        data_iter (list): Iterador aos dados a atualizar.

    Returns:
        int: _description_
    """
    data = [dict(zip(keys, linha, strict=True)) for linha in data_iter]

    instruction = insert(table.table).values(data)
    update_columns = {col.name: col for col in instruction.excluded if col.name in ("timestamp", "signal_id")}

    instruction = instruction.on_conflict_do_update(
        index_elements=["timestamp", "signal_id"],
        set_=update_columns,
    )

    result = conn.execute(instruction)

    return result.rowcount
