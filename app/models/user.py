from sqlalchemy import Column, Integer, String

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
    email = Column(String, unique=True, index=True, nullable=False)

    # Password encriptado
    password = Column(String, nullable=False)

    # Rol del usuario: "user" o "admin"
    role = Column(String, default="user")
