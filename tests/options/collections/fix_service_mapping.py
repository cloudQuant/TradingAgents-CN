#!/usr/bin/env python
"""
修复 option_refresh_service.py 中的服务映射
将聚合服务文件名改为实际存在的单独服务文件名
"""

# 正确的服务映射（使用实际存在的单独服务文件）
CORRECT_MAPPINGS = '''        service_mappings = {
            # 无参数集合
            "option_contract_info_ctp": ("app.services.data_sources.options.services.option_contract_info_ctp_service", "OptionContractInfoCtpService"),
            "option_current_day_sse": ("app.services.data_sources.options.services.option_current_day_sse_service", "OptionCurrentDaySseService"),
            "option_current_day_szse": ("app.services.data_sources.options.services.option_current_day_szse_service", "OptionCurrentDaySzseService"),
            "option_cffex_sz50_list_sina": ("app.services.data_sources.options.services.option_cffex_sz50_list_sina_service", "OptionCffexSz50ListSinaService"),
            "option_cffex_hs300_list_sina": ("app.services.data_sources.options.services.option_cffex_hs300_list_sina_service", "OptionCffexHs300ListSinaService"),
            "option_cffex_zz1000_list_sina": ("app.services.data_sources.options.services.option_cffex_zz1000_list_sina_service", "OptionCffexZz1000ListSinaService"),
            "option_current_em": ("app.services.data_sources.options.services.option_current_em_service", "OptionCurrentEmService"),
            "option_lhb_em": ("app.services.data_sources.options.services.option_lhb_em_service", "OptionLhbEmService"),
            "option_value_analysis_em": ("app.services.data_sources.options.services.option_value_analysis_em_service", "OptionValueAnalysisEmService"),
            "option_risk_analysis_em": ("app.services.data_sources.options.services.option_risk_analysis_em_service", "OptionRiskAnalysisEmService"),
            "option_premium_analysis_em": ("app.services.data_sources.options.services.option_premium_analysis_em_service", "OptionPremiumAnalysisEmService"),
            "option_comm_info": ("app.services.data_sources.options.services.option_comm_info_service", "OptionCommInfoService"),
            "option_margin": ("app.services.data_sources.options.services.option_margin_service", "OptionMarginService"),
            "option_vol_gfex": ("app.services.data_sources.options.services.option_vol_gfex_service", "OptionVolGfexService"),
            
            # 日期参数集合
            "option_risk_indicator_sse": ("app.services.data_sources.options.services.option_risk_indicator_sse_service", "OptionRiskIndicatorSseService"),
            "option_daily_stats_sse": ("app.services.data_sources.options.services.option_daily_stats_sse_service", "OptionDailyStatsSseService"),
            "option_daily_stats_szse": ("app.services.data_sources.options.services.option_daily_stats_szse_service", "OptionDailyStatsSzseService"),
            "option_czce_hist": ("app.services.data_sources.options.services.option_czce_hist_service", "OptionCzceHistService"),
            
            # 品种参数集合
            "option_finance_board": ("app.services.data_sources.options.services.option_finance_board_service", "OptionFinanceBoardService"),
            "option_cffex_sz50_spot_sina": ("app.services.data_sources.options.services.option_cffex_sz50_spot_sina_service", "OptionCffexSz50SpotSinaService"),
            "option_cffex_hs300_spot_sina": ("app.services.data_sources.options.services.option_cffex_hs300_spot_sina_service", "OptionCffexHs300SpotSinaService"),
            "option_cffex_zz1000_spot_sina": ("app.services.data_sources.options.services.option_cffex_zz1000_spot_sina_service", "OptionCffexZz1000SpotSinaService"),
            "option_cffex_sz50_daily_sina": ("app.services.data_sources.options.services.option_cffex_sz50_daily_sina_service", "OptionCffexSz50DailySinaService"),
            "option_cffex_hs300_daily_sina": ("app.services.data_sources.options.services.option_cffex_hs300_daily_sina_service", "OptionCffexHs300DailySinaService"),
            "option_cffex_zz1000_daily_sina": ("app.services.data_sources.options.services.option_cffex_zz1000_daily_sina_service", "OptionCffexZz1000DailySinaService"),
            "option_sse_list_sina": ("app.services.data_sources.options.services.option_sse_list_sina_service", "OptionSseListSinaService"),
            "option_sse_expire_day_sina": ("app.services.data_sources.options.services.option_sse_expire_day_sina_service", "OptionSseExpireDaySinaService"),
            "option_sse_codes_sina": ("app.services.data_sources.options.services.option_sse_codes_sina_service", "OptionSseCodesSinaService"),
            "option_sse_spot_price_sina": ("app.services.data_sources.options.services.option_sse_spot_price_sina_service", "OptionSseSpotPriceSinaService"),
            "option_sse_underlying_spot_price_sina": ("app.services.data_sources.options.services.option_sse_underlying_spot_price_sina_service", "OptionSseUnderlyingSpotPriceSinaService"),
            "option_sse_greeks_sina": ("app.services.data_sources.options.services.option_sse_greeks_sina_service", "OptionSseGreeksSinaService"),
            "option_sse_minute_sina": ("app.services.data_sources.options.services.option_sse_minute_sina_service", "OptionSseMinuteSinaService"),
            "option_sse_daily_sina": ("app.services.data_sources.options.services.option_sse_daily_sina_service", "OptionSseDailySinaService"),
            "option_finance_minute_sina": ("app.services.data_sources.options.services.option_finance_minute_sina_service", "OptionFinanceMinuteSinaService"),
            "option_minute_em": ("app.services.data_sources.options.services.option_minute_em_service", "OptionMinuteEmService"),
            "option_commodity_contract_sina": ("app.services.data_sources.options.services.option_commodity_contract_sina_service", "OptionCommodityContractSinaService"),
            "option_commodity_contract_table_sina": ("app.services.data_sources.options.services.option_commodity_contract_table_sina_service", "OptionCommodityContractTableSinaService"),
            "option_commodity_hist_sina": ("app.services.data_sources.options.services.option_commodity_hist_sina_service", "OptionCommodityHistSinaService"),
            
            # 品种+日期参数集合
            "option_hist_shfe": ("app.services.data_sources.options.services.option_hist_shfe_service", "OptionHistShfeService"),
            "option_hist_dce": ("app.services.data_sources.options.services.option_hist_dce_service", "OptionHistDceService"),
            "option_hist_czce": ("app.services.data_sources.options.services.option_hist_czce_service", "OptionHistCzceService"),
            "option_hist_gfex": ("app.services.data_sources.options.services.option_hist_gfex_service", "OptionHistGfexService"),
        }'''

def fix_service_mapping():
    """修复服务映射"""
    file_path = "/Users/yunjinqi/Documents/TradingAgents-CN/app/services/option_refresh_service.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 service_mappings 的开始和结束位置
    import re
    
    # 匹配从 "service_mappings = {" 到对应的 "}" 的内容
    pattern = r'        service_mappings = \{[^}]+\}'
    
    # 使用更精确的匹配
    start_marker = "        service_mappings = {"
    end_marker = "        }\n        \n        self._service_classes = service_mappings"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("未找到 service_mappings 开始位置")
        return False
    
    # 找到匹配的结束大括号
    brace_count = 0
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:]):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = start_idx + i + 1
                break
    
    if end_idx == start_idx:
        print("未找到 service_mappings 结束位置")
        return False
    
    # 替换内容
    new_content = content[:start_idx] + CORRECT_MAPPINGS + content[end_idx:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 已修复 {file_path}")
    print(f"  替换了 {end_idx - start_idx} 字符")
    return True


if __name__ == "__main__":
    fix_service_mapping()
