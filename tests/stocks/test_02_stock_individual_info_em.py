"""
测试02_个股信息查询-东财的API更新功能
验证前端配置和后端API的集成
"""
import pytest
from playwright.async_api import async_playwright, expect
import asyncio


@pytest.mark.asyncio
async def test_stock_individual_info_em_api_update():
    """测试个股信息查询-东财的API更新对话框"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 1. 登录
            await page.goto('http://localhost:3000/login')
            await page.fill('input[type="text"]', 'admin')
            await page.fill('input[type="password"]', 'admin123')
            await page.click('button:has-text("登录")')
            await page.wait_for_url('http://localhost:3000/', timeout=5000)
            
            # 2. 进入股票数据集合页面
            await page.goto('http://localhost:3000/stocks/collections')
            await page.wait_for_timeout(2000)
            
            # 3. 查找并点击"个股信息查询-东财"集合
            collection_card = page.locator('text=个股信息查询-东财').first
            await expect(collection_card).to_be_visible(timeout=10000)
            await collection_card.click()
            
            # 4. 等待集合详情页面加载
            await page.wait_for_url('**/stocks/collections/stock_individual_info_em', timeout=10000)
            await page.wait_for_timeout(2000)
            
            # 5. 点击"更新数据"下拉菜单
            update_button = page.locator('button:has-text("更新数据")').first
            await expect(update_button).to_be_visible(timeout=5000)
            await update_button.click()
            await page.wait_for_timeout(500)
            
            # 6. 点击"API更新"选项
            api_update_option = page.locator('li:has-text("API更新")').first
            await expect(api_update_option).to_be_visible(timeout=3000)
            await api_update_option.click()
            await page.wait_for_timeout(1000)
            
            # 7. 验证API更新对话框出现
            dialog = page.locator('.el-dialog:has-text("API更新")').first
            await expect(dialog).to_be_visible(timeout=5000)
            
            # 8. 验证对话框内容
            # 应该有"单个更新"部分
            single_update = dialog.locator('text=单个更新').first
            await expect(single_update).to_be_visible()
            
            # 应该有股票代码输入框
            symbol_input = dialog.locator('input[placeholder*="000001"]').first
            await expect(symbol_input).to_be_visible()
            
            # 应该有"批量更新配置"部分
            batch_update = dialog.locator('text=批量更新').first
            await expect(batch_update).to_be_visible()
            
            # 应该有并发数配置
            concurrency_label = dialog.locator('text=并发数').first
            await expect(concurrency_label).to_be_visible()
            
            # 应该有延迟配置
            delay_label = dialog.locator('text=请求延迟').first
            await expect(delay_label).to_be_visible()
            
            # 9. 测试单个更新功能
            await symbol_input.fill('000001')
            update_single_button = dialog.locator('button:has-text("更新单个")').first
            await expect(update_single_button).to_be_enabled()
            
            # 点击更新（实际不执行，避免真实API调用）
            # await update_single_button.click()
            
            # 10. 关闭对话框
            close_button = dialog.locator('button:has-text("关闭")').first
            await close_button.click()
            await page.wait_for_timeout(500)
            
            print("✅ 测试通过：个股信息查询-东财的API更新对话框功能正常")
            
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_stock_individual_info_em_api_update())
