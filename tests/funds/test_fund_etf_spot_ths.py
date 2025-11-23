"""
同花顺ETF基金实时行情测试用例
测试集合: fund_etf_spot_ths
"""
import pytest
import pandas as pd
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService


class TestFundETFSpotThsBackend:
    """测试后端数据服务"""
    
    @pytest.fixture
    async def data_service(self):
        """获取数据服务实例"""
        db = get_mongo_db()
        service = FundDataService(db)
        yield service
        # 清理测试数据
        await service.clear_fund_etf_spot_ths_data()
    
    @pytest.mark.asyncio
    async def test_save_fund_etf_spot_ths_data(self, data_service):
        """测试保存同花顺ETF实时行情数据"""
        # 创建测试数据
        test_data = pd.DataFrame({
            '序号': [1, 2],
            '基金代码': ['159691', '588200'],
            '基金名称': ['高股息ETF港股', '嘉实上证科创板芯片ETF'],
            '当前-单位净值': [1.2345, 0.9876],
            '当前-累计净值': [1.2345, 0.9876],
            '前一日-单位净值': [1.2300, 0.9800],
            '前一日-累计净值': [1.2300, 0.9800],
            '增长值': [0.0045, 0.0076],
            '增长率': [0.37, 0.78],
            '赎回状态': ['开放赎回', '开放赎回'],
            '申购状态': ['开放申购', '开放申购'],
            '最新-交易日': ['2024-06-20', '2024-06-20'],
            '最新-单位净值': [1.2345, 0.9876],
            '最新-累计净值': [1.2345, 0.9876],
            '基金类型': ['股票型', '股票型'],
            '查询日期': ['2024-06-20', '2024-06-20']
        })
        
        # 保存数据
        count = await data_service.save_fund_etf_spot_ths_data(test_data)
        
        # 验证
        assert count == 2
        
        # 验证数据已保存
        stats = await data_service.get_fund_etf_spot_ths_stats()
        assert stats['total_count'] == 2
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_spot_ths_stats(self, data_service):
        """测试获取统计信息"""
        # 创建测试数据
        test_data = pd.DataFrame({
            '序号': [1, 2, 3],
            '基金代码': ['159691', '588200', '513530'],
            '基金名称': ['高股息ETF港股', '嘉实上证科创板芯片ETF', '港股红利'],
            '当前-单位净值': [1.2345, 0.9876, 1.3692],
            '当前-累计净值': [1.2345, 0.9876, 1.3692],
            '前一日-单位净值': [1.2300, 0.9900, 1.3600],
            '前一日-累计净值': [1.2300, 0.9900, 1.3600],
            '增长值': [0.0045, -0.0024, 0.0092],
            '增长率': [0.37, -0.24, 0.68],
            '赎回状态': ['开放赎回', '开放赎回', '暂停赎回'],
            '申购状态': ['开放申购', '开放申购', '开放申购'],
            '最新-交易日': ['2024-06-20', '2024-06-20', '2024-06-20'],
            '最新-单位净值': [1.2345, 0.9876, 1.3692],
            '最新-累计净值': [1.2345, 0.9876, 1.3692],
            '基金类型': ['股票型', '股票型', '股票型'],
            '查询日期': ['2024-06-20', '2024-06-20', '2024-06-20']
        })
        
        await data_service.save_fund_etf_spot_ths_data(test_data)
        
        # 获取统计
        stats = await data_service.get_fund_etf_spot_ths_stats()
        
        # 验证
        assert stats['total_count'] == 3
        assert stats['rise_count'] == 2  # 两只上涨
        assert stats['fall_count'] == 1  # 一只下跌
        assert 'type_stats' in stats
        assert 'top_gainers' in stats
        assert 'top_losers' in stats
    
    @pytest.mark.asyncio
    async def test_clear_fund_etf_spot_ths_data(self, data_service):
        """测试清空数据"""
        # 创建测试数据
        test_data = pd.DataFrame({
            '序号': [1],
            '基金代码': ['159691'],
            '基金名称': ['高股息ETF港股'],
            '当前-单位净值': [1.2345],
            '当前-累计净值': [1.2345],
            '前一日-单位净值': [1.2300],
            '前一日-累计净值': [1.2300],
            '增长值': [0.0045],
            '增长率': [0.37],
            '赎回状态': ['开放赎回'],
            '申购状态': ['开放申购'],
            '最新-交易日': ['2024-06-20'],
            '最新-单位净值': [1.2345],
            '最新-累计净值': [1.2345],
            '基金类型': ['股票型'],
            '查询日期': ['2024-06-20']
        })
        
        await data_service.save_fund_etf_spot_ths_data(test_data)
        
        # 清空数据
        count = await data_service.clear_fund_etf_spot_ths_data()
        
        # 验证
        assert count == 1
        
        # 验证数据已清空
        stats = await data_service.get_fund_etf_spot_ths_stats()
        assert stats['total_count'] == 0


