#!/usr/bin/env python3
"""
简单的服务器重启脚本
"""

import subprocess
import time
import requests
import webbrowser

def test_server_status():
    """测试服务器状态"""
    print("🔍 测试服务器状态...")
    
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ 服务器正在运行")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 服务器未运行: {e}")
        return False

def test_login_page_cache():
    """测试登录页面缓存"""
    print("\n🔍 测试登录页面缓存...")
    
    try:
        response = requests.get('http://localhost:8000/jianai/login', timeout=10)
        
        print(f"   登录页面状态码: {response.status_code}")
        print(f"   Cache-Control: {response.headers.get('Cache-Control', 'Not set')}")
        print(f"   Pragma: {response.headers.get('Pragma', 'Not set')}")
        print(f"   Expires: {response.headers.get('Expires', 'Not set')}")
        
        if 'no-cache' not in response.headers.get('Cache-Control', ''):
            print("   ✅ 登录页面可以被缓存")
            return True
        else:
            print("   ❌ 登录页面仍然不缓存")
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
    print("🔧 简单的服务器重启工具")
    print("=" * 50)
    
    # 测试当前服务器状态
    if test_server_status():
        print("\n⚠️ 服务器正在运行，需要手动停止")
        print("💡 请按 Ctrl+C 停止当前服务器，然后重新运行此脚本")
        return
    
    print("\n🚀 启动服务器...")
    print("💡 服务器将在后台启动，请等待几秒钟...")
    
    try:
        # 启动服务器
        process = subprocess.Popen(
            ['python', 'main.py'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"   服务器进程已启动: PID {process.pid}")
        
        # 等待服务器启动
        print("   等待服务器启动...")
        for i in range(30):
            if test_server_status():
                print("   ✅ 服务器启动成功")
                break
            time.sleep(1)
            if i % 5 == 0:
                print(f"   等待中... ({i+1}/30)")
        else:
            print("   ❌ 服务器启动超时")
            return
        
        # 测试登录页面缓存
        print("\n" + "=" * 50)
        choice = input("是否要测试登录页面缓存？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是', 'Y']:
            test_login_page_cache()
        
        # 询问是否打开浏览器
        print("\n" + "=" * 50)
        choice = input("是否要在浏览器中打开登录页面？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是', 'Y']:
            open_admin_login()
        
        print("\n🎉 服务器重启完成！")
        print("💡 现在可以正常访问管理后台了")
        print("   登录地址: http://localhost:8000/jianai/login")
        print("   用户名: admin")
        print("   密码: admin123")
        
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")

if __name__ == "__main__":
    main() 