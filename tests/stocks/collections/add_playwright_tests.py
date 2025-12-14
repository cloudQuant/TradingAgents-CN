"""
批量为测试文件添加 Playwright UI 自动化测试

根据接口类型添加针对性的测试用例
"""
import os
import re
from typing import Dict, Optional, Tuple

# 接口配置：collection_name -> (update_type, test_params)
# update_type: 
#   - "no_param": 无参数，直接更新
#   - "symbol": 需要股票代码
#   - "symbol_hk": 需要港股代码
#   - "symbol_us": 需要美股代码
#   - "choice": 需要从选项中选择
#   - "date": 需要日期参数
#   - "date_quarter": 需要季度日期
INTERFACE_CONFIG: Dict[str, Tuple[str, dict]] = {
    # ===== 无参数接口 =====
    "stock_sse_summary": ("no_param", {}),
    "stock_zh_a_spot_em": ("no_param", {}),
    "stock_sh_a_spot_em": ("no_param", {}),
    "stock_sz_a_spot_em": ("no_param", {}),
    "stock_bj_a_spot_em": ("no_param", {}),
    "stock_cy_a_spot_em": ("no_param", {}),
    "stock_kc_a_spot_em": ("no_param", {}),
    "stock_new_a_spot_em": ("no_param", {}),
    "stock_zh_a_new_em": ("no_param", {}),
    "stock_zh_b_spot_em": ("no_param", {}),
    "stock_us_spot_em": ("no_param", {}),
    "stock_hk_spot_em": ("no_param", {}),
    "stock_hk_main_board_spot_em": ("no_param", {}),
    "stock_hot_rank_em": ("no_param", {}),
    "stock_hot_up_em": ("no_param", {}),
    "stock_hk_hot_rank_em": ("no_param", {}),
    "stock_hot_rank_latest_em": ("no_param", {}),
    "stock_hk_hot_rank_latest_em": ("no_param", {}),
    "stock_hot_search_baidu": ("no_param", {}),
    "stock_market_activity_legu": ("no_param", {}),
    "stock_board_industry_name_em": ("no_param", {}),
    "stock_board_concept_name_em": ("no_param", {}),
    "stock_tfp_em": ("no_param", {}),
    "stock_dxsyl_em": ("no_param", {}),
    "stock_xgsglb_em": ("no_param", {}),
    "stock_hsgt_fund_flow_summary_em": ("no_param", {}),
    "stock_hk_ggt_components_em": ("no_param", {}),
    "stock_hsgt_hist_em": ("no_param", {}),
    "stock_market_fund_flow": ("no_param", {}),
    "stock_main_fund_flow": ("no_param", {}),
    "stock_individual_fund_flow_rank": ("no_param", {}),
    "stock_gddh_em": ("no_param", {}),
    "stock_zdhtmx_em": ("no_param", {}),
    
    # ===== 需要日期参数 =====
    "stock_szse_summary": ("date", {"date": "20231229"}),
    "stock_szse_area_summary": ("date", {"date": "202312"}),
    "stock_szse_sector_summary": ("date", {"date": "202312"}),
    "stock_sse_deal_daily": ("date", {"date": "20231229"}),
    "stock_yjbb_em": ("date_quarter", {"date": "20231231"}),
    "stock_yjkb_em": ("date_quarter", {"date": "20231231"}),
    "stock_yjyg_em": ("date_quarter", {"date": "20231231"}),
    "stock_yysj_em": ("date", {"date": "2024"}),
    "stock_zt_pool_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_previous_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_strong_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_sub_new_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_zbgc_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_dtgc_em": ("date", {"date": "20231229"}),
    "stock_report_disclosure": ("date", {"date": "2024"}),
}

