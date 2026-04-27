from fastapi import HTTPException
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_token


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

    # Crear token JWT
    token = create_token({"sub": user.email})

    return {"acces_token": token, "token_type": "bearer"}
