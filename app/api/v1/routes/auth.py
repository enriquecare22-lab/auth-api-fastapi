from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import create_token, decode_token
from app.db.session import SessionLocal
from app.models.token_blacklist import TokenBlacklist
from app.schemas.user import TokenRefresh, UserCreate, UserLogin
from app.services.auth_service import login, register

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


def get_db():
    """
    Dependency para obtener la sesion de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register(db, user)


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login(db, user)


@router.post("/refresh")
def refresch_token(data: TokenRefresh):
    """
    FIX:
    - usa schema
    - valida tipo refresh
    """
    payload = decode_token(data.refresh_token, expected_type="refresh")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")

    new_access_token = create_token({
        "sub": email,
        "type": "access"
        })
    
    return {"access_token": new_access_token}


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    # Si ya está en blacklist, lo tratamos como logout idempotente
    exists = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    if exists:
        return {"message": "Logged out"}

    db.add(TokenBlacklist(token=token))
    db.commit()
    return {"message": "Logged out"}
