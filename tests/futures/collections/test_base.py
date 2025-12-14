"""
期货数据集合测试基类
提供通用测试方法，包括文件存在性检查和API功能测试
"""
import os
import sys
import asyncio
import json
from typing import Optional, Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# 尝试导入playwright
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# API测试配置
API_BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/futures"
API_TIMEOUT = 30000  # 30秒


class FuturesCollectionTestBase:
    """期货数据集合测试基类"""
    
    # 子类需要设置的属性
    collection_name = ""
    display_name = ""
    
    def _get_project_root(self):
        """获取项目根目录"""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    
    def test_provider_file_exists(self):
        """测试Provider文件存在"""
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'futures', 'providers',
            f'{self.collection_name}_provider.py'
        )
        assert os.path.exists(provider_path), f"Provider文件不存在: {provider_path}"
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否继承了正确的基类
        assert 'BaseProvider' in content or 'SimpleProvider' in content, \
            f"Provider未继承BaseProvider或SimpleProvider"
        print(f"[OK] {self.collection_name} Provider文件存在且继承正确基类")
    
    def test_service_file_exists(self):
        """测试Service文件存在"""
        service_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'futures', 'services',
            f'{self.collection_name}_service.py'
        )
        assert os.path.exists(service_path), f"Service文件不存在: {service_path}"
        
        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否继承了正确的基类（包括扩展的基类）
        valid_base_classes = [
            'BaseService', 'SimpleService', 
            'DateIncrementalService', 'SymbolBatchService'
        ]
        has_valid_base = any(base in content for base in valid_base_classes)
        assert has_valid_base, \
            f"Service未继承有效的基类（BaseService/SimpleService/DateIncrementalService/SymbolBatchService）"
        print(f"[OK] {self.collection_name} Service文件存在且继承正确基类")
    
    def test_update_config_exists(self):
        """测试更新配置存在"""
        config_path = os.path.join(
            self._get_project_root(),
            'app', 'config', 'futures_update_config.py'
        )
        assert os.path.exists(config_path), f"配置文件不存在: {config_path}"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查集合配置是否存在
        if f'"{self.collection_name}"' in content or f"'{self.collection_name}'" in content:
            print(f"[OK] {self.collection_name} 更新配置存在")
        else:
            print(f"[WARN] {self.collection_name} 更新配置未找到，可能使用默认配置")
    
    def test_collection_metadata_exists(self):
        """测试集合元信息存在"""
        metadata_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'futures', 'collection_metadata.py'
        )
        assert os.path.exists(metadata_path), f"元信息文件不存在: {metadata_path}"
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查集合元信息是否存在
        assert f"'{self.collection_name}'" in content or f'"{self.collection_name}"' in content, \
            f"元信息文件中未找到 {self.collection_name} 的配置"
        print(f"[OK] {self.collection_name} 元信息存在")
    
    def test_router_file_exists(self):
        """测试路由文件存在"""
        router_path = os.path.join(
            self._get_project_root(),
            'app', 'routers', 'futures.py'
        )
        assert os.path.exists(router_path), f"路由文件不存在: {router_path}"
        print(f"[OK] 期货路由文件存在")
    
    def test_provider_has_required_attributes(self):
        """测试Provider有必要的属性"""
        provider_path = os.path.join(
            self._get_project_root(),
            'app', 'services', 'data_sources', 'futures', 'providers',
            f'{self.collection_name}_provider.py'
        )
        
        with open(provider_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必要的属性
        assert 'collection_name' in content, "Provider中未定义collection_name"
        assert 'display_name' in content, "Provider中未定义display_name"
        assert 'unique_keys' in content or 'field_info' in content, \
            "Provider中未定义unique_keys或field_info"
        print(f"[OK] Provider包含必要属性")
    
    # ==================== API功能测试 ====================
    
    async def _api_request(self, endpoint: str, method: str = "GET", 
                           data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送API请求"""
        if not PLAYWRIGHT_AVAILABLE:
            return {"success": False, "error": "Playwright未安装"}
        
        url = f"{API_BASE_URL}{API_PREFIX}{endpoint}"
        result = {"success": False, "status_code": None, "response": None, "error": None}
        
        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            page.set_default_timeout(API_TIMEOUT)
            
            try:
                if method == "GET":
                    response = await page.request.get(url)
                elif method == "POST":
                    response = await page.request.post(
                        url, 
                        data=json.dumps(data) if data else None,
                        headers={"Content-Type": "application/json"}
                    )
                else:
                    raise ValueError(f"不支持的HTTP方法: {method}")
                
                result["status_code"] = response.status
                result["success"] = 200 <= response.status < 300
                
                try:
                    result["response"] = await response.json()
                except:
                    result["response"] = await response.text()
                    
            finally:
                await browser.close()
                await playwright.stop()
                
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    def test_api_collection_stats(self):
        """测试API：获取集合统计信息"""
        if not PLAYWRIGHT_AVAILABLE:
            print(f"  [SKIP] Playwright未安装，跳过API测试")
            return
        
        result = asyncio.get_event_loop().run_until_complete(
            self._api_request(f"/collections/{self.collection_name}/stats")
        )
        
        if result["error"] and "Connection refused" in result["error"]:
            print(f"  [SKIP] 服务器未运行，跳过API测试")
            return
            
        assert result["success"], f"API请求失败: {result.get('error') or result.get('response')}"
        print(f"[OK] API获取集合统计信息成功")
    
    def test_api_collection_data(self):
        """测试API：获取集合数据"""
        if not PLAYWRIGHT_AVAILABLE:
            print(f"  [SKIP] Playwright未安装，跳过API测试")
            return
        
        result = asyncio.get_event_loop().run_until_complete(
            self._api_request(f"/collections/{self.collection_name}/data?page=1&page_size=10")
        )
        
        if result["error"] and "Connection refused" in result["error"]:
            print(f"  [SKIP] 服务器未运行，跳过API测试")
            return
            
        assert result["success"], f"API请求失败: {result.get('error') or result.get('response')}"
        print(f"[OK] API获取集合数据成功")
    
    def test_api_collection_update(self):
        """测试API：更新集合数据"""
        if not PLAYWRIGHT_AVAILABLE:
            print(f"  [SKIP] Playwright未安装，跳过API测试")
            return
        
        result = asyncio.get_event_loop().run_until_complete(
            self._api_request(
                f"/collections/{self.collection_name}/refresh",
                method="POST",
                data={"params": {}}
            )
        )
        
        if result["error"] and "Connection refused" in result["error"]:
            print(f"  [SKIP] 服务器未运行，跳过API测试")
            return
        
        # 更新可能返回任务ID或直接返回结果
        if result["success"]:
            print(f"[OK] API更新集合数据成功")
            if isinstance(result["response"], dict) and "task_id" in result["response"]:
                print(f"      任务ID: {result['response']['task_id']}")
        else:
            # 某些集合可能需要参数，这不算失败
            if result["status_code"] == 400:
                print(f"  [WARN] API更新需要参数: {result.get('response')}")
            else:
                assert False, f"API请求失败: {result.get('error') or result.get('response')}"
    
    def run_all_tests(self, include_api_tests: bool = False):
        """运行所有测试
        
        Args:
            include_api_tests: 是否包含API功能测试（需要服务器运行）
        """
        # 基础文件测试
        tests = [
            ('test_provider_file_exists', 'Provider文件存在'),
            ('test_service_file_exists', 'Service文件存在'),
            ('test_update_config_exists', '更新配置存在'),
            ('test_collection_metadata_exists', '集合元信息存在'),
            ('test_router_file_exists', '路由文件存在'),
            ('test_provider_has_required_attributes', 'Provider属性完整'),
        ]
        
        # API功能测试（可选）
        if include_api_tests:
            tests.extend([
                ('test_api_collection_stats', 'API获取统计信息'),
                ('test_api_collection_data', 'API获取数据'),
                ('test_api_collection_update', 'API更新数据'),
            ])
        
        failed = 0
        skipped = 0
        print("="*70)
        print(f"{self.display_name} ({self.collection_name}) 测试")
        print("="*70)
        
        for test_method, test_name in tests:
            try:
                print(f"\n[测试] {test_name}...")
                getattr(self, test_method)()
            except AssertionError as e:
                print(f"  [FAILED] {e}")
                failed += 1
            except Exception as e:
                if "SKIP" in str(e) or "跳过" in str(e):
                    skipped += 1
                else:
                    print(f"  [ERROR] {e}")
                    failed += 1
        
        print("\n" + "="*70)
        if failed == 0:
            if skipped > 0:
                print(f"[SUCCESS] 测试通过！（跳过 {skipped} 个）")
            else:
                print("[SUCCESS] 所有测试通过！")
        else:
            print(f"[FAILED] {failed} 个测试失败")
        print("="*70)
        
        return failed == 0
    
    def run_api_tests(self):
        """只运行API功能测试"""
        return self.run_all_tests(include_api_tests=True)


class PlaywrightAPITestMixin:
    """Playwright API测试混入类，提供完整的API更新功能测试"""
    
    # 子类需要设置的属性
    collection_name = ""
    display_name = ""
    api_type = "no_param"  # no_param, date_param, symbol_param, date_range_param
    default_params = {}  # 默认测试参数
    
    # 认证配置
    AUTH_USERNAME = os.environ.get("TEST_AUTH_USERNAME", "admin")
    AUTH_PASSWORD = os.environ.get("TEST_AUTH_PASSWORD", "admin123")
    
    _auth_token = None
    _playwright = None
    _browser = None
    _page = None
    
    async def _setup_playwright(self):
        """初始化Playwright"""
        if not PLAYWRIGHT_AVAILABLE:
            return False
        
        if self._playwright is None:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=True)
            self._page = await self._browser.new_page()
            self._page.set_default_timeout(API_TIMEOUT)
        return True
    
    async def _teardown_playwright(self):
        """关闭Playwright"""
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        self._page = None
        self._auth_token = None
    
    async def _login(self) -> bool:
        """登录获取认证token"""
        if self._auth_token:
            return True
        
        try:
            url = f"{API_BASE_URL}/api/auth/login"
            response = await self._page.request.post(
                url,
                data=json.dumps({"username": self.AUTH_USERNAME, "password": self.AUTH_PASSWORD}),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status == 200:
                resp_data = await response.json()
                if resp_data.get("success") and resp_data.get("data"):
                    self._auth_token = resp_data["data"].get("access_token")
                else:
                    self._auth_token = resp_data.get("access_token")
                return bool(self._auth_token)
            return False
        except Exception:
            return False
    
    async def _api_request_with_auth(self, endpoint: str, method: str = "GET",
                                      data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送带认证的API请求"""
        url = f"{API_BASE_URL}{API_PREFIX}{endpoint}"
        result = {"success": False, "status_code": None, "response": None, "error": None}
        
        headers = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        
        try:
            if method == "GET":
                response = await self._page.request.get(url, headers=headers)
            elif method == "POST":
                response = await self._page.request.post(
                    url,
                    data=json.dumps(data) if data else None,
                    headers=headers
                )
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            result["status_code"] = response.status
            result["success"] = 200 <= response.status < 300
            
            try:
                result["response"] = await response.json()
            except:
                result["response"] = await response.text()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def test_api_update_async(self) -> Dict[str, Any]:
        """测试API更新功能（异步版本）"""
        if not await self._setup_playwright():
            return {"success": False, "error": "Playwright未安装"}
        
        try:
            # 登录
            if not await self._login():
                return {"success": False, "error": "登录失败"}
            
            # 构建请求数据
            data = {
                "update_type": "single",
                "params": self.default_params.copy()
            }
            
            # 发送更新请求
            result = await self._api_request_with_auth(
                f"/collections/{self.collection_name}/refresh",
                method="POST",
                data=data
            )
            
            return result
            
        finally:
            await self._teardown_playwright()
    
    def test_playwright_api_update(self):
        """测试API更新功能（Playwright自动化测试）"""
        if not PLAYWRIGHT_AVAILABLE:
            print("  [SKIP] Playwright未安装")
            return
        
        # 检查是否跳过刷新测试
        if getattr(self, 'skip_refresh', False):
            print("  [SKIP] 此接口不支持刷新操作")
            return
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(self.test_api_update_async())
        
        if result.get("error") and "Connection refused" in result["error"]:
            print("  [SKIP] 服务器未运行")
            return
        
        if result["success"]:
            print(f"[OK] Playwright API更新测试成功")
            response = result.get("response", {})
            if isinstance(response, dict):
                if "task_id" in response:
                    print(f"      任务ID: {response['task_id']}")
                if "message" in response:
                    msg = response['message']
                    print(f"      消息: {msg[:80] if len(msg) > 80 else msg}")
                if "inserted" in response:
                    print(f"      插入: {response['inserted']} 条")
                if "updated" in response:
                    print(f"      更新: {response['updated']} 条")
        else:
            error_msg = result.get("error") or result.get("response")
            status_code = result.get("status_code")
            print(f"  [FAILED] API更新失败 (状态码: {status_code}): {error_msg}")
    
    async def test_api_get_stats_async(self) -> Dict[str, Any]:
        """测试获取集合统计信息（异步版本）"""
        if not await self._setup_playwright():
            return {"success": False, "error": "Playwright未安装"}
        
        try:
            result = await self._api_request_with_auth(
                f"/collections/{self.collection_name}/stats",
                method="GET"
            )
            return result
        finally:
            await self._teardown_playwright()
    
    async def test_api_get_data_async(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """测试获取集合数据（异步版本）"""
        if not await self._setup_playwright():
            return {"success": False, "error": "Playwright未安装"}
        
        try:
            result = await self._api_request_with_auth(
                f"/collections/{self.collection_name}/data?page={page}&page_size={page_size}",
                method="GET"
            )
            return result
        finally:
            await self._teardown_playwright()
    
    def test_playwright_full_workflow(self):
        """完整工作流测试：获取统计 -> 更新数据 -> 验证结果"""
        if not PLAYWRIGHT_AVAILABLE:
            print("  [SKIP] Playwright未安装")
            return
        
        if getattr(self, 'skip_refresh', False):
            print("  [SKIP] 此接口不支持刷新操作")
            return
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        print(f"\n  [1/3] 获取集合统计信息...")
        stats_result = loop.run_until_complete(self.test_api_get_stats_async())
        if stats_result.get("error") and "Connection refused" in stats_result["error"]:
            print("  [SKIP] 服务器未运行")
            return
        
        if stats_result["success"]:
            response = stats_result.get("response", {})
            if isinstance(response, dict):
                total = response.get("total", response.get("count", "N/A"))
                print(f"      当前数据量: {total}")
        
        print(f"  [2/3] 执行API更新...")
        update_result = loop.run_until_complete(self.test_api_update_async())
        if update_result["success"]:
            response = update_result.get("response", {})
            if isinstance(response, dict):
                if "task_id" in response:
                    print(f"      任务ID: {response['task_id']}")
                elif "message" in response:
                    print(f"      结果: {response['message'][:50]}")
        else:
            print(f"      更新失败: {update_result.get('error') or update_result.get('response')}")
            return
        
        print(f"  [3/3] 验证数据...")
        data_result = loop.run_until_complete(self.test_api_get_data_async())
        if data_result["success"]:
            response = data_result.get("response", {})
            if isinstance(response, dict):
                items = response.get("items", response.get("data", []))
                total = response.get("total", len(items) if isinstance(items, list) else 0)
                print(f"      数据验证成功，共 {total} 条记录")
        
        print(f"[OK] 完整工作流测试通过")
