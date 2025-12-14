#!/usr/bin/env python
"""
详细测试每个期货数据集合的API更新功能
记录具体的错误信息，用于发现和修复bug
"""
import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.dirname(__file__))

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[ERROR] Playwright未安装")
    sys.exit(1)

# 配置
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/futures"
AUTH_USERNAME = os.environ.get("TEST_AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("TEST_AUTH_PASSWORD", "admin123")

# 所有接口的测试配置
TEST_CONFIGS = [
    # 无参数接口
    {"name": "futures_fees_info", "display": "期货交易费用参照表", "params": {}, "type": "no_param"},
    {"name": "futures_contract_info_dce", "display": "大连商品交易所合约信息", "params": {}, "type": "no_param"},
    {"name": "futures_contract_info_gfex", "display": "广州期货交易所合约信息", "params": {}, "type": "no_param"},
    {"name": "futures_hq_subscribe_exchange_symbol", "display": "外盘品种代码表", "params": {}, "type": "no_param"},
    {"name": "futures_global_spot_em", "display": "外盘实时行情数据-东财", "params": {}, "type": "no_param"},
    {"name": "index_hog_spot_price", "display": "生猪市场价格指数", "params": {}, "type": "no_param"},
    {"name": "futures_news_shmet", "display": "期货资讯", "params": {}, "type": "no_param"},
    {"name": "futures_stock_shfe_js", "display": "上海期货交易所-库存数据", "params": {}, "type": "no_param", "skip_refresh": True},
    
    # 日期参数接口
    {"name": "futures_rule", "display": "期货规则-交易日历表", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_dce_position_rank", "display": "大连商品交易所-持仓排名", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_gfex_position_rank", "display": "广州期货交易所-持仓排名", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_warehouse_receipt_czce", "display": "仓单日报-郑州商品交易所", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_warehouse_receipt_dce", "display": "仓单日报-大连商品交易所", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_shfe_warehouse_receipt", "display": "仓单日报-上海期货交易所", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_gfex_warehouse_receipt", "display": "仓单日报-广州期货交易所", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_shfe", "display": "上海期货交易所-合约信息", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_ine", "display": "上海国际能源交易中心-合约信息", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_czce", "display": "郑州商品交易所-合约信息", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_contract_info_cffex", "display": "中国金融期货交易所-合约信息", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_to_spot_dce", "display": "期现价格对比-大连", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_to_spot_czce", "display": "期现价格对比-郑州", "params": {"date": "20241213"}, "type": "date_param"},
    {"name": "futures_to_spot_shfe", "display": "期现价格对比-上海", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_dce", "display": "交割信息-大连", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_czce", "display": "交割信息-郑州", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_shfe", "display": "交割信息-上海", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_match_dce", "display": "交割配对-大连", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_delivery_match_czce", "display": "交割配对-郑州", "params": {"date": "202412"}, "type": "date_param"},
    {"name": "futures_settlement_price_sgx", "display": "新加坡交易所期货-结算价", "params": {"date": "20241213"}, "type": "date_param"},
    
    # Symbol参数接口
    {"name": "futures_comm_info", "display": "期货手续费与保证金", "params": {"symbol": "所有"}, "type": "symbol_param"},
    {"name": "futures_inventory_99", "display": "库存数据-99期货网", "params": {"symbol": "豆一"}, "type": "symbol_param"},
    {"name": "futures_inventory_em", "display": "库存数据-东方财富", "params": {"symbol": "A"}, "type": "symbol_param"},
    {"name": "futures_hold_pos_sina", "display": "持仓数据-新浪", "params": {"symbol": "IF"}, "type": "symbol_param"},
    {"name": "futures_spot_sys", "display": "现期图", "params": {"symbol": "铜"}, "type": "symbol_param"},
    {"name": "futures_zh_spot", "display": "内盘-实时行情数据", "params": {"market": "CF"}, "type": "symbol_param"},
    {"name": "futures_zh_realtime", "display": "内盘-实时行情数据(品种)", "params": {"symbol": "白糖"}, "type": "symbol_param"},
    {"name": "futures_zh_minute_sina", "display": "内盘-分钟数据", "params": {"symbol": "IF2501"}, "type": "symbol_param"},
    {"name": "futures_zh_daily_sina", "display": "内盘-日线数据", "params": {"symbol": "RB0"}, "type": "symbol_param"},
    {"name": "futures_main_sina", "display": "期货连续合约-新浪", "params": {"symbol": "V0"}, "type": "symbol_param"},
    {"name": "futures_contract_detail", "display": "期货合约详情-新浪", "params": {"symbol": "V2501"}, "type": "symbol_param"},
    {"name": "futures_contract_detail_em", "display": "期货合约详情-东财", "params": {"symbol": "螺纹钢主力"}, "type": "symbol_param"},
    {"name": "futures_foreign_commodity_realtime", "display": "外盘-实时行情", "params": {"symbol": "黄金"}, "type": "symbol_param"},
    {"name": "futures_global_hist_em", "display": "外盘-历史行情-东财", "params": {"symbol": "伦敦金"}, "type": "symbol_param"},
    {"name": "futures_foreign_hist", "display": "外盘-历史行情", "params": {"symbol": "GC"}, "type": "symbol_param"},
    {"name": "futures_foreign_detail", "display": "外盘-合约详情", "params": {"symbol": "GC"}, "type": "symbol_param"},
    {"name": "futures_index_ccidx", "display": "中证商品指数", "params": {"symbol": "中证商品期货指数"}, "type": "symbol_param"},
    {"name": "futures_spot_stock", "display": "现货库存", "params": {"symbol": "铜"}, "type": "symbol_param"},
    {"name": "futures_comex_inventory", "display": "COMEX库存数据", "params": {"symbol": "黄金"}, "type": "symbol_param"},
    {"name": "futures_hog_core", "display": "生猪核心数据", "params": {"symbol": "全国"}, "type": "symbol_param"},
    {"name": "futures_hog_cost", "display": "生猪成本数据", "params": {"symbol": "全国"}, "type": "symbol_param"},
    {"name": "futures_hog_supply", "display": "生猪供应数据", "params": {"symbol": "全国"}, "type": "symbol_param"},
    
    # 日期范围参数接口
    {"name": "futures_hist_em", "display": "内盘-历史行情-东财", "params": {"symbol": "螺纹钢主力", "period": "daily", "start_date": "20241201", "end_date": "20241213"}, "type": "date_range_param"},
    {"name": "get_futures_daily", "display": "内盘-历史行情-交易所", "params": {"start_date": "20241201", "end_date": "20241213", "market": "SHFE"}, "type": "date_range_param"},
]


class DetailedAPITester:
    """详细API测试器"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.auth_token = None
        self.results = []
    
    async def setup(self):
        """初始化"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        self.page.set_default_timeout(60000)
    
    async def teardown(self):
        """清理"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def login(self) -> bool:
        """登录"""
        try:
            url = f"{BASE_URL}/api/auth/login"
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
                return bool(self.auth_token)
            return False
        except Exception as e:
            print(f"登录失败: {e}")
            return False
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """获取集合统计信息"""
        url = f"{BASE_URL}{API_PREFIX}/collections/{collection_name}/stats"
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            response = await self.page.request.get(url, headers=headers)
            result = {
                "status_code": response.status,
                "success": 200 <= response.status < 300,
            }
            try:
                result["response"] = await response.json()
            except:
                result["response"] = await response.text()
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def refresh_collection(self, collection_name: str, params: Dict) -> Dict[str, Any]:
        """刷新集合数据"""
        url = f"{BASE_URL}{API_PREFIX}/collections/{collection_name}/refresh"
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        data = {
            "update_type": "single",
            "params": params
        }
        
        try:
            response = await self.page.request.post(
                url,
                data=json.dumps(data),
                headers=headers
            )
            result = {
                "status_code": response.status,
                "success": 200 <= response.status < 300,
            }
            try:
                result["response"] = await response.json()
            except:
                result["response"] = await response.text()
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_collection_data(self, collection_name: str, page: int = 1, page_size: int = 5) -> Dict[str, Any]:
        """获取集合数据"""
        url = f"{BASE_URL}{API_PREFIX}/collections/{collection_name}/data?page={page}&page_size={page_size}"
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            response = await self.page.request.get(url, headers=headers)
            result = {
                "status_code": response.status,
                "success": 200 <= response.status < 300,
            }
            try:
                result["response"] = await response.json()
            except:
                result["response"] = await response.text()
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_collection(self, config: Dict) -> Dict[str, Any]:
        """测试单个集合"""
        name = config["name"]
        display = config["display"]
        params = config["params"]
        skip_refresh = config.get("skip_refresh", False)
        
        result = {
            "name": name,
            "display": display,
            "type": config["type"],
            "params": params,
            "stats": None,
            "refresh": None,
            "data": None,
            "errors": [],
            "warnings": [],
            "success": True
        }
        
        # 1. 获取统计信息
        stats = await self.get_collection_stats(name)
        result["stats"] = stats
        if not stats.get("success"):
            result["errors"].append(f"获取统计信息失败: {stats.get('error') or stats.get('response')}")
            result["success"] = False
        else:
            resp = stats.get("response", {})
            if isinstance(resp, dict):
                total = resp.get("total", resp.get("count", 0))
                if total == 0:
                    result["warnings"].append(f"集合数据为空 (total=0)")
        
        # 2. 刷新数据（如果不跳过）
        if not skip_refresh:
            refresh = await self.refresh_collection(name, params)
            result["refresh"] = refresh
            if not refresh.get("success"):
                status_code = refresh.get("status_code")
                resp = refresh.get("response", {})
                error_msg = resp.get("detail") if isinstance(resp, dict) else str(resp)
                result["errors"].append(f"刷新失败 (状态码:{status_code}): {error_msg}")
                result["success"] = False
        else:
            result["refresh"] = {"skipped": True, "reason": "不支持刷新操作"}
        
        # 3. 获取数据
        data = await self.get_collection_data(name)
        result["data"] = data
        if not data.get("success"):
            result["errors"].append(f"获取数据失败: {data.get('error') or data.get('response')}")
            result["success"] = False
        else:
            resp = data.get("response", {})
            if isinstance(resp, dict):
                items = resp.get("items", resp.get("data", []))
                if not items:
                    result["warnings"].append("获取数据返回空列表")
        
        return result
    
    async def run_all_tests(self, configs: List[Dict] = None) -> List[Dict]:
        """运行所有测试"""
        if configs is None:
            configs = TEST_CONFIGS
        
        await self.setup()
        
        # 登录
        print("正在登录...")
        if not await self.login():
            print("[ERROR] 登录失败")
            await self.teardown()
            return []
        print("[OK] 登录成功\n")
        
        results = []
        total = len(configs)
        
        for i, config in enumerate(configs, 1):
            name = config["name"]
            display = config["display"]
            print(f"[{i}/{total}] 测试 {display} ({name})...")
            
            result = await self.test_collection(config)
            results.append(result)
            
            # 打印结果
            if result["success"] and not result["warnings"]:
                print(f"  [OK] 测试通过")
            elif result["success"] and result["warnings"]:
                print(f"  [WARN] 测试通过，但有警告:")
                for warn in result["warnings"]:
                    print(f"    - {warn}")
            else:
                print(f"  [FAILED] 测试失败:")
                for err in result["errors"]:
                    print(f"    - {err}")
            
            # 短暂延迟避免请求过快
            await asyncio.sleep(0.5)
        
        await self.teardown()
        self.results = results
        return results
    
    def print_summary(self):
        """打印测试汇总"""
        if not self.results:
            print("没有测试结果")
            return
        
        passed = sum(1 for r in self.results if r["success"] and not r["warnings"])
        warned = sum(1 for r in self.results if r["success"] and r["warnings"])
        failed = sum(1 for r in self.results if not r["success"])
        
        print("\n" + "="*70)
        print("测试结果汇总")
        print("="*70)
        print(f"通过: {passed}")
        print(f"警告: {warned}")
        print(f"失败: {failed}")
        print(f"总计: {len(self.results)}")
        
        if warned > 0:
            print("\n有警告的接口:")
            for r in self.results:
                if r["success"] and r["warnings"]:
                    print(f"  - {r['display']} ({r['name']})")
                    for warn in r["warnings"]:
                        print(f"      {warn}")
        
        if failed > 0:
            print("\n失败的接口:")
            for r in self.results:
                if not r["success"]:
                    print(f"  - {r['display']} ({r['name']})")
                    for err in r["errors"]:
                        print(f"      {err}")
        
        print("="*70)
    
    def save_results(self, filepath: str = "test_results.json"):
        """保存测试结果到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n测试结果已保存到: {filepath}")


async def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description="详细测试期货数据集合API")
    parser.add_argument("--name", type=str, help="只测试指定的集合")
    parser.add_argument("--type", type=str, choices=["no_param", "date_param", "symbol_param", "date_range_param"], help="只测试指定类型的接口")
    parser.add_argument("--save", action="store_true", help="保存测试结果到文件")
    args = parser.parse_args()
    
    tester = DetailedAPITester()
    
    # 过滤测试配置
    configs = TEST_CONFIGS
    if args.name:
        configs = [c for c in configs if c["name"] == args.name]
    if args.type:
        configs = [c for c in configs if c["type"] == args.type]
    
    if not configs:
        print("没有匹配的测试配置")
        return 1
    
    print("="*70)
    print("期货数据集合API详细测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试数量: {len(configs)}")
    print("="*70 + "\n")
    
    await tester.run_all_tests(configs)
    tester.print_summary()
    
    if args.save:
        tester.save_results()
    
    # 返回失败数量
    failed = sum(1 for r in tester.results if not r["success"])
    return failed


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
