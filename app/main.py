from fastapi import FastAPI
from app.api.v1.routes import auth

from app.models.user import Base
from app.db.session import engine

# Crear tablas (solo desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar rutas
app.include_router(auth.router)
