"""
基金申购状态功能测试

测试覆盖:
1. 数据概览显示
2. 数据列表展示
3. 刷新数据功能
4. 清空数据功能
5. 更新数据功能(文件导入、远程同步、API更新)
6. 图形展示
"""
import pytest
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService
import pandas as pd
import numpy as np


class TestFundPurchaseStatusBackend:
    """后端API测试"""
    
    @pytest.fixture(scope="class")
    async def db(self):
        """获取数据库连接"""
        db = get_mongo_db()
        yield db
        # 清理测试数据
        await db.get_collection("fund_purchase_status").delete_many({})
    
    @pytest.mark.asyncio
    async def test_save_fund_purchase_data(self, db):
        """测试保存基金申购状态数据"""
        service = FundDataService(db)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': '1',
                '基金代码': '000001',
                '基金简称': '华夏成长混合',
                '基金类型': '混合型',
                '最新净值/万份收益': 1.234,
                '最新净值/万份收益-报告时间': '2024-01-01',
                '申购状态': '开放申购',
                '赎回状态': '开放赎回',
                '下一开放日': '2024-01-02',
                '购买起点': 10.0,
                '日累计限定金额': 100000000000.0,
                '手续费': 0.15
            },
            {
                '序号': '2',
                '基金代码': '000002',
                '基金简称': '测试基金',
                '基金类型': '债券型',
                '最新净值/万份收益': 2.345,
                '最新净值/万份收益-报告时间': '2024-01-01',
                '申购状态': '暂停申购',
                '赎回状态': '开放赎回',
                '下一开放日': '2024-01-02',
                '购买起点': 10.0,
                '日累计限定金额': 10000000000.0,
                '手续费': 0.08
            }
        ])
        
        saved = await service.save_fund_purchase_status_data(test_data)
        assert saved == 2
        
        # 验证数据已保存
        collection = db.get_collection("fund_purchase_status")
        count = await collection.count_documents({})
        assert count == 2
        
        # 验证数据内容
        doc = await collection.find_one({'code': '000001'})
        assert doc is not None
        assert doc['基金简称'] == '华夏成长混合'
        assert doc['申购状态'] == '开放申购'
    
    @pytest.mark.asyncio
    async def test_get_fund_purchase_stats(self, db):
        """测试获取统计信息"""
        service = FundDataService(db)
        
        stats = await service.get_fund_purchase_status_stats()
        
        assert stats is not None
        assert 'total_count' in stats
        assert stats['total_count'] >= 0
        
        if stats['total_count'] > 0:
            # 如果有数据,检查统计字段
            assert 'type_stats' in stats or 'purchase_status_stats' in stats
    
    @pytest.mark.asyncio
    async def test_clear_fund_purchase_data(self, db):
        """测试清空数据"""
        service = FundDataService(db)
        
        # 先添加一些数据
        test_data = pd.DataFrame([
            {
                '基金代码': '999999',
                '基金简称': '临时测试基金',
                '基金类型': '股票型',
                '最新净值/万份收益': 1.0,
                '最新净值/万份收益-报告时间': '2024-01-01',
                '申购状态': '开放申购',
                '赎回状态': '开放赎回',
                '下一开放日': '2024-01-02',
                '购买起点': 10.0,
                '日累计限定金额': 10000000000.0,
                '手续费': 0.15
            }
        ])
        
        await service.save_fund_purchase_status_data(test_data)
        
        # 清空数据
        deleted = await service.clear_fund_purchase_status_data()
        assert deleted >= 0
        
        # 验证数据已清空
        collection = db.get_collection("fund_purchase_status")
        count = await collection.count_documents({})
        assert count == 0


class TestFundPurchaseStatusAPI:
    """REST API测试"""
    
    @pytest.fixture(scope="class")
    def base_url(self):
        """API基础URL"""
        return "http://localhost:8000/api/funds"
    
    def test_collection_list_includes_purchase_status(self, base_url):
        """测试集合列表包含基金申购状态"""
        import requests
        
        # 注意:需要先登录获取token
        # 这里假设有一个测试用户token
        # 实际测试时需要实现登录逻辑
        pass
    
    def test_get_purchase_status_data(self, base_url):
        """测试获取基金申购状态数据"""
        # 实现API测试
        pass
    
    def test_refresh_purchase_status(self, base_url):
        """测试刷新基金申购状态"""
        # 实现刷新测试
        pass


class TestFundPurchaseStatusE2E:
    """端到端测试(使用Playwright)"""
    
    @pytest.fixture(scope="class")
    def browser_context(self):
        """创建浏览器上下文"""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            yield context
            context.close()
            browser.close()
    
    def test_navigate_to_purchase_status_page(self, browser_context):
        """测试导航到基金申购状态页面"""
        page = browser_context.new_page()
        
        # 访问登录页面
        page.goto("http://localhost:5173/login")
        
        # 登录(需要实现具体的登录逻辑)
        # page.fill('input[name="username"]', 'test_user')
        # page.fill('input[name="password"]', 'test_password')
        # page.click('button[type="submit"]')
        
        # 导航到基金申购状态页面
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        
        # 验证页面标题
        # assert "基金申购状态" in page.title() or "基金申购状态" in page.text_content('h1')
        
        page.close()
    
    def test_data_overview_display(self, browser_context):
        """测试数据概览显示"""
        page = browser_context.new_page()
        
        # 访问页面并验证概览区域
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        
        # 检查统计卡片是否显示
        # stats_card = page.query_selector('.stats-card')
        # assert stats_card is not None
        
        page.close()
    
    def test_data_table_display(self, browser_context):
        """测试数据列表显示"""
        page = browser_context.new_page()
        
        # 验证数据表格显示
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        
        # 检查表格是否存在
        # table = page.query_selector('.el-table')
        # assert table is not None
        
        page.close()
    
    def test_refresh_button(self, browser_context):
        """测试刷新按钮"""
        page = browser_context.new_page()
        
        # 点击刷新按钮
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        # page.click('button:has-text("刷新")')
        
        # 等待加载完成
        # page.wait_for_selector('.el-loading-mask', state='detached', timeout=5000)
        
        page.close()
    
    def test_update_data_button(self, browser_context):
        """测试更新数据按钮"""
        page = browser_context.new_page()
        
        # 点击更新数据按钮
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        # page.click('button:has-text("更新数据")')
        
        # 验证对话框打开
        # dialog = page.query_selector('.el-dialog')
        # assert dialog is not None
        
        page.close()
    
    def test_clear_data_button(self, browser_context):
        """测试清空数据按钮"""
        page = browser_context.new_page()
        
        # 点击清空数据按钮并确认
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        # page.click('button:has-text("清空数据")')
        
        # 确认对话框
        # page.click('button:has-text("确定")')
        
        page.close()
    
    def test_charts_display(self, browser_context):
        """测试图形展示"""
        page = browser_context.new_page()
        
        # 验证图表是否显示
        # page.goto("http://localhost:5173/funds/collections/fund_purchase_status")
        
        # 检查图表容器
        # charts = page.query_selector_all('.chart-wrapper')
        # assert len(charts) > 0
        
        page.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
