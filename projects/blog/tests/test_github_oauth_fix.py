#!/usr/bin/env python3
import requests
import time

def test_github_oauth_after_fix():
    """测试修复后的GitHub OAuth"""
    print("=== 测试GitHub OAuth修复 ===\n")
    
    try:
        # 1. 检查OAuth配置
        print("1. 检查OAuth配置...")
        response = requests.get('http://localhost:8000/api/v1/config/oauth')
        if response.status_code == 200:
            config = response.json()
            print(f"✅ GitHub启用: {config.get('github_enabled')}")
            print(f"✅ 前端URL: {config.get('frontend_url')}")
        else:
            print(f"❌ 配置检查失败: {response.status_code}")
            return
        
        # 2. 测试GitHub OAuth登录
        print("\n2. 测试GitHub OAuth登录...")
        response = requests.get('http://localhost:8000/api/v1/oauth/github/login', allow_redirects=False)
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print("✅ GitHub OAuth重定向正常")
            
            # 解析重定向URI
            if 'redirect_uri=' in location:
                redirect_uri = location.split('redirect_uri=')[1].split('&')[0]
                redirect_uri = requests.utils.unquote(redirect_uri)
                print(f"✅ 重定向URI: {redirect_uri}")
                
                print("\n=== 下一步操作 ===")
                print("1. 确保GitHub OAuth应用设置中的重定向URI为:")
                print(f"   {redirect_uri}")
                print("2. 点击上面的GitHub授权链接进行测试")
                print("3. 如果仍然出现重定向URI错误，请检查GitHub应用设置")
                
                print(f"\n🔗 GitHub授权链接:")
                print(f"{location}")
                
            else:
                print("❌ 无法解析重定向URI")
        else:
            print(f"❌ GitHub OAuth异常: {response.status_code}")
            print(f"响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_github_oauth_after_fix() 