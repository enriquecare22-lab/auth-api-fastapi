from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Base para todos los modelos
Base = declarative_base()


class User(Base):
    """
    Modelo de usuario en la base de datos
    Representa la tabla 'users'
    """

    __tablename__ = "users"

    # ID unico del usuario
    id = Column(Integer, primary_key=True, index=True)

    # Email unico (nose puede repetir)
    email = Column(String, unique=True, index=True, nullable=False)

    # Password encriptado
    password = Column(String, nullable=False)
