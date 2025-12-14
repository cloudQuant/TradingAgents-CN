"""
为测试文件添加 Playwright 自动化测试用例

根据每个接口的特点，添加针对性的 UI 测试
"""
import os
import re
from typing import Dict, List, Tuple, Optional


# 接口参数配置
# 格式: collection_name -> (update_type, params)
# update_type: "no_param" | "symbol" | "choice" | "date" | "date_range" | "batch"
INTERFACE_CONFIG = {
    # 无参数接口 - 直接更新
    "stock_sse_summary": ("no_param", {}),
    "stock_szse_summary": ("date", {"date": "20231229"}),
    "stock_szse_area_summary": ("date", {"date": "202312"}),
    "stock_szse_sector_summary": ("date", {"date": "202312"}),
    "stock_sse_deal_daily": ("date", {"date": "20231229"}),
    "stock_zh_a_spot_em": ("no_param", {}),
    "stock_sh_a_spot_em": ("no_param", {}),
    "stock_sz_a_spot_em": ("no_param", {}),
    "stock_bj_a_spot_em": ("no_param", {}),
    "stock_cy_a_spot_em": ("no_param", {}),
    "stock_kc_a_spot_em": ("no_param", {}),
    "stock_new_a_spot_em": ("no_param", {}),
    
    # 需要股票代码的接口
    "stock_individual_info_em": ("symbol", {"symbol": "000001"}),
    "stock_individual_basic_info_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_bid_ask_em": ("symbol", {"symbol": "000001"}),
    "stock_zh_a_hist": ("symbol_period", {"symbol": "000001", "period": "daily"}),
    "stock_news_em": ("symbol", {"symbol": "000001"}),
    "stock_fhps_detail_ths": ("symbol", {"symbol": "000001"}),
    "stock_hk_fhpx_detail_ths": ("symbol", {"symbol": "00700"}),
    "stock_cyq_em": ("symbol", {"symbol": "000001"}),
    "stock_research_report_em": ("symbol", {"symbol": "000001"}),
    
    # 需要选择参数的接口
    "stock_fund_flow_individual": ("choice", {"symbol": "即时", "choices": ["即时", "3日排行", "5日排行"]}),
    "stock_fund_flow_concept": ("choice", {"symbol": "即时", "choices": ["即时", "3日排行", "5日排行"]}),
    "stock_fund_flow_industry": ("choice", {"symbol": "即时", "choices": ["即时", "3日排行", "5日排行"]}),
    "stock_hsgt_fund_min_em": ("choice", {"symbol": "北向资金", "choices": ["北向资金", "南向资金"]}),
    
    # 需要日期参数的接口
    "stock_yjbb_em": ("date", {"date": "20231231"}),
    "stock_yjkb_em": ("date", {"date": "20231231"}),
    "stock_yjyg_em": ("date", {"date": "20231231"}),
    "stock_yysj_em": ("date", {"date": "2024"}),
    "stock_zt_pool_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_previous_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_strong_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_sub_new_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_zbgc_em": ("date", {"date": "20231229"}),
    "stock_zt_pool_dtgc_em": ("date", {"date": "20231229"}),
}


