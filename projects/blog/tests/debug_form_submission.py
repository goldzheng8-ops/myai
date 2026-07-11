#!/usr/bin/env python3
"""
调试表单提交问题
"""

import requests
import json

BASE_URL = "http://localhost:8000"
ADMIN_PATH = "/jianai"

def check_login_page_form():
    """检查登录页面的表单结构"""
    print("🔍 检查登录页面表单结构...")
    
    try:
        response = requests.get(f"{BASE_URL}{ADMIN_PATH}/login", timeout=10)
        print(f"登录页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查表单元素
            if 'name="username"' in content:
                print("✅ 找到用户名输入框")
            else:
                print("❌ 未找到用户名输入框")
                
            if 'name="password"' in content:
                print("✅ 找到密码输入框")
            else:
                print("❌ 未找到密码输入框")
                
            if 'method="post"' in content:
                print("✅ 表单使用POST方法")
            else:
                print("❌ 表单未使用POST方法")
                
            if 'action=' in content:
                print("✅ 表单有action属性")
            else:
                print("❌ 表单缺少action属性")
                
            # 检查CSRF token
            if 'csrf' in content.lower() or 'token' in content.lower():
                print("⚠️ 可能包含CSRF token")
            else:
                print("ℹ️ 没有CSRF token")
                
            # 检查JavaScript错误
            if 'error' in content.lower():
                print("⚠️ 页面包含错误信息")
                
            return content
        else:
            print(f"❌ 无法获取登录页面: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 检查登录页面失败: {e}")
        return None

def test_form_submission_with_session():
    """使用会话测试表单提交"""
    print("\n🔍 使用会话测试表单提交...")
    
    session = requests.Session()
    
    # 1. 获取登录页面
    print("1. 获取登录页面...")
    response = session.get(f"{BASE_URL}{ADMIN_PATH}/login", timeout=10)
    print(f"   状态码: {response.status_code}")
    print(f"   Cookie: {dict(session.cookies)}")
    
    # 2. 提交登录表单
    print("\n2. 提交登录表单...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = session.post(
        f"{BASE_URL}{ADMIN_PATH}/login",
        data=login_data,
        allow_redirects=False,
        timeout=10
    )
    
    print(f"   登录响应状态码: {response.status_code}")
    print(f"   响应头: {dict(response.headers)}")
    print(f"   Cookie: {dict(session.cookies)}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', '')
        print(f"   重定向到: {location}")
        
        # 3. 跟随重定向
        print("\n3. 跟随重定向...")
        response = session.get(location, timeout=10)
        print(f"   重定向后状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 登录成功，可以访问管理后台")
            return True
        else:
            print("❌ 重定向后无法访问管理后台")
            return False
    else:
        print("❌ 登录失败，没有重定向")
        return False

def test_form_submission_without_session():
    """不使用会话测试表单提交"""
    print("\n🔍 不使用会话测试表单提交...")
    
    # 直接提交表单，不使用会话
    login_data = {
        "username": "admin",
        "password": "admin123"
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
        print("✅ 表单提交成功，有重定向")
        return True
    else:
        print("❌ 表单提交失败")
        return False

def check_admin_auth_debug():
    """检查AdminAuth的调试信息"""
    print("\n🔍 检查AdminAuth调试信息...")
    
    # 创建一个简单的测试来模拟AdminAuth的行为
    try:
        # 先通过API登录获取用户信息
        api_response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"},
            timeout=10
        )
        
        if api_response.status_code == 200:
            api_data = api_response.json()
            print(f"✅ API登录成功")
            print(f"   用户ID: {api_data.get('user_info', {}).get('id')}")
            print(f"   用户名: {api_data.get('user_info', {}).get('username')}")
            print(f"   角色: {api_data.get('user_info', {}).get('role')}")
        else:
            print(f"❌ API登录失败: {api_response.status_code}")
            
    except Exception as e:
        print(f"❌ API登录测试失败: {e}")

def main():
    """主函数"""
    print("🔧 表单提交问题调试")
    print("=" * 50)
    
    # 检查登录页面表单
    content = check_login_page_form()
    
    # 测试表单提交
    if test_form_submission_with_session():
        print("\n✅ 会话表单提交测试通过")
    else:
        print("\n❌ 会话表单提交测试失败")
    
    if test_form_submission_without_session():
        print("✅ 无会话表单提交测试通过")
    else:
        print("❌ 无会话表单提交测试失败")
    
    # 检查AdminAuth调试信息
    check_admin_auth_debug()
    
    print("\n" + "=" * 50)
    print("💡 可能的问题和解决方案:")
    print("1. 浏览器缓存问题 - 清除缓存和Cookie")
    print("2. JavaScript错误 - 检查浏览器控制台")
    print("3. 表单验证问题 - 检查表单字段名称")
    print("4. CSRF token问题 - 检查是否需要CSRF token")
    print("5. 会话配置问题 - 检查SessionMiddleware")

if __name__ == "__main__":
    main() 