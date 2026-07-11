#!/usr/bin/env python3
"""
测试UserRole枚举和数据库值的兼容性
"""

import asyncio
from app.core.database import async_session
from app.models.user import User, UserRole
from sqlalchemy import select
import sqlite3

def check_enum_values():
    """检查枚举值"""
    print("🔍 检查UserRole枚举值...")
    print(f"UserRole.ADMIN = {UserRole.ADMIN}")
    print(f"UserRole.ADMIN.value = {UserRole.ADMIN.value}")
    print(f"UserRole.ADMIN.name = {UserRole.ADMIN.name}")
    
    print(f"\n所有枚举值:")
    for role in UserRole:
        print(f"  {role.name} = '{role.value}'")
    
    # 测试字符串转换
    print(f"\n字符串转换测试:")
    test_values = ['admin', 'ADMIN', 'moderator', 'user', 'USER']
    for value in test_values:
        try:
            role = UserRole(value)
            print(f"  '{value}' -> {role}")
        except ValueError as e:
            print(f"  '{value}' -> 错误: {e}")

def check_database_values():
    """检查数据库中的值"""
    print("\n🔍 检查数据库中的角色值...")
    
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, role FROM user WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            username, role_value = result
            print(f"admin用户的角色值: '{role_value}'")
            
            # 测试枚举转换
            try:
                role = UserRole(role_value)
                print(f"✅ 可以转换为枚举: {role}")
            except ValueError as e:
                print(f"❌ 无法转换为枚举: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")

async def test_sqlmodel_query():
    """测试SQLModel查询"""
    print("\n🔍 测试SQLModel查询...")
    
    try:
        async with async_session() as session:
            # 直接查询admin用户
            result = await session.execute(select(User).where(User.username == "admin"))
            user = result.scalar_one_or_none()
            
            if user:
                print(f"✅ 找到admin用户")
                print(f"   用户名: {user.username}")
                print(f"   角色: {user.role}")
                print(f"   角色类型: {type(user.role)}")
                
                if hasattr(user.role, 'value'):
                    print(f"   角色值: {user.role.value}")
                
                # 测试角色比较
                print(f"\n角色比较测试:")
                print(f"  user.role == UserRole.ADMIN: {user.role == UserRole.ADMIN}")
                print(f"  user.role == 'admin': {user.role == 'admin'}")
                print(f"  str(user.role) == 'admin': {str(user.role) == 'admin'}")
                
            else:
                print("❌ 未找到admin用户")
                
    except Exception as e:
        print(f"❌ SQLModel查询失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🔧 测试UserRole枚举")
    print("=" * 50)
    
    # 检查枚举值
    check_enum_values()
    
    # 检查数据库值
    check_database_values()
    
    # 测试SQLModel查询
    asyncio.run(test_sqlmodel_query())
    
    print("\n" + "=" * 50)
    print("📋 测试完成")

if __name__ == "__main__":
    main() 