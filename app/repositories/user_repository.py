from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Buscar usuario por email.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str):
    """
    Crea un nuevo registro de usuario en la base de datos.
    """
    # Instanciamos el modelo User con los datos recibidos
    user = User(email=email, hashed_password=password)

    # Agregamos el objeto a la sesión (aún no se guarda en la DB)
    db.add(user)

    try:
        # Intentamos confirmar la transaccion (hacer commit)
        db.commit()

        # Refrescamos el objeto para obtener los datos generados por la DB
        db.refresh(user)
    except SQLAlchemyError:
        # Si ocurre un error (ej. email duplicado o fallo de conexion)
        # revertimos los cambios para mantener la integridad de la base de datos
        db.rollback()

        # Re-lanzamos la excepcion para que el controlador (API) sepa que algo fallo
        raise
    # Retornamo el usuario creado y verificado
    return user
