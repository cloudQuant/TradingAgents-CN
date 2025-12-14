#!/usr/bin/env python
"""
验证Service修复是否生效
需要重启后端服务后运行此脚本
"""
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright


async def verify_fix():
    """验证修复是否生效"""
    base_url = "http://localhost:8000"
    
    print("=" * 70)
    print("验证Service修复")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # 登录
        print("\n1. 登录...")
        response = await page.request.post(
            f"{base_url}/api/auth/login",
            data=json.dumps({"username": "admin", "password": "admin123"}),
            headers={"Content-Type": "application/json"}
        )
        data = await response.json()
        token = data["data"]["access_token"]
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        print("   ✓ 登录成功")
        
        # 测试第一个集合
        collection_name = "option_contract_info_ctp"
        print(f"\n2. 测试集合: {collection_name}")
        
        # 刷新
        print("   刷新数据...")
        response = await page.request.post(
            f"{base_url}/api/options/collections/{collection_name}/refresh",
            data=json.dumps({}),
            headers=headers
        )
        data = await response.json()
        if data.get("success"):
            task_id = data.get("task_id", "")[:8]
            print(f"   ✓ 刷新任务已提交 (task: {task_id})")
        else:
            print(f"   ✗ 刷新失败: {data.get('error')}")
            await browser.close()
            return
        
        # 等待并轮询检查数据
        print("   等待数据更新...")
        max_wait = 30
        for i in range(max_wait):
            await asyncio.sleep(1)
            response = await page.request.get(
                f"{base_url}/api/options/collections/{collection_name}",
                headers=headers
            )
            data = await response.json()
            if data.get("success"):
                total = data.get("data", {}).get("total", 0)
                if total > 0:
                    print(f"   ✓ 数据已更新! 数据量: {total}")
                    break
                print(f"   等待中... ({i+1}/{max_wait}秒, 当前数据量: {total})")
        else:
            print(f"   ✗ 等待超时，数据量仍为0")
            print("\n   可能的原因:")
            print("   1. 后端服务未重启，新代码未生效")
            print("   2. 数据获取过程中出现错误")
            print("\n   请重启后端服务后再次运行此脚本")
        
        await browser.close()


if __name__ == "__main__":
    import socket
    
    def check_port(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    
    if not check_port("localhost", 8000):
        print("错误: 后端服务未运行 (localhost:8000)")
        sys.exit(1)
    
    asyncio.run(verify_fix())
