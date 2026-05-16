from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.token_blacklist import TokenBlacklist
from app.models.user import User
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

    def role_checker(user: User = Depends(get_current_user)):
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
    """

    token = credentials.credentials

    # Validar blacklist
    if db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first():
        raise HTTPException(status_code=401, detail="Token revoked")

    # FIX: validar tipo acces
    payload = decode_token(token, expected_type="access")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
