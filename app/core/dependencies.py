from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.repositories.user_repository import get_user_by_email

# Define cómo se obtiene el token desde el header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    """
    Crea y cierra sesión de base de datos por request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_role(role: str):
    """
    Middleware para validar role
    """

    def role_checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Ferbidden")
        return user

    return role_checker


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Obtiene el usuario autenticado desde el JWT

    Flujo:
    1. Extrae token del header
    2. Decodifica JWT
    3. Obtiene email
    4. Busca usuario en DB
    """
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
