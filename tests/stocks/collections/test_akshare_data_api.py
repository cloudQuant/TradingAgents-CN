"""
测试 AKShare 数据接口的可用性

直接调用 akshare 接口测试数据是否能够正常获取
"""
import os
import re
import sys
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import importlib

# 尝试导入 akshare
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("警告: akshare 未安装，请运行 pip install akshare")


def get_akshare_function_name(collection_name: str) -> str:
    """从集合名称获取 akshare 函数名"""
    # 大多数情况下，集合名称就是函数名
    return collection_name


def test_akshare_function(func_name: str, test_params: dict = None) -> Tuple[bool, str, Optional[int]]:
    """
    测试单个 akshare 函数
    返回: (成功, 消息, 数据行数)
    """
    if not AKSHARE_AVAILABLE:
        return False, "akshare 未安装", None
    
    try:
        # 获取函数
        if not hasattr(ak, func_name):
            return False, f"函数 {func_name} 不存在", None
        
        func = getattr(ak, func_name)
        
        # 调用函数
        if test_params:
            df = func(**test_params)
        else:
            df = func()
        
        # 检查返回值
        if df is None:
            return False, "返回值为 None", None
        
        if hasattr(df, 'empty') and df.empty:
            return True, "返回空数据", 0
        
        if hasattr(df, '__len__'):
            row_count = len(df)
            return True, f"获取到 {row_count} 条数据", row_count
        
        return True, "获取成功", None
        
    except Exception as e:
        error_msg = str(e)
        if len(error_msg) > 100:
            error_msg = error_msg[:100] + "..."
        return False, f"错误: {error_msg}", None


