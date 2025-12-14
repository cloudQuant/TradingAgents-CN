#!/usr/bin/env python
"""
测试所有期权数据集合的刷新功能
确保所有API更新功能都可用
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


# 所有期权数据集合及其测试参数
ALL_OPTION_COLLECTIONS = [
    # 无参数集合
    ("option_contract_info_ctp", {}),
    ("option_current_day_sse", {}),
    ("option_current_day_szse", {}),
    ("option_cffex_sz50_list_sina", {}),
    ("option_cffex_hs300_list_sina", {}),
    ("option_cffex_zz1000_list_sina", {}),
    ("option_current_em", {}),
    ("option_value_analysis_em", {}),
    ("option_risk_analysis_em", {}),
    ("option_premium_analysis_em", {}),
    
    # 带参数集合 - 金融期权
    ("option_finance_board", {"symbol": "华夏上证50ETF期权", "end_month": "2512"}),
    ("option_risk_indicator_sse", {"date": "20241210"}),
    ("option_daily_stats_sse", {"date": "20241210"}),
    ("option_daily_stats_szse", {"date": "20241210"}),
    ("option_cffex_sz50_spot_sina", {"symbol": "ho2512"}),
    ("option_cffex_hs300_spot_sina", {"symbol": "io2512"}),
    ("option_cffex_zz1000_spot_sina", {"symbol": "mo2512"}),
    ("option_cffex_sz50_daily_sina", {"symbol": "ho2512C2500"}),
    ("option_cffex_hs300_daily_sina", {"symbol": "io2512C4000"}),
    ("option_cffex_zz1000_daily_sina", {"symbol": "mo2512C4900"}),
    
    # 上交所期权
    ("option_sse_list_sina", {"symbol": "50ETF", "exchange": "null"}),
    ("option_sse_expire_day_sina", {"trade_date": "202512", "symbol": "50ETF", "exchange": "null"}),
    ("option_sse_codes_sina", {"trade_date": "202512", "underlying": "510050"}),
    ("option_sse_spot_price_sina", {"symbol": "10008573"}),
    ("option_sse_underlying_spot_price_sina", {"symbol": "sh510050"}),
    ("option_sse_greeks_sina", {"symbol": "10008573"}),
    ("option_sse_minute_sina", {"symbol": "10008573"}),
    ("option_sse_daily_sina", {"symbol": "10008573"}),
    ("option_finance_minute_sina", {"symbol": "10008573"}),
    
    # 东财期权
    ("option_minute_em", {"symbol": "MO2512-C-4900"}),
    ("option_lhb_em", {"symbol": "510050", "indicator": "期权交易情况-认购交易量", "trade_date": "20241210"}),
    
    # 商品期权
    ("option_commodity_contract_sina", {"symbol": "黄金期权"}),
    ("option_commodity_contract_table_sina", {"symbol": "黄金期权", "contract": "au2602"}),
    ("option_commodity_hist_sina", {"symbol": "au2602C608"}),
    ("option_comm_info", {"symbol": "工业硅期权"}),
    ("option_margin", {"symbol": "原油期权"}),
    
    # 交易所期权数据
    ("option_hist_shfe", {"symbol": "铜期权", "date": "20241210"}),
    ("option_hist_dce", {"symbol": "豆粕期权", "date": "20241210"}),
    ("option_hist_czce", {"symbol": "白糖期权", "date": "20241210"}),
    ("option_hist_gfex", {"symbol": "工业硅", "date": "20241210"}),
    ("option_vol_gfex", {"symbol": "工业硅", "date": "20241210"}),
    ("option_czce_hist", {"symbol": "SR", "year": "2024"}),
]


async def test_all_refresh():
    """测试所有集合的刷新功能"""
    base_url = "http://localhost:8000"
    api_prefix = "/api/options"
    results = []
    
    print("=" * 70)
    print("期权数据集合刷新功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标地址: {base_url}")
    print(f"测试集合数: {len(ALL_OPTION_COLLECTIONS)}")
    print("=" * 70)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # 登录
        print("\n登录中...")
        response = await page.request.post(
            f"{base_url}/api/auth/login",
            data=json.dumps({"username": "admin", "password": "admin123"}),
            headers={"Content-Type": "application/json"}
        )
        
        if response.ok:
            data = await response.json()
            if data.get("success"):
                auth_token = data["data"]["access_token"]
                print("✓ 登录成功")
            else:
                print("✗ 登录失败")
                return
        else:
            print(f"✗ 登录失败: {response.status}")
            return
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        # 测试每个集合的刷新功能
        print("\n开始测试刷新功能...")
        print("-" * 70)
        
        for collection_name, params in ALL_OPTION_COLLECTIONS:
            try:
                url = f"{base_url}{api_prefix}/collections/{collection_name}/refresh"
                response = await page.request.post(
                    url,
                    data=json.dumps(params),
                    headers=headers,
                    timeout=30000
                )
                
                if response.ok:
                    data = await response.json()
                    if data.get("success"):
                        task_id = data.get("task_id", "")[:8]
                        print(f"✓ {collection_name}: 刷新任务已提交 (task: {task_id})")
                        results.append((collection_name, "成功", task_id))
                    else:
                        error = data.get("error", "未知错误")[:40]
                        print(f"✗ {collection_name}: {error}")
                        results.append((collection_name, "失败", error))
                else:
                    print(f"✗ {collection_name}: HTTP {response.status}")
                    results.append((collection_name, "HTTP错误", response.status))
            except PlaywrightTimeout:
                print(f"✗ {collection_name}: 超时")
                results.append((collection_name, "超时", ""))
            except Exception as e:
                error = str(e)[:40]
                print(f"✗ {collection_name}: {error}")
                results.append((collection_name, "异常", error))
        
        await browser.close()
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r[1] == "成功")
    fail_count = len(results) - success_count
    
    print(f"  总测试数: {len(results)}")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  成功率: {success_count/len(results)*100:.1f}%")
    
    if fail_count > 0:
        print("\n失败的集合:")
        for name, status, msg in results:
            if status != "成功":
                print(f"  - {name}: {status} - {msg}")
    
    return results


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
    
    await test_all_refresh()


if __name__ == "__main__":
    asyncio.run(main())
