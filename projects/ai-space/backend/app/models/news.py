from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Column

from app.db.base import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=False, default="unknown")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
