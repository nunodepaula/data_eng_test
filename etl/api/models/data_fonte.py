"""Definição do modelo SQLAlchemy para a tabela data do Banco de Dados Fonte.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from sqlalchemy import Column, DateTime, Float

from etl.api.models.base_fonte import BaseFonte


class DataFonte(BaseFonte):
    """Classe modelo para representar a tabela data do banco de dados fonte."""

    __tablename__ = "data"

    timestamp = Column(DateTime, primary_key=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)
