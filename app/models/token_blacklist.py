from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Base para todos los modelos
Base = declarative_base()


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
