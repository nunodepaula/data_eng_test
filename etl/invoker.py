"""Script principal para executar o ETL.

@Author: Nuno de Paula
@date: 24-10-2024
"""

from datetime import datetime, timedelta

import httpx
import pandas as pd
from sqlalchemy.orm import sessionmaker

from etl import dao
from etl.create_tables import create_tables


def get_signal_ids(signal_names: set[str]) -> dict[str, int]:
    """Get a map between signal names and their ids.

    Returns:
        dict[str, int]: A mapping between signal names and signal ids.
    """
    session = sessionmaker(bind=dao.engine)()
    if signal_names:
        signal_ids = session.query(dao.Signal).filter(dao.Signal.name.in_(signal_names)).all()
    else:
        signal_ids = session.query(dao.Signal).all()
    session.close()
    return {str(signal.name): int(signal.id) for signal in signal_ids}


def add_signal_names(signals: set[str]) -> None:
    """Adicionar uma lista de sinais à tabela sinais da Base de dados Alvo.

    Args:
        signals (set[str]): Conjunto com o nome dos sinais a adicionar.
    """
    session = sessionmaker(bind=dao.engine)()
    session.add_all([dao.Signal(name=signal_name) for signal_name in signals])
    session.commit()
    session.close()


def executar(date: datetime) -> None:
    """Executar o script ETL.

    Args:
        date (datetime): _description_

    Raises:
        ValueError: _description_
    """
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

    signal_names = set(df_agg.columns)
    signal_ids = get_signal_ids(signal_names)
    missing_cols = signal_names - signal_ids.keys()
    if missing_cols:
        add_signal_names(missing_cols)
        signal_ids = get_signal_ids(signal_names)

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
