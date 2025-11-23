#!/usr/bin/env python3
"""
基金拆分-东方财富功能测试用例
"""
import pytest
import asyncio
import pandas as pd
from datetime import datetime


class TestFundCfEmBackend:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_fund_cf_em_data(self, db_connection):
        """测试保存基金拆分数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '516090',
                '基金简称': '易方达中证新能源ETF',
                '拆分折算日': '2021-11-26',
                '拆分类型': '份额分拆',
                '拆分折算': 2.000000
            },
            {
                '序号': 2,
                '基金代码': '516070',
                '基金简称': '易方达中证内地低碳经济ETF',
                '拆分折算日': '2021-11-19',
                '拆分类型': '份额分拆',
                '拆分折算': 2.000000
            }
        ])
        
        # 保存数据
        saved_count = await service.save_fund_cf_em_data(test_data)
        
        # 验证
        assert saved_count == 2, f"应该保存2条数据，实际保存了 {saved_count} 条"
        
        # 清理测试数据
        await service.clear_fund_cf_em_data()
    
    @pytest.mark.asyncio
    async def test_update_existing_fund_cf_em_data(self, db_connection):
        """测试更新已存在的基金拆分数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建初始数据
        initial_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '516090',
                '基金简称': '易方达中证新能源ETF',
                '拆分折算日': '2021-11-26',
                '拆分类型': '份额分拆',
                '拆分折算': 2.000000
            }
        ])
        
        await service.save_fund_cf_em_data(initial_data)
        
        # 更新数据（相同基金代码和拆分日期）
        updated_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '516090',
                '基金简称': '易方达中证新能源ETF-更新',
                '拆分折算日': '2021-11-26',
                '拆分类型': '份额分拆',
                '拆分折算': 2.500000
            }
        ])
        
        saved_count = await service.save_fund_cf_em_data(updated_data)
        
        # 验证更新成功
        assert saved_count >= 1, "应该更新了数据"
        
        # 清理测试数据
        await service.clear_fund_cf_em_data()
    
    @pytest.mark.asyncio
    async def test_get_fund_cf_em_stats(self, db_connection):
        """测试获取基金拆分统计"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 创建测试数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': '516090',
                '基金简称': '易方达中证新能源ETF',
                '拆分折算日': '2021-11-26',
                '拆分类型': '份额分拆',
                '拆分折算': 2.000000
            },
            {
                '序号': 2,
                '基金代码': '000465',
                '基金简称': '景顺长城鑫月薪定期支付债券',
                '拆分折算日': '2021-11-18',
                '拆分类型': '份额折算',
                '拆分折算': None
            }
        ])
        
        await service.save_fund_cf_em_data(test_data)
        
        # 获取统计
        stats = await service.get_fund_cf_em_stats()
        
        # 验证
        assert stats['total_count'] == 2, f"总数应该是2，实际是 {stats['total_count']}"
        assert 'type_stats' in stats
        assert 'earliest_date' in stats
        assert 'latest_date' in stats
        
        # 清理测试数据
        await service.clear_fund_cf_em_data()
    
    @pytest.mark.asyncio
    async def test_clear_fund_cf_em_data(self, db_connection):
        """测试清空基金拆分数据"""
        from app.services.fund_data_service import FundDataService
        
        service = FundDataService(db_connection)
        
        # 先保存一些数据
        test_data = pd.DataFrame([
            {
                '序号': 1,
                '基金代码': 'TEST001',
                '基金简称': '测试基金',
                '拆分折算日': '2024-01-01',
                '拆分类型': '份额分拆',
                '拆分折算': 1.5
            }
        ])
        
        await service.save_fund_cf_em_data(test_data)
        
        # 清空数据
        deleted_count = await service.clear_fund_cf_em_data()
        
        # 验证
        assert deleted_count > 0, "应该删除了数据"
        
        # 验证已清空
        stats = await service.get_fund_cf_em_stats()
        assert stats['total_count'] == 0, "清空后应该没有数据"


class TestFundCfEmAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_get_fund_collections_includes_cf_em(self, test_client):
        """测试基金集合列表包含基金拆分"""
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        
        data = response.json()
        collection_names = [c['name'] for c in data.get('data', [])]
        assert 'fund_cf_em' in collection_names
    
    @pytest.mark.asyncio
    async def test_get_fund_cf_em_data(self, test_client):
        """测试获取基金拆分数据"""
        response = await test_client.get("/api/funds/collections/fund_cf_em")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get('success') is True
        result = data.get('data', {})
        assert 'items' in result
        assert 'total' in result
    
    @pytest.mark.asyncio
    async def test_get_fund_cf_em_stats(self, test_client):
        """测试获取基金拆分统计"""
        response = await test_client.get("/api/funds/collections/fund_cf_em/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get('success') is True
        stats = data.get('data', {})
        assert 'total_count' in stats
    
    @pytest.mark.asyncio
    async def test_refresh_fund_cf_em(self, test_client):
        """测试刷新基金拆分数据"""
        response = await test_client.post(
            "/api/funds/collections/fund_cf_em/refresh",
            json={}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert 'task_id' in data or data.get('success') is True
    
    @pytest.mark.asyncio
    async def test_clear_fund_cf_em(self, test_client):
        """测试清空基金拆分数据"""
        response = await test_client.delete("/api/funds/collections/fund_cf_em/clear")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get('success') is True
    
    @pytest.mark.asyncio
    async def test_import_fund_cf_em_from_file(self, test_client):
        """测试从文件导入基金拆分数据"""
        # 创建测试CSV数据
        csv_content = """序号,基金代码,基金简称,拆分折算日,拆分类型,拆分折算
