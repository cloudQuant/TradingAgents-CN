#!/usr/bin/env python
"""
期权数据集合API测试基类
提供Playwright API测试的通用方法
"""
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


class APITestBase:
    """API测试基类"""
    
    BASE_URL = "http://localhost:8000"
    API_PREFIX = "/api/options"
    
    def __init__(self):
        self.auth_token = None
        self.page = None
        self.browser = None
        self.context = None
        
    async def setup(self):
        """初始化浏览器和登录"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        await self.login()
        
    async def teardown(self):
        """清理资源"""
        if self.browser:
            await self.browser.close()
    
    async def login(self) -> bool:
        """登录获取认证token"""
        try:
            response = await self.page.request.post(
                f"{self.BASE_URL}/api/auth/login",
                data=json.dumps({"username": "admin", "password": "admin123"}),
                headers={"Content-Type": "application/json"}
            )
            if response.ok:
                data = await response.json()
                if data.get("success") and data.get("data", {}).get("access_token"):
                    self.auth_token = data["data"]["access_token"]
                    return True
            return False
        except Exception as e:
            print(f"登录异常: {e}")
            return False
    
    def get_headers(self) -> dict:
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    async def refresh_collection(self, collection_name: str, params: dict = None, timeout: int = 60000) -> dict:
        """刷新集合数据"""
        result = {"success": False, "task_id": "", "error": "", "message": ""}
        try:
            url = f"{self.BASE_URL}{self.API_PREFIX}/collections/{collection_name}/refresh"
            response = await self.page.request.post(
                url,
                data=json.dumps(params or {}),
                headers=self.get_headers(),
                timeout=timeout
            )
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    result["success"] = True
                    result["task_id"] = data.get("task_id", "")
                    result["message"] = data.get("message", "刷新成功")
                else:
                    result["error"] = data.get("error", "未知错误")
            else:
                result["error"] = f"HTTP {response.status}"
        except PlaywrightTimeout:
            result["error"] = "请求超时"
        except Exception as e:
            result["error"] = str(e)[:100]
        return result
    
    async def get_collection_data(self, collection_name: str, params: dict = None, timeout: int = 30000, debug: bool = False) -> dict:
        """获取集合数据"""
        result = {"success": False, "data": None, "total": 0, "error": "", "raw_response": None}
        try:
            url = f"{self.BASE_URL}{self.API_PREFIX}/collections/{collection_name}"
            if params:
                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                url = f"{url}?{query_string}"
            
            response = await self.page.request.get(url, headers=self.get_headers(), timeout=timeout)
            if response.ok:
                data = await response.json()
                result["raw_response"] = data
                if debug:
                    print(f"   [DEBUG] 响应数据结构: {type(data)}")
                    if isinstance(data, dict):
                        print(f"   [DEBUG] 响应键: {list(data.keys())}")
                        if "data" in data:
                            print(f"   [DEBUG] data类型: {type(data['data'])}")
                            if isinstance(data['data'], dict):
                                print(f"   [DEBUG] data键: {list(data['data'].keys())[:10]}")
                            elif isinstance(data['data'], list):
                                print(f"   [DEBUG] data长度: {len(data['data'])}")
                
                if data.get("success"):
                    result["success"] = True
                    result["data"] = data.get("data", {})
                    # 尝试多种方式获取数据量
                    if isinstance(result["data"], dict):
                        if "total" in result["data"]:
                            result["total"] = result["data"]["total"]
                        elif "items" in result["data"]:
                            result["total"] = len(result["data"]["items"])
                        elif "records" in result["data"]:
                            result["total"] = len(result["data"]["records"])
                        else:
                            # 可能data本身就是数据字典
                            result["total"] = len(result["data"])
                    elif isinstance(result["data"], list):
                        result["total"] = len(result["data"])
                else:
                    result["error"] = data.get("error", "未知错误")
            else:
                result["error"] = f"HTTP {response.status}"
        except PlaywrightTimeout:
            result["error"] = "请求超时"
        except Exception as e:
            result["error"] = str(e)[:100]
        return result
    
    async def get_collection_stats(self, collection_name: str, timeout: int = 30000) -> dict:
        """获取集合统计信息"""
        result = {"success": False, "total": 0, "error": ""}
        try:
            url = f"{self.BASE_URL}{self.API_PREFIX}/collections/{collection_name}/stats"
            response = await self.page.request.get(url, headers=self.get_headers(), timeout=timeout)
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    result["success"] = True
                    stats = data.get("data", {})
                    result["total"] = stats.get("total", 0)
                else:
                    result["error"] = data.get("error", "未知错误")
            else:
                result["error"] = f"HTTP {response.status}"
        except Exception as e:
            result["error"] = str(e)[:100]
        return result
    
    async def wait_for_task(self, task_id: str, max_wait: int = 30) -> bool:
        """等待任务完成"""
        for _ in range(max_wait):
            await asyncio.sleep(1)
            # 可以添加任务状态检查API
        return True


async def run_api_test(collection_name: str, display_name: str, params: dict = None, 
                       wait_time: int = 5, expected_min_count: int = 0) -> dict:
    """运行单个集合的API测试"""
    result = {
        "collection_name": collection_name,
        "display_name": display_name,
        "params": params,
        "refresh_success": False,
        "refresh_task_id": "",
        "refresh_error": "",
        "data_success": False,
        "data_count": 0,
        "data_error": "",
        "test_passed": False,
    }
    
    tester = APITestBase()
    try:
        await tester.setup()
        
        # 1. 刷新数据
        print(f"\n{'='*60}")
        print(f"测试: {display_name} ({collection_name})")
        print(f"参数: {params}")
        print(f"{'='*60}")
        
        print("1. 刷新数据...")
        refresh_result = await tester.refresh_collection(collection_name, params)
        result["refresh_success"] = refresh_result["success"]
        result["refresh_task_id"] = refresh_result["task_id"][:8] if refresh_result["task_id"] else ""
        result["refresh_error"] = refresh_result["error"]
        
        if refresh_result["success"]:
            print(f"   ✓ 刷新成功 (task: {result['refresh_task_id']})")
            # 等待数据更新，并轮询检查数据
            print(f"2. 等待数据更新...")
            for i in range(wait_time):
                await asyncio.sleep(1)
                # 检查是否已有数据
                check_result = await tester.get_collection_data(collection_name, params)
                if check_result["success"] and check_result["total"] > 0:
                    print(f"   数据已更新 (等待{i+1}秒, 数据量: {check_result['total']})")
                    break
                print(f"   等待中... ({i+1}/{wait_time}秒)")
        else:
            print(f"   ✗ 刷新失败: {refresh_result['error']}")
        
        # 2. 获取数据验证
        print("3. 获取数据验证...")
        data_result = await tester.get_collection_data(collection_name, params, debug=True)
        result["data_success"] = data_result["success"]
        result["data_count"] = data_result["total"]
        result["data_error"] = data_result["error"]
        
        if data_result["success"]:
            print(f"   ✓ 获取成功 (数据量: {data_result['total']})")
        else:
            print(f"   ✗ 获取失败: {data_result['error']}")
        
        # 3. 判断测试是否通过
        result["test_passed"] = (
            result["refresh_success"] and 
            result["data_success"] and 
            result["data_count"] >= expected_min_count
        )
        
        status = "✓ 通过" if result["test_passed"] else "✗ 失败"
        print(f"\n测试结果: {status}")
        
    except Exception as e:
        print(f"测试异常: {e}")
        result["data_error"] = str(e)[:100]
    finally:
        await tester.teardown()
    
    return result


def check_server_running() -> bool:
    """检查服务器是否运行"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(("localhost", 8000))
    sock.close()
    return result == 0