# 继续添加接口配置
INTERFACE_CONFIG.update({
    # ===== 需要股票代码 =====
    "stock_individual_info_em": ("symbol", {"symbol": "000001"}),
    "stock_individual_basic_info_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_bid_ask_em": ("symbol", {"symbol": "000001"}),
    "stock_zh_a_hist": ("symbol", {"symbol": "000001"}),
    "stock_zh_a_hist_min_em": ("symbol", {"symbol": "000001"}),
    "stock_intraday_em": ("symbol", {"symbol": "000001"}),
    "stock_news_em": ("symbol", {"symbol": "000001"}),
    "stock_fhps_detail_ths": ("symbol", {"symbol": "000001"}),
    "stock_fhps_em": ("symbol", {"symbol": "000001"}),
    "stock_fhps_detail_em": ("symbol", {"symbol": "000001"}),
    "stock_cyq_em": ("symbol", {"symbol": "000001"}),
    "stock_research_report_em": ("symbol", {"symbol": "000001"}),
    "stock_zcfz_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_lrb_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_xjll_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_balance_sheet_by_report_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_profit_sheet_by_report_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_cash_flow_sheet_by_report_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_financial_abstract": ("symbol", {"symbol": "000001"}),
    "stock_financial_abstract_ths": ("symbol", {"symbol": "000001"}),
    "stock_financial_analysis_indicator_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_gdfx_free_top_10_em": ("symbol", {"symbol": "000001"}),
    "stock_gdfx_top_10_em": ("symbol", {"symbol": "000001"}),
    "stock_individual_fund_flow": ("symbol", {"symbol": "000001"}),
    "stock_hsgt_individual_em": ("symbol", {"symbol": "000001"}),
    "stock_hsgt_individual_detail_em": ("symbol", {"symbol": "000001"}),
    "stock_hot_rank_detail_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_hot_rank_detail_realtime_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_hot_rank_relate_em": ("symbol", {"symbol": "SZ000001"}),
    "stock_irm_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_irm_ans_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_inner_trade_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_comment_em": ("symbol", {"symbol": "000001"}),
    "stock_comment_detail_zhpj_lspf_em": ("symbol", {"symbol": "000001"}),
    "stock_comment_detail_scrd_focus_em": ("symbol", {"symbol": "000001"}),
    "stock_comment_detail_scrd_desire_em": ("symbol", {"symbol": "000001"}),
    "stock_comment_detail_scrd_desire_daily_em": ("symbol", {"symbol": "000001"}),
    "stock_profile_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_history_dividend": ("symbol", {"symbol": "000001"}),
    "stock_notice_report": ("symbol", {"symbol": "000001"}),
    "stock_zh_a_disclosure_report_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_industry_category_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_share_change_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_allotment_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_ipo_summary_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_management_change_ths": ("symbol", {"symbol": "000001"}),
    "stock_shareholder_change_ths": ("symbol", {"symbol": "000001"}),
    "stock_ggcg_em": ("symbol", {"symbol": "000001"}),
    "stock_financial_debt_ths": ("symbol", {"symbol": "000001"}),
    "stock_financial_benefit_ths": ("symbol", {"symbol": "000001"}),
    "stock_financial_cash_ths": ("symbol", {"symbol": "000001"}),
    "stock_hot_follow_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_hot_tweet_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_hot_deal_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_changes_em": ("choice", {"symbol": "大笔买入"}),
    "stock_board_change_em": ("symbol", {"symbol": "BK0475"}),
    
    # ===== 港股代码 =====
    "stock_hk_fhpx_detail_ths": ("symbol_hk", {"symbol": "00700"}),
    "stock_individual_basic_info_hk_xq": ("symbol_hk", {"symbol": "00700"}),
    "stock_hk_hist": ("symbol_hk", {"symbol": "00700"}),
    "stock_hk_hist_min_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_hk_hot_rank_detail_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_hk_hot_rank_detail_realtime_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_financial_hk_report_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_financial_hk_analysis_indicator_em": ("symbol_hk", {"symbol": "00700"}),
    
    # ===== 美股代码 =====
    "stock_individual_basic_info_us_xq": ("symbol_us", {"symbol": "AAPL"}),
    "stock_us_hist": ("symbol_us", {"symbol": "105.AAPL"}),
    "stock_financial_us_report_em": ("symbol_us", {"symbol": "AAPL"}),
    "stock_financial_us_analysis_indicator_em": ("symbol_us", {"symbol": "AAPL"}),
    
    # ===== 选择参数 =====
    "stock_fund_flow_individual": ("choice", {"choices": ["即时", "3日排行", "5日排行"]}),
    "stock_fund_flow_concept": ("choice", {"choices": ["即时", "3日排行", "5日排行"]}),
    "stock_fund_flow_industry": ("choice", {"choices": ["即时", "3日排行", "5日排行"]}),
    "stock_hsgt_fund_min_em": ("choice", {"choices": ["北向资金", "南向资金"]}),
    "stock_hsgt_board_rank_em": ("choice", {"choices": ["北向资金", "南向资金"]}),
    "stock_sector_fund_flow_rank": ("choice", {"choices": ["今日", "3日", "5日"]}),
    "stock_rank_cxfl_ths": ("choice", {"choices": ["5日", "10日", "20日"]}),
    "stock_rank_cxsl_ths": ("choice", {"choices": ["5日", "10日", "20日"]}),
    "stock_rank_xstp_ths": ("choice", {"choices": ["60日", "120日", "250日"]}),
    "stock_rank_xxtp_ths": ("choice", {"choices": ["60日", "120日", "250日"]}),
    "stock_rank_ljqs_ths": ("choice", {"choices": ["5日", "10日", "20日"]}),
    "stock_rank_ljqd_ths": ("choice", {"choices": ["5日", "10日", "20日"]}),
    
    # ===== 板块参数 =====
    "stock_board_industry_cons_em": ("board", {"symbol": "银行"}),
    "stock_board_industry_hist_em": ("board", {"symbol": "BK0475"}),
    "stock_board_industry_hist_min_em": ("board", {"symbol": "BK0475"}),
    "stock_board_concept_cons_em": ("board", {"symbol": "锂电池"}),
    "stock_sector_fund_flow_summary": ("board", {"symbol": "银行"}),
    "stock_sector_fund_flow_hist": ("board", {"symbol": "银行"}),
    "stock_concept_fund_flow_hist": ("board", {"symbol": "锂电池"}),
    
    # ===== ESG =====
    "stock_esg_rate_sina": ("symbol", {"symbol": "000001"}),
    "stock_esg_msci_sina": ("symbol", {"symbol": "000001"}),
    "stock_esg_rft_sina": ("symbol", {"symbol": "000001"}),
    "stock_esg_zd_sina": ("symbol", {"symbol": "000001"}),
    "stock_esg_hz_sina": ("symbol", {"symbol": "000001"}),
})


