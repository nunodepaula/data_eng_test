"""Schema Pydantic para representar a tabela data do banco Fonte retornada pela API.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from datetime import datetime

from pydantic import BaseModel


class DataFonteSchema(BaseModel):
    """Schema representando a tabela data do Banco fonte retornada pela API."""

    timestamp: datetime
    wind_speed: float | None = None
    power: float | None = None
    ambient_temperature: float | None = None

    class Config:
        """Configurações internas ao Schema."""

        from_attibutes = True
