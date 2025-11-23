#!/usr/bin/env python3
"""
ETF基金实时行情功能测试用例
"""
import pytest
import asyncio
import pandas as pd
from datetime import datetime


class TestFundETFSpotBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_fund_etf_spot_data(self, db_connection):
        """测试保存ETF基金实时行情数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '代码': '520890',
                '名称': '港股通红利低波ETF',
                '最新价': 1.234,
                'IOPV实时估值': 1.235,
                '基金折价率': -0.08,
                '涨跌额': 0.012,
                '涨跌幅': 0.98,
                '成交量': 1234567.0,
                '成交额': 15234567.0,
                '开盘价': 1.220,
                '最高价': 1.240,
                '最低价': 1.210,
                '昨收': 1.222,
                '换手率': 2.5,
                '量比': 1.2,
                '委比': 0.5,
                '外盘': 567890.0,
                '内盘': 456789.0,
                '主力净流入-净额': 1234567.0,
                '主力净流入-净占比': 12.5,
                '超大单净流入-净额': 567890.0,
                '超大单净流入-净占比': 5.7,
                '大单净流入-净额': 666777.0,
                '大单净流入-净占比': 6.8,
                '中单净流入-净额': -123456.0,
                '中单净流入-净占比': -1.2,
                '小单净流入-净额': -1111111.0,
                '小单净流入-净占比': -11.3,
                '现手': 1234,
                '买一': 1.233,
                '卖一': 1.235,
                '最新份额': 1234567890.0,
                '流通市值': 1520000000,
                '总市值': 1520000000,
                '数据日期': '2024-12-26',
                '更新时间': '2024-12-26 16:11:57+08:00'
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_etf_spot_data(test_data)
        
        # 验证
        assert saved_count == 1, f"应该保存1条数据，实际保存了 {saved_count} 条"
        
        # 清理测试数据
        await service.clear_fund_etf_spot_data()
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_spot_stats(self, db_connection):
        """测试获取ETF基金实时行情统计"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '代码': '520890',
                '名称': '港股通红利低波ETF',
                '最新价': 1.234,
                '涨跌幅': 0.98,
                '成交额': 15234567.0,
                '数据日期': '2024-12-26',
                '更新时间': '2024-12-26 16:11:57+08:00'
            },
            {
                '代码': '159331',
                '名称': '红利港股ETF',
                '最新价': 2.345,
                '涨跌幅': -1.23,
                '成交额': 25234567.0,
                '数据日期': '2024-12-26',
                '更新时间': '2024-12-26 15:34:48+08:00'
            }
        ])
        
        await service.save_fund_etf_spot_data(test_data)
        
        # 获取统计
        stats = await service.get_fund_etf_spot_stats()
        
        # 验证
        assert stats['total_count'] == 2, f"总数应该是2，实际是 {stats['total_count']}"
        assert 'rise_count' in stats
        assert 'fall_count' in stats
        assert 'latest_date' in stats
        
        # 清理测试数据
        await service.clear_fund_etf_spot_data()
    
    @pytest.mark.asyncio
    async def test_clear_fund_etf_spot_data(self, db_connection):
        """测试清空ETF基金实时行情数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 先保存一些数据
        test_data = pd.DataFrame([
            {
                '代码': 'TEST001',
                '名称': '测试ETF',
                '最新价': 1.0,
                '数据日期': '2024-12-26',
                '更新时间': '2024-12-26 16:11:57+08:00'
            }
        ])
        
        await service.save_fund_etf_spot_data(test_data)
        
        # 清空数据
        deleted_count = await service.clear_fund_etf_spot_data()
        
        # 验证
        assert deleted_count > 0, "应该删除了数据"
        
        # 验证已清空
        stats = await service.get_fund_etf_spot_stats()
        assert stats['total_count'] == 0, "清空后应该没有数据"


class TestFundETFSpotAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_get_fund_collections_includes_etf_spot(self, test_client):
        """测试基金集合列表包含ETF实时行情"""
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        
        data = response.json()
        collection_names = [c['name'] for c in data]
        assert 'fund_etf_spot_em' in collection_names
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_spot_data(self, test_client):
        """测试获取ETF实时行情数据"""
        response = await test_client.get("/api/funds/collections/fund_etf_spot_em")
        assert response.status_code == 200
        
        data = response.json()
        assert 'items' in data
        assert 'total' in data
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_spot_stats(self, test_client):
        """测试获取ETF实时行情统计"""
        response = await test_client.get("/api/funds/collections/fund_etf_spot_em/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert 'total_count' in data
    
    @pytest.mark.asyncio
    async def test_refresh_fund_etf_spot(self, test_client):
        """测试刷新ETF实时行情数据"""
        response = await test_client.post(
            "/api/funds/collections/fund_etf_spot_em/refresh",
            json={}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert 'task_id' in data
    
    @pytest.mark.asyncio
    async def test_clear_fund_etf_spot(self, test_client):
        """测试清空ETF实时行情数据"""
        response = await test_client.delete("/api/funds/collections/fund_etf_spot_em/clear")
        assert response.status_code == 200


class TestFundETFSpotE2E:
    """端到端测试（基于Playwright）"""
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_etf_spot_page(self, page):
        """测试导航到ETF实时行情页面"""
        await page.goto("http://localhost:5173")
        
        # 登录（如需要）
        # ...
        
        # 导航到基金投研
        await page.click("text=基金投研")
        
        # 点击数据集合
        await page.click("text=数据集合")
        
        # 选择ETF基金实时行情
        await page.click("text=ETF基金实时行情")
        
        # 验证页面标题
        title = await page.text_content("h1")
        assert "ETF基金实时行情" in title
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_data_overview_display(self, page):
        """测试数据概览显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_spot_em")
        
        # 等待数据加载
        await page.wait_for_selector(".stats-card")
        
        # 验证统计卡片存在
        assert await page.is_visible(".stats-card")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_data_table_display(self, page):
        """测试数据表格显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_spot_em")
        
        # 等待表格加载
        await page.wait_for_selector(".el-table")
        
        # 验证表格存在
        assert await page.is_visible(".el-table")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_refresh_button(self, page):
        """测试刷新按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_spot_em")
        
        # 点击刷新按钮
        await page.click("button:has-text('刷新')")
        
        # 等待加载完成
        await page.wait_for_load_state("networkidle")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_update_data_button(self, page):
        """测试更新数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_spot_em")
        
        # 点击更新数据按钮
        await page.click("button:has-text('更新数据')")
        
        # 验证对话框打开
        await page.wait_for_selector(".el-dialog")
        assert await page.is_visible(".el-dialog")
        
        # 验证有文件导入区域
        assert await page.is_visible("text=文件导入")
        
        # 验证有远程同步区域
        assert await page.is_visible("text=远程同步")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_clear_data_button(self, page):
        """测试清空数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_spot_em")
        
        # 点击清空数据按钮
        await page.click("button:has-text('清空数据')")
        
        # 验证确认对话框
        await page.wait_for_selector(".el-message-box")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_charts_display(self, page):
        """测试图表显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_spot_em")
        
        # 等待图表加载
        await page.wait_for_selector(".analysis-tabs", timeout=5000)
        
        # 验证图表标签页存在
        if await page.is_visible(".analysis-tabs"):
            assert True
        else:
            # 如果没有数据，可能不显示图表
            pass


@pytest.fixture
async def db_connection():
    """数据库连接fixture"""
    from app.core.database import get_mongo_db
    db = get_mongo_db()
    yield db


@pytest.fixture
async def test_client():
    """测试客户端fixture"""
    from httpx import AsyncClient
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def page():
    """Playwright页面fixture"""
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        yield page
        await browser.close()
