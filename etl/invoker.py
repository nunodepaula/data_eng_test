"""Script principal para executar o ETL.

@Author: Nuno de Paula
@date: 24-10-2024
"""

from datetime import datetime, timedelta

import httpx
import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from etl import dao


def create_tables() -> None:
    """Cria as tabelas ainda não existentes do Banco de Dados alvo."""
    inspetor = inspect(dao.engine)

    tabelas = inspetor.get_table_names()

    tabelas_alvo = {"data": dao.Data, "signal": dao.Signal}

    for nome in tabelas_alvo.keys() - set(tabelas):
        tabelas_alvo[nome].__table__.create(bind=dao.engine)  # type: ignore[attr-defined] # object é um objeto Base de sqlalchemy


def get_signal_ids() -> dict[str, int]:
    """Get a map between signal names and their ids.

    Returns:
        dict[str, int]: A mapping between signal names and signal ids.
    """
    session = sessionmaker(bind=dao.engine)()
    signal_ids = session.query(dao.Signal).all()
    session.close()
    return {str(signal.name): int(signal.id) for signal in signal_ids}


def add_signal_names(signals: dict[str, int]) -> None:
    session = sessionmaker(bind=dao.engine)()
    session.add_all([dao.Signal(id=idx, name=col) for col, idx in signals.items()])
    session.commit()
    session.close()


def executar(date: datetime) -> None:
    # Nesse projeto exemplo, usei apenas localhost para simplificaros acessos.
    API_FONTE_URL = "http://localhost:8000"

    params = {
        "start_time": date,
        "end_time": date + timedelta(days=1),
        "signal_names": ["wind_speed", "power"],
    }

    response = httpx.get(f"{API_FONTE_URL}/fetch", params=params)

    if response.status_code != 200:
        # TODO: Add propper error logging and exceptions handling
        raise ValueError(response.json())

    df_response = pd.DataFrame(response.json())
    df_response["timestamp"] = pd.to_datetime(df_response["timestamp"], format="%Y-%m-%d %H:%M:%S")
    df_response = df_response.set_index("timestamp")

    df_agg = df_response.resample("10min").agg(["sum", "mean", "max", "std"])
    df_agg.columns = ["_".join(multi_col) for multi_col in df_agg.columns]

    # Verifica se as tabelas necessárias existem, se não, as cria.
    create_tables()

    # TODO: Check if it can be more efficient instead of getting all then add missing
    signal_ids = get_signal_ids()
    missing_cols = set(df_agg.columns) - signal_ids.keys()
    last_id = max(signal_ids.values())
    signals_2_add = {missing_col: idx + last_id + 1 for idx, missing_col in enumerate(missing_cols)}
    if signals_2_add:
        add_signal_names(signals_2_add)
    signal_ids.update(signals_2_add)

    df_agg = pd.melt(df_agg.reset_index(), id_vars=["timestamp"], var_name="signal", value_name="value")
    df_agg["signal_id"] = df_agg["signal"].replace(signal_ids)
    df_agg[["timestamp", "signal_id", "value"]].to_sql(
        "data",
        dao.engine,
        if_exists="append",
        index=False,
        method=dao.upsert_data_method,
    )


if __name__ == "__main__":
    executar(datetime(2024, 10, 1))
