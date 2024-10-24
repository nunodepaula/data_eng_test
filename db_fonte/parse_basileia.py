"""Script para ler, interpretar o dados histórico de Basileira e exportar o dado pronto para a base de dados.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from pathlib import Path

import numpy as np
import pandas as pd


def parse_basileia() -> Path:
    """Ler, interpretar e salvar dados para a base de dados fonte.

    Returns:
        (Path): Caminho para o arquivo csv com o dado fonte.

    """
    df_historic = pd.read_csv(Path(__file__).parent / "dataexport_basileia.csv", header=9)
    df_historic["timestamp"] = pd.to_datetime(df_historic["timestamp"], format="%Y%m%dT%H%M")
    df_historic = df_historic.set_index("timestamp")

    # Extrapolação do dado histórico para frequência 1-minutal e cálculo de potência aleatória
    df_basileia = df_historic.resample("1min").interpolate(method="linear")
    rng = np.random.default_rng()
    random_power = rng.random(len(df_basileia)) * 5 + 12  # *5 + 12 para deixar num intervalo de 12 a 17
    df_basileia["power"] = random_power
    df_basileia = df_basileia.rename(columns={"Temperature": "ambient_temperature", "Wind Speed": "wind_speed"})
    df_basileia = df_basileia[["wind_speed", "power", "ambient_temperature"]]

    basileia_path = Path(__file__).parent / "data_basileia.csv"
    df_basileia.to_csv(basileia_path, header=False)
    return basileia_path