# 定义需要参数的接口及其测试参数
PARAMETERIZED_FUNCTIONS = {
    # 个股信息类 - 需要股票代码
    "stock_individual_info_em": {"symbol": "000001"},
    "stock_individual_basic_info_xq": {"symbol": "SZ000001"},
    "stock_bid_ask_em": {"symbol": "000001"},
    "stock_zh_a_hist": {"symbol": "000001", "period": "daily", "adjust": "qfq"},
    "stock_zh_a_hist_min_em": {"symbol": "000001", "period": "1"},
    "stock_intraday_em": {"symbol": "000001"},
    "stock_intraday_sina": {"symbol": "sz000001"},
    "stock_zh_a_hist_pre_min_em": {"symbol": "000001"},
    "stock_zh_a_tick_tx": {"symbol": "sz000001"},
    
    # 港股类
    "stock_hk_hist": {"symbol": "00700", "adjust": "qfq"},
    "stock_hk_hist_min_em": {"symbol": "00700", "period": "1"},
    "stock_individual_basic_info_hk_xq": {"symbol": "00700"},
    "stock_hk_company_profile_em": {"symbol": "00700"},
    "stock_hk_security_profile_em": {"symbol": "00700"},
    "stock_hk_financial_indicator_em": {"symbol": "00700"},
    "stock_hk_dividend_payout_em": {"symbol": "00700"},
    "stock_hk_growth_comparison_em": {"symbol": "00700"},
    "stock_hk_valuation_comparison_em": {"symbol": "00700"},
    "stock_hk_scale_comparison_em": {"symbol": "00700"},
    
    # 美股类
    "stock_us_hist": {"symbol": "105.AAPL", "adjust": "qfq"},
    "stock_us_hist_min_em": {"symbol": "105.AAPL", "period": "1"},
    "stock_individual_basic_info_us_xq": {"symbol": "AAPL"},
    
    # 财务报表类 - 需要股票代码
    "stock_zcfz_em": {"symbol": "SZ000001"},
    "stock_lrb_em": {"symbol": "SZ000001"},
    "stock_xjll_em": {"symbol": "SZ000001"},
    "stock_balance_sheet_by_report_em": {"symbol": "SZ000001"},
    "stock_balance_sheet_by_yearly_em": {"symbol": "SZ000001"},
    "stock_profit_sheet_by_report_em": {"symbol": "SZ000001"},
    "stock_profit_sheet_by_yearly_em": {"symbol": "SZ000001"},
    "stock_profit_sheet_by_quarterly_em": {"symbol": "SZ000001"},
    "stock_cash_flow_sheet_by_report_em": {"symbol": "SZ000001"},
    "stock_cash_flow_sheet_by_yearly_em": {"symbol": "SZ000001"},
    "stock_cash_flow_sheet_by_quarterly_em": {"symbol": "SZ000001"},
    "stock_financial_abstract": {"symbol": "000001"},
    "stock_financial_abstract_ths": {"symbol": "000001"},
    "stock_financial_analysis_indicator_em": {"symbol": "SZ000001"},
    "stock_financial_analysis_indicator": {"symbol": "000001"},
    
    # 股东类
    "stock_gdfx_free_top_10_em": {"symbol": "000001"},
    "stock_gdfx_top_10_em": {"symbol": "000001"},
    "stock_gdfx_free_holding_change_em": {"symbol": "000001"},
    "stock_gdfx_holding_change_em": {"symbol": "000001"},
    "stock_gdfx_free_holding_analyse_em": {"symbol": "000001"},
    "stock_gdfx_holding_analyse_em": {"symbol": "000001"},
    "stock_gdfx_free_holding_detail_em": {"symbol": "000001"},
    "stock_gdfx_holding_detail_em": {"symbol": "000001"},
    "stock_gdfx_free_holding_statistics_em": {"symbol": "000001"},
    "stock_gdfx_holding_statistics_em": {"symbol": "000001"},
    "stock_gdfx_free_holding_teamwork_em": {"symbol": "000001"},
    "stock_gdfx_holding_teamwork_em": {"symbol": "000001"},
    "stock_zh_a_gdhs": {"symbol": "000001"},
    "stock_zh_a_gdhs_detail_em": {"symbol": "000001"},
    
    # 资金流向类
    "stock_individual_fund_flow": {"symbol": "000001"},
    "stock_fund_flow_individual": {"symbol": "即时"},
    "stock_fund_flow_concept": {"symbol": "即时"},
    "stock_fund_flow_industry": {"symbol": "即时"},
    "stock_sector_fund_flow_rank": {"indicator": "今日", "sector_type": "行业资金流"},
    "stock_sector_fund_flow_summary": {"symbol": "银行"},
    "stock_sector_fund_flow_hist": {"symbol": "银行"},
    "stock_concept_fund_flow_hist": {"symbol": "锂电池"},
    
    # 板块类
    "stock_board_industry_cons_em": {"symbol": "银行"},
    "stock_board_industry_hist_em": {"symbol": "BK0475", "period": "日k", "adjust": ""},
    "stock_board_industry_hist_min_em": {"symbol": "BK0475", "period": "1"},
    "stock_board_concept_cons_em": {"symbol": "锂电池"},
    "stock_board_concept_hist_em": {"symbol": "BK0493", "period": "日k", "adjust": ""},
    "stock_board_concept_hist_min_em": {"symbol": "BK0493", "period": "1"},
    
    # 热度类
    "stock_hot_rank_detail_em": {"symbol": "SZ000001"},
    "stock_hk_hot_rank_detail_em": {"symbol": "00700"},
    "stock_hot_rank_detail_realtime_em": {"symbol": "SZ000001"},
    "stock_hk_hot_rank_detail_realtime_em": {"symbol": "00700"},
    "stock_hot_rank_relate_em": {"symbol": "SZ000001"},
    
    # 新闻类
    "stock_news_em": {"symbol": "000001"},
    
    # 分红类
    "stock_fhps_detail_ths": {"symbol": "000001"},
    "stock_hk_fhpx_detail_ths": {"symbol": "00700"},
    "stock_fhps_em": {"symbol": "000001"},
    "stock_fhps_detail_em": {"symbol": "000001"},
    "stock_history_dividend": {"symbol": "000001"},
    "stock_history_dividend_detail": {"symbol": "000001"},
    
    # 研报类
    "stock_research_report_em": {"symbol": "000001"},
    
    # 筹码分布
    "stock_cyq_em": {"symbol": "000001"},
    
    # 龙虎榜类
    "stock_lhb_stock_detail_em": {"symbol": "000001"},
    
    # 沪深港通类
    "stock_hsgt_individual_em": {"symbol": "000001"},
    "stock_hsgt_individual_detail_em": {"symbol": "000001"},
    "stock_hsgt_fund_min_em": {"symbol": "北向资金"},
    "stock_hsgt_board_rank_em": {"symbol": "北向资金", "indicator": "今日排行"},
    "stock_hsgt_hold_stock_em": {"market": "北向", "indicator": "今日排行"},
    "stock_hsgt_stock_statistics_em": {"symbol": "北向持股", "start_date": "20231201", "end_date": "20231231"},
    "stock_hsgt_institution_statistics_em": {"market": "北向持股", "start_date": "20231201", "end_date": "20231231"},
    
    # 业绩类
    "stock_yjbb_em": {"date": "20231231"},
    "stock_yjkb_em": {"date": "20231231"},
    "stock_yjyg_em": {"date": "20231231"},
    "stock_yysj_em": {"date": "2024"},
    
    # 公告类
    "stock_notice_report": {"symbol": "000001"},
    "stock_zh_a_disclosure_report_cninfo": {"symbol": "000001"},
    "stock_zh_a_disclosure_relation_cninfo": {"symbol": "000001"},
    
    # 估值类
    "stock_value_em": {"symbol": "000001"},
    "stock_zh_valuation_baidu": {"symbol": "000001"},
    "stock_hk_valuation_baidu": {"symbol": "00700"},
    
    # 异动类
    "stock_changes_em": {"symbol": "大笔买入"},
    "stock_board_change_em": {"symbol": "BK0475"},
    
    # 涨停类
    "stock_zt_pool_em": {"date": "20231229"},
    "stock_zt_pool_previous_em": {"date": "20231229"},
    "stock_zt_pool_strong_em": {"date": "20231229"},
    "stock_zt_pool_sub_new_em": {"date": "20231229"},
    "stock_zt_pool_zbgc_em": {"date": "20231229"},
    "stock_zt_pool_dtgc_em": {"date": "20231229"},
    
    # 互动易类
    "stock_irm_cninfo": {"symbol": "000001"},
    "stock_irm_ans_cninfo": {"symbol": "000001"},
    
    # 内部交易
    "stock_inner_trade_xq": {"symbol": "SZ000001"},
    
    # 其他需要参数的接口
    "stock_profile_cninfo": {"symbol": "000001"},
    "stock_ipo_summary_cninfo": {"symbol": "000001"},
    "stock_industry_category_cninfo": {"symbol": "000001"},
    "stock_industry_change_cninfo": {"symbol": "000001"},
    "stock_share_change_cninfo": {"symbol": "000001"},
    "stock_allotment_cninfo": {"symbol": "000001"},
    "stock_report_disclosure": {"symbol": "000001"},
    
    # 商誉类
    "stock_sy_em": {"symbol": "000001"},
    "stock_sy_yq_em": {"symbol": "000001"},
    "stock_sy_jz_em": {"symbol": "000001"},
    "stock_sy_hy_em": {"symbol": "银行"},
    
    # 质押类
    "stock_gpzy_pledge_ratio_em": {"symbol": "000001"},
    "stock_gpzy_pledge_ratio_detail_em": {"symbol": "000001"},
    
    # 限售解禁
    "stock_restricted_release_detail_em": {"symbol": "000001"},
    "stock_restricted_release_stockholder_em": {"symbol": "000001"},
    
    # 机构调研
    "stock_jgdy_tj_em": {"symbol": "000001"},
    "stock_jgdy_detail_em": {"symbol": "000001"},
    
    # 主营业务
    "stock_zyjs_ths": {"symbol": "000001"},
    "stock_zygc_em": {"symbol": "000001"},
    
    # 高管持股
    "stock_management_change_ths": {"symbol": "000001"},
    "stock_shareholder_change_ths": {"symbol": "000001"},
    "stock_ggcg_em": {"symbol": "000001"},
    
    # 财务报表-同花顺
    "stock_financial_debt_ths": {"symbol": "000001"},
    "stock_financial_benefit_ths": {"symbol": "000001"},
    "stock_financial_cash_ths": {"symbol": "000001"},
    
    # 退市股票财务
    "stock_balance_sheet_by_report_delisted_em": {"symbol": "000001"},
    "stock_profit_sheet_by_report_delisted_em": {"symbol": "000001"},
    "stock_cash_flow_sheet_by_report_delisted_em": {"symbol": "000001"},
    
    # 港股/美股财务
    "stock_financial_hk_report_em": {"symbol": "00700"},
    "stock_financial_us_report_em": {"symbol": "AAPL"},
    "stock_financial_hk_analysis_indicator_em": {"symbol": "00700"},
    "stock_financial_us_analysis_indicator_em": {"symbol": "AAPL"},
    
    # 评论类
    "stock_comment_em": {"symbol": "000001"},
    "stock_comment_detail_zhpj_lspf_em": {"symbol": "000001"},
    "stock_comment_detail_scrd_focus_em": {"symbol": "000001"},
    "stock_comment_detail_scrd_desire_em": {"symbol": "000001"},
    "stock_comment_detail_scrd_desire_daily_em": {"symbol": "000001"},
    "stock_comment_detail_zlkp_jgcyd_em": {"symbol": "000001"},
    
    # 雪球热度
    "stock_hot_follow_xq": {"symbol": "SZ000001"},
    "stock_hot_tweet_xq": {"symbol": "SZ000001"},
    "stock_hot_deal_xq": {"symbol": "SZ000001"},
    
    # 分时数据
    "stock_zh_a_minute": {"symbol": "sz000001", "period": "1"},
    "stock_zh_b_minute": {"symbol": "sh900901", "period": "1"},
    
    # B股
    "stock_zh_b_daily": {"symbol": "sh900901", "adjust": "qfq"},
    
    # A+H股
    "stock_zh_ah_daily": {"symbol": "02318", "adjust": "qfq"},
    
    # 科创板
    "stock_zh_kcb_daily": {"symbol": "688001", "adjust": "qfq"},
    
    # CDR
    "stock_zh_a_cdr_daily": {"symbol": "689009", "adjust": "qfq"},
    
    # 新股
    "stock_zh_a_new": {"symbol": "sh688001"},
    
    # 板块详情
    "stock_sector_detail": {"sector": "银行"},
    
    # 机构持股
    "stock_institute_hold": {"symbol": "000001"},
    "stock_institute_hold_detail": {"symbol": "000001"},
    
    # 基金持股
    "stock_fund_stock_holder": {"symbol": "000001"},
    "stock_report_fund_hold": {"symbol": "000001"},
    "stock_report_fund_hold_detail": {"symbol": "000001"},
    
    # 融资融券
    "stock_margin_detail_sse": {"symbol": "000001"},
    "stock_margin_detail_szse": {"symbol": "000001"},
    
    # 大宗交易
    "stock_dzjy_mrmx": {"symbol": "000001"},
    "stock_dzjy_mrtj": {"symbol": "000001"},
    
    # 盈利预测
    "stock_profit_forecast_em": {"symbol": "000001"},
    "stock_profit_forecast_ths": {"symbol": "000001"},
    "stock_hk_profit_forecast_et": {"symbol": "00700"},
    
    # 股东人数
    "stock_hold_num_cninfo": {"symbol": "000001"},
    "stock_hold_change_cninfo": {"symbol": "000001"},
    "stock_hold_control_cninfo": {"symbol": "000001"},
    "stock_hold_management_detail_cninfo": {"symbol": "000001"},
    "stock_hold_management_detail_em": {"symbol": "000001"},
    "stock_hold_management_person_em": {"symbol": "000001"},
    
    # 股权质押
    "stock_cg_guarantee_cninfo": {"symbol": "000001"},
    "stock_cg_lawsuit_cninfo": {"symbol": "000001"},
    "stock_cg_equity_mortgage_cninfo": {"symbol": "000001"},
    
    # 行业分类
    "stock_industry_clf_hist_sw": {"symbol": "000001"},
    
    # 分析师
    "stock_analyst_rank_em": {"year": "2023"},
    "stock_analyst_detail_em": {"analyst_id": "11000200927"},
    
    # 股票回购
    "stock_repurchase_em": {"symbol": "000001"},
    
    # 股本结构
    "stock_zh_a_gbjg_em": {"symbol": "000001"},
    
    # 一致行动人
    "stock_yzxdr_em": {"symbol": "000001"},
    
    # 龙虎榜详情
    "stock_lhb_detail_em": {"start_date": "20231201", "end_date": "20231231"},
    "stock_lhb_stock_statistic_em": {"symbol": "近一月"},
    "stock_lhb_jgmmtj_em": {"start_date": "20231201", "end_date": "20231231"},
    "stock_lhb_jgstatistic_em": {"symbol": "近一月"},
    "stock_lhb_hyyyb_em": {"start_date": "20231201", "end_date": "20231231"},
    "stock_lhb_yyb_detail_em": {"symbol": "华泰证券股份有限公司总部"},
    "stock_lhb_yybph_em": {"symbol": "近一月"},
    "stock_lhb_traderstatistic_em": {"symbol": "近一月"},
    
    # 龙虎榜-新浪
    "stock_lhb_detail_daily_sina": {"date": "20231229"},
    "stock_lhb_ggtj_sina": {"recent_day": "5"},
    "stock_lhb_yytj_sina": {"recent_day": "5"},
    "stock_lhb_jgzz_sina": {"recent_day": "5"},
    "stock_lhb_jgmx_sina": {"symbol": "000001"},
    
    # 技术选股
    "stock_rank_cxfl_ths": {"symbol": "5日"},
    "stock_rank_cxsl_ths": {"symbol": "5日"},
    "stock_rank_xstp_ths": {"symbol": "60日"},
    "stock_rank_xxtp_ths": {"symbol": "60日"},
    "stock_rank_ljqs_ths": {"symbol": "5日"},
    "stock_rank_ljqd_ths": {"symbol": "5日"},
    "stock_rank_xzjp_ths": {"symbol": "险资"},
    
    # ESG
    "stock_esg_rate_sina": {"symbol": "000001"},
    "stock_esg_msci_sina": {"symbol": "000001"},
    "stock_esg_rft_sina": {"symbol": "000001"},
    "stock_esg_zd_sina": {"symbol": "000001"},
    "stock_esg_hz_sina": {"symbol": "000001"},
}


