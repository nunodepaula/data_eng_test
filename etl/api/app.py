"""Main app for the API.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from etl.api.connexion_fonte import get_fonte
from etl.api.models.data_fonte import DataFonte
from etl.api.models.data_fonte_schema import DataFonteSchema

app = FastAPI()

# ruff: noqa: B008 (FastAPI syntax)


@app.get("/", response_model=str)
async def landing() -> str:
    """Rota raiz da API.

    Returns:
        str: Mensagem de boas vindas.
    """
    return "Bem vindos à API de acesso ao Banco de Dados Fonte."


@app.get("/fetch", response_model=list[DataFonteSchema])
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
        description="Timestamp final para filtrar os dados. (Não incluso)",
        example="2024-10-23T10:12:30",
    ),
    signal_names: list[str] | None = Query(
        None,
        title="Lista de sinais a serem retornados.",
        example=["wind_speed", "power"],
    ),
    db_fonte: Session = Depends(get_fonte),
) -> JSONResponse:
    """Consultar dados na tabela data do banco Fonte.

    Essa rota permite consultar dados do banco de dados fonte, permitindo a seleção de variáveis a serem retornadas.

    Args:
        start_time (datetime): Timestamp inicial.
        end_time (datetime): Timestamp final
        signal_names (list[str] | None, optional): Lista de sinais a serem retornados.
        db_fonte (Session): Sessão de conexão ao Banco Fonte.

    Raises:
        HTTPException: Se end_time < start_time
        HTTPException: Se signal_names contem nomes inválidos.

    Returns:
        JSONResponse: Lista de dados obtidos.
    """
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="start_time deve ser menor que end_time")
    signals = set(signal_names) if signal_names else set()
    if invalid := signals - {"wind_speed", "power", "ambient_temperature"}:
        raise HTTPException(status_code=400, detail=f"Sinais invalidos: {", ".join(invalid)}")

    data = db_fonte.query(DataFonte).where((DataFonte.timestamp >= start_time) & (DataFonte.timestamp < end_time)).all()

    return JSONResponse(content=[datum.to_dict(signals) for datum in data])
