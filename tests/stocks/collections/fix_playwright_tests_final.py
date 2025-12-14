"""
修复 Playwright 测试代码 - 最终版

策略：删除有问题的 Playwright 测试部分，重新生成正确格式的代码
"""
import os
import re
import ast


# 接口配置（从 add_playwright_tests.py 复制）
INTERFACE_CONFIG = {
    # 无参数接口
    "stock_sse_summary": ("no_param", {}),
    "stock_szse_summary": ("no_param", {}),
    "stock_szse_area_summary": ("no_param", {}),
    "stock_szse_sector_summary": ("no_param", {}),
    "stock_sse_deal_daily": ("no_param", {}),
    "stock_zh_a_spot_em": ("no_param", {}),
    "stock_sh_a_spot_em": ("no_param", {}),
    "stock_sz_a_spot_em": ("no_param", {}),
    "stock_bj_a_spot_em": ("no_param", {}),
    "stock_new_a_spot_em": ("no_param", {}),
    "stock_cy_a_spot_em": ("no_param", {}),
    "stock_kc_a_spot_em": ("no_param", {}),
    "stock_zh_b_spot_em": ("no_param", {}),
    "stock_us_spot_em": ("no_param", {}),
    "stock_hk_spot_em": ("no_param", {}),
    "stock_hot_rank_em": ("no_param", {}),
    "stock_hot_up_em": ("no_param", {}),
    "stock_hk_hot_rank_em": ("no_param", {}),
    "stock_board_change_em": ("no_param", {}),
    "stock_market_activity_legu": ("no_param", {}),
    
    # 需要股票代码的接口
    "stock_individual_info_em": ("symbol", {"symbol": "000001"}),
    "stock_individual_basic_info_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_bid_ask_em": ("symbol", {"symbol": "000001"}),
    "stock_inner_trade_xq": ("symbol", {"symbol": "SZ000001"}),
    "stock_hot_rank_detail_em": ("symbol", {"symbol": "000001"}),
    "stock_hk_hot_rank_detail_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_hot_rank_detail_realtime_em": ("symbol", {"symbol": "000001"}),
    "stock_hk_hot_rank_detail_realtime_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_hot_rank_latest_em": ("symbol", {"symbol": "000001"}),
    "stock_hk_hot_rank_latest_em": ("symbol_hk", {"symbol": "00700"}),
    "stock_hot_rank_relate_em": ("symbol", {"symbol": "000001"}),
    "stock_changes_em": ("symbol", {"symbol": "000001"}),
    
    # 需要板块名称的接口
    "stock_board_industry_cons_em": ("board", {"board": "小金属"}),
    "stock_board_industry_hist_em": ("board", {"board": "小金属"}),
    "stock_board_industry_hist_min_em": ("board", {"board": "小金属"}),
    
    # 需要日期的接口
    "stock_zt_pool_em": ("date", {"date": "20231215"}),
    "stock_zt_pool_previous_em": ("date", {"date": "20231215"}),
    "stock_zt_pool_strong_em": ("date", {"date": "20231215"}),
    "stock_zt_pool_sub_new_em": ("date", {"date": "20231215"}),
    "stock_zt_pool_zbgc_em": ("date", {"date": "20231215"}),
    "stock_zt_pool_dtgc_em": ("date", {"date": "20231215"}),
    
    # 雪球热度接口
    "stock_hot_follow_xq": ("no_param", {}),
    "stock_hot_tweet_xq": ("no_param", {}),
    "stock_hot_deal_xq": ("no_param", {}),
    
    # 互动问答接口
    "stock_irm_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_irm_ans_cninfo": ("symbol", {"symbol": "000001"}),
    "stock_sns_sseinfo": ("symbol", {"symbol": "600000"}),
    
    # 热搜接口
    "stock_hot_keyword_em": ("symbol", {"symbol": "000001"}),
    "stock_hot_search_baidu": ("date", {"date": "20231215"}),
    
    # 排名接口
    "stock_rank_cxfl_ths": ("no_param", {}),
    "stock_rank_cxsl_ths": ("no_param", {}),
    "stock_rank_xstp_ths": ("no_param", {}),
    "stock_rank_xxtp_ths": ("no_param", {}),
    "stock_rank_ljqs_ths": ("no_param", {}),
    "stock_rank_ljqd_ths": ("no_param", {}),
    "stock_rank_xzjp_ths": ("no_param", {}),
    
    # ESG 接口
    "stock_esg_rate_sina": ("no_param", {}),
    "stock_esg_msci_sina": ("no_param", {}),
    "stock_esg_rft_sina": ("no_param", {}),
    "stock_esg_zd_sina": ("no_param", {}),
    "stock_esg_hz_sina": ("no_param", {}),
}


def get_collection_name(filename: str) -> str:
    """从文件名提取集合名称"""
    # 007_stock_sse_summary_collection.py -> stock_sse_summary
    match = re.match(r'\d+_(.+)_collection\.py', filename)
    if match:
        return match.group(1)
    return ""