def extract_collections_from_docs(req_dir: str) -> Dict[str, str]:
    """从需求文档中提取集合名称"""
    pattern = re.compile(r'http://localhost:3000/stocks/collections/([a-zA-Z0-9_\-]+)')
    collections = {}
    
    for fn in os.listdir(req_dir):
        if not fn.endswith('.md'):
            continue
        
        fp = os.path.join(req_dir, fn)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                text = f.read()
            for name in pattern.findall(text):
                if name not in collections:
                    collections[name] = fn
        except:
            continue
    
    return collections


def main():
    """主函数"""
    print("=" * 70)
    print("AKShare 数据接口可用性测试")
    print("=" * 70)
    
    if not AKSHARE_AVAILABLE:
        print("\n错误: akshare 未安装，请运行 pip install akshare")
        return
    
    # 获取需求文档中的集合
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_dir = os.path.join(script_dir, '..', 'requirements')
    
    collections = extract_collections_from_docs(req_dir)
    print(f"\n从需求文档中找到 {len(collections)} 个集合")
    
    # 测试结果统计
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    results = []
    
    print(f"\n开始测试...")
    print("-" * 70)
    
    for idx, (collection_name, doc_name) in enumerate(sorted(collections.items()), 1):
        func_name = get_akshare_function_name(collection_name)
        
        # 获取测试参数
        test_params = PARAMETERIZED_FUNCTIONS.get(func_name, None)
        
        # 测试
        success, message, row_count = test_akshare_function(func_name, test_params)
        
        if "不存在" in message:
            status = "SKIP"
            skip_count += 1
        elif success:
            status = "OK"
            success_count += 1
        else:
            status = "FAIL"
            fail_count += 1
        
        results.append({
            'collection': collection_name,
            'func': func_name,
            'status': status,
            'message': message,
            'rows': row_count,
            'doc': doc_name
        })
        
        # 打印进度
        status_icon = "✓" if status == "OK" else ("⊘" if status == "SKIP" else "✗")
        print(f"[{idx:3d}/{len(collections)}] {status_icon} {collection_name}: {message}")
        
        # 添加延迟避免请求过快
        if success and row_count and row_count > 0:
            time.sleep(0.5)
    
    # 输出统计
    print("\n" + "=" * 70)
    print("测试结果统计")
    print("=" * 70)
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print(f"  跳过: {skip_count}")
    print(f"  总计: {len(collections)}")
    print(f"  成功率: {100 * success_count / (success_count + fail_count) if (success_count + fail_count) > 0 else 0:.1f}%")
    
    # 输出失败的接口
    if fail_count > 0:
        print("\n" + "-" * 70)
        print("失败的接口:")
        for r in results:
            if r['status'] == 'FAIL':
                print(f"  - {r['collection']}: {r['message']}")
                print(f"    文档: {r['doc']}")
    
    # 保存结果到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = os.path.join(script_dir, f"akshare_test_result_{timestamp}.txt")
    
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write("AKShare 数据接口测试结果\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"成功: {success_count}\n")
        f.write(f"失败: {fail_count}\n")
        f.write(f"跳过: {skip_count}\n")
        f.write(f"总计: {len(collections)}\n\n")
        
        f.write("详细结果:\n")
        f.write("-" * 70 + "\n")
        for r in results:
            f.write(f"{r['status']:4s} | {r['collection']}: {r['message']}\n")
    
    print(f"\n结果已保存到: {result_file}")


if __name__ == "__main__":
    main()
