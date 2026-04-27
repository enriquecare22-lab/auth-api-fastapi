from fastapi import FastAPI

from app.api.v1.routes import auth, user
from app.db.session import engine
from app.models.user import Base

# Crear tablas (solo desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar rutas
app.include_router(auth.router)

# ruta protegida
app.include_router(user.router)
