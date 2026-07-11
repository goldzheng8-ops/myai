#!/usr/bin/env python3
"""
简单的管理后台登录测试
"""

import requests

BASE_URL = "http://localhost:8000"
ADMIN_PATH = "/jianai"

def test_admin_login():
    """测试管理后台登录"""
    print("🔍 测试管理后台登录...")
    
    # 测试用户列表
    test_users = [
        ("admin", "admin123"),
        ("admin1", "admin123"),
        ("admin2", "admin123"),
        ("admin_sql", "admin123")
    ]
    
    session = requests.Session()
    
    for username, password in test_users:
        print(f"\n🔐 测试用户: {username}")
        
        try:
            # 1. 获取登录页面
            print("  1. 获取登录页面...")
            response = session.get(f"{BASE_URL}{ADMIN_PATH}/login", timeout=10)
            print(f"     状态码: {response.status_code}")
            
            if response.status_code != 200:
                print("     ❌ 无法获取登录页面")
                continue
            
            # 2. 提交登录表单
            print("  2. 提交登录表单...")
            login_data = {
                "username": username,
                "password": password
            }
            
            response = session.post(
                f"{BASE_URL}{ADMIN_PATH}/login",
                data=login_data,
                allow_redirects=False,
                timeout=10
            )
            
            print(f"     登录响应状态码: {response.status_code}")
            
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                print(f"     重定向到: {location}")
                
                if 'login' not in location:
                    print("     ✅ 登录成功！")
                    print(f"     用户名: {username}")
                    print(f"     密码: {password}")
                    
                    # 测试访问管理后台主页
                    print("  3. 测试访问管理后台...")
                    response = session.get(f"{BASE_URL}{ADMIN_PATH}/", timeout=10)
                    print(f"     管理后台状态码: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("     ✅ 可以访问管理后台")
                        return True
                    else:
                        print("     ❌ 无法访问管理后台")
                else:
                    print("     ❌ 登录失败，重定向回登录页面")
            elif response.status_code == 200:
                print("     ❌ 登录失败，返回登录页面")
            else:
                print(f"     ❌ 意外的响应状态码: {response.status_code}")
                
        except Exception as e:
            print(f"     ❌ 请求失败: {e}")
    
    return False

def test_server_status():
    """测试服务器状态"""
    print("🔍 测试服务器状态...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        return False

def main():
    """主函数"""
    print("🔧 管理后台登录测试")
    print("=" * 50)
    
    # 测试服务器状态
    if not test_server_status():
        print("❌ 服务器未运行，请先启动服务器")
        return
    
    # 测试登录
    if test_admin_login():
        print("\n🎉 管理后台登录测试成功！")
        print("💡 现在可以在浏览器中正常登录管理后台了")
        print(f"   登录地址: {BASE_URL}{ADMIN_PATH}/login")
        print("   推荐使用: admin / admin123")
    else:
        print("\n❌ 管理后台登录测试失败")
        print("💡 请检查:")
        print("   1. 服务器是否正常运行")
        print("   2. 管理员用户是否存在")
        print("   3. 密码是否正确")
        print("   4. 浏览器控制台是否有错误")

if __name__ == "__main__":
    main() 