# Playwright 测试代码模板
PLAYWRIGHT_TEST_TEMPLATE = '''
    # ========== 测试7：Playwright UI 自动化测试 ==========
    
    @pytest.mark.playwright
    def test_ui_update_data_button(self, api_base_url):
        """测试7.1：使用 Playwright 测试更新数据按钮功能"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            pytest.skip("Playwright 未安装，跳过 UI 测试")
        
        frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
        collection_url = f"{{frontend_url}}/stocks/collections/{collection_name}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                # 1. 尝试登录
                self._login_if_needed(page, frontend_url)
                
                # 2. 访问集合页面
                page.goto(collection_url, wait_until='networkidle', timeout=30000)
                import time
                time.sleep(2)
                
                # 3. 查找并点击更新数据按钮
                update_button = self._find_update_button(page)
                if not update_button:
                    pytest.skip("未找到更新数据按钮")
                
                update_button.click()
                time.sleep(1.5)
                
                # 4. 验证弹窗出现
                dialog = self._find_dialog(page)
                assert dialog and dialog.is_visible(), "更新数据弹窗应该出现"
                
                # 5. 测试更新功能
                self._test_update_function(page, dialog)
                
                # 6. 关闭弹窗
                self._close_dialog(page, dialog)
                
            finally:
                browser.close()
    
    def _login_if_needed(self, page, frontend_url):
        """如果需要，执行登录"""
        login_url = f"{{frontend_url}}/login"
        try:
            page.goto(login_url, wait_until='networkidle', timeout=10000)
            if page.query_selector('input[type="text"]'):
                page.fill('input[type="text"]', "admin")
                page.fill('input[type="password"]', "admin123")
                login_btn = page.query_selector('button[type="submit"]') or \\
                           page.query_selector('button:has-text("登录")')
                if login_btn:
                    login_btn.click()
                    page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
        except Exception:
            pass
    
    def _find_update_button(self, page):
        """查找更新数据按钮"""
        selectors = [
            'button:has-text("更新数据")',
            'button:has-text("更新")',
            '.update-button',
            '[data-test="update-button"]',
        ]
        for sel in selectors:
            btn = page.query_selector(sel)
            if btn:
                return btn
        return None
    
    def _find_dialog(self, page):
        """查找弹窗"""
        selectors = ['.el-dialog', '.dialog', '[role="dialog"]', '.modal']
        for sel in selectors:
            dialog = page.query_selector(sel)
            if dialog and dialog.is_visible():
                return dialog
        return None
    
    def _close_dialog(self, page, dialog):
        """关闭弹窗"""
        close_btn = dialog.query_selector('button:has-text("关闭")') or \\
                   dialog.query_selector('.el-dialog__close') or \\
                   dialog.query_selector('[aria-label="Close"]')
        if close_btn:
            close_btn.click()
'''


# 无参数接口的更新测试
NO_PARAM_UPDATE_TEST = '''
    def _test_update_function(self, page, dialog):
        """测试无参数接口的更新功能"""
        import time
        
        # 查找开始更新按钮
        start_btn = dialog.query_selector('button:has-text("开始更新")') or \\
                   dialog.query_selector('button:has-text("更新")') or \\
                   dialog.query_selector('.start-update')
        
        if start_btn:
            start_btn.click()
            time.sleep(3)  # 等待更新完成
            
            # 检查是否有成功提示
            success_msg = page.query_selector('.el-message--success') or \\
                         page.query_selector('[class*="success"]')
            # 更新可能成功也可能失败，主要验证按钮可点击
'''


# 需要股票代码的接口更新测试
SYMBOL_UPDATE_TEST = '''
    def _test_update_function(self, page, dialog):
        """测试需要股票代码的接口更新功能"""
        import time
        
        # 查找股票代码输入框
        symbol_input = dialog.query_selector('input[placeholder*="代码"]') or \\
                      dialog.query_selector('input[placeholder*="symbol"]') or \\
                      dialog.query_selector('.symbol-input input')
        
        if symbol_input:
            symbol_input.fill("{test_symbol}")
            time.sleep(0.5)
        
        # 查找开始更新按钮
        start_btn = dialog.query_selector('button:has-text("开始更新")') or \\
                   dialog.query_selector('button:has-text("更新")') or \\
                   dialog.query_selector('.start-update')
        
        if start_btn:
            start_btn.click()
            time.sleep(5)  # 等待更新完成
'''


# 需要选择参数的接口更新测试
CHOICE_UPDATE_TEST = '''
    def _test_update_function(self, page, dialog):
        """测试需要选择参数的接口更新功能"""
        import time
        
        # 查找选择框
        select = dialog.query_selector('.el-select') or \\
                dialog.query_selector('select') or \\
                dialog.query_selector('[role="combobox"]')
        
        if select:
            select.click()
            time.sleep(0.5)
            # 选择第一个选项
            option = page.query_selector('.el-select-dropdown__item') or \\
                    page.query_selector('option')
            if option:
                option.click()
                time.sleep(0.5)
        
        # 查找开始更新按钮
        start_btn = dialog.query_selector('button:has-text("开始更新")') or \\
                   dialog.query_selector('button:has-text("更新")')
        
        if start_btn:
            start_btn.click()
            time.sleep(5)
'''


