#!/usr/bin/env python3
"""
测试代理连接
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_proxy_connection():
    """测试代理连接"""
    print("🔍 测试代理连接")
    print("="*50)
    
    # 检查代理配置
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')
    
    print(f"HTTP_PROXY: {http_proxy or '未设置'}")
    print(f"HTTPS_PROXY: {https_proxy or '未设置'}")
    
    # 配置代理 - httpx使用不同的格式
    proxies = None
    if http_proxy or https_proxy:
        proxies = {}
        if http_proxy:
            proxies['http://'] = http_proxy
        if https_proxy:
            proxies['https://'] = https_proxy
    
    if not proxies:
        print("❌ 未配置代理")
        return
    
    print(f"使用代理: {proxies}")
    
    # 测试连接
    test_urls = [
        "https://accounts.google.com/.well-known/openid_configuration",
        "https://api.github.com",
        "https://www.google.com"
    ]
    
    # 使用正确的httpx代理配置
    transport = httpx.AsyncHTTPTransport(proxy=proxies.get('https://') or proxies.get('http://'))
    
    async with httpx.AsyncClient(transport=transport, timeout=10.0) as client:
        for url in test_urls:
            try:
                print(f"\n📡 测试: {url}")
                response = await client.get(url)
                print(f"✅ 成功 - 状态码: {response.status_code}")
                if response.status_code == 200:
                    print(f"响应长度: {len(response.text)} 字符")
            except Exception as e:
                print(f"❌ 失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_proxy_connection()) 