from fastapi import Depends, HTTPException

# Define cómo se obtiene el token desde el header Authorization
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
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
            raise HTTPException(status_code=403, detail="Ferbidden")
        return user

    return role_checker


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Obtiene usuario desde token Bearer
    """

    # Extrae el token sin el "Bearer"
    token = credentials.credentials

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
