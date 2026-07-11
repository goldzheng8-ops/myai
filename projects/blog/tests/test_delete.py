#!/usr/bin/env python3
"""
测试管理后台删除功能
"""

import sqlite3
import requests
import json

def check_database():
    """检查数据库中的用户"""
    print("🔍 检查数据库中的用户...")
    
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 检查所有用户
        cursor.execute("SELECT id, username, role, is_active FROM user")
        users = cursor.fetchall()
        
        print(f"总用户数: {len(users)}")
        for user in users:
            user_id, username, role, is_active = user
            print(f"  - ID: {user_id}, 用户名: {username}, 角色: {role}, 状态: {is_active}")
        
        # 检查管理员用户
        cursor.execute("SELECT id, username, role FROM user WHERE role = 'ADMIN'")
        admin_users = cursor.fetchall()
        print(f"\n管理员用户数: {len(admin_users)}")
        for user in admin_users:
            print(f"  - ID: {user[0]}, 用户名: {user[1]}, 角色: {user[2]}")
        
        conn.close()
        return users, admin_users
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return [], []

def test_admin_login():
    """测试管理后台登录"""
    print("\n🔍 测试管理后台登录...")
    
    try:
        # 测试登录页面
        response = requests.get("http://localhost:8000/jianai/login")
        print(f"登录页面状态码: {response.status_code}")
        
        # 尝试登录
        login_data = {
            "username": "aaa",
            "password": "123456"
        }
        
        response = requests.post(
            "http://localhost:8000/jianai/login",
            data=login_data,
            allow_redirects=False
        )
        
        print(f"登录响应状态码: {response.status_code}")
        print(f"登录响应头: {dict(response.headers)}")
        
        if response.status_code == 302:
            print("✅ 登录成功，有重定向")
            # 获取session cookie
            cookies = response.cookies
            return cookies
        else:
            print(f"❌ 登录失败，响应内容: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        return None

def test_delete_endpoints(cookies):
    """测试删除端点"""
    print("\n🔍 测试删除端点...")
    
    try:
        # 获取一个普通用户ID
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM user WHERE role = 'USER' LIMIT 1")
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_id, username = user
            print(f"测试删除用户: ID={user_id}, 用户名={username}")
            
            # 测试不同的删除端点格式
            endpoints_to_test = [
                f"http://localhost:8000/jianai/user/delete/{user_id}",
                f"http://localhost:8000/jianai/user/{user_id}/delete",
                f"http://localhost:8000/jianai/user/delete",
                f"http://localhost:8000/jianai/user/action/delete",
            ]
            
            for endpoint in endpoints_to_test:
                print(f"\n测试端点: {endpoint}")
                
                # 测试POST请求
                response = requests.post(
                    endpoint,
                    data={"pks": [user_id]},
                    cookies=cookies,
                    allow_redirects=False
                )
                print(f"  POST状态码: {response.status_code}")
                print(f"  POST响应: {response.text[:100]}")
                
                # 测试DELETE请求
                response = requests.delete(
                    endpoint,
                    cookies=cookies,
                    allow_redirects=False
                )
                print(f"  DELETE状态码: {response.status_code}")
                print(f"  DELETE响应: {response.text[:100]}")
        else:
            print("❌ 没有找到普通用户用于测试")
            
    except Exception as e:
        print(f"❌ 删除端点测试失败: {e}")

def test_admin_pages(cookies):
    """测试管理后台页面"""
    print("\n🔍 测试管理后台页面...")
    
    try:
        # 测试用户列表页面
        response = requests.get(
            "http://localhost:8000/jianai/user/list",
            cookies=cookies
        )
        print(f"用户列表页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 用户列表页面可访问")
            # 检查页面内容是否包含删除按钮
            if "delete" in response.text.lower():
                print("✅ 页面包含删除相关内容")
            else:
                print("❌ 页面不包含删除相关内容")
        else:
            print(f"❌ 用户列表页面不可访问: {response.text[:100]}")
            
    except Exception as e:
        print(f"❌ 管理后台页面测试失败: {e}")

if __name__ == "__main__":
    print("🔧 管理后台删除功能测试")
    print("=" * 50)
    
    # 检查数据库
    users, admin_users = check_database()
    
    # 测试登录
    cookies = test_admin_login()
    
    if cookies:
        # 测试删除端点
        test_delete_endpoints(cookies)
        
        # 测试管理后台页面
        test_admin_pages(cookies)
    
    print("\n" + "=" * 50)
    print("测试完成") 