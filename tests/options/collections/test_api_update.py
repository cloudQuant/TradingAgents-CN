#!/usr/bin/env python
"""
期权数据集合API更新功能测试
按照接口清单顺序，逐个测试每个集合的刷新功能
确保API更新功能可用，并验证数据正确更新
"""
import sys
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


class APIUpdateTester:
    """API更新功能测试器"""
    
    # 按照接口清单顺序定义所有42个集合及其测试参数
    COLLECTIONS = [
        # 1. openctp期权合约信息
        {"name": "option_contract_info_ctp", "display": "openctp期权合约信息", "params": {}},
        # 2. 金融期权行情数据
        {"name": "option_finance_board", "display": "金融期权行情数据", 
         "params": {"symbol": "华夏上证50ETF期权", "end_month": "2512"}},
        # 3. 上交所期权风险指标
        {"name": "option_risk_indicator_sse", "display": "上交所期权风险指标", 
         "params": {"date": "20241210"}},
        # 4. 上交所当日合约
        {"name": "option_current_day_sse", "display": "上交所当日合约", "params": {}},
        # 5. 深交所当日合约
        {"name": "option_current_day_szse", "display": "深交所当日合约", "params": {}},
        # 6. 上交所每日统计
        {"name": "option_daily_stats_sse", "display": "上交所每日统计", 
         "params": {"date": "20241210"}},
        # 7. 深交所日度概况
        {"name": "option_daily_stats_szse", "display": "深交所日度概况", 
         "params": {"date": "20241210"}},
        # 8. 中金所上证50指数合约列表
        {"name": "option_cffex_sz50_list_sina", "display": "中金所上证50指数合约列表", "params": {}},
        # 9. 中金所沪深300指数合约列表
        {"name": "option_cffex_hs300_list_sina", "display": "中金所沪深300指数合约列表", "params": {}},
        # 10. 中金所中证1000指数合约列表
        {"name": "option_cffex_zz1000_list_sina", "display": "中金所中证1000指数合约列表", "params": {}},
        # 11. 中金所上证50指数实时行情
        {"name": "option_cffex_sz50_spot_sina", "display": "中金所上证50指数实时行情", 
         "params": {"symbol": "ho2512"}},
        # 12. 中金所沪深300指数实时行情
        {"name": "option_cffex_hs300_spot_sina", "display": "中金所沪深300指数实时行情", 
         "params": {"symbol": "io2512"}},
        # 13. 中金所中证1000指数实时行情
        {"name": "option_cffex_zz1000_spot_sina", "display": "中金所中证1000指数实时行情", 
         "params": {"symbol": "mo2512"}},
        # 14. 中金所上证50指数日频行情
        {"name": "option_cffex_sz50_daily_sina", "display": "中金所上证50指数日频行情", 
         "params": {"symbol": "ho2512C2500"}},
        # 15. 中金所沪深300指数日频行情
        {"name": "option_cffex_hs300_daily_sina", "display": "中金所沪深300指数日频行情", 
         "params": {"symbol": "io2512C4000"}},
        # 16. 中金所中证1000指数日频行情
        {"name": "option_cffex_zz1000_daily_sina", "display": "中金所中证1000指数日频行情", 
         "params": {"symbol": "mo2512C4900"}},
        # 17. 上交所50ETF合约到期月份列表
        {"name": "option_sse_list_sina", "display": "上交所50ETF合约到期月份列表", 
         "params": {"symbol": "50ETF", "exchange": "null"}},
        # 18. 剩余到期时间
        {"name": "option_sse_expire_day_sina", "display": "剩余到期时间", 
         "params": {"trade_date": "202512", "symbol": "50ETF", "exchange": "null"}},
        # 19. 看涨看跌合约代码
        {"name": "option_sse_codes_sina", "display": "看涨看跌合约代码", 
         "params": {"trade_date": "202512", "underlying": "510050"}},
        # 20. 期权实时数据
        {"name": "option_sse_spot_price_sina", "display": "期权实时数据", 
         "params": {"symbol": "10008573"}, "skip_refresh": True, "skip_reason": "实时数据接口不支持刷新"},
        # 21. 期权标的物实时数据
        {"name": "option_sse_underlying_spot_price_sina", "display": "期权标的物实时数据", 
         "params": {"symbol": "sh510050"}},
        # 22. 期权希腊字母信息表
        {"name": "option_sse_greeks_sina", "display": "期权希腊字母信息表", 
         "params": {"symbol": "10008573"}},
        # 23. 期权分钟数据
        {"name": "option_sse_minute_sina", "display": "期权分钟数据", 
         "params": {"symbol": "10008573"}},
        # 24. 期权日数据
        {"name": "option_sse_daily_sina", "display": "期权日数据", 
         "params": {"symbol": "10008573"}},
        # 25. 金融期权股票期权分时行情
        {"name": "option_finance_minute_sina", "display": "金融期权股票期权分时行情", 
         "params": {"symbol": "10008573"}},
        # 26. 东财期权分时行情
        {"name": "option_minute_em", "display": "东财期权分时行情", 
         "params": {"symbol": "MO2512-C-4900"}},
        # 27. 东财期权行情
        {"name": "option_current_em", "display": "东财期权行情", "params": {}},
        # 28. 期权龙虎榜
        {"name": "option_lhb_em", "display": "期权龙虎榜", 
         "params": {"symbol": "510050", "indicator": "期权交易情况-认购交易量", "trade_date": "20241210"}},
        # 29. 期权价值分析
        {"name": "option_value_analysis_em", "display": "期权价值分析", "params": {}},
        # 30. 期权风险分析
        {"name": "option_risk_analysis_em", "display": "期权风险分析", "params": {}},
        # 31. 期权折溢价
        {"name": "option_premium_analysis_em", "display": "期权折溢价", "params": {}},
        # 32. 商品期权当前合约
        {"name": "option_commodity_contract_sina", "display": "商品期权当前合约", 
         "params": {"symbol": "黄金期权"}},
        # 33. 商品期权T型报价表
        {"name": "option_commodity_contract_table_sina", "display": "商品期权T型报价表", 
         "params": {"symbol": "黄金期权", "contract": "au2602"}},
        # 34. 商品期权历史行情
        {"name": "option_commodity_hist_sina", "display": "商品期权历史行情", 
         "params": {"symbol": "au2602C608"}},
        # 35. 商品期权手续费
        {"name": "option_comm_info", "display": "商品期权手续费", 
         "params": {"symbol": "工业硅期权"}},
        # 36. 期权保证金
        {"name": "option_margin", "display": "期权保证金", 
         "params": {"symbol": "原油期权"}},
        # 37. 上期所期权数据
        {"name": "option_hist_shfe", "display": "上期所期权数据", 
         "params": {"symbol": "铜期权", "date": "20241210"}},
        # 38. 大商所期权数据
        {"name": "option_hist_dce", "display": "大商所期权数据", 
         "params": {"symbol": "豆粕期权", "date": "20241210"}},
        # 39. 郑商所期权数据
        {"name": "option_hist_czce", "display": "郑商所期权数据", 
         "params": {"symbol": "白糖期权", "date": "20241210"}},
        # 40. 广期所期权数据
        {"name": "option_hist_gfex", "display": "广期所期权数据", 
         "params": {"symbol": "工业硅", "date": "20241210"}},
        # 41. 广期所隐含波动率
        {"name": "option_vol_gfex", "display": "广期所隐含波动率", 
         "params": {"symbol": "工业硅", "date": "20241210"}},
        # 42. 郑商所期权历史行情
        {"name": "option_czce_hist", "display": "郑商所期权历史行情", 
         "params": {"symbol": "SR", "year": "2024"}},
    ]
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_prefix = "/api/options"
        self.auth_token = None
        self.results = []
        
    async def login(self, page) -> bool:
        """登录获取认证token"""
        try:
            response = await page.request.post(
                f"{self.base_url}/api/auth/login",
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

    async def test_refresh(self, page, collection: dict) -> dict:
        """测试单个集合的刷新功能"""
        name = collection["name"]
        display = collection["display"]
        params = collection["params"]
        skip_refresh = collection.get("skip_refresh", False)
        skip_reason = collection.get("skip_reason", "")
        
        result = {
            "index": self.COLLECTIONS.index(collection) + 1,
            "name": name,
            "display": display,
            "refresh_status": "未测试",
            "refresh_task_id": "",
            "refresh_error": "",
            "data_status": "未测试",
            "data_count": 0,
            "data_error": "",
        }
        
        # 如果跳过刷新测试
        if skip_refresh:
            result["refresh_status"] = "跳过"
            result["refresh_error"] = skip_reason
        else:
            # 测试刷新功能
            try:
                url = f"{self.base_url}{self.api_prefix}/collections/{name}/refresh"
                response = await page.request.post(
                    url,
                    data=json.dumps(params),
                    headers=self.get_headers(),
                    timeout=60000
                )
                
                if response.ok:
                    data = await response.json()
                    if data.get("success"):
                        result["refresh_status"] = "成功"
                        result["refresh_task_id"] = data.get("task_id", "")[:8]
                    else:
                        result["refresh_status"] = "失败"
                        result["refresh_error"] = data.get("error", "未知错误")[:50]
                else:
                    result["refresh_status"] = "HTTP错误"
                    result["refresh_error"] = f"HTTP {response.status}"
            except PlaywrightTimeout:
                result["refresh_status"] = "超时"
            except Exception as e:
                result["refresh_status"] = "异常"
                result["refresh_error"] = str(e)[:50]
        
        # 等待刷新完成
        if result["refresh_status"] == "成功":
            await asyncio.sleep(2)
        
        # 测试获取数据
        try:
            url = f"{self.base_url}{self.api_prefix}/collections/{name}"
            if params:
                query_string = "&".join([f"{k}={v}" for k, v in params.items()])
                url = f"{url}?{query_string}"
            
            response = await page.request.get(url, headers=self.get_headers(), timeout=30000)
            
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    records = data.get("data", {})
                    if isinstance(records, dict):
                        count = records.get("total", len(records.get("items", [])))
                    elif isinstance(records, list):
                        count = len(records)
                    else:
                        count = 0
                    result["data_status"] = "成功"
                    result["data_count"] = count
                else:
                    result["data_status"] = "失败"
                    result["data_error"] = data.get("error", "未知错误")[:50]
            else:
                result["data_status"] = "HTTP错误"
                result["data_error"] = f"HTTP {response.status}"
        except PlaywrightTimeout:
            result["data_status"] = "超时"
        except Exception as e:
            result["data_status"] = "异常"
            result["data_error"] = str(e)[:50]
        
        return result
    
    async def test_batch_refresh(self, page, collection_names: list) -> dict:
        """测试批量刷新功能"""
        result = {
            "status": "未测试",
            "success_count": 0,
            "fail_count": 0,
            "error": "",
        }
        
        try:
            url = f"{self.base_url}{self.api_prefix}/collections/batch-refresh"
            response = await page.request.post(
                url,
                data=json.dumps({"collections": collection_names}),
                headers=self.get_headers(),
                timeout=120000
            )
            
            if response.ok:
                data = await response.json()
                if data.get("success"):
                    result["status"] = "成功"
                    result["success_count"] = data.get("success_count", 0)
                    result["fail_count"] = data.get("fail_count", 0)
                else:
                    result["status"] = "失败"
                    result["error"] = data.get("error", "未知错误")[:50]
            else:
                result["status"] = "HTTP错误"
                result["error"] = f"HTTP {response.status}"
        except PlaywrightTimeout:
            result["status"] = "超时"
        except Exception as e:
            result["status"] = "异常"
            result["error"] = str(e)[:50]
        
        return result
    
    def print_result(self, result: dict):
        """打印单个测试结果"""
        idx = result["index"]
        name = result["name"]
        display = result["display"]
        
        refresh_icon = "✓" if result["refresh_status"] == "成功" else ("⊘" if result["refresh_status"] == "跳过" else "✗")
        data_icon = "✓" if result["data_status"] == "成功" else "✗"
        
        print(f"{idx:2d}. {name}")
        print(f"    显示名称: {display}")
        print(f"    刷新: {refresh_icon} {result['refresh_status']}", end="")
        if result["refresh_task_id"]:
            print(f" (task: {result['refresh_task_id']})", end="")
        if result["refresh_error"]:
            print(f" - {result['refresh_error']}", end="")
        print()
        print(f"    数据: {data_icon} {result['data_status']}", end="")
        if result["data_count"] > 0:
            print(f" (数据量: {result['data_count']})", end="")
        if result["data_error"]:
            print(f" - {result['data_error']}", end="")
        print()

    async def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("期权数据集合API更新功能测试")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"目标地址: {self.base_url}")
        print(f"测试集合数: {len(self.COLLECTIONS)}")
        print("=" * 80)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # 登录
            print("\n登录中...")
            if await self.login(page):
                print("✓ 登录成功")
            else:
                print("✗ 登录失败，退出测试")
                return
            
            # 逐个测试每个集合
            print("\n" + "-" * 80)
            print("开始逐个测试API更新功能")
            print("-" * 80)
            
            for collection in self.COLLECTIONS:
                result = await self.test_refresh(page, collection)
                self.results.append(result)
                self.print_result(result)
                print()
                # 避免请求过快
                await asyncio.sleep(0.5)
            
            await browser.close()
        
        # 打印测试摘要
        self.print_summary()
        
        # 生成测试报告
        self.generate_report()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 80)
        print("测试摘要")
        print("=" * 80)
        
        refresh_success = sum(1 for r in self.results if r["refresh_status"] == "成功")
        refresh_skip = sum(1 for r in self.results if r["refresh_status"] == "跳过")
        refresh_fail = len(self.results) - refresh_success - refresh_skip
        
        data_success = sum(1 for r in self.results if r["data_status"] == "成功")
        data_fail = len(self.results) - data_success
        
        print(f"\n刷新功能测试:")
        print(f"  总测试数: {len(self.results)}")
        print(f"  成功: {refresh_success}")
        print(f"  跳过: {refresh_skip}")
        print(f"  失败: {refresh_fail}")
        print(f"  成功率: {refresh_success/(len(self.results)-refresh_skip)*100:.1f}%" if (len(self.results)-refresh_skip) > 0 else "N/A")
        
        print(f"\n数据获取测试:")
        print(f"  总测试数: {len(self.results)}")
        print(f"  成功: {data_success}")
        print(f"  失败: {data_fail}")
        print(f"  成功率: {data_success/len(self.results)*100:.1f}%" if self.results else "N/A")
        
        # 打印失败的集合
        failed_refresh = [r for r in self.results if r["refresh_status"] not in ("成功", "跳过")]
        failed_data = [r for r in self.results if r["data_status"] != "成功"]
        
        if failed_refresh:
            print("\n刷新失败的集合:")
            for r in failed_refresh:
                print(f"  - {r['name']}: {r['refresh_status']} - {r['refresh_error']}")
        
        if failed_data:
            print("\n数据获取失败的集合:")
            for r in failed_data:
                print(f"  - {r['name']}: {r['data_status']} - {r['data_error']}")
    
    def generate_report(self):
        """生成测试报告"""
        report_path = Path(__file__).parent / "test_api_update_report.md"
        
        refresh_success = sum(1 for r in self.results if r["refresh_status"] == "成功")
        refresh_skip = sum(1 for r in self.results if r["refresh_status"] == "跳过")
        refresh_fail = len(self.results) - refresh_success - refresh_skip
        
        data_success = sum(1 for r in self.results if r["data_status"] == "成功")
        data_fail = len(self.results) - data_success
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 期权数据集合API更新功能测试报告\n\n")
            f.write(f"## 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 测试摘要\n\n")
            f.write(f"| 测试项 | 总数 | 成功 | 跳过 | 失败 | 成功率 |\n")
            f.write(f"|--------|------|------|------|------|--------|\n")
            refresh_rate = f"{refresh_success/(len(self.results)-refresh_skip)*100:.1f}%" if (len(self.results)-refresh_skip) > 0 else "N/A"
            data_rate = f"{data_success/len(self.results)*100:.1f}%" if self.results else "N/A"
            f.write(f"| 刷新功能 | {len(self.results)} | {refresh_success} | {refresh_skip} | {refresh_fail} | {refresh_rate} |\n")
            f.write(f"| 数据获取 | {len(self.results)} | {data_success} | - | {data_fail} | {data_rate} |\n\n")
            
            f.write("## 详细测试结果\n\n")
            f.write("| 序号 | 集合名称 | 显示名称 | 刷新状态 | 数据状态 | 数据量 |\n")
            f.write("|------|----------|----------|----------|----------|--------|\n")
            
            for r in self.results:
                refresh_icon = "✓" if r["refresh_status"] == "成功" else ("⊘" if r["refresh_status"] == "跳过" else "✗")
                data_icon = "✓" if r["data_status"] == "成功" else "✗"
                f.write(f"| {r['index']} | {r['name']} | {r['display']} | {refresh_icon} {r['refresh_status']} | {data_icon} {r['data_status']} | {r['data_count']} |\n")
            
            # 失败详情
            failed_refresh = [r for r in self.results if r["refresh_status"] not in ("成功", "跳过")]
            failed_data = [r for r in self.results if r["data_status"] != "成功"]
            
            if failed_refresh:
                f.write("\n## 刷新失败详情\n\n")
                f.write("| 集合名称 | 状态 | 错误信息 |\n")
                f.write("|----------|------|----------|\n")
                for r in failed_refresh:
                    f.write(f"| {r['name']} | {r['refresh_status']} | {r['refresh_error']} |\n")
            
            if failed_data:
                f.write("\n## 数据获取失败详情\n\n")
                f.write("| 集合名称 | 状态 | 错误信息 |\n")
                f.write("|----------|------|----------|\n")
                for r in failed_data:
                    f.write(f"| {r['name']} | {r['data_status']} | {r['data_error']} |\n")
        
        print(f"\n测试报告已生成: {report_path}")


async def main():
    """主函数"""
    import socket
    
    def check_port(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    
    if not check_port("localhost", 8000):
        print("错误: 后端服务未运行 (localhost:8000)")
        print("请先启动后端服务")
        return
    
    tester = APIUpdateTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
