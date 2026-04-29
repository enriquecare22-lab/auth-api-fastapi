from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

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
    Genera un token JWT con expircaion
    """
    to_encode = data.copy()

    # Tiempo actual
    now = datetime.utcnow()
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": now, "type": "access"})

    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict):
    """
    Gener refresh token
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str):
    """
    Decodifica un JWT y retorna el payload
    - Si el token es valido: devuelve datos (ej: email)
    - Si es invalido: retorna NONE
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        print(payload)
        return payload
    except JWTError:
        return None
