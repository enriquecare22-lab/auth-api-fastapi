from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.user import Token, UserCreate, UserLogin


def generate_auth_tokens(data: dict) -> Token:
    """
    Centraliza generacion de tokens JWT.
    """
    return Token(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
        token_type="bearer",
    )


def register(db: Session, user: UserCreate):
    """
    Logica para registrar un nuevo usuario
    """

    email = user.email.lower().strip()

    # Validadr si el correo ya esta registrado
    if get_user_by_email(db, email):
        raise HTTPException(status_code=409, detail="User already exists")

    # Hash password
    hashed_password = hash_password(user.password)

    # Persistencia: Guardar usuario con la contraseña hasheada
    return create_user(db, email, hashed_password)


def login(db: Session, user: UserLogin) -> Token:
    """
    Login de usuario: autenticar usuario y generar sus token de acceso
    """

    email = user.email.lower().strip()

    db_user = get_user_by_email(db, email)

    # FIX: validar credenciales, correcta
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not db_user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")

    # Preparacion del Payload: Informacion que viajara dentro del JWT
    data = {
        "sub": str(db_user.id),
        "role": db_user.role,
    }

    # Generacion del Tokens:
    # - access_token: Para peticiones normales
    # - refresh_token: Para renovar el acceso sin pedir contrasña
    return generate_auth_tokens(data)
