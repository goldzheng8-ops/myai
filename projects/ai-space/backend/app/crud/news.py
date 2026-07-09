from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.news import News


def create_news(db: Session, payload: dict) -> News:
    stmt = insert(News).values(
        title=payload["title"],
        url=payload["url"],
        source=payload.get("source", "unknown"),
    )

    stmt = stmt.on_conflict_do_nothing(
        index_elements=["url"]
    )

    db.execute(stmt)
    db.commit()


def list_news(db: Session, skip: int = 0, limit: int = 100) -> list[News]:
    return db.query(News).order_by(News.created_at.desc()).offset(skip).limit(limit).all()
