from sqlalchemy.orm import Session

from app.models.news import News


def create_news(db: Session, payload: dict) -> News:
    news = News(
        title=payload["title"],
        url=payload["url"],
        source=payload.get("source", "unknown"),
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def list_news(db: Session, skip: int = 0, limit: int = 100) -> list[News]:
    return db.query(News).order_by(News.created_at.desc()).offset(skip).limit(limit).all()
