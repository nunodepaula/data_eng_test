"""Classe representando a tabela data do bando de dados alvo.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, PrimaryKeyConstraint

from etl.dao.base import Base


class Data(Base):
    """Classe representando a tabela Data e seus atributos."""

    __tablename__ = "data"

    timestamp = Column(DateTime, index=True)
    signal_id = Column(Integer, ForeignKey("signal.id"), index=True)
    value = Column(Float)

    # Chave primária composta (timestamp, signal_id)
    __table_args__ = (PrimaryKeyConstraint("timestamp", "signal_id"),)
