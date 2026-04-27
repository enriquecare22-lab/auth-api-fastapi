from app.models.user import User


def get_user_by_email(db, email):
    """
    Busca usuario por email
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db, email, password):
    """
    crea un nuevo usuario en la base de datos
    """
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


    
