#!/usr/bin/env python3
"""
测试管理后台登录功能
"""

import requests
import json
import sqlite3
import os

BASE_URL = "http://localhost:8000"
ADMIN_PATH = "/jianai"

def check_admin_users():
    """检查数据库中的管理员用户"""
    print("🔍 检查数据库中的管理员用户...")
    
    try:
        # 连接数据库
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 查询管理员用户
        cursor.execute("""
            SELECT id, username, email, role, is_active, hashed_password 
            FROM user 
            WHERE role = 'admin'
        """)
        
        admin_users = cursor.fetchall()
        
        if admin_users:
            print(f"✅ 找到 {len(admin_users)} 个管理员用户:")
            for user in admin_users:
                user_id, username, email, role, is_active, hashed_password = user
                print(f"   - ID: {user_id}")
                print(f"     用户名: {username}")
                print(f"     邮箱: {email}")
                print(f"     角色: {role}")
                print(f"     状态: {'激活' if is_active else '禁用'}")
                print(f"     密码哈希: {hashed_password[:20] if hashed_password else 'None'}...")
                print()
        else:
            print("❌ 没有找到管理员用户")
            
        conn.close()
        return admin_users
        
    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")
        return []

def test_admin_login(username, password):
    """测试管理后台登录"""
    print(f"🔐 测试管理后台登录: {username}")
    
    try:
        # 测试登录表单提交
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
        
        print(f"登录响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 302:
            print("✅ 登录成功，重定向到管理后台")
            return True
        elif response.status_code == 200:
            print("⚠️ 登录页面返回，可能登录失败")
            # 检查响应内容是否包含错误信息
            if "error" in response.text.lower() or "invalid" in response.text.lower():
                print("❌ 登录失败，页面包含错误信息")
            return False
        else:
            print(f"❌ 意外的响应状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False

def test_admin_page_access():
    """测试管理后台页面访问"""
    print("🔍 测试管理后台页面访问...")
    
    try:
        response = requests.get(f"{BASE_URL}{ADMIN_PATH}/", timeout=10)
        print(f"管理后台页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 管理后台页面可以访问")
            return True
        elif response.status_code == 302:
            print("✅ 管理后台页面重定向到登录页面（正常）")
            return True
        else:
            print(f"❌ 管理后台页面访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 管理后台页面访问失败: {e}")
        return False

def create_admin_user(username, password, email="admin@example.com"):
    """创建管理员用户"""
    print(f"👤 创建管理员用户: {username}")
    
    try:
        # 使用注册API创建管理员用户
        register_data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": "管理员",
            "role": "admin"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=register_data,
            timeout=10
        )
        
        print(f"注册响应状态码: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ 管理员用户创建成功")
            return True
        else:
            print(f"❌ 管理员用户创建失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 创建管理员用户失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 管理后台登录功能诊断")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ 后端服务器未正常运行")
            return
        print("✅ 后端服务器运行正常")
    except Exception as e:
        print(f"❌ 无法连接到后端服务器: {e}")
        return
    
    # 检查管理后台页面
    test_admin_page_access()
    
    # 检查现有管理员用户
    admin_users = check_admin_users()
    
    if not admin_users:
        print("\n📝 没有找到管理员用户，尝试创建一个...")
        if create_admin_user("admin", "admin123"):
            admin_users = check_admin_users()
    
    if admin_users:
        # 测试登录
        print("\n🔐 测试管理员登录...")
        for user in admin_users:
            username = user[1]  # username字段
            print(f"\n测试用户: {username}")
            
            # 尝试常见密码
            test_passwords = ["admin123", "admin", "password", "123456"]
            
            for password in test_passwords:
                print(f"尝试密码: {password}")
                if test_admin_login(username, password):
                    print(f"✅ 登录成功！用户名: {username}, 密码: {password}")
                    break
            else:
                print(f"❌ 用户 {username} 的所有测试密码都失败")
    
    print("\n" + "=" * 50)
    print("💡 诊断建议:")
    print("1. 确保有管理员用户存在")
    print("2. 确保管理员用户密码正确")
    print("3. 确保管理员用户状态为激活")
    print("4. 检查浏览器控制台是否有JavaScript错误")
    print("5. 尝试清除浏览器缓存和Cookie")

if __name__ == "__main__":
    main() 