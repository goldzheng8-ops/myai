#!/usr/bin/env python3
"""
测试重置密码功能
"""
import requests
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_forgot_password():
    """测试忘记密码功能"""
    print("=== 测试忘记密码功能 ===")
    
    url = f"{BASE_URL}/api/v1/auth/forgot-password"
    data = {"email": "trumpmaga@qq.com"}  # 使用你的测试邮箱
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 忘记密码请求成功")
            return True
        else:
            print("❌ 忘记密码请求失败")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_reset_password_api():
    """测试重置密码API"""
    print("\n=== 测试重置密码API ===")
    
    # 注意：这里需要一个有效的重置token，通常从邮件中获取
    # 为了测试，我们使用一个无效的token
    url = f"{BASE_URL}/api/v1/auth/reset-password"
    data = {
        "token": "invalid_token_for_testing",
        "new_password": "newpassword123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 422:
            print("✅ 重置密码API正常（返回422是预期的，因为token无效）")
            return True
        elif response.status_code == 401:
            print("✅ 重置密码API正常（返回401是预期的，因为token无效）")
            return True
        else:
            print("⚠️  重置密码API响应异常")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_frontend_routes():
    """测试前端路由"""
    print("\n=== 测试前端路由 ===")
    
    try:
        # 测试忘记密码页面
        forgot_url = "http://localhost:5173/forgot-password"
        response = requests.get(forgot_url)
        print(f"忘记密码页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 忘记密码页面可访问")
        else:
            print("❌ 忘记密码页面无法访问")
        
        # 测试重置密码页面（带无效token）
        reset_url = "http://localhost:5173/reset-password?token=invalid_token"
        response = requests.get(reset_url)
        print(f"重置密码页面状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 重置密码页面可访问")
        else:
            print("❌ 重置密码页面无法访问")
            
    except Exception as e:
        print(f"❌ 前端路由测试异常: {e}")

def test_email_config():
    """测试邮箱配置"""
    print("\n=== 测试邮箱配置 ===")
    
    url = f"{BASE_URL}/api/v1/auth/config"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            config = response.json()
            email_enabled = config.get('email_enabled', False)
            print(f"邮箱功能启用: {email_enabled}")
            
            if email_enabled:
                print("✅ 邮箱功能已启用，可以发送重置密码邮件")
                return True
            else:
                print("⚠️  邮箱功能已禁用，无法发送重置密码邮件")
                return False
        else:
            print("❌ 无法获取邮箱配置")
            return False
            
    except Exception as e:
        print(f"❌ 邮箱配置测试异常: {e}")
        return False

def main():
    """主函数"""
    print("重置密码功能测试")
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
    
    # 测试邮箱配置
    email_enabled = test_email_config()
    
    if email_enabled:
        # 测试忘记密码功能
        test_forgot_password()
    
    # 测试重置密码API
    test_reset_password_api()
    
    # 测试前端路由
    test_frontend_routes()
    
    print("\n=== 测试完成 ===")
    print("💡 使用说明:")
    print("1. 确保EMAIL_ENABLED=true")
    print("2. 访问 http://localhost:5173/forgot-password 申请密码重置")
    print("3. 检查邮箱，点击重置链接")
    print("4. 在重置页面输入新密码")
    print("5. 使用新密码登录")

if __name__ == "__main__":
    main() 