from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings


# Configuracion del algoritmo de hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    """
    Genera un hash seguro de la contraseña
    Nunca guardamos passwords en texto plano
    """
    return pwd_context.hash(password)


def verify_password(password, hashed):
    """
    Verificamos si la contraseña ingresada coincide con el hash guardado
    """
    return pwd_context.verify(password, hashed)


def create_token(data: dict):
    """
    Genera un token JWT con la información del usuario
    """
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
