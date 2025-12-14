"""
批量测试数据集合

测试所有数据集合的 UI 更新功能，记录结果
"""
import os
import sys
import time
import json
import re
from datetime import datetime


def get_all_collections():
    """获取所有集合名称"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [f for f in os.listdir(script_dir) 
                  if f.endswith('_collection.py') and f[0].isdigit()]
    
    collections = []
    for fn in sorted(test_files):
        match = re.match(r'(\d+)_(.+)_collection\.py', fn)
        if match:
            collections.append({
                'id': match.group(1),
                'name': match.group(2),
                'file': fn
            })
    return collections


def test_collection(page, collection_name: str, frontend_url: str) -> dict:
    """测试单个集合"""
    result = {
        'name': collection_name,
        'status': 'unknown',
        'has_data': False,
        'has_update_button': False,
        'has_dialog': False,
        'update_success': None,
        'error': None
    }
    
    try:
        collection_url = f"{frontend_url}/stocks/collections/{collection_name}"
        page.goto(collection_url, wait_until='networkidle', timeout=30000)
        time.sleep(1)
        
        # 检查是否需要登录
        if "/login" in page.url:
            result['status'] = 'need_login'
            return result
        
        # 检查是否有数据
        empty_el = page.query_selector('.el-empty') or page.query_selector('[class*="empty"]')
        result['has_data'] = not (empty_el and empty_el.is_visible())
        
        # 查找更新按钮
        update_btn = None
        for text in ["更新数据", "更新", "刷新", "Update"]:
            btn = page.query_selector(f'button:has-text("{text}")')
            if btn and btn.is_visible():
                update_btn = btn
                result['has_update_button'] = True
                break
        
        if not update_btn:
            result['status'] = 'no_update_button'
            return result
        
        # 点击更新按钮
        update_btn.click()
        time.sleep(1.5)
        
        # 检查弹窗
        dialog = None
        for selector in ['.el-dialog', '.el-drawer', '[role="dialog"]', '.modal']:
            d = page.query_selector(selector)
            if d and d.is_visible():
                dialog = d
                result['has_dialog'] = True
                break
        
        if dialog:
            # 点击开始更新
            start_btn = None
            for text in ["开始更新", "更新", "确定", "Start"]:
                btn = dialog.query_selector(f'button:has-text("{text}")')
                if btn and btn.is_visible():
                    start_btn = btn
                    break
            
            if start_btn:
                start_btn.click()
                time.sleep(3)
                
                # 检查结果
                error_msg = page.query_selector('.el-message--error')
                if error_msg and error_msg.is_visible():
                    result['update_success'] = False
                    result['error'] = error_msg.inner_text()[:100]
                else:
                    result['update_success'] = True
            
            # 关闭弹窗
            close_btn = dialog.query_selector('button:has-text("关闭")') or \
                       dialog.query_selector('.el-dialog__close')
            if close_btn:
                close_btn.click()
        else:
            # 没有弹窗，等待更新完成
            time.sleep(3)
            error_msg = page.query_selector('.el-message--error')
            if error_msg and error_msg.is_visible():
                result['update_success'] = False
                result['error'] = error_msg.inner_text()[:100]
            else:
                result['update_success'] = True
        
        result['status'] = 'tested'
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)[:100]
    
    return result


def do_login(page, frontend_url: str) -> bool:
    """执行登录"""
    try:
        page.goto(f"{frontend_url}/login", timeout=10000)
        time.sleep(1)
        
        username_input = page.query_selector('input[type="text"]')
        if username_input:
            username_input.fill("admin")
            password_input = page.query_selector('input[type="password"]')
            if password_input:
                password_input.fill("admin123")
            login_btn = page.query_selector('button:has-text("登录")')
            if login_btn:
                login_btn.click()
                page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                return True
    except:
        pass
    return False


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误: Playwright 未安装")
        print("请运行: pip install playwright && playwright install chromium")
        return
    
    frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
    collections = get_all_collections()
    
    print("=" * 70)
    print("批量测试数据集合")
    print("=" * 70)
    print(f"前端地址: {frontend_url}")
    print(f"集合数量: {len(collections)}")
    print()
    
    # 限制测试数量
    max_tests = int(os.getenv("MAX_TESTS", "20"))
    collections = collections[:max_tests]
    print(f"本次测试: {len(collections)} 个集合")
    print()
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 登录
        print("登录中...")
        if do_login(page, frontend_url):
            print("登录成功\n")
        else:
            print("登录失败\n")
        
        # 测试每个集合
        for i, col in enumerate(collections, 1):
            name = col['name']
            print(f"[{i}/{len(collections)}] 测试 {name}...", end=" ", flush=True)
            
            result = test_collection(page, name, frontend_url)
            results.append(result)
            
            # 输出结果
            if result['status'] == 'tested':
                if result['update_success']:
                    print(f"✓ 更新成功" + (" (有数据)" if result['has_data'] else " (无数据)"))
                elif result['update_success'] is False:
                    print(f"✗ 更新失败: {result['error']}")
                else:
                    print(f"? 未知结果")
            elif result['status'] == 'no_update_button':
                print("⚠ 无更新按钮")
            elif result['status'] == 'need_login':
                print("⚠ 需要登录")
            else:
                print(f"✗ 错误: {result['error']}")
        
        browser.close()
    
    # 统计结果
    print()
    print("=" * 70)
    print("测试结果统计")
    print("=" * 70)
    
    success = sum(1 for r in results if r['update_success'] is True)
    failed = sum(1 for r in results if r['update_success'] is False)
    no_button = sum(1 for r in results if r['status'] == 'no_update_button')
    errors = sum(1 for r in results if r['status'] == 'error')
    has_data = sum(1 for r in results if r['has_data'])
    
    print(f"  更新成功: {success}")
    print(f"  更新失败: {failed}")
    print(f"  无更新按钮: {no_button}")
    print(f"  测试错误: {errors}")
    print(f"  有数据: {has_data}")
    
    # 保存结果
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_file = os.path.join(script_dir, f"batch_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告: {report_file}")
    
    # 输出失败的集合
    if failed > 0:
        print()
        print("=" * 70)
        print("更新失败的集合")
        print("=" * 70)
        for r in results:
            if r['update_success'] is False:
                print(f"  - {r['name']}: {r['error']}")


if __name__ == "__main__":
    main()
