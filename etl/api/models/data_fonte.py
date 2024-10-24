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

    def to_dict(self, include_set: set[str] | None = None) -> dict[str, object]:
        """Converte uma instância de DataFonte para dicionário.

        Args:
            include_set (set[str] | None, optional): Set de colunas para incluir. Defaults to None.

        Returns:
            dict[str, object]: Dicionário filtrado pelas colunas dadas.
        """
        data = {
            "timestamp": str(self.timestamp),
            "wind_speed": float(self.wind_speed),
            "power": float(self.power),
            "ambient_temperature": float(self.ambient_temperature),
        }
        if include_set:
            include_set.add("timestamp")
            data = {key: value for key, value in data.items() if key in include_set}

        return data
