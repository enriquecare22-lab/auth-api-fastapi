from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

PasswordStr = Annotated[
    str,
    Field(
        min_length=8,
        max_length=100,
    ),
]


# Clase base: contiene los atributos comunes para evitar repetir código
class UserBase(BaseModel):
    email: EmailStr  # Valida automaticamente que el formato sea un correo real


class UserCreate(UserBase):
    # Obliga a que la contraseña tenga una longitud segura antes de procesarla
    password: PasswordStr


# Esquema para el inicio de sesión
class UserLogin(UserBase):
    password: PasswordStr


# Esquema para enviar datos al cliente (lo que el usuairo ve)
class UserResponse(UserBase):
    id: UUID
    email: str
    role: str
    # Configuracion para la compatibilidad con ORMs (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
