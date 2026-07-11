#!/usr/bin/env python3
"""
FastAPI Blog System 启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path
import uvicorn

def check_redis():
    """检查 Redis 是否运行"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis 连接正常")
        return True
    except Exception as e:
        print(f"❌ Redis 连接失败: {e}")
        print("请确保 Redis 服务正在运行")
        return False

def create_env_file():
    """创建 .env 文件"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 创建 .env 文件...")
        env_content = """# Database
DATABASE_URL=sqlite+aiosqlite:///./blog.db

# JWT Settings
SECRET_KEY=your-secret-key-here-make-it-long-and-secure-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Email Settings
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
EMAIL_USER=your-email@qq.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=your-email@qq.com
EMAIL_ENABLED=false

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# App Settings
APP_NAME=FastAPI Blog System
DEBUG=true

# Scheduler Settings
TIMEZONE=Asia/Shanghai

# OAuth Settings
# GitHub OAuth - Get from https://github.com/settings/developers
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Google OAuth - Get from https://console.cloud.google.com/apis/credentials
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# OAuth Base URL
OAUTH_BASE_URL=http://localhost:8000
"""
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env 文件已创建")
        print("⚠️  请编辑 .env 文件，配置你的邮箱信息并设置 EMAIL_ENABLED=true")
    else:
        print("✅ .env 文件已存在")

def install_dependencies():
    """安装依赖"""
    print("📦 检查依赖...")
    try:
        import fastapi
        import uvicorn
        import sqlmodel
        import redis
        print("✅ 所有依赖已安装")
    except ImportError:
        print("📦 安装依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")

def main():
    """主函数"""
    print("🚀 FastAPI Blog System 启动检查")
    print("=" * 50)
    
    # 检查依赖
    install_dependencies()
    
    # 创建 .env 文件
    create_env_file()
    
    # 检查 Redis
    if not check_redis():
        print("\n💡 启动 Redis 的提示:")
        print("Windows: redis-server")
        print("Linux/Mac: sudo service redis start")
        print("Docker: docker run -d -p 6379:6379 redis:alpine")
        return
    
    print("\n🎉 所有检查通过！")
    print("=" * 50)
    print("启动应用...")
    print("🌐 应用将在以下地址运行:")
    print("   - 本地访问: http://127.0.0.1:8000")
    print("   - API文档: http://127.0.0.1:8000/docs")
    print("   - ReDoc文档: http://127.0.0.1:8000/redoc")
    print("=" * 50)
    
    # 启动应用
    try:
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            reload_dirs=["app"],
        )
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main() 