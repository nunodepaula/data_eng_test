"""Principais recursos relacionados a camada DAO de acesso ao Banco de Dados Alvo."""

from etl.dao.connexion_alvo import engine
from etl.dao.data import Data
from etl.dao.signal import Signal
from etl.dao.upsert_method import upsert_data_method

__all__ = [
    "Data",
    "engine",
    "Signal",
    "upsert_data_method",
]
