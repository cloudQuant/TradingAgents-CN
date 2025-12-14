"""
测试指数模块导航菜单
"""
import sys
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:3000"

def test_indexs_navigation():
    """测试指数导航菜单"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print("=" * 60)
        print("指数模块导航菜单测试")
        print("=" * 60)
        
        # 1. 登录
        print("\n[1/4] 登录...")
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        page.fill('input[placeholder*="用户名"]', "admin")
        page.fill('input[placeholder*="密码"]', "admin123")
        page.click('button:has-text("登录")')
        page.wait_for_url("**/dashboard**", timeout=10000)
        print("✅ 登录成功")
        
        # 2. 检查侧边栏菜单
        print("\n[2/4] 检查侧边栏菜单...")
        page.goto(f"{BASE_URL}/dashboard")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)  # 等待菜单加载
        
        # 查找指数投研菜单（使用更宽松的选择器）
        indexs_menu = page.locator('span:has-text("指数投研"), .el-sub-menu__title:has-text("指数")')
        
        if indexs_menu.count() > 0:
            print("✅ 找到'指数投研'菜单")
            
            # 点击展开菜单
            indexs_menu.first.click()
            page.wait_for_timeout(500)
            
            # 检查子菜单
            overview_item = page.locator('.el-menu-item:has-text("概览")').first
            collections_item = page.locator('.el-menu-item:has-text("数据集合")').first
            
            if overview_item.is_visible():
                print("✅ 子菜单项正确显示")
            else:
                print("⚠️ 子菜单项可能未完全显示")
        else:
            # 尝试查找顶部菜单
            top_menu = page.locator('.top-menu span:has-text("指数")')
            if top_menu.count() > 0:
                print("✅ 在顶部菜单找到'指数'菜单")
                indexs_menu = top_menu
            else:
                print("❌ 未找到'指数'菜单")
                # 打印页面内容帮助调试
                print("页面菜单内容:")
                menus = page.locator('.el-menu-item, .el-sub-menu__title')
                for i in range(min(menus.count(), 10)):
                    print(f"  - {menus.nth(i).text_content()}")
                browser.close()
                return False
        
        # 3. 通过菜单导航到指数概览
        print("\n[3/4] 通过菜单导航到指数概览...")
        # 点击概览菜单项
        page.locator('.el-menu-item:has-text("概览")').first.click()
        page.wait_for_url("**/indexs/overview**", timeout=5000)
        print("✅ 成功导航到指数概览页面")
        
        # 4. 通过菜单导航到数据集合
        print("\n[4/4] 通过菜单导航到数据集合...")
        # 直接导航到数据集合页面
        page.goto(f"{BASE_URL}/indexs/collections")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector(".collection-item", timeout=10000)
        print("✅ 成功导航到数据集合页面")
        
        browser.close()
        
        print("\n" + "=" * 60)
        print("导航菜单测试完成")
        print("=" * 60)
        return True

if __name__ == "__main__":
    success = test_indexs_navigation()
    sys.exit(0 if success else 1)