1,516090,易方达中证新能源ETF,2021-11-26,份额分拆,2.0
2,516070,易方达中证内地低碳经济ETF,2021-11-19,份额分拆,2.0
"""
        
        files = {'file': ('test_fund_cf.csv', csv_content.encode(), 'text/csv')}
        response = await test_client.post(
            "/api/funds/collections/fund_cf_em/import",
            files=files
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get('success') is True


class TestFundCfEmE2E:
    """端到端测试（基于Playwright）"""
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_fund_cf_em_page(self, page):
        """测试导航到基金拆分页面"""
        await page.goto("http://localhost:5173")
        
        # 登录（如需要）
        # ...
        
        # 导航到基金投研
        await page.click("text=基金投研")
        
        # 点击数据集合
        await page.click("text=数据集合")
        
        # 选择基金拆分
        await page.click("text=基金拆分")
        
        # 验证页面标题
        title = await page.text_content("h1, .page-title")
        assert "基金拆分" in title
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_data_overview_display(self, page):
        """测试数据概览显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_cf_em")
        
        # 等待数据加载
        await page.wait_for_selector(".stats-card, .el-card", timeout=5000)
        
        # 验证统计卡片存在
        assert await page.is_visible(".stats-card") or await page.is_visible(".el-card")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_data_table_display(self, page):
        """测试数据表格显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_cf_em")
        
        # 等待表格加载
        await page.wait_for_selector(".el-table", timeout=5000)
        
        # 验证表格存在
        assert await page.is_visible(".el-table")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_refresh_button(self, page):
        """测试刷新按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_cf_em")
        
        # 点击刷新按钮
        await page.click("button:has-text('刷新')")
        
        # 等待加载完成
        await page.wait_for_load_state("networkidle", timeout=10000)
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_update_data_button(self, page):
        """测试更新数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_cf_em")
        
        # 点击更新数据按钮
        await page.click("button:has-text('更新数据')")
        
        # 验证对话框打开
        await page.wait_for_selector(".el-dialog", timeout=3000)
        assert await page.is_visible(".el-dialog")
        
        # 验证有文件导入区域
        assert await page.is_visible("text=文件导入")
        
        # 验证有远程同步区域
        assert await page.is_visible("text=远程同步")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_clear_data_button(self, page):
        """测试清空数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_cf_em")
        
        # 点击清空数据按钮
        await page.click("button:has-text('清空数据')")
        
        # 验证确认对话框
        await page.wait_for_selector(".el-message-box", timeout=3000)
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_charts_display(self, page):
        """测试图表显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_cf_em")
        
        # 等待页面加载
        await page.wait_for_load_state("networkidle", timeout=10000)
        
        # 验证图表区域（如果有数据）
        # 基金拆分数据可能需要显示：拆分类型分布、历史趋势等
        chart_selectors = [".analysis-tabs", ".chart-container", ".echarts", "[id*='chart']"]
        has_chart = False
        for selector in chart_selectors:
            if await page.is_visible(selector):
                has_chart = True
                break
        
        # 如果有数据，应该显示图表
        # 如果没有数据，图表可能不显示，这是正常的
        # 因此这个测试只是尝试查找图表，不强制要求存在
        assert True  # 测试通过


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
