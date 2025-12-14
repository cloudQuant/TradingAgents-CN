"""
测试指数模块前端页面
使用 Playwright 进行端到端测试
"""
import sys
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://localhost:3000"

def test_indexs_frontend():
    """测试指数模块前端页面"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print("=" * 60)
        print("指数模块前端测试")
        print("=" * 60)
        
        # 1. 登录
        print("\n[1/5] 登录...")
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        
        # 填写登录表单
        page.fill('input[placeholder*="用户名"]', "admin")
        page.fill('input[placeholder*="密码"]', "admin123")
        page.click('button:has-text("登录")')
        
        # 等待登录完成（跳转到dashboard或其他页面）
        page.wait_for_url("**/dashboard**", timeout=10000)
        print("✅ 登录成功")
        
        # 2. 访问指数概览页面
        print("\n[2/5] 访问指数概览页面...")
        page.goto(f"{BASE_URL}/indexs/overview")
        page.wait_for_load_state("networkidle")
        
        # 检查页面标题
        title = page.locator("h1").first
        expect(title).to_contain_text("指数概览")
        print("✅ 指数概览页面加载成功")
        
        # 3. 访问指数数据集合列表页面
        print("\n[3/5] 访问指数数据集合列表页面...")
        page.goto(f"{BASE_URL}/indexs/collections")
        page.wait_for_load_state("networkidle")
        
        # 等待集合列表加载
        page.wait_for_selector(".collection-item", timeout=10000)
        
        # 检查集合数量
        collection_items = page.locator(".collection-item")
        count = collection_items.count()
        print(f"✅ 找到 {count} 个数据集合")
        
        if count == 0:
            print("❌ 未找到任何数据集合")
            browser.close()
            return False
        
        # 4. 访问第一个集合详情页面
        print("\n[4/5] 访问集合详情页面...")
        first_collection = collection_items.first
        first_collection.click()
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)  # 等待页面完全加载
        
        # 检查页面是否有数据表格或空状态
        has_table = page.locator(".el-table").count() > 0
        has_empty = page.locator(".el-empty").count() > 0
        
        if has_table or has_empty:
            print("✅ 集合详情页面加载成功")
        else:
            print("⚠️ 集合详情页面可能未完全加载")
        
        # 5. 测试API更新按钮
        print("\n[5/5] 测试API更新按钮...")
        # 查找更新按钮
        update_button = page.locator('button:has-text("API更新"), button:has-text("更新")')
        if update_button.count() > 0:
            print("✅ 找到API更新按钮")
        else:
            print("⚠️ 未找到API更新按钮（可能在下拉菜单中）")
        
        browser.close()
        
        print("\n" + "=" * 60)
        print("前端测试完成")
        print("=" * 60)
        return True

if __name__ == "__main__":
    success = test_indexs_frontend()
    sys.exit(0 if success else 1)
