from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.session import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
