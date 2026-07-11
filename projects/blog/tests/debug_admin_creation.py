#!/usr/bin/env python3
"""
详细诊断管理后台用户创建和登录问题
"""

import requests
import json
import sqlite3
import os

BASE_URL = "http://localhost:8000"
ADMIN_PATH = "/jianai"

def test_register_api():
    """测试注册API"""
    print("🔍 测试注册API...")
    
    # 测试数据
    test_users = [
        {
            "username": "admin1",
            "email": "admin1@example.com",
            "password": "admin123",
            "full_name": "管理员1",
            "role": "admin"
        },
        {
            "username": "admin2",
            "email": "admin2@example.com",
            "password": "admin123",
            "full_name": "管理员2",
            "role": "admin"
        }
    ]
    
    for user_data in test_users:
        print(f"\n📝 尝试创建用户: {user_data['username']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/register",
                json=user_data,
                timeout=10
            )
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code in [200, 201]:
                print("✅ 用户创建成功")
                result = response.json()
                if "access_token" in result:
                    print(f"✅ 返回了访问令牌: {result['access_token'][:20]}...")
            else:
                print("❌ 用户创建失败")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")

def check_database_directly():
    """直接检查数据库"""
    print("\n🔍 直接检查数据库...")
    
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 检查用户表结构
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        print("用户表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 检查所有用户
        cursor.execute("SELECT id, username, email, role, is_active FROM user")
        users = cursor.fetchall()
        
        print(f"\n找到 {len(users)} 个用户:")
        for user in users:
            user_id, username, email, role, is_active = user
            print(f"  - ID: {user_id}, 用户名: {username}, 邮箱: {email}, 角色: {role}, 状态: {is_active}")
        
        # 检查管理员用户
        cursor.execute("SELECT id, username, email, role, is_active, hashed_password FROM user WHERE role = 'admin'")
        admin_users = cursor.fetchall()
        
        print(f"\n找到 {len(admin_users)} 个管理员用户:")
        for user in admin_users:
            user_id, username, email, role, is_active, hashed_password = user
            print(f"  - ID: {user_id}")
            print(f"    用户名: {username}")
            print(f"    邮箱: {email}")
            print(f"    角色: {role}")
            print(f"    状态: {'激活' if is_active else '禁用'}")
            print(f"    密码哈希: {hashed_password[:20] if hashed_password else 'None'}...")
            print()
        
        conn.close()
        return admin_users
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return []

def test_admin_login_detailed(username, password):
    """详细测试管理后台登录"""
    print(f"\n🔐 详细测试管理后台登录: {username}")
    
    try:
        # 1. 获取登录页面
        print("1. 获取登录页面...")
        response = requests.get(f"{BASE_URL}{ADMIN_PATH}/login", timeout=10)
        print(f"   登录页面状态码: {response.status_code}")
        
        # 2. 提交登录表单
        print("2. 提交登录表单...")
        login_data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(
            f"{BASE_URL}{ADMIN_PATH}/login",
            data=login_data,
            allow_redirects=False,
            timeout=10
        )
        
        print(f"   登录响应状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"   重定向到: {location}")
            if 'login' not in location:
                print("✅ 登录成功，重定向到管理后台")
                return True
            else:
                print("❌ 登录失败，重定向回登录页面")
                return False
        elif response.status_code == 200:
            print("⚠️ 登录页面返回，检查内容...")
            content = response.text.lower()
            if "error" in content or "invalid" in content:
                print("❌ 页面包含错误信息")
            else:
                print("⚠️ 页面没有明显错误信息")
            return False
        else:
            print(f"❌ 意外的响应状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        return False

def create_admin_via_sql():
    """通过SQL直接创建管理员用户"""
    print("\n🔧 通过SQL直接创建管理员用户...")
    
    try:
        from app.core.security import get_password_hash
        
        # 创建密码哈希
        password = "admin123"
        hashed_password = get_password_hash(password)
        
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 检查用户是否已存在
        cursor.execute("SELECT id FROM user WHERE username = ?", ("admin_sql",))
        if cursor.fetchone():
            print("⚠️ 用户 admin_sql 已存在")
            conn.close()
            return True
        
        # 插入新用户
        cursor.execute("""
            INSERT INTO user (username, email, full_name, role, is_active, hashed_password, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, ("admin_sql", "admin_sql@example.com", "SQL管理员", "admin", True, hashed_password))
        
        conn.commit()
        print("✅ 通过SQL成功创建管理员用户: admin_sql")
        print(f"   密码: {password}")
        print(f"   密码哈希: {hashed_password[:20]}...")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ SQL创建失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 管理后台用户创建和登录详细诊断")
    print("=" * 60)
    
    # 检查服务器
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ 后端服务器未正常运行")
            return
        print("✅ 后端服务器运行正常")
    except Exception as e:
        print(f"❌ 无法连接到后端服务器: {e}")
        return
    
    # 测试注册API
    test_register_api()
    
    # 检查数据库
    admin_users = check_database_directly()
    
    # 如果没有管理员用户，尝试通过SQL创建
    if not admin_users:
        print("\n📝 没有找到管理员用户，尝试通过SQL创建...")
        if create_admin_via_sql():
            admin_users = check_database_directly()
    
    # 测试登录
    if admin_users:
        print("\n🔐 测试管理员登录...")
        for user in admin_users:
            username = user[1]  # username字段
            print(f"\n测试用户: {username}")
            
            # 尝试登录
            if test_admin_login_detailed(username, "admin123"):
                print(f"✅ 登录成功！用户名: {username}, 密码: admin123")
                break
            else:
                print(f"❌ 用户 {username} 登录失败")
    
    print("\n" + "=" * 60)
    print("💡 诊断总结:")
    print("1. 检查注册API是否正常工作")
    print("2. 检查数据库中是否有管理员用户")
    print("3. 检查管理员用户的密码哈希是否正确")
    print("4. 检查管理后台登录逻辑")
    print("5. 检查浏览器控制台错误")

if __name__ == "__main__":
    main() 