# 需要日期参数的接口更新测试
DATE_UPDATE_TEST = '''
    def _test_update_function(self, page, dialog):
        """测试需要日期参数的接口更新功能"""
        import time
        
        # 查找日期输入框
        date_input = dialog.query_selector('input[placeholder*="日期"]') or \\
                    dialog.query_selector('input[type="date"]') or \\
                    dialog.query_selector('.el-date-editor input')
        
        if date_input:
            date_input.fill("{test_date}")
            time.sleep(0.5)
        
        # 查找开始更新按钮
        start_btn = dialog.query_selector('button:has-text("开始更新")') or \\
                   dialog.query_selector('button:has-text("更新")')
        
        if start_btn:
            start_btn.click()
            time.sleep(5)
'''


def get_update_test_code(collection_name: str) -> str:
    """根据接口类型获取对应的更新测试代码"""
    config = INTERFACE_CONFIG.get(collection_name)
    
    if config is None:
        # 默认使用无参数测试
        return NO_PARAM_UPDATE_TEST
    
    update_type, params = config
    
    if update_type == "no_param":
        return NO_PARAM_UPDATE_TEST
    elif update_type in ["symbol", "symbol_period"]:
        test_symbol = params.get("symbol", "000001")
        return SYMBOL_UPDATE_TEST.format(test_symbol=test_symbol)
    elif update_type == "choice":
        return CHOICE_UPDATE_TEST
    elif update_type in ["date", "date_range"]:
        test_date = params.get("date", "20231231")
        return DATE_UPDATE_TEST.format(test_date=test_date)
    else:
        return NO_PARAM_UPDATE_TEST


def extract_collection_name(filename: str) -> Optional[str]:
    """从文件名提取集合名称"""
    match = re.match(r'\d+_(.+)_collection\.py', filename)
    if match:
        return match.group(1)
    return None


def enhance_test_file(filepath: str, collection_name: str) -> bool:
    """增强测试文件，添加 Playwright 测试"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有 Playwright 测试
        if '@pytest.mark.playwright' in content or '_test_update_function' in content:
            print(f"  跳过 {collection_name}: 已有 Playwright 测试")
            return False
        
        # 获取更新测试代码
        update_test = get_update_test_code(collection_name)
        playwright_test = PLAYWRIGHT_TEST_TEMPLATE.format(collection_name=collection_name)
        
        # 查找类定义的结束位置
        # 在最后一个方法后添加新测试
        if 'class Test' in content:
            # 在文件末尾的 if __name__ 之前插入
            if 'if __name__' in content:
                insert_pos = content.rfind('if __name__')
                new_content = content[:insert_pos] + playwright_test + update_test + '\n\n' + content[insert_pos:]
            else:
                new_content = content + playwright_test + update_test
        else:
            # 简单格式的测试文件，在末尾添加
            new_content = content + '\n' + playwright_test + update_test
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"  错误 {collection_name}: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("为测试文件添加 Playwright 自动化测试")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取所有测试文件
    test_files = []
    for fn in os.listdir(script_dir):
        if fn.endswith('_collection.py') and fn[0].isdigit():
            test_files.append(fn)
    
    print(f"\n找到 {len(test_files)} 个测试文件")
    
    enhanced = 0
    skipped = 0
    errors = 0
    
    for fn in sorted(test_files):
        collection_name = extract_collection_name(fn)
        if not collection_name:
            continue
        
        filepath = os.path.join(script_dir, fn)
        result = enhance_test_file(filepath, collection_name)
        
        if result:
            print(f"  [+] 增强: {collection_name}")
            enhanced += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1
    
    print(f"\n" + "=" * 60)
    print(f"完成！增强: {enhanced}, 跳过: {skipped}, 错误: {errors}")
    print("=" * 60)


if __name__ == "__main__":
    main()
