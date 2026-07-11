#!/usr/bin/env python3
"""
详细诊断管理后台登录问题
"""

import requests
import json
import sqlite3
import asyncio
from app.core.database import async_session
from app.models.user import User, UserRole
from sqlalchemy import select

BASE_URL = "http://localhost:8000"
ADMIN_PATH = "/jianai"

def check_server_status():
    """检查服务器状态"""
    print("🔍 检查服务器状态...")
    
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

def check_database_connection():
    """检查数据库连接"""
    print("\n🔍 检查数据库连接...")
    
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 检查admin用户
        cursor.execute("SELECT id, username, role, is_active, hashed_password FROM user WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            user_id, username, role, is_active, hashed_password = result
            print(f"✅ 找到admin用户:")
            print(f"   ID: {user_id}")
            print(f"   用户名: {username}")
            print(f"   角色: '{role}'")
            print(f"   激活状态: {is_active}")
            print(f"   密码哈希: {'已设置' if hashed_password else '未设置'}")
            
            if role != 'ADMIN':
                print(f"❌ 角色错误: 期望 'ADMIN', 实际 '{role}'")
                return False
            if not is_active:
                print("❌ 用户未激活")
                return False
            if not hashed_password:
                print("❌ 密码哈希未设置")
                return False
                
            return True
        else:
            print("❌ 未找到admin用户")
            return False
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_session_middleware():
    """检查Session中间件"""
    print("\n🔍 检查Session中间件...")
    
    try:
        session = requests.Session()
        
        # 访问登录页面
        response = session.get(f"{BASE_URL}{ADMIN_PATH}/login", timeout=10)
        print(f"   登录页面状态码: {response.status_code}")
        
        # 检查是否有session cookie
        cookies = dict(session.cookies)
        print(f"   初始Cookie: {cookies}")
        
        # 提交登录表单
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
        
        # 检查登录后的cookie
        cookies_after = dict(session.cookies)
        print(f"   登录后Cookie: {cookies_after}")
        
        if 'session' in cookies_after:
            print("✅ Session Cookie已设置")
            
            # 尝试访问管理后台
            response = session.get(f"{BASE_URL}{ADMIN_PATH}/", timeout=10)
            print(f"   管理后台状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 可以访问管理后台")
                return True
            else:
                print("❌ 无法访问管理后台")
                return False
        else:
            print("❌ Session Cookie未设置")
            return False
            
    except Exception as e:
        print(f"❌ Session测试失败: {e}")
        return False

async def check_admin_auth_logic():
    """检查AdminAuth逻辑"""
    print("\n🔍 检查AdminAuth逻辑...")
    
    try:
        async with async_session() as session:
            # 查找admin用户
            result = await session.execute(select(User).where(User.username == "admin"))
            user = result.scalar_one_or_none()
            
            if user:
                print(f"✅ 找到admin用户: {user.username}")
                print(f"   角色: {user.role}")
                print(f"   角色类型: {type(user.role)}")
                print(f"   激活状态: {user.is_active}")
                
                # 测试角色比较
                is_admin = user.role == UserRole.ADMIN
                print(f"   是管理员: {is_admin}")
                
                if is_admin and user.is_active:
                    print("✅ AdminAuth逻辑检查通过")
                    return True
                else:
                    print("❌ AdminAuth逻辑检查失败")
                    return False
            else:
                print("❌ 未找到admin用户")
                return False
                
    except Exception as e:
        print(f"❌ AdminAuth逻辑检查失败: {e}")
        return False

def test_browser_simulation():
    """模拟浏览器行为"""
    print("\n🔍 模拟浏览器行为...")
    
    try:
        session = requests.Session()
        
        # 设置User-Agent模拟浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 1. 访问登录页面
        print("1. 访问登录页面...")
        response = session.get(f"{BASE_URL}{ADMIN_PATH}/login", headers=headers, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code != 200:
            print("❌ 无法获取登录页面")
            return False
        
        # 2. 提交登录表单
        print("\n2. 提交登录表单...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = session.post(
            f"{BASE_URL}{ADMIN_PATH}/login",
            data=login_data,
            headers=headers,
            allow_redirects=False,
            timeout=10
        )
        
        print(f"   登录响应状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"   重定向到: {location}")
            
            # 3. 跟随重定向
            print("\n3. 跟随重定向...")
            response = session.get(location, headers=headers, timeout=10)
            print(f"   重定向后状态码: {response.status_code}")
            print(f"   最终URL: {response.url}")
            
            if response.status_code == 200:
                content = response.text
                if "博客管理系统" in content or "用户管理" in content:
                    print("✅ 成功进入管理后台")
                    return True
                else:
                    print("⚠️ 页面内容不是管理后台")
                    print(f"   页面长度: {len(content)}")
                    print(f"   页面片段: {content[:200]}...")
                    return False
            else:
                print("❌ 重定向后无法访问")
                return False
        else:
            print("❌ 登录失败，没有重定向")
            return False
            
    except Exception as e:
        print(f"❌ 浏览器模拟失败: {e}")
        return False

def check_configuration():
    """检查配置"""
    print("\n🔍 检查配置...")
    
    try:
        from app.core.config import settings
        print(f"   调试模式: {settings.debug}")
        print(f"   密钥: {settings.secret_key[:20]}..." if settings.secret_key else "未设置")
        print(f"   允许的源: {settings.allowed_origins}")
        
        # 检查SessionMiddleware配置
        from app.core.middleware import setup_middleware
        print("✅ 配置检查完成")
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 详细诊断管理后台登录问题")
    print("=" * 60)
    
    # 检查各项
    checks = [
        ("服务器状态", check_server_status),
        ("数据库连接", check_database_connection),
        ("Session中间件", check_session_middleware),
        ("AdminAuth逻辑", lambda: asyncio.run(check_admin_auth_logic())),
        ("浏览器模拟", test_browser_simulation),
        ("配置检查", check_configuration),
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ {name}检查异常: {e}")
            results[name] = False
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 诊断结果总结:")
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
    
    failed_checks = [name for name, result in results.items() if not result]
    
    if not failed_checks:
        print("\n🎉 所有检查都通过了！")
        print("💡 如果浏览器中还是不行，可能是:")
        print("   1. 浏览器缓存问题 - 清除缓存和Cookie")
        print("   2. 浏览器扩展干扰 - 禁用扩展")
        print("   3. 网络代理问题 - 检查代理设置")
    else:
        print(f"\n❌ 以下检查失败: {', '.join(failed_checks)}")
        print("💡 请根据失败的检查项进行修复")

if __name__ == "__main__":
    main() 