# Playwright 测试代码模板 - 基础部分
PLAYWRIGHT_BASE_CODE = '''
    # ========== Playwright UI 自动化测试 ==========
    
    @pytest.mark.playwright
    def test_ui_update_data_flow(self):
        """使用 Playwright 测试更新数据完整流程"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            pytest.skip("Playwright 未安装")
        
        import time
        frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
        collection_url = f"{{frontend_url}}/stocks/collections/{collection_name}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                self._do_login(page, frontend_url)
                page.goto(collection_url, wait_until='networkidle', timeout=30000)
                time.sleep(2)
                
                if "/login" in page.url:
                    pytest.skip("需要登录")
                
                update_btn = self._find_button(page, ["更新数据", "更新"])
                if not update_btn:
                    pytest.skip("未找到更新按钮")
                
                update_btn.click()
                time.sleep(1.5)
                
                dialog = self._find_dialog(page)
                if not dialog:
                    pytest.fail("弹窗未出现")
                
                {update_logic}
                
                self._close_dialog(dialog)
                
            finally:
                browser.close()
    
    def _do_login(self, page, frontend_url):
        import time
        try:
            page.goto(f"{{frontend_url}}/login", timeout=10000)
            inp = page.query_selector('input[type="text"]')
            if inp:
                inp.fill("admin")
                pwd = page.query_selector('input[type="password"]')
                if pwd:
                    pwd.fill("admin123")
                btn = page.query_selector('button[type="submit"]')
                if btn:
                    btn.click()
                    page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                    time.sleep(1)
        except:
            pass
    
    def _find_button(self, container, texts):
        for t in texts:
            b = container.query_selector(f'button:has-text("{{t}}")')
            if b and b.is_visible():
                return b
        return None
    
    def _find_dialog(self, page):
        for s in ['.el-dialog', '[role="dialog"]', '.modal']:
            d = page.query_selector(s)
            if d and d.is_visible():
                return d
        return None
    
    def _close_dialog(self, dialog):
        b = dialog.query_selector('button:has-text("关闭")') or dialog.query_selector('.el-dialog__close')
        if b:
            b.click()
'''

