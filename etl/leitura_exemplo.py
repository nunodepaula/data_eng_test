"""Exemplo simplificado para verificar a inserção dos dados na Base Alvo.

@Author: Nuno de Paula
@date: 24-10-2024
"""

# ruff: noqa: S608 (Variáveis verificadas no script)
# ruff:noqa: T201 (prints usado para demonstrar os dados lidos)

import pandas as pd

from etl import dao

start_time = "2024-10-01 00:00:00"
end_time = "2024-10-01 00:20:00"

query = f"""
SELECT *
FROM data
WHERE  timestamp BETWEEN '{start_time}' AND '{end_time}'
"""

df_alvo = pd.read_sql_query(query, dao.engine)

df_signals = pd.read_sql_query("SELECT * FROM signal", dao.engine)

print(df_alvo)
print(df_signals)
