#!/usr/bin/env python
"""调试API，检查刷新任务状态和数据"""
import sys
import json
import asyncio
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright


async def debug_api():
    """调试API"""
    base_url = "http://localhost:8000"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # 登录
        print("1. 登录...")
        response = await page.request.post(
            f"{base_url}/api/auth/login",
            data=json.dumps({"username": "admin", "password": "admin123"}),
            headers={"Content-Type": "application/json"}
        )
        data = await response.json()
        token = data["data"]["access_token"]
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        print(f"   登录成功")
        
        # 获取集合列表
        print("\n2. 获取集合列表...")
        response = await page.request.get(f"{base_url}/api/options/collections", headers=headers)
        data = await response.json()
        print(f"   集合数量: {len(data.get('data', []))}")
        
        # 测试刷新
        collection_name = "option_contract_info_ctp"
        print(f"\n3. 刷新集合: {collection_name}")
        response = await page.request.post(
            f"{base_url}/api/options/collections/{collection_name}/refresh",
            data=json.dumps({}),
            headers=headers
        )
        data = await response.json()
        print(f"   响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get("success"):
            task_id = data.get("task_id", "")
            print(f"\n4. 任务已提交 (task_id: {task_id})")
        
        # 等待一段时间
        print("\n5. 等待10秒...")
        await asyncio.sleep(10)
        
        # 获取数据
        print(f"\n6. 获取集合数据: {collection_name}")
        response = await page.request.get(
            f"{base_url}/api/options/collections/{collection_name}",
            headers=headers
        )
        data = await response.json()
        print(f"   success: {data.get('success')}")
        if data.get('data'):
            print(f"   total: {data['data'].get('total', 'N/A')}")
            print(f"   items数量: {len(data['data'].get('items', []))}")
            if data['data'].get('items'):
                print(f"   第一条数据: {json.dumps(data['data']['items'][0], ensure_ascii=False)[:200]}...")
        
        # 获取统计信息
        print(f"\n7. 获取集合统计: {collection_name}")
        response = await page.request.get(
            f"{base_url}/api/options/collections/{collection_name}/stats",
            headers=headers
        )
        data = await response.json()
        print(f"   响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_api())
