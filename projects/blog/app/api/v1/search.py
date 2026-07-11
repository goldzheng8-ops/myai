from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.search import FTSSearch
from app.schemas.article import ArticleListResponse
from app.models.article import ArticleStatus

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=List[ArticleListResponse])
async def search_articles(
    db: Annotated[AsyncSession, Depends(get_db)],
    q: Optional[str] = Query(None, description="搜索关键词"),
    tag: Optional[str] = Query(None, description="按标签搜索"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    status: Optional[ArticleStatus] = Query(None, description="文章状态过滤"),
    author: Optional[str] = Query(None, description="作者用户名过滤")
):
    """全文搜索文章
    
    基于 SQLite FTS5 全文索引搜索文章标题和内容
    如果FTS索引不可用，则使用简单的LIKE搜索作为备选
    """
    """全文搜索 + 标签过滤"""

    try:
        results = await get_articles_by_tag_or_not( db, q=q, skip=skip, limit=limit, status=status, author=author,tag=tag)
        if results:
            return results

        # FTS 无结果，用 LIKE 回退
        print(f"FTS搜索无结果，使用LIKE搜索备选方案")
        return await search_articles_fallback(db, q, skip, limit, status, author,tag=tag)

    except Exception as e:
        print(f"FTS搜索失败，使用LIKE搜索备选方案: {e}")
        await db.rollback()
        return await search_articles_fallback(db, q, skip, limit, status, author,tag=tag)


async def search_articles_fallback(
    db: AsyncSession,
    query: str|None,
    skip: int = 0,
    limit: int = 10,
    status: Optional[ArticleStatus] = None,
    author: Optional[str] = None,
    tag: Optional[str] = None
) -> List[ArticleListResponse]:
    """
    备选搜索方案：使用简单的LIKE搜索
    q 一定存在，tag 可选
    支持交集查询
    """
    from app.models.article import Article
    from app.models.tag import ArticleTag, Tag
    from app.models.user import User
    from app.schemas.article import UserBasicInfo, TagInfo
    print(f"🐱‍🏍🐱‍🏍🐱‍🏍🐱‍🏍{tag}")
    # ===== 第一步：根据 q 搜索文章 ID =====
    stmt_q = select(Article.id).where(
        Article.title.contains(query) | Article.content.contains(query)
    )

    # 状态过滤
    if status:
        stmt_q = stmt_q.where(Article.status == status)
    else:
        stmt_q = stmt_q.where(Article.status == ArticleStatus.PUBLISHED)

    # 作者过滤
    if author:
        stmt_q = stmt_q.join(User, User.id == Article.author_id).where(User.username == author)

    result_q = await db.execute(stmt_q)
    article_ids = [row[0] for row in result_q.fetchall()]
    print(f"🐱‍🏍{article_ids}")
    if not article_ids:
        return []

    # ===== 第二步：如果有 tag，进一步过滤 =====
    if tag:
        stmt_tag = (
            select(Article.id)
            .join(ArticleTag, Article.id == ArticleTag.article_id)
            .join(Tag, Tag.id == ArticleTag.tag_id)
            .where(Article.id.in_(article_ids))  # 保证交集
            .where(Tag.name == tag)
        )
        result_tag = await db.execute(stmt_tag)
        article_ids = [row[0] for row in result_tag.fetchall()]
        print(f"🐱‍🏍🐱‍🏍{article_ids}")
        if not article_ids:
            return []

    # ===== 第三步：查询完整 Article 对象并加载关系 =====
    stmt_articles = (
        select(Article)
        .where(Article.id.in_(article_ids))
        .options(
            selectinload(Article.author),
            selectinload(Article.tags).selectinload(ArticleTag.tag),
            selectinload(Article.comments)
        )
        .order_by(Article.published_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(stmt_articles)
    articles = result.scalars().all()

    # ===== 构建响应 =====
    return [
        ArticleListResponse(
            id=a.id,
            title=a.title,
            summary=a.summary,
            status=a.status,
            author=UserBasicInfo.model_validate(a.author),
            tags=[TagInfo.model_validate(at.tag) for at in a.tags if at.tag],
            created_at=a.created_at,
            updated_at=a.updated_at,
            view_count=a.view_count,
            comment_count=len(a.comments or [])
        )
        for a in articles
    ]





async def get_articles_by_tag_or_not(
    db: AsyncSession,
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    status: Optional[ArticleStatus] = None,
    author: Optional[str] = None,
    tag: str|None = None
) -> List[ArticleListResponse]:
    from app.models.article import Article
    from app.models.tag import ArticleTag, Tag
    from app.models.user import User
    from app.schemas.article import UserBasicInfo, TagInfo

    # 查标签
    # 如果有关键字搜索
    if q:
        results = await FTSSearch.search_articles(
            db=db,
            query=q,
            skip=skip,
            limit=limit,
            status=status,
            author=author,
            tag=tag,  # 标签过滤
        )
        if results:
            return results
    # 如果只有标签过滤
    if tag:
        tag_result = await db.execute(select(Tag).where(Tag.name == tag))
        tagentity = tag_result.scalar_one_or_none()
        if not tagentity:
            return []

        stmt = (
            select(Article)
            .join(ArticleTag, Article.id == ArticleTag.article_id)
            .join(Tag, Tag.id == ArticleTag.tag_id)
            .options(
                selectinload(Article.author),
                selectinload(Article.tags).selectinload(ArticleTag.tag),
                selectinload(Article.comments)
            )
            .where(Tag.id == tagentity.id)
        )

        # 状态过滤
        if status:
            stmt = stmt.where(Article.status == status)
        else:
            stmt = stmt.where(Article.status == ArticleStatus.PUBLISHED)

        # 作者过滤
        if author:
            stmt = stmt.join(User, User.id == Article.author_id).where(User.username == author)
        # 关键字过滤
        if q:
            stmt = stmt.where(
                Article.title.contains(q) | Article.content.contains(q)
            )

        stmt = stmt.order_by(Article.published_at.desc()).offset(skip).limit(limit)

        result = await db.execute(stmt)
        articles = result.scalars().all()
        return [
            ArticleListResponse(
                id=a.id,
                title=a.title,
                summary=a.summary,
                status=a.status,
                author=UserBasicInfo.model_validate(a.author),
                tags=[TagInfo.model_validate(at.tag) for at in a.tags if at.tag],
                created_at=a.created_at,
                updated_at=a.updated_at,
                view_count=a.view_count,
                comment_count=len(a.comments or [])
            )
            for a in articles
        ]

    # 如果既没有 q 也没有 tag，返回空列表
    return await search_articles_fallback(
        db, q, skip, limit, status, author, tag=tag
    )



@router.get("/suggestions")
async def get_search_suggestions(
    db: Annotated[AsyncSession, Depends(get_db)],
    q: str = Query(..., description="搜索关键词"),
    limit: int = Query(5, ge=1, le=20, description="建议数量")
):
    """获取搜索建议
    
    基于当前搜索词提供相关建议
    """
    suggestions = await FTSSearch.get_search_suggestions(
        db=db,
        query=q,
        limit=limit
    )
    return {
        "query": q,
        "suggestions": suggestions,
        "count": len(suggestions)
    }


@router.get("/popular")
async def get_popular_searches(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = Query(10, ge=1, le=50, description="热门搜索词数量")
):
    """获取热门搜索词
    
    基于文章标题中的关键词统计热门搜索词
    """
    popular_words = await FTSSearch.get_popular_searches(
        db=db,
        limit=limit
    )
    return {
        "popular_searches": popular_words,
        "count": len(popular_words)
    }


@router.post("/init")
async def initialize_search_index(db: Annotated[AsyncSession, Depends(get_db)]):
    """初始化搜索索引
    
    创建 FTS5 虚拟表和触发器，并填充现有数据
    """
    try:
        # 先删除已存在的表和触发器
        await FTSSearch.drop_fts_table(db)
        
        # 创建 FTS5 表
        await FTSSearch.create_fts_table(db)
        
        # 填充数据
        await FTSSearch.populate_fts_table(db)
        
        return {
            "message": "搜索索引初始化成功",
            "status": "completed"
        }
    except Exception as e:
        return {
            "message": f"搜索索引初始化失败: {str(e)}",
            "status": "error"
        }


@router.get("/stats")
async def get_search_stats(db: Annotated[AsyncSession, Depends(get_db)]):
    """获取搜索统计信息"""
    # 获取 FTS5 表统计信息
    result = await db.execute(text("SELECT COUNT(*) FROM articles_fts"))
    fts_count = result.scalar() or 0
    
    # 获取文章总数 - 使用大写的PUBLISHED状态
    result = await db.execute(text("SELECT COUNT(*) FROM article WHERE status = 'PUBLISHED'"))
    article_count = result.scalar() or 0
    
    return {
        "fts_indexed_articles": fts_count,
        "total_published_articles": article_count,
        "index_coverage": fts_count / article_count if article_count > 0 else 0
    } 