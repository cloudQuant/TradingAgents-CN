"""
LOF基金实时行情-东财测试用例
测试集合: fund_lof_spot_em
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


class TestFundLOFSpotEmBackend:
    """测试后端数据服务"""
    
    @pytest.fixture
    async def data_service(self):
        """获取数据服务实例"""
        db = get_mongo_db()
        service = FundDataService(db)
        yield service
        # 清理测试数据
        await service.clear_fund_lof_spot_data()
    
    @pytest.mark.asyncio
    async def test_save_fund_lof_spot_data(self, data_service):
        """测试保存LOF基金实时行情数据"""
        # 创建测试数据
        test_data = pd.DataFrame({
            '代码': ['166009', '161811'],
            '名称': ['中欧动力LOF', '沪深300LOF银华'],
            '最新价': [3.123, 0.859],
            '涨跌额': [0.114, 0.029],
            '涨跌幅': [3.79, 3.61],
            '成交量': [1000000.0, 500000.0],
            '成交额': [3123000.0, 429500.0],
            '开盘价': [2.954, 0.830],
            '最高价': [3.229, 0.880],
            '最低价': [2.954, 0.830],
            '昨收': [3.009, 0.830],
            '换手率': [0.64, 0.04],
            '流通市值': [6716805, 7986026],
            '总市值': [6716805, 7986026]
        })
        
        # 保存数据
        count = await data_service.save_fund_lof_spot_data(test_data)
        
        # 验证
        assert count == 2
        
        # 验证数据已保存
        stats = await data_service.get_fund_lof_spot_stats()
        assert stats['total_count'] == 2
    
    @pytest.mark.asyncio
    async def test_get_fund_lof_spot_stats(self, data_service):
        """测试获取统计信息"""
        # 创建测试数据
        test_data = pd.DataFrame({
            '代码': ['166009', '161811', '160807'],
            '名称': ['中欧动力LOF', '沪深300LOF银华', '长盛沪深300LOF'],
            '最新价': [3.123, 0.859, 1.454],
            '涨跌额': [0.114, 0.029, 0.033],
            '涨跌幅': [3.79, 3.61, 2.32],
            '成交量': [1000000.0, 500000.0, 800000.0],
            '成交额': [3123000.0, 429500.0, 1163200.0],
            '开盘价': [2.954, 0.830, 1.421],
            '最高价': [3.229, 0.880, 1.470],
            '最低价': [2.954, 0.830, 1.421],
            '昨收': [3.009, 0.830, 1.421],
            '换手率': [0.64, 0.04, 0.56],
            '流通市值': [6716805, 7986026, 3979752],
            '总市值': [6716805, 7986026, 3979752]
        })
        
        await data_service.save_fund_lof_spot_data(test_data)
        
        # 获取统计
        stats = await data_service.get_fund_lof_spot_stats()
        
        # 验证
        assert stats['total_count'] == 3
        assert stats['rise_count'] == 3  # 三只都上涨
        assert stats['fall_count'] == 0
        assert 'top_volume' in stats
        assert 'top_gainers' in stats
    
    @pytest.mark.asyncio
    async def test_clear_fund_lof_spot_data(self, data_service):
        """测试清空数据"""
        # 创建测试数据
        test_data = pd.DataFrame({
            '代码': ['166009'],
            '名称': ['中欧动力LOF'],
            '最新价': [3.123],
            '涨跌额': [0.114],
            '涨跌幅': [3.79],
            '成交量': [1000000.0],
            '成交额': [3123000.0],
            '开盘价': [2.954],
            '最高价': [3.229],
            '最低价': [2.954],
            '昨收': [3.009],
            '换手率': [0.64],
            '流通市值': [6716805],
            '总市值': [6716805]
        })
        
        await data_service.save_fund_lof_spot_data(test_data)
        
        # 清空数据
        count = await data_service.clear_fund_lof_spot_data()
        
        # 验证
        assert count == 1
        
        # 验证数据已清空
        stats = await data_service.get_fund_lof_spot_stats()
        assert stats['total_count'] == 0


class TestFundLOFSpotEmAPI:
    """测试API接口"""
    
    @pytest.mark.asyncio
    async def test_list_collections(self):
        """测试集合列表中包含fund_lof_spot_em"""
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/funds/collections")
            assert response.status_code == 200
            data = response.json()
            
            # 验证包含fund_lof_spot_em
            collection_names = [c['name'] for c in data['data']]
            assert 'fund_lof_spot_em' in collection_names
    
    @pytest.mark.asyncio
    async def test_get_data(self):
        """测试获取数据"""
        from httpx import AsyncClient
        from app.main import app
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/funds/collections/fund_lof_spot_em?page=1&page_size=10")
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
            response = await client.get("/api/funds/collections/fund_lof_spot_em/stats")
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
            response = await client.post("/api/funds/collections/fund_lof_spot_em/refresh", json={})
            assert response.status_code == 200
            
            # 测试清空
            response = await client.delete("/api/funds/collections/fund_lof_spot_em/clear")
            assert response.status_code == 200


class TestFundLOFSpotEmE2E:
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
        
        # 登录
        page.fill('input[type="text"]', 'admin')
        page.fill('input[type="password"]', 'admin123')
        page.click('button[type="submit"]')
        
        # 等待登录完成
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # 导航到基金数据集合
        page.goto("http://localhost:5173/funds/collections/fund_lof_spot_em")
        
        # 验证页面标题
        assert page.title() != ""
    
    def test_data_overview(self, browser_context):
        """测试数据概览显示"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_lof_spot_em")
        
        # 验证统计卡片存在
        assert page.locator('.stat-card').count() > 0
    
    def test_data_table(self, browser_context):
        """测试数据表格"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_lof_spot_em")
        
        # 验证表格存在
        assert page.locator('.el-table').is_visible()
    
    def test_buttons(self, browser_context):
        """测试按钮功能"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_lof_spot_em")
        
        # 验证刷新按钮
        assert page.locator('button:has-text("刷新")').is_visible()
        
        # 验证更新数据按钮
        assert page.locator('button:has-text("更新数据")').is_visible()
        
        # 验证清空数据按钮
        assert page.locator('button:has-text("清空数据")').is_visible()
    
    def test_charts(self, browser_context):
        """测试图表显示"""
        page = browser_context
        page.goto("http://localhost:5173/funds/collections/fund_lof_spot_em")
        
        # 验证图表区域存在
        chart_exists = page.locator('.analysis-tabs').is_visible()
        assert chart_exists or page.locator('.el-empty').is_visible()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
