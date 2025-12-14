"""
使用Playwright测试所有股票数据集合的前端页面加载和API更新对话框功能
"""
import os
import sys
import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

# 添加项目根目录到路径
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
TIMEOUT = 30000  # 30秒超时
AUTH_USERNAME = os.environ.get("TEST_AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("TEST_AUTH_PASSWORD", "admin123")


class FrontendTester:
    """前端测试器"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.results: List[Dict[str, Any]] = []
        self.auth_token: Optional[str] = None
        
    async def setup(self):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=HEADLESS)
        self.page = await self.browser.new_page()
        self.page.set_default_timeout(TIMEOUT)
    
    async def login(self) -> bool:
        """登录获取认证token"""
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
                else:
                    self.auth_token = resp_data.get("access_token")
                    
                if self.auth_token:
                    return True
            return False
        except Exception as e:
            print(f"  [WARN] 登录异常: {e}")
            return False
        
    async def teardown(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def get_all_collections(self) -> List[Dict]:
        """从后端获取所有集合列表"""
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
                # stocks 返回的是列表
                if isinstance(data, list):
                    return data
                return data.get("data", [])
        except Exception as e:
            print(f"[ERROR] 获取集合列表失败: {e}")
        return []
    
    async def test_update_config_api(self, collection_name: str) -> Dict[str, Any]:
        """测试更新配置API"""
        result = {
            "collection": collection_name,
            "success": False,
            "has_config": False,
            "error": None
        }
        
        try:
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            url = f"{BACKEND_URL}/api/stocks/collections/{collection_name}/update-config"
            response = await self.page.request.get(url, headers=headers)
            
            if response.status == 200:
                data = await response.json()
                result["success"] = True
                result["has_config"] = bool(data.get("data"))
            else:
                result["error"] = f"API返回: {response.status}"
                
        except Exception as e:
            result["error"] = str(e)[:100]
            
        return result
    
    async def test_refresh_api(self, collection_name: str) -> Dict[str, Any]:
        """测试刷新API"""
        result = {
            "collection": collection_name,
            "success": False,
            "error": None
        }
        
        try:
            url = f"{BACKEND_URL}/api/stocks/collections/{collection_name}/refresh"
            headers = {"Content-Type": "application/json"}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            response = await self.page.request.post(
                url,
                data=json.dumps({"update_type": "single", "params": {}}),
                headers=headers
            )
            
            if response.status == 200:
                result["success"] = True
            else:
                try:
                    data = await response.json()
                    result["error"] = data.get("detail", f"API返回: {response.status}")
                except:
                    result["error"] = f"API返回: {response.status}"
                
        except Exception as e:
            result["error"] = str(e)[:100]
            
        return result


async def run_all_tests():
    """运行所有测试"""
    if not PLAYWRIGHT_AVAILABLE:
        print("[ERROR] Playwright未安装")
        return False
    
    tester = FrontendTester()
    
    try:
        print("="*70)
        print("股票数据集合 - 前端功能全面测试")
        print(f"前端地址: {FRONTEND_URL}")
        print(f"后端地址: {BACKEND_URL}")
        print("="*70)
        
        await tester.setup()
        
        # 登录
        print("\n[1] 登录...")
        logged_in = await tester.login()
        if logged_in:
            print("    登录成功")
        else:
            print("    登录失败，刷新API测试将跳过认证")
        
        # 获取所有集合
        print("\n[2] 获取集合列表...")
        collections = await tester.get_all_collections()
        print(f"    共 {len(collections)} 个集合")
        
        if not collections:
            print("[ERROR] 无法获取集合列表")
            return False
        
        # 测试结果统计
        update_config_success = 0
        refresh_api_success = 0
        failed_collections = []
        
        # 测试每个集合
        print("\n[3] 测试各集合...")
        print("-"*70)
        
        for i, coll in enumerate(collections, 1):
            name = coll.get("name", "")
            display = coll.get("display_name", name)
            
            # 测试更新配置API
            config_result = await tester.test_update_config_api(name)
            
            # 测试刷新API
            refresh_result = await tester.test_refresh_api(name)
            
            # 统计结果
            config_ok = config_result["success"]
            refresh_ok = refresh_result["success"]
            
            if config_ok:
                update_config_success += 1
            if refresh_ok:
                refresh_api_success += 1
            
            # 打印结果
            status = "✓" if (config_ok and refresh_ok) else "✗"
            config_status = "✓" if config_ok else "✗"
            refresh_status = "✓" if refresh_ok else "✗"
            
            print(f"  [{i:3d}/{len(collections)}] {status} {name}")
            print(f"             配置API: {config_status}  刷新API: {refresh_status}")
            
            if not config_ok or not refresh_ok:
                error_msg = config_result.get("error") or refresh_result.get("error")
                if error_msg:
                    print(f"             错误: {error_msg[:60]}")
                failed_collections.append({
                    "name": name,
                    "display": display,
                    "config_error": config_result.get("error"),
                    "refresh_error": refresh_result.get("error")
                })
        
        # 打印汇总
        print("\n" + "="*70)
        print("测试结果汇总")
        print("="*70)
        print(f"集合总数: {len(collections)}")
        print(f"更新配置API成功: {update_config_success}/{len(collections)}")
        print(f"刷新API成功: {refresh_api_success}/{len(collections)}")
        
        if failed_collections:
            print(f"\n失败的集合 ({len(failed_collections)}个):")
            for fc in failed_collections[:20]:  # 只显示前20个
                print(f"  - {fc['name']}: {fc.get('config_error') or fc.get('refresh_error')}")
            if len(failed_collections) > 20:
                print(f"  ... 还有 {len(failed_collections) - 20} 个失败")
        
        print("="*70)
        
        # 保存结果
        results = {
            "test_time": datetime.now().isoformat(),
            "total": len(collections),
            "update_config_success": update_config_success,
            "refresh_api_success": refresh_api_success,
            "failed": failed_collections
        }
        
        with open("tests/stocks/collections/frontend_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return len(failed_collections) == 0
        
    except Exception as e:
        print(f"\n[ERROR] 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        await tester.teardown()


def main():
    """主函数"""
    success = asyncio.run(run_all_tests())
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
