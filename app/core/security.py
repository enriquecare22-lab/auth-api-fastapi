from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configuracion del algoritmo de hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    # Genera un hash seguro de la contraseña
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    # Verificamos si la contraseña ingresada coincide con el hash guardado
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    if "sub" not in data:
        raise ValueError("Token missing subject")

    to_encode = data.copy()

    # Tiempo actual
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": now, "type": "access"})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict[str, Any]) -> str:
    """
    Gener refresh token
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
            "type": "refresh",
        }
    )

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, expected_type: str = "access"):
    """
    Decodifica un JWT
    """
    try:
        # Intenta descifrar el token usando la llave secreta y el algoritmo (ej. HS256)
        # Si el token expiró o la firma fue alterada, lanzará una excepción JWTError.

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        # Validación de Seguridad Crítica:
        # Verifica que el 'tipo' de token en el payload coincida con lo esperado.
        # Esto evita que usen un 'refresh_token' para acceder a rutas de datos (access).
        if payload.get("type") != expected_type:
            return None

            # Si todo es correcto, devuelve los datos contenidos (sub, exp, type, etc.)
        return payload

    except JWTError:
        # Si el token es invalido, mal formado o ha expirado,
        # capturamos el error y retornamos None para denegar el acceso
        return None
