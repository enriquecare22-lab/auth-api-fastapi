from fastapi import HTTPException

from app.core.security import (
    create_refresh_token,
    create_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import create_user, get_user_by_email


def register(db, user):
    """
    Registro de usuario
    """

    # Validadr si ya existe
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    # Encriptar password
    hashed = hash_password(user.password)

    # Crear usuario
    return create_user(db, user.email, hashed)


def login(db, user):
    """
    Login de usuario
    """
    db_user = get_user_by_email(db, user.email)

    # Validar credenciales
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    data = {"sub": user.email}

    acces_token = create_token(data)
    refresh_token = create_refresh_token(data)

    return {"acces_token": acces_token, "refresh_token": refresh_token}
