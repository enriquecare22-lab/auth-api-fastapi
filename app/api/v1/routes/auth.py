from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_token, decode_token
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import login, register

router = APIRouter(prefix="/auth", tags=["Auth"])


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
def refresch_token(token: str):
    payload = decode_token(token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")

    new_access_token = create_token({"sub": email})
    return {"acces_token": new_access_token}
