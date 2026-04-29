from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_refresh_token,
    create_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import create_user, get_user_by_email


def register(db: Session, user):
    """
    Logica para registrar un nuevo usuario en el sistema
    """

    # Validadr si el correo ya esta registrado
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="User already exists")

    # Encriptar password - no guardar en texto plano
    hashed = hash_password(user.password)

    # Persistencia: Guardar usuario con la contraseña hasheada
    return create_user(db, user.email, hashed)


def login(db: Session, user):
    """
    Login de usuario: autenticar usuario y generar sus token de acceso
    """
    # Buscamos el usuario por email
    db_user = get_user_by_email(db, user.email)

    # Validar credenciales
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Preparacion del Payload: Informacion que viajara dentro del JWT
    data = {"sub": db_user.email, "role": db_user.role}

    # Generacion del Tokens:
    # - access_token: Para peticiones normales
    # - refresh_token: Para renovar el acceso sin pedir contrasña
    return {
        "acces_token": create_token(data),
        "refresh_token": create_refresh_token(data),
        "token_type": "bearer",
    }