class TestFundETFSpotThsAPI:
    """测试API接口"""
    
    @pytest.mark.asyncio
    async def test_list_collections(self):
        """测试集合列表中包含fund_etf_spot_ths"""
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 需要登录token
            # 这里假设已有认证机制
            response = await client.get("/api/funds/collections")
            assert response.status_code == 200
            data = response.json()
            
            # 验证包含fund_etf_spot_ths
            collection_names = [c['name'] for c in data['data']]
            assert 'fund_etf_spot_ths' in collection_names
    
    @pytest.mark.asyncio
    async def test_get_data(self):
        """测试获取数据"""
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/funds/collections/fund_etf_spot_ths?page=1&page_size=10")
            assert response.status_code == 200
            data = response.json()
            assert 'data' in data
            assert 'items' in data['data']
    
    @pytest.mark.asyncio
    async def test_get_stats(self):
        """测试获取统计信息"""
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/funds/collections/fund_etf_spot_ths/stats")
            assert response.status_code == 200
            data = response.json()
            assert 'data' in data
            assert 'total_count' in data['data']
    
    @pytest.mark.asyncio
    async def test_refresh_and_clear(self):
        """测试刷新和清空功能"""
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 测试刷新
            response = await client.post("/api/funds/collections/fund_etf_spot_ths/refresh", json={})
            assert response.status_code == 200
            
            # 测试清空
            response = await client.delete("/api/funds/collections/fund_etf_spot_ths/clear")
            assert response.status_code == 200


class TestFundETFSpotThsE2E:
    """端到端测试（Playwright）"""
    
    @pytest.fixture
    def browser_context(self):
        """创建浏览器上下文"""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            yield page
            context.close()
            browser.close()
    
    def test_navigation(self, browser_context):
        """测试页面导航"""
        page = browser_context
        
        # 访问登录页
        page.goto("http://localhost:5173/login")
        
        # 登录（需要根据实际情况调整）
        page.fill('input[type="text"]', 'admin')
        page.fill('input[type="password"]', 'admin123')
        page.click('button[type="submit"]')
        
        # 等待登录完成
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # 导航到基金数据集合
        page.goto("http://localhost:5173/funds/collections/fund_etf_spot_ths")
        
        # 验证页面标题
        assert page.title() != ""
    
    def test_data_overview(self, browser_context):
        """测试数据概览显示"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_etf_spot_ths")
        
        # 验证统计卡片存在
        assert page.locator('.stat-card').count() > 0
    
    def test_data_table(self, browser_context):
        """测试数据表格"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_etf_spot_ths")
        
        # 验证表格存在
        assert page.locator('.el-table').is_visible()
    
    def test_buttons(self, browser_context):
        """测试按钮功能"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_etf_spot_ths")
        
        # 验证刷新按钮
        assert page.locator('button:has-text("刷新")').is_visible()
        
        # 验证更新数据按钮
        assert page.locator('button:has-text("更新数据")').is_visible()
        
        # 验证清空数据按钮
        assert page.locator('button:has-text("清空数据")').is_visible()
    
    def test_charts(self, browser_context):
        """测试图表显示"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_etf_spot_ths")
        
        # 验证图表区域存在
        chart_exists = page.locator('.analysis-tabs').is_visible()
        assert chart_exists or page.locator('.el-empty').is_visible()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
