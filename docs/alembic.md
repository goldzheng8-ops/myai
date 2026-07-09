# 初始化
alembic init migrations

# 修改env.py

导入：
from app.core.config import settings
from app.db.base import Base

导入所有 Model，确保 metadata 已注册
from app.models.news import News


config = context.config下行新增：
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url
)

修改target_metadata值
target_metadata = Base.metadata

# 正常迁移
alembic revision --autogenerate -m "add unique constraint to news url"
alembic upgrade head

# 写错时
alembic downgrade -1
alembic downgrade base

# 验证配置
alembic current

