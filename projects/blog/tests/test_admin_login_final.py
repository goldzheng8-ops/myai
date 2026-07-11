#!/usr/bin/env python3
"""
最终的管理后台登录测试
"""

import requests
import webbrowser

def test_admin_login():
    """测试管理后台登录"""
    print("🔍 测试管理后台登录...")
    
    session = requests.Session()
    
    try:
        # 1. 获取登录页面
        print("1. 获取登录页面...")
        response = session.get('http://localhost:8000/jianai/login', timeout=10)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code != 200:
            print("   ❌ 无法获取登录页面")
            return False
        
        # 2. 提交登录表单
        print("2. 提交登录表单...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = session.post(
            'http://localhost:8000/jianai/login',
            data=login_data,
            allow_redirects=False,
            timeout=10
        )
        
        print(f"   登录响应状态码: {response.status_code}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"   重定向到: {location}")
            
            if 'login' not in location:
                print("   ✅ 登录成功！")
                
                # 3. 测试访问管理后台
                print("3. 测试访问管理后台...")
                response = session.get('http://localhost:8000/jianai/', timeout=10)
                print(f"   管理后台状态码: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ 可以访问管理后台")
                    return True
                else:
                    print("   ❌ 无法访问管理后台")
                    return False
            else:
                print("   ❌ 登录失败，重定向回登录页面")
                return False
        else:
            print("   ❌ 登录失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False

def open_admin_login():
    """打开管理后台登录页面"""
    print("\n🌐 打开管理后台登录页面...")
    
    login_url = "http://localhost:8000/jianai/login"
    print(f"登录页面URL: {login_url}")
    
    try:
        webbrowser.open(login_url)
        print("✅ 已在浏览器中打开登录页面")
        return True
    except Exception as e:
        print(f"❌ 无法打开浏览器: {e}")
        return False

def main():
    """主函数"""
    print("🔧 最终管理后台登录测试")
    print("=" * 50)
    
    # 测试登录
    if test_admin_login():
        print("\n🎉 管理后台登录测试成功！")
        print("💡 现在可以在浏览器中正常登录管理后台了")
        
        # 询问是否打开浏览器
        choice = input("\n是否要在浏览器中打开登录页面？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是', 'Y']:
            open_admin_login()
    else:
        print("\n❌ 管理后台登录测试失败")
        print("💡 请检查:")
        print("   1. 服务器是否正常运行")
        print("   2. 管理员用户是否存在")
        print("   3. 密码是否正确")

if __name__ == "__main__":
    main() 