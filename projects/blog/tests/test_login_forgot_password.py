#!/usr/bin/env python3
"""
测试登录页面找回密码功能的显示/隐藏
"""
import requests
import time
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def test_auth_config():
    """测试获取认证配置"""
    print("=== 测试获取认证配置 ===")
    
    url = f"{BASE_URL}/api/v1/auth/config"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            config = response.json()
            email_enabled = config.get('email_enabled', False)
            print(f"邮箱功能启用: {email_enabled}")
            return email_enabled
        else:
            print(f"❌ 请求失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def test_forgot_password_api():
    """测试忘记密码API"""
    print("\n=== 测试忘记密码API ===")
    
    url = f"{BASE_URL}/api/v1/auth/forgot-password"
    data = {"email": "test@example.com"}
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 忘记密码API正常")
            return True
        else:
            print("❌ 忘记密码API异常")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_frontend_page():
    """测试前端页面"""
    print("\n=== 测试前端页面 ===")
    
    try:
        # 测试登录页面
        login_url = f"{FRONTEND_URL}/login"
        response = requests.get(login_url)
        print(f"登录页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 登录页面可访问")
            
            # 检查页面内容是否包含找回密码相关元素
            content = response.text
            if "忘记密码" in content or "forgot-password" in content:
                print("✅ 登录页面包含找回密码元素")
            else:
                print("⚠️  登录页面可能不包含找回密码元素")
        else:
            print("❌ 登录页面无法访问")
        
        # 测试忘记密码页面
        forgot_url = f"{FRONTEND_URL}/forgot-password"
        response = requests.get(forgot_url)
        print(f"忘记密码页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 忘记密码页面可访问")
        else:
            print("❌ 忘记密码页面无法访问")
            
    except Exception as e:
        print(f"❌ 前端页面测试异常: {e}")

def test_dynamic_behavior():
    """测试动态行为"""
    print("\n=== 测试动态行为 ===")
    
    # 测试EMAIL_ENABLED=true时
    print("\n1. 测试EMAIL_ENABLED=true时:")
    os.environ['EMAIL_ENABLED'] = 'true'
    email_enabled = test_auth_config()
    
    if email_enabled:
        print("✅ EMAIL_ENABLED=true时，找回密码功能应该显示")
    else:
        print("❌ EMAIL_ENABLED=true时，找回密码功能应该显示但配置显示为false")
    
    # 测试EMAIL_ENABLED=false时
    print("\n2. 测试EMAIL_ENABLED=false时:")
    os.environ['EMAIL_ENABLED'] = 'false'
    email_enabled = test_auth_config()
    
    if not email_enabled:
        print("✅ EMAIL_ENABLED=false时，找回密码功能应该隐藏")
    else:
        print("❌ EMAIL_ENABLED=false时，找回密码功能应该隐藏但配置显示为true")

def main():
    """主函数"""
    print("登录页面找回密码功能测试")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ 后端服务器未正常运行，请先启动服务器")
            return
    except:
        print("❌ 无法连接到后端服务器，请先启动服务器")
        return
    
    print("✅ 后端服务器连接正常")
    
    # 检查前端是否运行
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code != 200:
            print("⚠️  前端服务器可能未运行，但继续测试后端功能")
    except:
        print("⚠️  无法连接到前端服务器，但继续测试后端功能")
    
    # 测试认证配置
    email_enabled = test_auth_config()
    if email_enabled is None:
        print("❌ 无法获取认证配置，测试终止")
        return
    
    print(f"\n当前EMAIL_ENABLED状态: {email_enabled}")
    print(f"找回密码功能应该: {'显示' if email_enabled else '隐藏'}")
    
    # 测试忘记密码API
    test_forgot_password_api()
    
    # 测试前端页面
    test_frontend_page()
    
    # 测试动态行为
    test_dynamic_behavior()
    
    print("\n=== 测试完成 ===")
    print("💡 提示:")
    print("1. 如果EMAIL_ENABLED=true，登录页面应该显示'忘记密码？'链接")
    print("2. 如果EMAIL_ENABLED=false，登录页面应该隐藏'忘记密码？'链接")
    print("3. 点击'忘记密码？'链接应该跳转到/forgot-password页面")
    print("4. 忘记密码页面应该可以发送密码重置邮件")

if __name__ == "__main__":
    main() 