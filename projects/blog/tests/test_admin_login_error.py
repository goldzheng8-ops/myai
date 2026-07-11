#!/usr/bin/env python3
"""
捕获管理后台登录的详细错误信息
"""

import requests
import json

BASE_URL = "http://localhost:8000"
ADMIN_PATH = "/jianai"

def test_admin_login_with_error_capture():
    """测试管理后台登录并捕获错误"""
    print("🔍 测试管理后台登录并捕获错误...")
    
    # 测试用户
    test_users = [
        ("admin_sql", "admin123"),
        ("admin1", "admin123"),
        ("admin", "admin123")
    ]
    
    for username, password in test_users:
        print(f"\n🔐 测试用户: {username}")
        
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
            print(f"   响应内容: {response.text}")
            
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                print(f"   重定向到: {location}")
                if 'login' not in location:
                    print("✅ 登录成功，重定向到管理后台")
                    return True
                else:
                    print("❌ 登录失败，重定向回登录页面")
            elif response.status_code == 200:
                print("⚠️ 登录页面返回，可能登录失败")
                return False
            elif response.status_code == 500:
                print("❌ 服务器内部错误")
                print(f"   错误详情: {response.text}")
                return False
            else:
                print(f"❌ 意外的响应状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    return False

def test_admin_auth_directly():
    """直接测试AdminAuth逻辑"""
    print("\n🔧 直接测试AdminAuth逻辑...")
    
    try:
        # 使用API登录获取token
        login_data = {
            "username": "admin_sql",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"✅ API登录成功，获取到token: {token[:20]}...")
            
            # 使用token访问管理后台
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}{ADMIN_PATH}/", headers=headers, timeout=10)
            print(f"管理后台访问状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 使用API token可以访问管理后台")
            else:
                print(f"❌ 使用API token无法访问管理后台: {response.status_code}")
        else:
            print(f"❌ API登录失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 直接测试失败: {e}")

def check_session_config():
    """检查会话配置"""
    print("\n🔍 检查会话配置...")
    
    try:
        # 检查健康端点
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"健康检查状态码: {response.status_code}")
        
        # 检查会话相关的响应头
        print(f"健康检查响应头: {dict(response.headers)}")
        
        # 尝试获取一个需要会话的页面
        response = requests.get(f"{BASE_URL}{ADMIN_PATH}/login", timeout=5)
        print(f"登录页面状态码: {response.status_code}")
        print(f"登录页面响应头: {dict(response.headers)}")
        
        # 检查是否有Set-Cookie头
        set_cookie = response.headers.get('Set-Cookie')
        if set_cookie:
            print(f"✅ 会话Cookie已设置: {set_cookie[:50]}...")
        else:
            print("⚠️ 没有设置会话Cookie")
            
    except Exception as e:
        print(f"❌ 会话配置检查失败: {e}")

def main():
    """主函数"""
    print("🔧 管理后台登录错误详细诊断")
    print("=" * 60)
    
    # 检查会话配置
    check_session_config()
    
    # 测试管理后台登录
    test_admin_login_with_error_capture()
    
    # 直接测试AdminAuth逻辑
    test_admin_auth_directly()
    
    print("\n" + "=" * 60)
    print("💡 可能的解决方案:")
    print("1. 检查SessionMiddleware配置")
    print("2. 检查AdminAuth类的login方法")
    print("3. 检查数据库连接和用户查询")
    print("4. 检查密码验证逻辑")
    print("5. 检查会话存储配置")

if __name__ == "__main__":
    main() 