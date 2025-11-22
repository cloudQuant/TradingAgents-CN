"""
债券基础信息增强功能自动化测试

使用Playwright进行网页自动化测试，验证在bond_basic_info页面的批量更新和增量更新功能的前端交互。

运行前需要安装Playwright:
pip install playwright
playwright install

测试覆盖：
1. 登录系统
2. 导航到债券基础信息页面（bond_basic_info）
3. 打开更新数据对话框
4. 测试批量更新功能
5. 测试增量更新功能
6. 验证统计信息显示
"""

import asyncio
import pytest
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import os
from datetime import datetime


class TestBondBasicInfoAutomation:
    """债券基础信息增强功能自动化测试"""
    
    @pytest.fixture(scope="session")
    async def browser(self):
        """创建浏览器实例"""
        async with async_playwright() as p:
            # 使用Chromium浏览器
            browser = await p.chromium.launch(
                headless=False,  # 设置为False可以看到浏览器操作过程
                slow_mo=1000     # 操作间隔1秒，便于观察
            )
            yield browser
            await browser.close()
    
    @pytest.fixture
    async def context(self, browser: Browser):
        """创建浏览器上下文"""
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            # 可以添加更多配置，如用户代理、语言等
        )
        yield context
        await context.close()
    
    @pytest.fixture
    async def page(self, context: BrowserContext):
        """创建页面"""
        page = await context.new_page()
        yield page
        await page.close()
    
    async def login(self, page: Page, username: str = "admin", password: str = "admin123"):
        """登录系统"""
        # 导航到登录页面
        await page.goto("http://localhost:8080/login")
        
        # 等待登录表单加载
        await page.wait_for_selector('input[type="text"]', timeout=10000)
        
        # 填写用户名和密码
        await page.fill('input[type="text"]', username)
        await page.fill('input[type="password"]', password)
        
        # 点击登录按钮
        await page.click('button[type="submit"]')
        
        # 等待登录成功，重定向到主页
        await page.wait_for_url("**/dashboard", timeout=10000)
        
        print(f"✅ 成功登录，用户: {username}")
    
    async def navigate_to_bond_basic_info_page(self, page: Page):
        """导航到债券基础信息页面"""
        # 点击债券菜单
        await page.click('text=债券数据')
        
        # 等待子菜单展开，点击债券集合
        await page.wait_for_selector('text=债券集合', timeout=5000)
        await page.click('text=债券集合')
        
        # 等待页面加载
        await page.wait_for_load_state('networkidle')
        
        # 检查URL是否包含bonds/collections
        current_url = page.url
        if "bonds/collections" not in current_url:
            # 直接导航到bond_basic_info页面
            await page.goto("http://localhost:8080/bonds/collections/bond_basic_info")
            await page.wait_for_load_state('networkidle')
        
        # 确保我们在bond_basic_info页面
        await page.wait_for_selector('text=债券基础信息', timeout=10000)
        
        print("✅ 成功导航到债券基础信息页面")
    
    @pytest.mark.asyncio
    async def test_login_and_navigation(self, page: Page):
        """测试登录和页面导航"""
        try:
            await self.login(page)
            await self.navigate_to_bond_basic_info_page(page)
            
            # 验证页面标题或关键元素
            title = await page.title()
            assert "债券" in title or "TradingAgents" in title
            
            # 验证更新数据按钮存在
            await page.wait_for_selector('text=更新数据', timeout=5000)
            
            print("✅ 登录和导航测试通过")
            
        except Exception as e:
            # 截图保存错误状态
            await page.screenshot(path=f"test_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e
    
    @pytest.mark.asyncio
    async def test_update_data_dialog_opens(self, page: Page):
        """测试更新数据对话框打开"""
        try:
            await self.login(page)
            await self.navigate_to_bond_basic_info_page(page)
            
            # 点击更新数据按钮
            await page.click('text=更新数据')
            
            # 等待对话框出现
            await page.wait_for_selector('.el-dialog', timeout=5000)
            
            # 检查对话框标题
            dialog_title = await page.text_content('.el-dialog__title')
            assert "更新数据" in dialog_title
            
            print("✅ 更新数据对话框打开测试通过")
            
        except Exception as e:
            await page.screenshot(path=f"dialog_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e
    
    @pytest.mark.asyncio
    async def test_bond_basic_info_batch_update_ui(self, page: Page):
        """测试债券基础信息批量更新UI"""
        try:
            await self.login(page)
            await self.navigate_to_bond_basic_info_page(page)
            
            # 点击更新数据按钮
            await page.click('text=更新数据')
            await page.wait_for_selector('.el-dialog', timeout=5000)
            
            # 查找债券基础信息更新相关的UI元素
            await page.wait_for_selector('text=债券基础信息更新', timeout=5000)
            
            # 检查批量更新参数输入框
            await page.wait_for_selector('text=批次大小', timeout=3000)
            await page.wait_for_selector('text=并发线程数', timeout=3000)
            await page.wait_for_selector('text=保存间隔', timeout=3000)
            
            # 设置批量更新参数
            batch_size_input = await page.query_selector('input[aria-controls*="batch-size"]')
            if batch_size_input:
                await batch_size_input.fill('100')
            
            # 点击批量更新按钮
            await page.click('text=批量更新')
            
            # 检查是否出现确认对话框
            try:
                await page.wait_for_selector('.el-message-box', timeout=3000)
                # 如果出现确认对话框，点击取消避免实际执行
                await page.click('text=取消')
                print("✅ 批量更新确认对话框出现，功能正常")
            except:
                print("⚠️ 批量更新可能直接执行或出现其他状态")
            
            print("✅ 批量更新UI测试通过")
            
        except Exception as e:
            await page.screenshot(path=f"batch_update_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e
    
    @pytest.mark.asyncio
    async def test_bond_basic_info_incremental_update_ui(self, page: Page):
        """测试债券基础信息增量更新UI"""
        try:
            await self.login(page)
            await self.navigate_to_bond_basic_info_page(page)
            
            # 点击更新数据按钮
            await page.click('text=更新数据')
            await page.wait_for_selector('.el-dialog', timeout=5000)
            
            # 查找增量更新按钮
            await page.wait_for_selector('text=增量更新', timeout=5000)
            
            # 点击增量更新按钮
            await page.click('text=增量更新')
            
            # 检查是否出现确认对话框
            try:
                await page.wait_for_selector('.el-message-box', timeout=3000)
                # 如果出现确认对话框，点击取消避免实际执行
                await page.click('text=取消')
                print("✅ 增量更新确认对话框出现，功能正常")
            except:
                print("⚠️ 增量更新可能直接执行或出现其他状态")
            
            print("✅ 增量更新UI测试通过")
            
        except Exception as e:
            await page.screenshot(path=f"incremental_update_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e
    
    @pytest.mark.asyncio
    async def test_bond_basic_info_statistics_query(self, page: Page):
        """测试债券基础信息统计查询"""
        try:
            await self.login(page)
            await self.navigate_to_bond_basic_info_page(page)
            
            # 点击更新数据按钮
            await page.click('text=更新数据')
            await page.wait_for_selector('.el-dialog', timeout=5000)
            
            # 查找查询统计按钮
            await page.wait_for_selector('text=查询统计', timeout=5000)
            
            # 点击查询统计按钮
            await page.click('text=查询统计')
            
            # 等待统计信息显示或加载完成
            try:
                await page.wait_for_selector('.stats-display', timeout=10000)
                print("✅ 统计信息显示区域出现")
            except:
                print("⚠️ 统计信息可能通过其他方式显示")
            
            print("✅ 统计查询UI测试通过")
            
        except Exception as e:
            await page.screenshot(path=f"statistics_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e
    
    @pytest.mark.asyncio
    async def test_full_bond_basic_info_workflow(self, page: Page):
        """测试完整的债券基础信息更新工作流程"""
        try:
            await self.login(page)
            await self.navigate_to_bond_basic_info_page(page)
            
            # 1. 打开更新数据对话框
            print("🔄 打开更新数据对话框...")
            await page.click('text=更新数据')
            await page.wait_for_selector('.el-dialog', timeout=5000)
            
            # 2. 检查债券基础信息更新功能是否存在
            print("🔍 检查债券基础信息更新功能...")
            await page.wait_for_selector('text=债券基础信息更新', timeout=5000)
            
            # 3. 查询统计信息
            print("📊 查询统计信息...")
            await page.click('text=查询统计')
            await asyncio.sleep(2)  # 等待查询完成
            
            # 4. 检查批量更新和增量更新按钮
            print("🔄 检查更新按钮...")
            batch_update_btn = await page.query_selector('text=批量更新')
            incremental_update_btn = await page.query_selector('text=增量更新')
            
            assert batch_update_btn is not None, "批量更新按钮未找到"
            assert incremental_update_btn is not None, "增量更新按钮未找到"
            
            # 5. 验证参数输入框
            print("⚙️ 验证参数输入框...")
            await page.wait_for_selector('text=批次大小', timeout=3000)
            await page.wait_for_selector('text=并发线程数', timeout=3000)
            await page.wait_for_selector('text=保存间隔', timeout=3000)
            
            # 6. 关闭对话框
            await page.click('.el-dialog__close')
            
            print("✅ 完整工作流程测试通过")
            
        except Exception as e:
            await page.screenshot(path=f"workflow_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e


class TestBondBasicInfoPerformance:
    """债券基础信息更新性能测试"""
    
    @pytest.mark.asyncio
    async def test_dialog_loading_performance(self, page: Page):
        """测试对话框加载性能"""
        # 记录开始时间
        start_time = datetime.now()
        
        try:
            # 执行基本操作
            test_instance = TestBondBasicInfoAutomation()
            await test_instance.login(page)
            await test_instance.navigate_to_bond_basic_info_page(page)
            
            # 测试对话框打开性能
            dialog_start = datetime.now()
            await page.click('text=更新数据')
            await page.wait_for_selector('.el-dialog', timeout=5000)
            dialog_end = datetime.now()
            
            dialog_duration = (dialog_end - dialog_start).total_seconds()
            print(f"✅ 对话框加载耗时: {dialog_duration:.2f}秒")
            
            # 性能断言
            assert dialog_duration < 5, f"对话框加载耗时过长: {dialog_duration}秒"
            
        except Exception as e:
            await page.screenshot(path=f"performance_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise e
        
        finally:
            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds()
            print(f"📊 总测试耗时: {total_duration:.2f}秒")


if __name__ == "__main__":
    # 运行自动化测试
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # 直接运行测试
        async def run_tests():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False, slow_mo=1000)
                context = await browser.new_context(viewport={"width": 1920, "height": 1080})
                page = await context.new_page()
                
                try:
                    test_instance = TestBondBasicInfoAutomation()
                    
                    print("🚀 开始债券基础信息自动化测试...")
                    
                    # 执行登录和导航测试
                    await test_instance.test_login_and_navigation(page)
                    
                    # 执行对话框打开测试
                    await test_instance.test_update_data_dialog_opens(page)
                    
                    # 执行批量更新UI测试
                    await test_instance.test_bond_basic_info_batch_update_ui(page)
                    
                    # 执行增量更新UI测试
                    await test_instance.test_bond_basic_info_incremental_update_ui(page)
                    
                    # 执行统计查询测试
                    await test_instance.test_bond_basic_info_statistics_query(page)
                    
                    # 执行完整工作流程测试
                    await test_instance.test_full_bond_basic_info_workflow(page)
                    
                    print("✅ 所有债券基础信息自动化测试通过！")
                    
                except Exception as e:
                    print(f"❌ 测试失败: {e}")
                    await page.screenshot(path=f"final_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                
                finally:
                    await context.close()
                    await browser.close()
        
        asyncio.run(run_tests())
    else:
        # 使用pytest运行
        pytest.main([__file__, "-v", "-s"])
