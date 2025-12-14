#!/usr/bin/env python
"""
使用Playwright测试期权数据集合Web API
测试网站上期权数据集合中API更新功能是否可用
"""
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


class OptionCollectionAPITester:
    """期权数据集合API测试器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_prefix = "/api/options"
        self.results = []
        self.auth_token = None
        
    async def login(self, page):
        """登录获取认证token"""
        try:
            # 尝试使用默认凭据登录
            response = await page.request.post(
                f"{self.base_url}/api/auth/login",
                data=json.dumps({
                    "username": "admin",
                    "password": "admin123"
                }),
                headers={"Content-Type": "application/json"}
            )
            
            if response.ok:
                data = await response.json()
                # 检查嵌套的data结构
                if data.get("success") and data.get("data", {}).get("access_token"):
                    self.auth_token = data["data"]["access_token"]
                    print(f"✓ 登录成功")
                    return True
                elif data.get("access_token"):
                    self.auth_token = data["access_token"]
                    print(f"✓ 登录成功")
                    return True
            
            print(f"✗ 登录失败: {response.status}")
            return False
        except Exception as e:
            print(f"✗ 登录异常: {e}")
            return False
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    async def test_collections_list(self, page):
        """测试获取集合列表"""
        print("\n测试: 获取期权数据集合列表")
        try:
            response = await page.request.get(
                f"{self.base_url}{self.api_prefix}/collections",
                headers=self.get_headers()
            )
            
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    collections = data.get("data", [])
                    print(f"  ✓ 成功! 集合数量: {len(collections)}")
                    self.results.append(("collections_list", "成功", len(collections)))
                    return collections
                else:
                    print(f"  ✗ 失败: {data.get('error', '未知错误')}")
                    self.results.append(("collections_list", "失败", data.get('error')))
            else:
                print(f"  ✗ HTTP错误: {response.status}")
                self.results.append(("collections_list", "HTTP错误", response.status))
        except Exception as e:
            print(f"  ✗ 异常: {e}")
            self.results.append(("collections_list", "异常", str(e)))
        return []
    
    async def test_collection_data(self, page, collection_name: str, params: dict = None):
        """测试获取集合数据"""
        print(f"\n测试: 获取集合数据 - {collection_name}")
        try:
            # 使用正确的路由: /collections/{collection_name}
            url = f"{self.base_url}{self.api_prefix}/collections/{collection_name}"
            if params:
                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                url = f"{url}?{query_string}"
            
            response = await page.request.get(url, headers=self.get_headers())
            
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    records = data.get("data", {})
                    if isinstance(records, dict):
                        count = records.get("total", len(records.get("items", [])))
                    else:
                        count = len(records) if isinstance(records, list) else 0
                    print(f"  ✓ 成功! 数据量: {count}")
                    self.results.append((collection_name, "成功", count))
                    return True
                else:
                    error = data.get("error", "未知错误")
                    print(f"  ✗ 失败: {error}")
                    self.results.append((collection_name, "失败", error[:50]))
            else:
                print(f"  ✗ HTTP错误: {response.status}")
                self.results.append((collection_name, "HTTP错误", response.status))
        except PlaywrightTimeout:
            print(f"  ✗ 超时")
            self.results.append((collection_name, "超时", ""))
        except Exception as e:
            print(f"  ✗ 异常: {str(e)[:50]}")
            self.results.append((collection_name, "异常", str(e)[:50]))
        return False
    
    async def test_collection_update(self, page, collection_name: str, params: dict = None):
        """测试更新集合数据（API更新功能）- 使用refresh接口"""
        print(f"\n测试: 刷新集合数据 - {collection_name}")
        try:
            # 使用正确的路由: /collections/{collection_name}/refresh
            url = f"{self.base_url}{self.api_prefix}/collections/{collection_name}/refresh"
            
            body = params or {}
            response = await page.request.post(
                url,
                data=json.dumps(body),
                headers=self.get_headers(),
                timeout=120000  # 120秒超时，因为刷新可能需要较长时间
            )
            
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    message = data.get("message", "刷新成功")
                    task_id = data.get("task_id", "")
                    print(f"  ✓ 成功! {message} (task_id: {task_id[:20] if task_id else 'N/A'})")
                    self.results.append((f"{collection_name}_refresh", "成功", message[:50]))
                    return True
                else:
                    error = data.get("error", "未知错误")
                    print(f"  ✗ 失败: {error}")
                    self.results.append((f"{collection_name}_refresh", "失败", error[:50]))
            else:
                print(f"  ✗ HTTP错误: {response.status}")
                self.results.append((f"{collection_name}_refresh", "HTTP错误", response.status))
        except PlaywrightTimeout:
            print(f"  ✗ 超时")
            self.results.append((f"{collection_name}_refresh", "超时", ""))
        except Exception as e:
            print(f"  ✗ 异常: {str(e)[:50]}")
            self.results.append((f"{collection_name}_refresh", "异常", str(e)[:50]))
        return False
    
    async def test_collection_stats(self, page, collection_name: str):
        """测试获取集合统计信息"""
        print(f"\n测试: 获取集合统计 - {collection_name}")
        try:
            # 使用正确的路由: /collections/{collection_name}/stats
            url = f"{self.base_url}{self.api_prefix}/collections/{collection_name}/stats"
            response = await page.request.get(url, headers=self.get_headers())
            
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    stats = data.get("data", {})
                    total = stats.get("total", 0)
                    print(f"  ✓ 成功! 总数据量: {total}")
                    self.results.append((f"{collection_name}_stats", "成功", total))
                    return stats
                else:
                    error = data.get("error", "未知错误")
                    print(f"  ✗ 失败: {error}")
                    self.results.append((f"{collection_name}_stats", "失败", error[:50]))
            else:
                print(f"  ✗ HTTP错误: {response.status}")
                self.results.append((f"{collection_name}_stats", "HTTP错误", response.status))
        except Exception as e:
            print(f"  ✗ 异常: {str(e)[:50]}")
            self.results.append((f"{collection_name}_stats", "异常", str(e)[:50]))
        return None
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("=" * 70)
        print("期权数据集合Web API测试")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"目标地址: {self.base_url}")
        print("=" * 70)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # 登录
            await self.login(page)
            
            # 测试集合列表
            collections = await self.test_collections_list(page)
            
            # 测试部分集合的数据获取和更新
            test_collections = [
                # 无参数集合
                ("option_contract_info_ctp", {}),
                ("option_current_day_sse", {}),
                ("option_current_day_szse", {}),
                ("option_current_em", {}),
                ("option_value_analysis_em", {}),
                # 带参数集合
                ("option_finance_board", {"symbol": "华夏上证50ETF期权", "end_month": "2512"}),
                ("option_risk_indicator_sse", {"date": "20241210"}),
                ("option_daily_stats_sse", {"date": "20241210"}),
                ("option_cffex_sz50_list_sina", {}),
                ("option_cffex_hs300_list_sina", {}),
                ("option_commodity_contract_sina", {"symbol": "黄金期权"}),
                ("option_comm_info", {"symbol": "工业硅期权"}),
                ("option_margin", {"symbol": "原油期权"}),
                ("option_hist_shfe", {"symbol": "铜期权", "date": "20241210"}),
                ("option_hist_czce", {"symbol": "白糖期权", "date": "20241210"}),
                ("option_hist_gfex", {"symbol": "工业硅", "date": "20241210"}),
            ]
            
            for collection_name, params in test_collections:
                # 测试获取统计信息
                await self.test_collection_stats(page, collection_name)
                
                # 测试获取数据
                await self.test_collection_data(page, collection_name, params)
                
                # 测试刷新数据（API更新功能）
                await self.test_collection_update(page, collection_name, params)
            
            await browser.close()
        
        # 打印测试摘要
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 70)
        print("测试摘要")
        print("=" * 70)
        
        success_count = sum(1 for r in self.results if r[1] == "成功")
        fail_count = len(self.results) - success_count
        
        print(f"  总测试数: {len(self.results)}")
        print(f"  成功: {success_count}")
        print(f"  失败: {fail_count}")
        print(f"  成功率: {success_count/len(self.results)*100:.1f}%" if self.results else "N/A")
        
        if fail_count > 0:
            print("\n失败的测试:")
            for name, status, msg in self.results:
                if status != "成功":
                    print(f"  - {name}: {status} - {msg}")


async def main():
    """主函数"""
    # 检查服务是否运行
    import socket
    
    def check_port(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    
    if not check_port("localhost", 8000):
        print("错误: 后端服务未运行 (localhost:8000)")
        print("请先启动后端服务: python run.py 或 ./start_app.sh")
        return
    
    tester = OptionCollectionAPITester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
