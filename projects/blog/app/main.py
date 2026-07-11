# 在所有导入前加载dotenv
import json
from pathlib import Path
import traceback
from typing import Optional
import uuid
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from wtforms.fields import SelectField
from sqlalchemy.orm import selectinload
from app.models.scheduled_task import ScheduledTask
from app.utils.decor_test import action_with_pks
from app.utils.file_ops import delete_file
from app.core.file_path import get_file_path_from_url
from app.core.websocket import manager
load_dotenv()

# 设置代理环境变量（如果.env中有配置）
import os
if os.getenv('HTTP_PROXY') is not None:
    os.environ['HTTP_PROXY'] = str(os.getenv('HTTP_PROXY'))
if os.getenv('HTTPS_PROXY') is not None:
    os.environ['HTTPS_PROXY'] = str(os.getenv('HTTPS_PROXY'))
if os.getenv('NO_PROXY') is not None:
    os.environ['NO_PROXY'] = str(os.getenv('NO_PROXY'))

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.apscheduler.base import scheduler
from app.core.apscheduler.registry import start_scheduler, stop_scheduler
from app.core.config import settings
from app.core.database import engine, create_db_and_tables, async_session
from app.core.redis import redis_manager
from app.core.middleware import setup_middleware
from app.core.exceptions import BlogException
from app.api.v1.auth import router as auth_router
from app.api.v1.article import router as article_router
from app.api.v1.tag import router as tag_router
from app.api.v1.websocket import router as websocket_router
from app.api.v1.search import router as search_router
from app.api.v1.scheduler import router as scheduler_router
from app.api.v1.oauth import router as oauth_router
from app.api.v1.config import router as config_router
from app.api.v1.donation import router as donation_router
from app.api.v1.admin import router as admin_router
from sqladmin import Admin, ModelView, action
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse
from sqlalchemy import select, delete
from app.models.user import User, OAuthAccount
from app.models.article import Article
from app.models.tag import Tag, ArticleTag
from app.models.comment import Comment
from app.core.security import verify_password
from app.models.user import UserRole
from app.models.media import MediaFile
from app.models.system_notification import SystemNotification
from app.models.donation import DonationConfig, DonationRecord, DonationGoal
from app.core.apscheduler.jobs import task_func_map
from app.core.config import settings
import logging
logger = logging.getLogger(__name__)

ADMIN_PATH = settings.admin_path
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_PUBLIC_DIR = BASE_DIR.parent / "frontend" / "public"
UPLOADS_DIR = BASE_DIR.parent / "uploads"