# 不同类型的更新逻辑
UPDATE_LOGIC_NO_PARAM = '''
                # 无参数接口，直接点击更新
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)
'''

UPDATE_LOGIC_SYMBOL = '''
                # 输入股票代码
                inp = dialog.query_selector('input[placeholder*="代码"]') or dialog.query_selector('input[type="text"]')
                if inp:
                    inp.fill("{symbol}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(8)
'''

UPDATE_LOGIC_DATE = '''
                # 输入日期
                inp = dialog.query_selector('input[placeholder*="日期"]') or dialog.query_selector('.el-date-editor input')
                if inp:
                    inp.fill("{date}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)
'''

UPDATE_LOGIC_CHOICE = '''
                # 选择参数
                select = dialog.query_selector('.el-select') or dialog.query_selector('select')
                if select:
                    select.click()
                    time.sleep(0.5)
                    opt = page.query_selector('.el-select-dropdown__item')
                    if opt:
                        opt.click()
                        time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)
'''

UPDATE_LOGIC_BOARD = '''
                # 输入板块名称
                inp = dialog.query_selector('input[placeholder*="板块"]') or dialog.query_selector('input[type="text"]')
                if inp:
                    inp.fill("{symbol}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)
'''


def get_update_logic(collection_name: str) -> str:
    """获取更新逻辑代码"""
    config = INTERFACE_CONFIG.get(collection_name)
    
    if config is None:
        return UPDATE_LOGIC_NO_PARAM
    
    update_type, params = config
    
    if update_type == "no_param":
        return UPDATE_LOGIC_NO_PARAM
    elif update_type in ["symbol", "symbol_hk", "symbol_us"]:
        symbol = params.get("symbol", "000001")
        return UPDATE_LOGIC_SYMBOL.format(symbol=symbol)
    elif update_type in ["date", "date_quarter"]:
        date = params.get("date", "20231231")
        return UPDATE_LOGIC_DATE.format(date=date)
    elif update_type == "choice":
        return UPDATE_LOGIC_CHOICE
    elif update_type == "board":
        symbol = params.get("symbol", "银行")
        return UPDATE_LOGIC_BOARD.format(symbol=symbol)
    else:
        return UPDATE_LOGIC_NO_PARAM


def extract_collection_name(filename: str) -> Optional[str]:
    """从文件名提取集合名称"""
    match = re.match(r'\d+_(.+)_collection\.py', filename)
    return match.group(1) if match else None


def add_playwright_test(filepath: str, collection_name: str) -> bool:
    """为测试文件添加 Playwright 测试"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 Playwright 测试
        if '@pytest.mark.playwright' in content:
            return False
        
        # 获取更新逻辑
        update_logic = get_update_logic(collection_name)
        playwright_code = PLAYWRIGHT_BASE_CODE.format(
            collection_name=collection_name,
            update_logic=update_logic
        )
        
        # 在 if __name__ 之前插入
        if 'if __name__' in content:
            pos = content.rfind('if __name__')
            new_content = content[:pos] + playwright_code + '\n\n' + content[pos:]
        else:
            new_content = content + '\n' + playwright_code
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False


def main():
    print("=" * 60)
    print("批量添加 Playwright UI 测试")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    test_files = [f for f in os.listdir(script_dir) 
                  if f.endswith('_collection.py') and f[0].isdigit()]
    
    print(f"\n找到 {len(test_files)} 个测试文件")
    
    added = 0
    skipped = 0
    
    for fn in sorted(test_files):
        collection_name = extract_collection_name(fn)
        if not collection_name:
            continue
        
        filepath = os.path.join(script_dir, fn)
        
        if add_playwright_test(filepath, collection_name):
            print(f"  [+] {collection_name}")
            added += 1
        else:
            skipped += 1
    
    print(f"\n完成！添加: {added}, 跳过: {skipped}")


if __name__ == "__main__":
    main()
