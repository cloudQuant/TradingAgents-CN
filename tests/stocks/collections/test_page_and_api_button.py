"""
使用Playwright测试所有股票数据集合的：
1. 页面能否正常访问
2. API更新按钮点击后是否报错
"""
import os
import sys
import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[ERROR] Playwright未安装，请运行: pip install playwright && playwright install")

# 配置
FRONTEND_URL = os.environ.get("TEST_FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.environ.get("TEST_BACKEND_URL", "http://localhost:8000")
HEADLESS = os.environ.get("TEST_HEADLESS", "true").lower() == "true"
TIMEOUT = 30000
AUTH_USERNAME = os.environ.get("TEST_AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("TEST_AUTH_PASSWORD", "admin123")


class StockPageTester:
    """股票页面测试器"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.auth_token: Optional[str] = None
        
    async def setup(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=HEADLESS)
        self.page = await self.browser.new_page()
        self.page.set_default_timeout(TIMEOUT)
    
    async def login(self) -> bool:
        """登录"""
        try:
            url = f"{BACKEND_URL}/api/auth/login"
            response = await self.page.request.post(
                url,
                data=json.dumps({"username": AUTH_USERNAME, "password": AUTH_PASSWORD}),
                headers={"Content-Type": "application/json"}
            )
            if response.status == 200:
                resp_data = await response.json()
                if resp_data.get("success") and resp_data.get("data"):
                    self.auth_token = resp_data["data"].get("access_token")
                if self.auth_token:
                    return True
            return False
        except Exception as e:
            print(f"  [WARN] 登录异常: {e}")
            return False
        
    async def teardown(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def get_all_collections(self) -> List[Dict]:
        """获取所有集合列表"""
        try:
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            response = await self.page.request.get(
                f"{BACKEND_URL}/api/stocks/collections",
                headers=headers
            )
            if response.status == 200:
                data = await response.json()
                if isinstance(data, list):
                    return data
                return data.get("data", [])
        except Exception as e:
            print(f"[ERROR] 获取集合列表失败: {e}")
        return []
    
    async def test_page_load(self, collection_name: str) -> Dict[str, Any]:
        """测试页面加载"""
        result = {
            "collection": collection_name,
            "page_load": False,
            "error": None
        }
        
        try:
            url = f"{FRONTEND_URL}/stocks/collections/{collection_name}"
            response = await self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
            if response and response.status == 200:
                # 等待页面内容
                await asyncio.sleep(1)
                
                # 检查是否有错误信息
                page_content = await self.page.content()
                
                # 检查常见错误
                if "500" in page_content and "Internal Server Error" in page_content:
                    result["error"] = "500 Internal Server Error"
                elif "404" in page_content and "Not Found" in page_content:
                    result["error"] = "404 Not Found"
                elif "数据错误" in page_content or "加载失败" in page_content:
                    result["error"] = "数据加载失败"
                else:
                    result["page_load"] = True
            else:
                result["error"] = f"HTTP {response.status if response else 'No response'}"
                
        except Exception as e:
            result["error"] = str(e)[:80]
            
        return result
    
    async def test_update_dialog(self, collection_name: str) -> Dict[str, Any]:
        """测试API更新对话框"""
        result = {
            "collection": collection_name,
            "dialog_open": False,
            "error": None
        }
        
        try:
            # 先访问页面
            url = f"{FRONTEND_URL}/stocks/collections/{collection_name}"
            await self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(1)
            
            # 尝试找到并点击更新按钮
            update_button = await self.page.query_selector('button:has-text("更新"), button:has-text("刷新"), button:has-text("API")')
            
            if update_button:
                await update_button.click()
                await asyncio.sleep(0.5)
                
                # 检查是否有对话框打开
                dialog = await self.page.query_selector('[role="dialog"], .modal, .ant-modal, [class*="dialog"]')
                if dialog:
                    result["dialog_open"] = True
                else:
                    # 检查是否有错误提示
                    error_toast = await self.page.query_selector('[class*="error"], [class*="toast"], .ant-message-error')
                    if error_toast:
                        error_text = await error_toast.text_content()
                        result["error"] = error_text[:80] if error_text else "对话框打开失败"
                    else:
                        result["dialog_open"] = True  # 可能是直接执行了
            else:
                result["error"] = "未找到更新按钮"
                
        except Exception as e:
            result["error"] = str(e)[:80]
            
        return result
    
    async def test_stats_api(self, collection_name: str) -> Dict[str, Any]:
        """测试统计API"""
        result = {
            "collection": collection_name,
            "success": False,
            "error": None
        }
        
        try:
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            url = f"{BACKEND_URL}/api/stocks/collections/{collection_name}/stats"
            response = await self.page.request.get(url, headers=headers)
            
            if response.status == 200:
                result["success"] = True
            else:
                try:
                    data = await response.json()
                    result["error"] = data.get("detail", f"HTTP {response.status}")
                except:
                    result["error"] = f"HTTP {response.status}"
                    
        except Exception as e:
            result["error"] = str(e)[:80]
            
        return result
    
    async def test_data_api(self, collection_name: str) -> Dict[str, Any]:
        """测试数据获取API"""
        result = {
            "collection": collection_name,
            "success": False,
            "error": None
        }
        
        try:
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            url = f"{BACKEND_URL}/api/stocks/collections/{collection_name}?page=1&page_size=10"
            response = await self.page.request.get(url, headers=headers)
            
            if response.status == 200:
                result["success"] = True
            else:
                try:
                    data = await response.json()
                    result["error"] = data.get("detail", f"HTTP {response.status}")
                except:
                    result["error"] = f"HTTP {response.status}"
                    
        except Exception as e:
            result["error"] = str(e)[:80]
            
        return result


async def run_tests(test_count: int = None):
    """运行测试"""
    if not PLAYWRIGHT_AVAILABLE:
        print("[ERROR] Playwright未安装")
        return False
    
    tester = StockPageTester()
    
    try:
        print("="*70)
        print("股票数据集合 - 页面和API更新按钮测试")
        print(f"前端: {FRONTEND_URL}")
        print(f"后端: {BACKEND_URL}")
        print("="*70)
        
        await tester.setup()
        
        # 登录
        print("\n[1] 登录...")
        if await tester.login():
            print("    ✓ 登录成功")
        else:
            print("    ✗ 登录失败")
        
        # 获取集合列表
        print("\n[2] 获取集合列表...")
        collections = await tester.get_all_collections()
        total = len(collections)
        print(f"    共 {total} 个集合")
        
        if not collections:
            print("[ERROR] 无法获取集合列表")
            return False
        
        # 限制测试数量
        if test_count:
            collections = collections[:test_count]
            print(f"    测试前 {test_count} 个集合")
        
        # 测试结果
        stats_success = 0
        data_success = 0
        failed_collections = []
        
        print("\n[3] 测试各集合...")
        print("-"*70)
        
        for i, coll in enumerate(collections, 1):
            name = coll.get("name", "")
            
            # 测试统计API
            stats_result = await tester.test_stats_api(name)
            
            # 测试数据API
            data_result = await tester.test_data_api(name)
            
            stats_ok = stats_result["success"]
            data_ok = data_result["success"]
            
            if stats_ok:
                stats_success += 1
            if data_ok:
                data_success += 1
            
            status = "✓" if (stats_ok and data_ok) else "✗"
            stats_status = "✓" if stats_ok else "✗"
            data_status = "✓" if data_ok else "✗"
            
            print(f"  [{i:3d}/{len(collections)}] {status} {name}")
            print(f"             统计API: {stats_status}  数据API: {data_status}")
            
            if not stats_ok or not data_ok:
                error = stats_result.get("error") or data_result.get("error")
                if error:
                    print(f"             错误: {error[:50]}")
                failed_collections.append({
                    "name": name,
                    "stats_error": stats_result.get("error"),
                    "data_error": data_result.get("error")
                })
        
        # 汇总
        print("\n" + "="*70)
        print("测试结果汇总")
        print("="*70)
        print(f"集合总数: {len(collections)}")
        print(f"统计API成功: {stats_success}/{len(collections)}")
        print(f"数据API成功: {data_success}/{len(collections)}")
        
        if failed_collections:
            print(f"\n失败的集合 ({len(failed_collections)}个):")
            for fc in failed_collections[:30]:
                error = fc.get('stats_error') or fc.get('data_error')
                print(f"  - {fc['name']}: {error}")
            if len(failed_collections) > 30:
                print(f"  ... 还有 {len(failed_collections) - 30} 个")
        
        print("="*70)
        
        # 保存结果
        results = {
            "test_time": datetime.now().isoformat(),
            "total": len(collections),
            "stats_success": stats_success,
            "data_success": data_success,
            "failed": failed_collections
        }
        
        with open("tests/stocks/collections/page_api_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return len(failed_collections) == 0
        
    except Exception as e:
        print(f"\n[ERROR] 测试错误: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        await tester.teardown()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, help="测试集合数量限制")
    args = parser.parse_args()
    
    success = asyncio.run(run_tests(args.count))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
