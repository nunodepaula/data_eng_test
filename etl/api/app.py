"""Main app for the API.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query

from etl.api.models.signals_to_fetch import Signals2Fetch

app = FastAPI()

# ruff: noqa: B008


@app.get("/", response_model=str)
async def landing() -> str:
    """Rota raiz da API.

    Returns:
        str: Mensagem de boas vindas.
    """
    return "Bem vindos à API de acesso ao Banco de Dados Fonte."


@app.get("/fetch")
async def fetch_data(
    start_time: datetime = Query(
        ...,
        title="Timestamp de inicio",
        description="Timestamp inicial para filtrar os dados",
        example="2024-10-23T10:10:01",
    ),
    end_time: datetime = Query(
        ...,
        title="Timestamp final",
        description="Ultimo timestamp incluido no filtro de obtenção de dados.",
        example="2024-10-23T10:12:30",
    ),
    signal_names: Signals2Fetch = Depends(),
) -> str:
    if end_time < start_time:
        raise HTTPException(status_code=400, detail="start_time deve ser menor que end_time")
    signals = signal_names.signals
    return ""
