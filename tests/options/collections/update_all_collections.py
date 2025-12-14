#!/usr/bin/env python
"""
直接调用Service更新所有期权数据集合
绕过后端API，直接操作数据库
"""
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 所有集合配置
COLLECTIONS = [
    # 无参数集合
    {"name": "option_contract_info_ctp", "service": "OptionContractInfoCtpService", 
     "module": "option_contract_info_ctp_service", "params": {}},
    {"name": "option_current_day_sse", "service": "OptionCurrentDaySseService", 
     "module": "option_current_day_sse_service", "params": {}},
    {"name": "option_current_day_szse", "service": "OptionCurrentDaySzseService", 
     "module": "option_current_day_szse_service", "params": {}},
    {"name": "option_cffex_sz50_list_sina", "service": "OptionCffexSz50ListSinaService", 
     "module": "option_cffex_sz50_list_sina_service", "params": {}},
    {"name": "option_cffex_hs300_list_sina", "service": "OptionCffexHs300ListSinaService", 
     "module": "option_cffex_hs300_list_sina_service", "params": {}},
    {"name": "option_cffex_zz1000_list_sina", "service": "OptionCffexZz1000ListSinaService", 
     "module": "option_cffex_zz1000_list_sina_service", "params": {}},
    {"name": "option_current_em", "service": "OptionCurrentEmService", 
     "module": "option_current_em_service", "params": {}},
    {"name": "option_value_analysis_em", "service": "OptionValueAnalysisEmService", 
     "module": "option_value_analysis_em_service", "params": {}},
    {"name": "option_risk_analysis_em", "service": "OptionRiskAnalysisEmService", 
     "module": "option_risk_analysis_em_service", "params": {}},
    {"name": "option_premium_analysis_em", "service": "OptionPremiumAnalysisEmService", 
     "module": "option_premium_analysis_em_service", "params": {}},
    
    # 带参数集合
    {"name": "option_finance_board", "service": "OptionFinanceBoardService", 
     "module": "option_finance_board_service", "params": {"symbol": "华夏上证50ETF期权", "end_month": "2512"}},
    {"name": "option_risk_indicator_sse", "service": "OptionRiskIndicatorSseService", 
     "module": "option_risk_indicator_sse_service", "params": {"date": "20241210"}},
    {"name": "option_daily_stats_sse", "service": "OptionDailyStatsSseService", 
     "module": "option_daily_stats_sse_service", "params": {"date": "20241210"}},
    {"name": "option_daily_stats_szse", "service": "OptionDailyStatsSzseService", 
     "module": "option_daily_stats_szse_service", "params": {"date": "20241210"}},
    {"name": "option_cffex_sz50_spot_sina", "service": "OptionCffexSz50SpotSinaService", 
     "module": "option_cffex_sz50_spot_sina_service", "params": {"symbol": "ho2512"}},
    {"name": "option_cffex_hs300_spot_sina", "service": "OptionCffexHs300SpotSinaService", 
     "module": "option_cffex_hs300_spot_sina_service", "params": {"symbol": "io2512"}},
    {"name": "option_cffex_zz1000_spot_sina", "service": "OptionCffexZz1000SpotSinaService", 
     "module": "option_cffex_zz1000_spot_sina_service", "params": {"symbol": "mo2512"}},
    {"name": "option_cffex_sz50_daily_sina", "service": "OptionCffexSz50DailySinaService", 
     "module": "option_cffex_sz50_daily_sina_service", "params": {"symbol": "ho2512C2500"}},
    {"name": "option_cffex_hs300_daily_sina", "service": "OptionCffexHs300DailySinaService", 
     "module": "option_cffex_hs300_daily_sina_service", "params": {"symbol": "io2512C4000"}},
    {"name": "option_cffex_zz1000_daily_sina", "service": "OptionCffexZz1000DailySinaService", 
     "module": "option_cffex_zz1000_daily_sina_service", "params": {"symbol": "mo2512C4900"}},
    {"name": "option_sse_list_sina", "service": "OptionSseListSinaService", 
     "module": "option_sse_list_sina_service", "params": {"symbol": "50ETF", "exchange": "null"}},
    {"name": "option_sse_expire_day_sina", "service": "OptionSseExpireDaySinaService", 
     "module": "option_sse_expire_day_sina_service", "params": {"trade_date": "202512", "symbol": "50ETF", "exchange": "null"}},
    {"name": "option_sse_codes_sina", "service": "OptionSseCodesSinaService", 
     "module": "option_sse_codes_sina_service", "params": {"trade_date": "202512", "underlying": "510050"}},
    {"name": "option_sse_underlying_spot_price_sina", "service": "OptionSseUnderlyingSpotPriceSinaService", 
     "module": "option_sse_underlying_spot_price_sina_service", "params": {"symbol": "sh510050"}},
    {"name": "option_sse_greeks_sina", "service": "OptionSseGreeksSinaService", 
     "module": "option_sse_greeks_sina_service", "params": {"symbol": "10008573"}},
    {"name": "option_sse_minute_sina", "service": "OptionSseMinuteSinaService", 
     "module": "option_sse_minute_sina_service", "params": {"symbol": "10008573"}},
    {"name": "option_sse_daily_sina", "service": "OptionSseDailySinaService", 
     "module": "option_sse_daily_sina_service", "params": {"symbol": "10008573"}},
    {"name": "option_finance_minute_sina", "service": "OptionFinanceMinuteSinaService", 
     "module": "option_finance_minute_sina_service", "params": {"symbol": "10008573"}},
    {"name": "option_minute_em", "service": "OptionMinuteEmService", 
     "module": "option_minute_em_service", "params": {"symbol": "MO2512-C-4900"}},
    {"name": "option_lhb_em", "service": "OptionLhbEmService", 
     "module": "option_lhb_em_service", "params": {"symbol": "510050", "indicator": "期权交易情况-认购交易量", "trade_date": "20241210"}},
    {"name": "option_commodity_contract_sina", "service": "OptionCommodityContractSinaService", 
     "module": "option_commodity_contract_sina_service", "params": {"symbol": "黄金期权"}},
    {"name": "option_commodity_contract_table_sina", "service": "OptionCommodityContractTableSinaService", 
     "module": "option_commodity_contract_table_sina_service", "params": {"symbol": "黄金期权", "contract": "au2602"}},
    {"name": "option_commodity_hist_sina", "service": "OptionCommodityHistSinaService", 
     "module": "option_commodity_hist_sina_service", "params": {"symbol": "au2602C608"}},
    {"name": "option_comm_info", "service": "OptionCommInfoService", 
     "module": "option_comm_info_service", "params": {"symbol": "工业硅期权"}},
    {"name": "option_margin", "service": "OptionMarginService", 
     "module": "option_margin_service", "params": {"symbol": "原油期权"}},
    {"name": "option_hist_shfe", "service": "OptionHistShfeService", 
     "module": "option_hist_shfe_service", "params": {"symbol": "铜期权", "date": "20241210"}},
    {"name": "option_hist_dce", "service": "OptionHistDceService", 
     "module": "option_hist_dce_service", "params": {"symbol": "豆粕期权", "date": "20241210"}},
    {"name": "option_hist_czce", "service": "OptionHistCzceService", 
     "module": "option_hist_czce_service", "params": {"symbol": "白糖期权", "date": "20241210"}},
    {"name": "option_hist_gfex", "service": "OptionHistGfexService", 
     "module": "option_hist_gfex_service", "params": {"symbol": "工业硅", "date": "20241210"}},
    {"name": "option_vol_gfex", "service": "OptionVolGfexService", 
     "module": "option_vol_gfex_service", "params": {"symbol": "工业硅", "date": "20241210"}},
    {"name": "option_czce_hist", "service": "OptionCzceHistService", 
     "module": "option_czce_hist_service", "params": {"symbol": "SR", "year": "2024"}},
]


