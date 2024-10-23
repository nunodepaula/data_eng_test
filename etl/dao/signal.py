"""Classe representando a tabela Signal do banco de dados alvo.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from sqlalchemy import Column, Integer, String

from etl.dao.base import Base


class Signal(Base):
    """Classe representando a tabela Signal e seus atributos."""

    __tablename__ = "signal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
