"""
单个数据集合测试脚本

使用 Playwright 测试单个数据集合的更新功能
用法: python test_single_collection.py <collection_name>
"""
import os
import sys
import time
import argparse


def test_collection_ui(collection_name: str, headless: bool = True):
    """使用 Playwright 测试单个集合的 UI 更新功能"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误: Playwright 未安装")
        print("请运行: pip install playwright && playwright install chromium")
        return False
    
    frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
    collection_url = f"{frontend_url}/stocks/collections/{collection_name}"
    
    print(f"\n{'='*60}")
    print(f"测试集合: {collection_name}")
    print(f"页面地址: {collection_url}")
    print(f"{'='*60}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        try:
            # 1. 尝试登录
            print("\n[1] 尝试登录...")
            login_url = f"{frontend_url}/login"
            page.goto(login_url, timeout=10000)
            time.sleep(1)
            
            username_input = page.query_selector('input[type="text"]')
            if username_input:
                username_input.fill("admin")
                password_input = page.query_selector('input[type="password"]')
                if password_input:
                    password_input.fill("admin123")
                # 查找登录按钮
                login_btn = page.query_selector('button:has-text("登录")') or \
                           page.query_selector('button[type="submit"]') or \
                           page.query_selector('button[type="button"]')
                if login_btn:
                    login_btn.click()
                    try:
                        page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                        print("    登录成功")
                    except:
                        print("    登录可能失败，继续测试...")
            time.sleep(1)
            
            # 2. 访问集合页面
            print(f"\n[2] 访问集合页面...")
            page.goto(collection_url, wait_until='networkidle', timeout=30000)
            time.sleep(2)
            
            # 检查页面状态
            if "/login" in page.url:
                print("    ✗ 需要登录才能访问")
                return False
            
            if page.query_selector('.el-empty') or page.query_selector('[class*="empty"]'):
                print("    ⚠ 页面显示为空状态")
            
            # 截图保存
            screenshot_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            page.screenshot(path=f"{screenshot_dir}/{collection_name}_page.png")
            print(f"    截图已保存: {screenshot_dir}/{collection_name}_page.png")
            
            # 3. 查找更新按钮
            print(f"\n[3] 查找更新数据按钮...")
            update_btn = None
            for text in ["更新数据", "更新", "Update", "刷新"]:
                btn = page.query_selector(f'button:has-text("{text}")')
                if btn and btn.is_visible():
                    update_btn = btn
                    print(f"    找到按钮: {text}")
                    break
            
            if not update_btn:
                # 尝试其他选择器
                for selector in ['.update-button', '[data-test="update-button"]', '.el-button--primary']:
                    btn = page.query_selector(selector)
                    if btn and btn.is_visible():
                        update_btn = btn
                        print(f"    找到按钮 (选择器: {selector})")
                        break
            
            if not update_btn:
                print("    ✗ 未找到更新按钮")
                # 打印页面上所有按钮
                buttons = page.query_selector_all('button')
                print(f"    页面上的按钮 ({len(buttons)} 个):")
                for i, btn in enumerate(buttons[:10]):
                    text = btn.inner_text().strip()[:30]
                    print(f"      {i+1}. {text}")
                return False
            
            # 4. 点击更新按钮
            print(f"\n[4] 点击更新按钮...")
            update_btn.click()
            time.sleep(2)
            
            # 5. 检查弹窗
            print(f"\n[5] 检查弹窗...")
            dialog = None
            for selector in ['.el-dialog', '.el-drawer', '[role="dialog"]', '.modal', '.dialog']:
                d = page.query_selector(selector)
                if d and d.is_visible():
                    dialog = d
                    print(f"    找到弹窗 (选择器: {selector})")
                    break
            
            if not dialog:
                print("    ⚠ 未找到弹窗，可能直接开始更新")
                time.sleep(5)
            else:
                # 截图弹窗
                page.screenshot(path=f"{screenshot_dir}/{collection_name}_dialog.png")
                print(f"    弹窗截图: {screenshot_dir}/{collection_name}_dialog.png")
                
                # 6. 查找并填写参数
                print(f"\n[6] 检查参数输入...")
                inputs = dialog.query_selector_all('input')
                print(f"    发现 {len(inputs)} 个输入框")
                
                for inp in inputs:
                    placeholder = inp.get_attribute('placeholder') or ''
                    input_type = inp.get_attribute('type') or 'text'
                    print(f"      - 类型: {input_type}, 占位符: {placeholder}")
                
                # 7. 点击开始更新
                print(f"\n[7] 点击开始更新...")
                start_btn = None
                for text in ["开始更新", "更新", "确定", "Start", "OK"]:
                    btn = dialog.query_selector(f'button:has-text("{text}")')
                    if btn and btn.is_visible():
                        start_btn = btn
                        print(f"    找到按钮: {text}")
                        break
                
                if start_btn:
                    start_btn.click()
                    print("    已点击开始更新")
                    time.sleep(5)
                    
                    # 检查错误消息
                    error_msg = page.query_selector('.el-message--error')
                    if error_msg and error_msg.is_visible():
                        error_text = error_msg.inner_text()
                        print(f"    ✗ 错误: {error_text}")
                    
                    success_msg = page.query_selector('.el-message--success')
                    if success_msg and success_msg.is_visible():
                        success_text = success_msg.inner_text()
                        print(f"    ✓ 成功: {success_text}")
                else:
                    print("    ✗ 未找到开始更新按钮")
                
                # 8. 关闭弹窗
                print(f"\n[8] 关闭弹窗...")
                close_btn = dialog.query_selector('button:has-text("关闭")') or \
                           dialog.query_selector('button:has-text("取消")') or \
                           dialog.query_selector('.el-dialog__close') or \
                           dialog.query_selector('[aria-label="Close"]')
                if close_btn:
                    close_btn.click()
                    print("    已关闭弹窗")
            
            # 最终截图
            time.sleep(2)
            page.screenshot(path=f"{screenshot_dir}/{collection_name}_final.png")
            print(f"\n最终截图: {screenshot_dir}/{collection_name}_final.png")
            
            print(f"\n{'='*60}")
            print("测试完成")
            print(f"{'='*60}")
            return True
            
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(description='测试单个数据集合')
    parser.add_argument('collection', help='集合名称，如 stock_sse_summary')
    parser.add_argument('--show', action='store_true', help='显示浏览器窗口')
    args = parser.parse_args()
    
    success = test_collection_ui(args.collection, headless=not args.show)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