async def update_collection(db, config):
    """更新单个集合"""
    name = config["name"]
    service_name = config["service"]
    module_name = config["module"]
    params = config["params"]
    
    try:
        # 动态导入Service
        module_path = f"app.services.data_sources.options.services.{module_name}"
        module = __import__(module_path, fromlist=[service_name])
        service_class = getattr(module, service_name)
        
        # 创建Service实例
        service = service_class(db)
        
        # 检查provider
        if service.provider is None:
            return {"name": name, "success": False, "error": "provider为None"}
        
        # 执行更新
        result = await service.update_batch_data(**params)
        
        return {
            "name": name,
            "success": result.get("success", False),
            "inserted": result.get("inserted", 0),
            "message": result.get("message", "")
        }
    except Exception as e:
        return {"name": name, "success": False, "error": str(e)[:100]}


async def main():
    """主函数"""
    print("=" * 70)
    print("更新所有期权数据集合")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"集合数: {len(COLLECTIONS)}")
    print("=" * 70)
    
    # 连接MongoDB
    from motor.motor_asyncio import AsyncIOMotorClient
    
    try:
        from app.config.settings import settings
        mongo_uri = settings.MONGODB_URI
    except:
        mongo_uri = "mongodb://localhost:27017"
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client["tradingagents"]
    
    results = []
    
    for i, config in enumerate(COLLECTIONS, 1):
        print(f"\n[{i}/{len(COLLECTIONS)}] {config['name']}")
        result = await update_collection(db, config)
        results.append(result)
        
        if result.get("success"):
            print(f"   ✓ 成功: {result.get('inserted', 0)} 条数据")
        else:
            error = result.get("error", result.get("message", "未知错误"))
            print(f"   ✗ 失败: {error}")
        
        # 避免请求过快
        await asyncio.sleep(0.5)
    
    client.close()
    
    # 打印摘要
    print("\n" + "=" * 70)
    print("更新摘要")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r.get("success"))
    fail_count = len(results) - success_count
    
    print(f"总数: {len(results)}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"成功率: {success_count/len(results)*100:.1f}%")
    
    if fail_count > 0:
        print("\n失败的集合:")
        for r in results:
            if not r.get("success"):
                print(f"  - {r['name']}: {r.get('error', r.get('message', ''))}")


if __name__ == "__main__":
    asyncio.run(main())
