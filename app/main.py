from app.models.user import Base
from app.db.session import settings

Base.metadata.create_all(bind=engine)