def get_interface_config(collection_name: str) -> tuple:
    """获取接口配置"""
    return INTERFACE_CONFIG.get(collection_name, ("no_param", {}))


def generate_playwright_test_class(collection_name: str) -> str:
    """生成类方法形式的 Playwright 测试代码"""
    update_type, params = get_interface_config(collection_name)
    
    # 根据更新类型生成不同的测试逻辑
    if update_type == "no_param":
        param_code = """
                # 无参数接口，直接点击开始更新
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)"""
    elif update_type == "symbol":
        symbol = params.get("symbol", "000001")
        param_code = f"""
                # 输入股票代码
                inp = dialog.query_selector('input[placeholder*="代码"]') or dialog.query_selector('input[type="text"]')
                if inp:
                    inp.fill("{symbol}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)"""
    elif update_type == "symbol_hk":
        symbol = params.get("symbol", "00700")
        param_code = f"""
                # 输入港股代码
                inp = dialog.query_selector('input[placeholder*="代码"]') or dialog.query_selector('input[type="text"]')
                if inp:
                    inp.fill("{symbol}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)"""
    elif update_type == "board":
        board = params.get("board", "小金属")
        param_code = f"""
                # 输入板块名称
                inp = dialog.query_selector('input[placeholder*="板块"]') or dialog.query_selector('input[type="text"]')
                if inp:
                    inp.fill("{board}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)"""
    elif update_type == "date":
        date = params.get("date", "20231215")
        param_code = f"""
                # 输入日期
                inp = dialog.query_selector('input[placeholder*="日期"]') or dialog.query_selector('.el-date-editor input')
                if inp:
                    inp.fill("{date}")
                    time.sleep(0.5)
                
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)"""
    else:
        param_code = """
                # 默认：直接点击开始更新
                start_btn = self._find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)"""
    
    return f'''
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
                {param_code}
                
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


def generate_playwright_test_function(collection_name: str) -> str:
    """生成函数形式的 Playwright 测试代码"""
    update_type, params = get_interface_config(collection_name)
    
    # 根据更新类型生成不同的测试逻辑
    if update_type == "no_param":
        param_code = """
            # 无参数接口，直接点击开始更新
            start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
            if start_btn:
                start_btn.click()
                time.sleep(5)"""
    elif update_type == "symbol":
        symbol = params.get("symbol", "000001")
        param_code = f"""
            # 输入股票代码
            inp = dialog.query_selector('input[placeholder*="代码"]') or dialog.query_selector('input[type="text"]')
            if inp:
                inp.fill("{symbol}")
                time.sleep(0.5)
            
            start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
            if start_btn:
                start_btn.click()
                time.sleep(5)"""
    elif update_type == "symbol_hk":
        symbol = params.get("symbol", "00700")
        param_code = f"""
            # 输入港股代码
            inp = dialog.query_selector('input[placeholder*="代码"]') or dialog.query_selector('input[type="text"]')
            if inp:
                inp.fill("{symbol}")
                time.sleep(0.5)
            
            start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
            if start_btn:
                start_btn.click()
                time.sleep(5)"""
    elif update_type == "board":
        board = params.get("board", "小金属")
        param_code = f"""
            # 输入板块名称
            inp = dialog.query_selector('input[placeholder*="板块"]') or dialog.query_selector('input[type="text"]')
            if inp:
                inp.fill("{board}")
                time.sleep(0.5)
            
            start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
            if start_btn:
                start_btn.click()
                time.sleep(5)"""
    elif update_type == "date":
        date = params.get("date", "20231215")
        param_code = f"""
            # 输入日期
            inp = dialog.query_selector('input[placeholder*="日期"]') or dialog.query_selector('.el-date-editor input')
            if inp:
                inp.fill("{date}")
                time.sleep(0.5)
            
            start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
            if start_btn:
                start_btn.click()
                time.sleep(5)"""
    else:
        param_code = """
            # 默认：直接点击开始更新
            start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
            if start_btn:
                start_btn.click()
                time.sleep(5)"""
    
    return f'''

    # ========== Playwright UI 自动化测试 ==========
    
@pytest.mark.playwright
def test_ui_update_data_flow():
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
            _do_login(page, frontend_url)
            page.goto(collection_url, wait_until='networkidle', timeout=30000)
            time.sleep(2)
            
            if "/login" in page.url:
                pytest.skip("需要登录")
            
            update_btn = _find_button(page, ["更新数据", "更新"])
            if not update_btn:
                pytest.skip("未找到更新按钮")
            
            update_btn.click()
            time.sleep(1.5)
            
            dialog = _find_dialog(page)
            if not dialog:
                pytest.fail("弹窗未出现")
            {param_code}
            
            _close_dialog(dialog)
            
        finally:
            browser.close()

def _do_login(page, frontend_url):
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

def _find_button(container, texts):
    for t in texts:
        b = container.query_selector(f'button:has-text("{{t}}")')
        if b and b.is_visible():
            return b
    return None

