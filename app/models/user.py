from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.session import Base


class User(Base):
    """
    Modelo de usuario en la base de datos
    Representa la tabla 'users'
    """

    __tablename__ = "users"

    # ID unico del usuario
    id = Column(Integer, primary_key=True, index=True)

    # Email unico (nose puede repetir)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Password encriptado
    password = Column(String(255), nullable=False)

    # Rol del usuario: "user" o "admin"
    role = Column(String(50), default="user", nullable=False)

    is_active = Column(DateTime, default=datetime.utcnow)
