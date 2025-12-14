"""
使用Playwright测试网站上的期货数据集合API更新功能
确保每个期货数据接口的更新功能都可用
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
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/futures"
HEADLESS = os.environ.get("TEST_HEADLESS", "true").lower() == "true"
TIMEOUT = 60000  # 60秒超时

# 认证配置（可通过环境变量设置）
AUTH_USERNAME = os.environ.get("TEST_AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("TEST_AUTH_PASSWORD", "admin123")


class WebAPITester:
    """网站API测试器"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
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
    
    async def login(self, username: str = AUTH_USERNAME, password: str = AUTH_PASSWORD) -> bool:
        """登录获取认证token"""
        try:
            url = f"{self.base_url}/api/auth/login"
            response = await self.page.request.post(
                url,
                data=json.dumps({"username": username, "password": password}),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status == 200:
                resp_data = await response.json()
                # 支持两种响应格式
                if resp_data.get("success") and resp_data.get("data"):
                    self.auth_token = resp_data["data"].get("access_token")
                else:
                    self.auth_token = resp_data.get("access_token")
                    
                if self.auth_token:
                    print(f"  [OK] 登录成功")
                    return True
            
            print(f"  [WARN] 登录失败: {response.status}")
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
            
    async def api_request(self, endpoint: str, method: str = "GET", 
                          data: Optional[Dict] = None, 
                          require_auth: bool = False) -> Dict[str, Any]:
        """发送API请求"""
        url = f"{self.base_url}{API_PREFIX}{endpoint}"
        result = {
            "endpoint": endpoint,
            "method": method,
            "url": url,
            "success": False,
            "status_code": None,
            "response": None,
            "error": None,
            "duration_ms": 0
        }
        
        start_time = datetime.now()
        
        # 构建请求头
        headers = {"Content-Type": "application/json"}
        if require_auth and self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method == "GET":
                response = await self.page.request.get(url, headers=headers)
            elif method == "POST":
                response = await self.page.request.post(
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
            
        result["duration_ms"] = (datetime.now() - start_time).total_seconds() * 1000
        self.results.append(result)
        return result
    
    async def test_collection_update(self, collection_name: str, 
                                      params: Optional[Dict] = None,
                                      update_type: str = "single") -> Dict[str, Any]:
        """测试集合更新功能
        
        Args:
            collection_name: 集合名称
            params: 更新参数
            update_type: 更新类型 (single/batch)
        """
        endpoint = f"/collections/{collection_name}/refresh"
        data = {
            "update_type": update_type,
            "params": params or {}
        }
        return await self.api_request(endpoint, method="POST", data=data, require_auth=True)
    
    async def test_collection_batch_update(self, collection_name: str) -> Dict[str, Any]:
        """测试集合批量更新功能"""
        endpoint = f"/collections/{collection_name}/batch-refresh"
        return await self.api_request(endpoint, method="POST", require_auth=True)
    
    async def wait_for_task(self, task_id: str, max_wait: int = 60) -> Dict[str, Any]:
        """等待任务完成"""
        for _ in range(max_wait):
            result = await self.api_request(f"/tasks/{task_id}")
            if result["success"] and result["response"]:
                status = result["response"].get("status")
                if status in ["completed", "failed", "error"]:
                    return result
            await asyncio.sleep(1)
        return {"success": False, "error": "任务超时"}
    
    def print_result(self, result: Dict[str, Any], indent: int = 2):
        """打印测试结果"""
        prefix = " " * indent
        status = "✓" if result["success"] else "✗"
        print(f"{prefix}[{status}] {result['method']} {result['endpoint']}")
        print(f"{prefix}    状态码: {result['status_code']}, 耗时: {result['duration_ms']:.0f}ms")
        if result["error"]:
            print(f"{prefix}    错误: {result['error'][:100]}")
        elif not result["success"] and result["response"]:
            resp_str = str(result["response"])[:150]
            print(f"{prefix}    响应: {resp_str}")


# 期货集合配置 - 按类型分组
COLLECTIONS_BY_TYPE = {
    "no_param": [
        {"name": "futures_fees_info", "display": "期货交易费用参照表"},
        {"name": "futures_contract_info_dce", "display": "大连商品交易所合约信息"},
        {"name": "futures_contract_info_gfex", "display": "广州期货交易所合约信息"},
        {"name": "futures_hq_subscribe_exchange_symbol", "display": "外盘品种代码表"},
        {"name": "futures_global_spot_em", "display": "外盘实时行情数据-东财"},
        {"name": "index_hog_spot_price", "display": "生猪市场价格指数"},
        {"name": "futures_news_shmet", "display": "期货资讯"},
        # futures_stock_shfe_js 不支持刷新操作
    ],
    "date_param": [
        {"name": "futures_rule", "display": "期货规则-交易日历表", "params": {"date": "20241213"}},
        {"name": "futures_dce_position_rank", "display": "大连商品交易所-持仓排名", "params": {"date": "20241213"}},
        {"name": "futures_gfex_position_rank", "display": "广州期货交易所-持仓排名", "params": {"date": "20241213"}},
        {"name": "futures_warehouse_receipt_czce", "display": "仓单日报-郑州商品交易所", "params": {"date": "20241213"}},
        {"name": "futures_warehouse_receipt_dce", "display": "仓单日报-大连商品交易所", "params": {"date": "20241213"}},
        {"name": "futures_shfe_warehouse_receipt", "display": "仓单日报-上海期货交易所", "params": {"date": "20241213"}},
        {"name": "futures_gfex_warehouse_receipt", "display": "仓单日报-广州期货交易所", "params": {"date": "20241213"}},
        {"name": "futures_contract_info_shfe", "display": "上海期货交易所-合约信息", "params": {"date": "20241213"}},
        {"name": "futures_contract_info_ine", "display": "上海国际能源交易中心-合约信息", "params": {"date": "20241213"}},
        {"name": "futures_contract_info_czce", "display": "郑州商品交易所-合约信息", "params": {"date": "20241213"}},
        {"name": "futures_contract_info_cffex", "display": "中国金融期货交易所-合约信息", "params": {"date": "20241213"}},
        {"name": "futures_settlement_price_sgx", "display": "新加坡交易所期货-结算价", "params": {"date": "20241213"}},
    ],
    "symbol_param": [
        {"name": "futures_comm_info", "display": "期货手续费与保证金", "params": {"symbol": "所有"}},
        {"name": "futures_inventory_99", "display": "库存数据-99期货网", "params": {"symbol": "豆一"}},
        {"name": "futures_inventory_em", "display": "库存数据-东方财富", "params": {"symbol": "A"}},
        {"name": "futures_spot_sys", "display": "现期图", "params": {"symbol": "铜"}},
        {"name": "futures_zh_realtime", "display": "内盘-实时行情数据(品种)", "params": {"symbol": "白糖"}},
        {"name": "futures_main_sina", "display": "期货连续合约-新浪", "params": {"symbol": "V0"}},
        {"name": "futures_contract_detail", "display": "期货合约详情-新浪", "params": {"symbol": "V2501"}},
        {"name": "futures_foreign_detail", "display": "外盘-合约详情", "params": {"symbol": "GC"}},
        {"name": "futures_comex_inventory", "display": "COMEX库存数据", "params": {"symbol": "黄金"}},
        {"name": "futures_index_ccidx", "display": "中证商品指数", "params": {"symbol": "中证商品期货指数"}},
    ],
}


async def run_web_api_tests(test_update: bool = True, test_batch: bool = False):
    """运行网站API测试"""
    if not PLAYWRIGHT_AVAILABLE:
        print("[ERROR] Playwright未安装")
        return False
    
    tester = WebAPITester()
    
    try:
        print("="*70)
        print("期货数据集合 - 网站API更新功能测试")
        print(f"测试地址: {BASE_URL}")
        print("="*70)
        
        await tester.setup()
        
        # 1. 测试服务器连接
        print("\n[1] 测试服务器连接")
        print("-"*50)
        result = await tester.api_request("/collections")
        tester.print_result(result)
        
        if not result["success"]:
            if result["error"] and "Connection refused" in result["error"]:
                print("\n[ERROR] 服务器未运行，请先启动服务器")
            else:
                print(f"\n[ERROR] 无法连接服务器: {result.get('error')}")
            return False
        
        # 1.5 尝试登录
        print("\n[1.5] 尝试登录")
        print("-"*50)
        logged_in = await tester.login()
        if not logged_in:
            print("  [WARN] 未能登录，将跳过需要认证的测试")
            print("  [INFO] 可通过环境变量设置认证信息:")
            print("         TEST_AUTH_USERNAME=your_username")
            print("         TEST_AUTH_PASSWORD=your_password")
        
        # 2. 测试无参数接口的更新功能
        if test_update:
            print("\n[2] 测试无参数接口更新功能")
            print("-"*50)
            
            for coll in COLLECTIONS_BY_TYPE["no_param"]:
                print(f"\n  {coll['display']} ({coll['name']})")
                result = await tester.test_collection_update(coll["name"])
                tester.print_result(result, indent=4)
                
                # 如果返回任务ID，等待任务完成
                if result["success"] and isinstance(result["response"], dict):
                    task_id = result["response"].get("task_id")
                    if task_id:
                        print(f"      任务ID: {task_id}")
                        # 不等待任务完成，只检查任务是否创建成功
        
        # 3. 测试日期参数接口的更新功能
        if test_update:
            print("\n[3] 测试日期参数接口更新功能")
            print("-"*50)
            
            for coll in COLLECTIONS_BY_TYPE["date_param"][:5]:  # 只测试前5个
                print(f"\n  {coll['display']} ({coll['name']})")
                params = coll.get("params", {})
                result = await tester.test_collection_update(coll["name"], params)
                tester.print_result(result, indent=4)
        
        # 4. 测试symbol参数接口的更新功能
        if test_update:
            print("\n[4] 测试symbol参数接口更新功能")
            print("-"*50)
            
            for coll in COLLECTIONS_BY_TYPE["symbol_param"][:5]:  # 只测试前5个
                print(f"\n  {coll['display']} ({coll['name']})")
                params = coll.get("params", {})
                result = await tester.test_collection_update(coll["name"], params)
                tester.print_result(result, indent=4)
        
        # 5. 测试批量更新功能（可选）
        if test_batch:
            print("\n[5] 测试批量更新功能")
            print("-"*50)
            
            # 只测试一个无参数接口的批量更新
            coll = COLLECTIONS_BY_TYPE["no_param"][0]
            print(f"\n  {coll['display']} ({coll['name']})")
            result = await tester.test_collection_batch_update(coll["name"])
            tester.print_result(result, indent=4)
        
        # 打印汇总
        print("\n" + "="*70)
        print("测试结果汇总")
        print("="*70)
        
        total = len(tester.results)
        success = sum(1 for r in tester.results if r["success"])
        failed = total - success
        
        print(f"成功: {success}")
        print(f"失败: {failed}")
        print(f"总计: {total}")
        
        if failed > 0:
            print("\n失败的测试:")
            for r in tester.results:
                if not r["success"]:
                    print(f"  - {r['endpoint']}: {r.get('error') or r.get('status_code')}")
        
        print("="*70)
        
        return failed == 0
        
    except Exception as e:
        print(f"\n[ERROR] 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        await tester.teardown()


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="期货数据集合网站API更新功能测试")
    parser.add_argument("--batch", action="store_true", help="测试批量更新功能")
    parser.add_argument("--no-update", action="store_true", help="跳过更新测试")
    args = parser.parse_args()
    
    success = asyncio.run(run_web_api_tests(
        test_update=not args.no_update,
        test_batch=args.batch
    ))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
