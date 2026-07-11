#!/usr/bin/env python3
"""
检查数据库中的管理员用户
"""

import sqlite3
import asyncio
from app.core.database import async_session
from app.models.user import User, UserRole
from sqlalchemy import select

def check_admin_users_sqlite():
    """使用SQLite直接检查管理员用户"""
    print("🔍 使用SQLite检查管理员用户...")
    
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 查询所有用户
        cursor.execute("SELECT id, username, email, role, is_active, hashed_password FROM user")
        users = cursor.fetchall()
        
        print(f"总用户数: {len(users)}")
        print("\n所有用户:")
        for user in users:
            user_id, username, email, role, is_active, hashed_password = user
            print(f"  ID: {user_id}, 用户名: {username}, 邮箱: {email}, 角色: {role}, 激活: {is_active}")
        
        # 查询管理员用户
        cursor.execute("SELECT id, username, email, role, is_active FROM user WHERE role LIKE '%admin%'")
        admin_users = cursor.fetchall()
        
        print(f"\n管理员用户数: {len(admin_users)}")
        if admin_users:
            print("管理员用户:")
            for user in admin_users:
                user_id, username, email, role, is_active = user
                print(f"  ID: {user_id}, 用户名: {username}, 邮箱: {email}, 角色: {role}, 激活: {is_active}")
        else:
            print("❌ 没有找到管理员用户")
        
        conn.close()
        return admin_users
        
    except Exception as e:
        print(f"❌ SQLite查询失败: {e}")
        return []

async def check_admin_users_async():
    """使用异步会话检查管理员用户"""
    print("\n🔍 使用异步会话检查管理员用户...")
    
    try:
        async with async_session() as session:
            # 查询所有用户
            result = await session.execute(select(User))
            users = result.scalars().all()
            
            print(f"总用户数: {len(users)}")
            print("\n所有用户:")
            for user in users:
                print(f"  ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 角色: {user.role}, 激活: {user.is_active}")
            
            # 查询管理员用户
            admin_result = await session.execute(select(User).where(User.role == UserRole.ADMIN))
            admin_users = admin_result.scalars().all()
            
            print(f"\n管理员用户数: {len(admin_users)}")
            if admin_users:
                print("管理员用户:")
                for user in admin_users:
                    print(f"  ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 角色: {user.role}, 激活: {user.is_active}")
            else:
                print("❌ 没有找到管理员用户")
            
            return admin_users
            
    except Exception as e:
        print(f"❌ 异步查询失败: {e}")
        return []

def create_admin_user():
    """创建一个管理员用户"""
    print("\n📝 创建管理员用户...")
    
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 检查是否已存在admin用户
        cursor.execute("SELECT id FROM user WHERE username = 'admin'")
        existing = cursor.fetchone()
        
        if existing:
            print("✅ admin用户已存在")
            conn.close()
            return True
        
        # 创建admin用户
        from app.core.security import get_password_hash
        hashed_password = get_password_hash("admin123")
        
        cursor.execute("""
            INSERT INTO user (username, email, full_name, hashed_password, role, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, ("admin", "admin@example.com", "管理员", hashed_password, "ADMIN", True))
        
        conn.commit()
        conn.close()
        print("✅ admin用户创建成功")
        print("   用户名: admin")
        print("   密码: admin123")
        return True
        
    except Exception as e:
        print(f"❌ 创建管理员用户失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 管理员用户检查工具")
    print("=" * 50)
    
    # 使用SQLite检查
    admin_users_sqlite = check_admin_users_sqlite()
    
    # 使用异步会话检查
    admin_users_async = asyncio.run(check_admin_users_async())
    
    # 如果没有管理员用户，创建一个
    if not admin_users_sqlite and not admin_users_async:
        print("\n📝 没有找到管理员用户，尝试创建一个...")
        if create_admin_user():
            print("\n🔄 重新检查管理员用户...")
            check_admin_users_sqlite()
    
    print("\n" + "=" * 50)
    print("💡 建议:")
    print("1. 确保有管理员用户存在")
    print("2. 确保管理员用户角色为 'ADMIN'")
    print("3. 确保管理员用户状态为激活")
    print("4. 使用正确的用户名和密码登录")
    print("5. 管理后台地址: http://localhost:8000/jianai/login")

if __name__ == "__main__":
    main() 