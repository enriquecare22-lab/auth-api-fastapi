from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.token_blacklist import TokenBlacklist
from app.repositories.user_repository import get_user_by_email

security = HTTPBearer()


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
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return role_checker


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Dependencia para obtener el usuario autenticado actual.
    Valida el token, revisa la lista negra y recupera al usuario de la DB.
    """

    token = credentials.credentials

    # Seguridad: Verifica si el token esta en la  "blacklist"
    if db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first():
        raise HTTPException(status_code=401, detail="Token revoked")

    # FIX: validar tipo acces
    payload = decode_token(token, expected_type="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Identificacion: Busca al usuario usuando el 'sub' (email) guardado en el token
    user = get_user_by_email(db, payload.get("sub"))

    if not user:
        raise HTTPException(status_code=401, detail="Users not found")

    # Autorizacion: si todo esta bien, inyecta el objeto 'user' en el endpoint
    return user
