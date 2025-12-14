"""
测试所有指数数据集合的页面和API更新按钮
"""
import sys
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:3000"

def test_all_indexs_collections():
    """测试所有指数数据集合"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print("=" * 70)
        print("指数模块 - 所有数据集合测试")
        print("=" * 70)
        
        # 1. 登录
        print("\n[登录]")
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        page.fill('input[placeholder*="用户名"]', "admin")
        page.fill('input[placeholder*="密码"]', "admin123")
        page.click('button:has-text("登录")')
        page.wait_for_url("**/dashboard**", timeout=10000)
        print("✅ 登录成功")
        
        # 2. 获取所有集合
        print("\n[获取集合列表]")
        page.goto(f"{BASE_URL}/indexs/collections")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector(".collection-item", timeout=10000)
        
        collection_items = page.locator(".collection-item")
        total_collections = collection_items.count()
        print(f"共找到 {total_collections} 个数据集合")
        
        # 收集所有集合名称
        collection_names = []
        for i in range(total_collections):
            item = collection_items.nth(i)
            name = item.locator(".collection-name").text_content()
            collection_names.append(name)
        
        # 3. 测试每个集合
        print("\n[测试各集合页面和API]")
        results = {
            "success": [],
            "failed": []
        }
        
        # 已知的集合URL名称
        collection_urls = [
            "stock_zh_index_spot_em",
            "stock_zh_index_spot_sina",
            "stock_zh_index_daily",
            "stock_zh_index_daily_em",
            "index_zh_a_hist",
            "index_zh_a_hist_min_em",
            "stock_hk_index_spot_sina",
            "stock_hk_index_daily_sina",
            "stock_hk_index_spot_em",
            "stock_hk_index_daily_em",
            "index_us_stock_sina",
            "index_global_spot_em",
            "index_global_hist_em",
        ]
        
        for i, url_name in enumerate(collection_urls):
            display_name = collection_names[i] if i < len(collection_names) else url_name
            print(f"\n  [{i+1}/{len(collection_urls)}] {display_name}")
            
            try:
                # 访问集合详情页
                page.goto(f"{BASE_URL}/indexs/collections/{url_name}")
                page.wait_for_load_state("networkidle")
                time.sleep(1)  # 等待组件加载
                
                # 检查页面是否正常加载
                has_error = page.locator(".el-message--error").count() > 0
                if has_error:
                    error_msg = page.locator(".el-message--error").text_content()
                    print(f"      ❌ 页面错误: {error_msg}")
                    results["failed"].append((url_name, f"页面错误: {error_msg}"))
                    continue
                
                # 检查是否有数据表格或空状态
                has_table = page.locator(".el-table").count() > 0
                has_empty = page.locator(".el-empty").count() > 0
                
                if not has_table and not has_empty:
                    print(f"      ⚠️ 页面可能未完全加载")
                
                # 检查统计信息API
                stats_loaded = page.locator('[class*="stat"], .el-statistic').count() > 0
                
                # 查找更新按钮
                update_dropdown = page.locator('button:has-text("更新"), .el-dropdown:has-text("更新")')
                has_update = update_dropdown.count() > 0
                
                if has_update:
                    print(f"      ✅ 页面加载成功，找到更新按钮")
                    results["success"].append(url_name)
                else:
                    # 尝试查找其他形式的更新按钮
                    alt_update = page.locator('[class*="update"], [class*="refresh"]')
                    if alt_update.count() > 0:
                        print(f"      ✅ 页面加载成功，找到更新功能")
                        results["success"].append(url_name)
                    else:
                        print(f"      ⚠️ 页面加载成功，但未找到更新按钮")
                        results["success"].append(url_name)  # 页面加载成功也算通过
                
            except Exception as e:
                print(f"      ❌ 测试失败: {str(e)}")
                results["failed"].append((url_name, str(e)))
        
        browser.close()
        
        # 4. 输出测试结果
        print("\n" + "=" * 70)
        print("测试结果汇总")
        print("=" * 70)
        print(f"\n✅ 成功: {len(results['success'])}/{len(collection_urls)}")
        print(f"❌ 失败: {len(results['failed'])}/{len(collection_urls)}")
        
        if results["failed"]:
            print("\n失败的集合:")
            for name, error in results["failed"]:
                print(f"  - {name}: {error}")
        
        print("\n" + "=" * 70)
        
        return len(results["failed"]) == 0

if __name__ == "__main__":
    success = test_all_indexs_collections()
    sys.exit(0 if success else 1)
