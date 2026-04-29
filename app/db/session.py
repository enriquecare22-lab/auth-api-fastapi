from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Base para todos los modelos
Base = declarative_base()


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
