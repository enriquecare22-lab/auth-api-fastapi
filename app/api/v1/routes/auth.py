from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register, login
from app.db.session import SessionLocal

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
    return register_user(db, user)

@router.post("/login")
def login_user(user: UserLogin, db: Session=Depends(get_db)):
    return login(db, user)