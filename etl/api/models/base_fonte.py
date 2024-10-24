"""Base class for SQLAlchemy entities.

A definição dessa Base global permite a extensão de comportamentos comuns desejados para todas as entidades.

@Author: Nuno de Paula
@date: 23-10-2024
"""

from sqlalchemy.ext.declarative import declarative_base

BaseFonte = declarative_base()