os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("Starting up...")
    
    # Connect to Redis
    await redis_manager.connect()
    print("Connected to Redis")
    # 简单的健康检查
    try:
        assert redis_manager.redis is not None, "Redis client is not initialized"
        pong = await redis_manager.redis.ping()
        print(f"Redis ping response: {pong}")  # 应该打印 True
    except Exception as e:
        print(f"Redis health check failed: {e}")
    # Create database tables
    await create_db_and_tables()
    print("Database tables created")
    
    # Initialize OAuth
    # oauth.init_app(app)  # Temporarily disabled due to linter issues
    print("OAuth initialization skipped")
    
    # Start scheduler
    await manager.connect_redis_pubsub()
    await start_scheduler()
    print("Scheduler started")
    # Create management backend
    admin = Admin(
        app, 
        engine, 
        authentication_backend=AdminAuth(secret_key=settings.secret_key), 
        base_url=ADMIN_PATH,
        title="博客管理系统",
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        templates_dir= str(BASE_DIR / "templates")
        # scheme="https"  # 强制所有链接为 https
    )

    class UserAdmin(ModelView, model=User):
        column_list = ["id", "username", "email", "role", "is_active", "created_at"]
        form_columns = ["username", "email", "full_name", "role", "is_active", "oauth_provider", "oauth_id", "oauth_username", "avatar_url"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "用户管理"
        name_plural = "用户"
        form_include_pk = False
        form_widget_args = {
            "hashed_password": {"readonly": True}
        }
        
        async def delete_model(self, request: Request, pks: list) -> bool:
            print(f"delete_model called: {pks}")
            """自定义删除方法，防止删除管理员用户"""
            async with async_session() as session:
                try:
                    # 检查是否要删除管理员用户
                    for pk in pks:
                        result = await session.execute(select(User).where(User.id == pk))
                        user = result.scalar_one_or_none()
                        if user and user.role == "ADMIN":
                            print(f"不能删除管理员用户: {user.username}")
                            return False
                    
                    for pk in pks:
                        # 删除用户相关的评论
                        await session.execute(delete(Comment).where(Comment.author_id == pk))
                        
                        # 删除用户的所有文章（包括文章标签关联）
                        article_result = await session.execute(select(Article).where(Article.author_id == pk))
                        user_articles = article_result.scalars().all()
                        
                        for article in user_articles:
                            # 删除文章相关的评论
                            await session.execute(delete(Comment).where(Comment.article_id == article.id))
                            # 删除文章标签关联
                            await session.execute(delete(ArticleTag).where(ArticleTag.article_id == article.id))
                        
                        # 删除用户的所有文章
                        await session.execute(delete(Article).where(Article.author_id == pk))
                    
                    # 删除用户
                    for pk in pks:
                        await session.execute(delete(User).where(User.id == pk))
                    
                    await session.commit()
                    return True
                except Exception as e:
                    await session.rollback()
                    print(f"删除用户失败: {e}")
                    return False

    class ArticleAdmin(ModelView, model=Article):
        column_list = ["id", "title", "author_id", "status", "view_count", "created_at"]
        form_columns = ["title", "content", "summary", "status", "author_id", "is_featured", "has_latex", "latex_content", "view_count"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "文章管理"
        name_plural = "文章"
        form_include_pk = False
        
        async def delete_model(self, request: Request, pks: list) -> bool:
            pks_int = [int(pk) for pk in pks]
            async with async_session() as session:
                try:
                    # 1. 先删除文章与标签的关联记录
                    await session.execute(
                        delete(ArticleTag).where(ArticleTag.article_id.in_(pks_int))
                    )
                    
                    # 2. 再删除文章本身
                    stmt = delete(Article).where(Article.id.in_(pks_int))
                    await session.execute(stmt)
                    
                    await session.commit()
                    return True
                except Exception as e:
                    await session.rollback()
                    print(f"删除文章失败: {e}")
                    return False

    class TagAdmin(ModelView, model=Tag):
        column_list = ["id", "name", "description", "created_at"]
        form_columns = ["name", "description"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "标签管理"
        name_plural = "标签"
        form_include_pk = False

    class ArticleTagAdmin(ModelView, model=ArticleTag):
        column_list = ["id", "article_id", "tag_id"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "文章标签关联"
        name_plural = "文章标签关联"
        form_include_pk = False
        form_excluded_columns = []

    class CommentAdmin(ModelView, model=Comment):
        column_list = ["id", "article_id", "author_id", "content", "created_at", "is_approved"]
        form_columns = ["article_id", "author_id", "content", "parent_id", "is_approved"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "评论管理"
        name_plural = "评论"
        form_include_pk = False
        
        async def delete_model(self, request: Request, pks: list) -> bool:
            print(f"delete_model called: {pks}")
            """自定义删除方法，删除评论时也删除子评论"""
            async with async_session() as session:
                try:
                    for pk in pks:
                        # 删除子评论
                        await session.execute(delete(Comment).where(Comment.parent_id == pk))
                        
                        # 删除评论本身
                        await session.execute(delete(Comment).where(Comment.id == pk))
                    
                    await session.commit()
                    return True
                except Exception as e:
                    await session.rollback()
                    print(f"删除评论失败: {e}")
                    return False

    class MediaFileAdmin(ModelView, model=MediaFile):
        column_list = ["id", "filename", "type", "url", "size", "upload_time", "description", "uploader_id", "uploader"]
        column_formatters = {
            "uploader": lambda m, p: m.uploader.username if m.uploader else ""
        }
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "多媒体文件"
        name_plural = "多媒体文件"
        async def delete_model(self, request: Request, pks: list[int]) -> bool:
            current_user_id = request.session.get("user_id")
            if not current_user_id:
                raise ValueError("无有效用户")

            # 确保 pks 是整数
            try:
                pks = [int(pk) for pk in pks]
            except Exception as e:
                print(f"pks 转换整数失败: {pks} -> {e}")
                return False

            async with async_session() as session:
                try:
                    media_files: list[MediaFile] = []
                    for pk in pks:
                        media = await session.get(MediaFile, pk)
                        if media is not None:
                            media_files.append(media)

                    for media in media_files:
                        # 类型安全检查 url 和 uploader_id
                        if not media.url:
                            print(f"⚠️ MediaFile {media.id} url 为空，跳过删除物理文件")
                            continue
                        if media.uploader_id is None:
                            print(f"⚠️ MediaFile {media.id} uploader_id 为空，跳过权限检查")
                            continue

                        file_path = get_file_path_from_url(media.url)
                        try:
                            await delete_file(
                                file_path=file_path,
                                current_user_id=current_user_id,
                                owner_id=media.uploader_id,
                                admin_override=True
                            )
                        except Exception as e:
                            print(f"⚠️ 删除物理文件失败: {media.filename} -> {e}")

                    # 批量删除数据库对象
                    for media in media_files:
                        await session.delete(media)

                    await session.commit()
                    return True

                except Exception as e:
                    await session.rollback()
                    print(f"❌ 删除 MediaFile 失败: {e}")
                    return False

    class OAuthAccountAdmin(ModelView, model=OAuthAccount):
        column_list = ["id", "user_id", "provider", "provider_user_id", "provider_username", "created_at", "updated_at"]
        form_columns = ["user_id", "provider", "provider_user_id", "provider_username", "provider_email", "provider_avatar_url"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "OAuth账号绑定"
        name_plural = "OAuth账号绑定"
        form_include_pk = False

    class SystemNotificationAdmin(ModelView, model=SystemNotification):
        column_list = ["id", "title", "message", "notification_type", "created_at", "is_sent", "admin_id"]
        form_columns = ["title", "message", "notification_type", "is_sent", "admin_id"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "系统通知"
        name_plural = "系统通知"
        form_include_pk = False

        async def is_accessible(self, request):
            # 只有管理员能访问
            user_id = request.session.get("user_id")
            if not user_id:
                return False
            async with async_session() as session:
                user = await session.get(User, user_id)
                return user and user.role == UserRole.ADMIN

        async def insert_model(self, request, data):
            # 自动填充 admin_id 字段
            user_id = request.session.get("user_id")
            if user_id:
                data["admin_id"] = user_id
            return await super().insert_model(request, data)

    class DonationConfigAdmin(ModelView, model=DonationConfig):
        column_list = [
            "id", "is_enabled", "title", "description", "alipay_enabled", "wechat_enabled", "paypal_enabled", "preset_amounts", "created_at", "updated_at"
        ]
        form_columns = [
            "is_enabled", "title", "description", "alipay_enabled", "wechat_enabled", "paypal_enabled", "preset_amounts"
        ]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "捐赠配置"
        name_plural = "捐赠配置"
        form_include_pk = False

    class DonationRecordAdmin(ModelView, model=DonationRecord):
        column_list = [
            "id", "donor_name", "donor_email", "donor_message", "is_anonymous", "amount", "currency", "payment_method", "payment_status", "transaction_id", "user_id", "goal_id", "created_at", "updated_at", "paid_at"
        ]
        form_columns = [
            "donor_name", "donor_email", "donor_message", "is_anonymous", "amount", "currency", "payment_method", "payment_status", "transaction_id", "user_id", "goal_id", "paid_at"
        ]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "捐赠记录"
        name_plural = "捐赠记录"
        form_include_pk = False

    class DonationGoalAdmin(ModelView, model=DonationGoal):
        column_list = ["id", "title", "description", "target_amount", "current_amount", "currency", "start_date", "end_date", "is_active", "is_completed", "created_at", "updated_at"]
        form_columns = ["title", "description", "target_amount", "current_amount", "currency", "start_date", "end_date", "is_active"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "捐赠目标"
        name_plural = "捐赠目标"
        form_include_pk = False
    class ScheduledTaskAdmin(ModelView, model=ScheduledTask):
            # 显示列表
        column_list = [
            "id",
            "name",
            "func_name",
            "trigger",
            "is_enabled",
            "last_run_time",
            "next_run_time"
        ]

        form_overrides = {
            "trigger": SelectField,
            "func_name": SelectField,
        }
        form_args = {
            "func_name": {
                "label": "任务函数",
                "choices": [(name, name) for name in task_func_map.keys()],
                "description": "请选择要执行的函数"
            },
            "trigger": {
                "label": "触发器类型",
                "choices": [
                    ("interval", "interval"),
                    ("cron", "cron"),
                    ("date", "date")
                ],
                "description": "选择任务的触发器类型"
            },
            "trigger_args": {
                "label": "触发器配置",
                "description": (
                    "JSON配置，必填！根据trigger类型填写对应参数。\n"
                    "示例:\n"
                    "- interval: {\"seconds\":10}\n"
                    "- cron: {\"minute\":\"0\", \"hour\":\"12\"}\n"
                    "- date: {\"run_date\":\"2025-08-07 12:00:00\"}"
                ),
                "default": "{\"seconds\":10}"
            },
            "args": {
                "description": "位置参数 JSON数组，例如 [\"param1\", 2]",
                "default": "[]"
            },
            "kwargs": {
                "description": "关键字参数 JSON对象，例如 {\"key\":\"value\"}",
                "default": "{}"
            }
        }
        form_columns = ["name", "func_name", "trigger", "args", "kwargs", "trigger_args", "is_enabled"]
        can_create = True
        can_edit = True
        can_delete = True
        can_view_details = True
        name = "定时任务管理"
        name_plural = "定时任务"
        form_include_pk = False

        
        # JSON 字段在后台自动转字符串，重写验证函数让它能输入JSON格式字符串
        async def before_create(self, request: Request, data: dict) -> dict:
            data["id"] = str(uuid.uuid4())
            for field in ("args", "kwargs", "trigger_args"):
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = json.loads(data[field])
                    except Exception as e:
                        logger.warning(f"字段 {field} JSON解析失败，值：{data[field]}，错误：{e}")
                        data[field] = [] if field in ("args", "kwargs") else {}
            return data
        
        async def before_update(self, request: Request, pk: str, data: dict) -> dict:
            for field in ("args", "kwargs", "trigger_args"):
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = json.loads(data[field])
                    except Exception as e:
                        logger.warning(f"字段 {field} JSON解析失败，值：{data[field]}，错误：{e}")
                        data[field] = [] if field in ("args", "kwargs") else {}
            return data
        
        async def after_create(self, request: Request, obj: ScheduledTask):
            # 新增后同步到调度器
            await scheduler.add_job_from_db(obj)
        
        async def after_update(self, request: Request, obj: ScheduledTask):
            # 更新后同步调度器（先删除旧任务，再添加）
            await scheduler.remove_job(obj.id)
            if obj.is_enabled:
                await scheduler.add_job_from_db(obj)
        
        async def after_delete(self, request: Request, obj: ScheduledTask):
            # 删除后从调度器删除任务
            await scheduler.remove_job(obj.id)

        @action(
            name="view_job_status",  # 内部标识符，只能用字母数字下划线
            label="查看任务状态",     # 展示给用户的文字，可以用中文
            add_in_list=True,
            add_in_detail=True
        )
        async def view_job_status(self, request: Request):
            job_status = scheduler.get_job_status()
            request.session["job_status"] = job_status
            referer = request.headers.get("referer")
            if referer:
                return RedirectResponse(referer, status_code=303)
            base_path = "/".join(request.url.path.split("/")[:3])
            return RedirectResponse(f"{base_path}/list", status_code=303)

        @action_with_pks(name="pause_job", label="暂停任务", confirmation_message="确定要暂停选中任务吗？")
        async def pause_job(self, request: Request, item: ScheduledTask):
            await scheduler.pause_job(item.func_name)
            return f"任务 {item.name} 已暂停"


        @action_with_pks(name="resume_job", label="恢复任务", confirmation_message="确定要恢复选中任务吗？")
        async def resume_job(self, request: Request, item: ScheduledTask):
            await scheduler.resume_job(item.func_name)
            return f"任务 {item.name} 已恢复"


        @action_with_pks(name="remove_job", label="从调度器移除", confirmation_message="不会删除数据库中的任务，仅从调度器中移除，确认？")
        async def remove_job(self, request: Request, item: ScheduledTask):
            await scheduler.remove_job(item.func_name)
            return f"任务 {item.name} 已从调度器移除"


        @action_with_pks(name="add_job", label="重新添加到调度器", confirmation_message="是否将选中任务重新添加到调度器？")
        async def add_job(self, request: Request, item: ScheduledTask):
            await scheduler.add_job_from_db(item)
            return f"任务 {item.name} 已重新添加"


        @action_with_pks(name="run_once", label="立即执行一次", confirmation_message="任务将立即被调度执行一次，确认继续？")
        async def run_once(self, request: Request, item: ScheduledTask):
            func = scheduler.task_func_map.get(item.func_name)
            if not func:
                raise Exception(f"找不到函数: {item.func_name}")
            if asyncio.iscoroutinefunction(func):
                await func(*item.args or [], **item.kwargs or {})
            else:
                func(*item.args or [], **item.kwargs or {})
            return f"任务 {item.name} 已执行"

        actions = [
            pause_job,
            resume_job,
            remove_job,
            add_job,
            run_once,
        ]
        
            

    admin.add_view(UserAdmin)
    admin.add_view(OAuthAccountAdmin)
    admin.add_view(ArticleAdmin)
    admin.add_view(TagAdmin)
    admin.add_view(ArticleTagAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(MediaFileAdmin)
    admin.add_view(SystemNotificationAdmin)
    admin.add_view(DonationConfigAdmin)
    admin.add_view(DonationRecordAdmin)
    admin.add_view(DonationGoalAdmin)
    admin.add_view(ScheduledTaskAdmin)
    
    yield
    
    # Shutdown
    print("Shutting down...")
    
    # Stop scheduler
    await stop_scheduler()
    print("Scheduler stopped")
    
    # Disconnect from Redis
    await redis_manager.disconnect()
    print("Disconnected from Redis")



# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A complete FastAPI blog system with JWT authentication, articles, comments, and tags",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan
)

# 挂载 uploads 静态资源目录
import os
# app.mount("/uploads", StaticFiles(directory=os.path.abspath("uploads")), name="uploads")
app.mount("/public", StaticFiles(directory=FRONTEND_PUBLIC_DIR), name="public")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# 找到 sqladmin 的 static 路径
# sqladmin_static_dir = os.path.join(os.path.dirname(sqladmin.__file__), "static")

# 手动挂载 static，路径必须是 /admin/statics 才能匹配模板引用的资源路径
app.mount("/admin/statics", StaticFiles(directory="app/static/sqladmin"), name="sqladmin-static")
# Setup middleware

@app.middleware("http")
async def flash_message_middleware(request: Request, call_next):
    # 从 session 取出一次性消息
        # 确保 session 存在再操作
    try:
        if hasattr(request, "session"):
            flash_messages = request.session.pop("flash_messages", None)
            job_status = request.session.pop("job_status", None)
            # print(f"🐱‍🏍🐱‍🏍🐱‍🏍{job_status.jobs}")
            if flash_messages:
                request.state.flash_messages = flash_messages
            if job_status:
                request.state.job_status = job_status
    except Exception as e:
        # 避免 session 弹出出错导致请求失败
        # 这里可以日志记录异常
        pass
    response = await call_next(request)
    return response
setup_middleware(app)  # 恢复中间件

# Exception handlers
@app.exception_handler(BlogException)
async def blog_exception_handler(request: Request, exc: BlogException):
    """Handle custom blog exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "status_code": 422
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "status_code": 422
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    print("🔥 全局异常:", traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )



# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(article_router, prefix="/api/v1")
app.include_router(tag_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/wss")
app.include_router(search_router, prefix="/api/v1")
app.include_router(scheduler_router, prefix="/api/v1")
app.include_router(oauth_router, prefix="/api/v1")
app.include_router(config_router, prefix="/api/v1")
app.include_router(donation_router, prefix="/api/v1")
app.include_router(admin_router,prefix="/api/v1")



@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI Blog System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running"
    }
# 初始化模板目录（假设你的 templates 目录和 main.py 同级）
templates = Jinja2Templates(directory="app/templates")
@app.get("/admin/somepage")
async def admin_page(request: Request):
    flash_messages = request.session.pop("flash_messages", None)
    return templates.TemplateResponse(
        "partials/list.html",
        {
            "request": request,
            "flash_messages": flash_messages
        }
    )
@app.get("/set-flash")
async def set_flash(request: Request):
    # 往 session 里放一次性提示
    request.session["flash"] = ["✅ 操作成功！", "❌ 有一条失败了"]
    return HTMLResponse("Flash 已设置，<a href='/show'>去看看</a>")


@app.get("/show", response_class=HTMLResponse)
async def show_page(request: Request):
    # 读取并移除 flash
    flash_messages = request.session.pop("flash", None)
    return templates.TemplateResponse(
        "partials/list.html",  # 你的模板路径
        {
            "request": request,
            "flash_messages": flash_messages
        }
    )

class AdminAuth(AuthenticationBackend):
    MAX_FAILED_ATTEMPTS = 5
    LOCK_TIME = 10 * 60  # 10 分钟
    async def authenticate(self, request: Request):
        if request.session.get("user_id"):
            async with async_session() as session:
                user = await session.get(User, request.session["user_id"])
                if user and user.role == UserRole.ADMIN:
                    return True
        return False

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username") or "")
        password = str(form.get("password") or "")
        code = str(form.get("code") or "")
        # 检查是否被锁定
        lock_key = f"login_fail:{username}"
        fail_count = await redis_manager.get_key(lock_key)
        if fail_count and int(fail_count) >= self.MAX_FAILED_ATTEMPTS:
            raise HTTPException(status_code=403, detail="账户已被锁定，请10分钟后再试")
        async with async_session() as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()
            key = f"email_verification:{username}"
            stored_code = await redis_manager.get_key(key)
            # print(f"User found: {user}")
            if (
                user and user.role == UserRole.ADMIN and user.is_active
                and user.hashed_password
                and verify_password(password, user.hashed_password)
                and stored_code and stored_code ==code

            ):
                # 验证通过后删除验证码（一次性使用）
                await redis_manager.delete_key(key)
                await redis_manager.delete_key(lock_key)
                # 设置 session
                # request.session.update({"user_id": user.id, "is_admin": True})
                # print(f"User {user.username} authenticated successfully")
                request.session["user_id"] = user.id
                return True
            else:
                # print(f"Authentication failed for user {username}")
                await self._increase_fail_count(username)
                request.session.pop("user_id", None)
        return False

    async def logout(self, request: Request) -> None:
        request.session.pop("user_id", None)
    async def _increase_fail_count(self, username: str):
        """增加登录失败次数，并在超过限制时锁定账户"""
        lock_key = f"login_fail:{username}"
        current = await redis_manager.get_key(lock_key)
        if current is None:
            # 第一次失败，设置计数 + 过期时间
            await redis_manager.set_key(lock_key, "1", expire=self.LOCK_TIME)
        else:
            new_count = int(current) + 1
            await redis_manager.set_key(lock_key, str(new_count), expire=self.LOCK_TIME)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*"
    )