def _find_dialog(page):
    for s in ['.el-dialog', '[role="dialog"]', '.modal']:
        d = page.query_selector(s)
        if d and d.is_visible():
            return d
    return None

def _close_dialog(dialog):
    b = dialog.query_selector('button:has-text("关闭")') or dialog.query_selector('.el-dialog__close')
    if b:
        b.click()
'''


def check_syntax(filepath: str) -> tuple[bool, str]:
    """检查文件语法"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"


def fix_file(filepath: str, filename: str) -> tuple[bool, str]:
    """修复测试文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有 Playwright 测试
        if '@pytest.mark.playwright' not in content:
            return False, "no playwright"
        
        # 检查语法
        ok, err = check_syntax(filepath)
        if ok:
            return False, "already ok"
        
        collection_name = get_collection_name(filename)
        if not collection_name:
            return False, "cannot get collection name"
        
        # 判断是类还是函数形式
        is_class_based = 'class Test' in content
        
        # 删除现有的 Playwright 测试部分
        # 找到 "# ========== Playwright" 或 "@pytest.mark.playwright" 开始的位置
        patterns = [
            r'\n    # ========== 测试7：Playwright.*?(?=\nif __name__|$)',
            r'\n    # ========== Playwright UI.*?(?=\nif __name__|$)',
            r'\n    @pytest\.mark\.playwright.*?(?=\nif __name__|$)',
            r'\n# ========== Playwright UI.*?(?=\nif __name__|$)',
            r'\n@pytest\.mark\.playwright.*?(?=\nif __name__|$)',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 删除辅助函数
        helper_patterns = [
            r'\n    def _do_login\(.*?(?=\n    def |\nif __name__|$)',
            r'\n    def _find_button\(.*?(?=\n    def |\nif __name__|$)',
            r'\n    def _find_dialog\(.*?(?=\n    def |\nif __name__|$)',
            r'\n    def _close_dialog\(.*?(?=\n    def |\nif __name__|$)',
            r'\ndef _do_login\(.*?(?=\ndef |\nif __name__|$)',
            r'\ndef _find_button\(.*?(?=\ndef |\nif __name__|$)',
            r'\ndef _find_dialog\(.*?(?=\ndef |\nif __name__|$)',
            r'\ndef _close_dialog\(.*?(?=\ndef |\nif __name__|$)',
        ]
        
        for pattern in helper_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 清理多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 找到插入位置
        if is_class_based:
            # 在类的最后一个方法后面插入
            # 找到 "if __name__" 之前的位置
            if 'if __name__' in content:
                insert_pos = content.rfind('\nif __name__')
                new_code = generate_playwright_test_class(collection_name)
                content = content[:insert_pos] + new_code + content[insert_pos:]
            else:
                # 在文件末尾添加
                content = content.rstrip() + generate_playwright_test_class(collection_name) + '\n'
        else:
            # 函数形式
            if 'if __name__' in content:
                insert_pos = content.rfind('\nif __name__')
                new_code = generate_playwright_test_function(collection_name)
                content = content[:insert_pos] + new_code + content[insert_pos:]
            else:
                content = content.rstrip() + generate_playwright_test_function(collection_name) + '\n'
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 验证语法
        ok, err = check_syntax(filepath)
        if ok:
            return True, "fixed"
        else:
            return True, f"fixed but still has error: {err}"
    
    except Exception as e:
        return False, f"error: {e}"


def main():
    print("=" * 60)
    print("修复 Playwright 测试代码 - 最终版")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    test_files = [f for f in os.listdir(script_dir) 
                  if f.endswith('_collection.py') and f[0].isdigit()]
    
    # 先统计有问题的文件
    print("\n检查语法错误...")
    error_files = []
    for fn in sorted(test_files):
        filepath = os.path.join(script_dir, fn)
        ok, err = check_syntax(filepath)
        if not ok:
            error_files.append((fn, err))
    
    print(f"发现 {len(error_files)} 个有语法错误的文件")
    
    # 修复文件
    print("\n开始修复...")
    fixed = 0
    still_error = []
    
    for fn, _ in error_files:
        filepath = os.path.join(script_dir, fn)
        changed, msg = fix_file(filepath, fn)
        if changed:
            if "still has error" in msg:
                still_error.append((fn, msg))
                print(f"  [!] {fn}: {msg}")
            else:
                print(f"  [+] {fn}")
                fixed += 1
    
    print(f"\n修复了 {fixed} 个文件")
    
    if still_error:
        print(f"\n仍有 {len(still_error)} 个文件有错误:")
        for fn, msg in still_error[:10]:
            print(f"  - {fn}: {msg}")
    
    # 最终验证
    print("\n最终验证...")
    final_errors = []
    for fn in sorted(test_files):
        filepath = os.path.join(script_dir, fn)
        ok, err = check_syntax(filepath)
        if not ok:
            final_errors.append((fn, err))
    
    if final_errors:
        print(f"仍有 {len(final_errors)} 个文件有语法错误")
    else:
        print("所有文件语法检查通过！")


if __name__ == "__main__":
    main()
