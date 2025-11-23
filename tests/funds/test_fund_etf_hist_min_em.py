#!/usr/bin/env python3
"""ETF基金分时行情-东财 测试用例

测试内容：
1. 后端数据服务（保存 / 统计 / 清空）
2. API 接口（集合列表 / 数据 / 统计 / 刷新 / 清空）
3. 前端 E2E（导航、概览、表格、按钮、更新数据对话框）
"""

import pytest
import pandas as pd


class TestFundETFHistMinBackend:
    """后端数据服务单元测试"""

    @pytest.mark.asyncio
    async def test_save_fund_etf_hist_min_data(self, db_connection):
        """测试保存 ETF 分时行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_connection)

        # 构造示例数据（5 分钟、后复权）
        test_data = pd.DataFrame([
            {
                "代码": "513500",
                "时间": "2023-12-11 09:35:00",
                "开盘": 3.114,
                "收盘": 3.114,
                "最高": 3.116,
                "最低": 3.114,
                "成交量": 49422,
                "成交额": 7694560.0,
            },
            {
                "代码": "513500",
                "时间": "2023-12-11 09:40:00",
                "开盘": 3.112,
                "收盘": 3.116,
                "最高": 3.116,
                "最低": 3.112,
                "成交量": 11297,
                "成交额": 1758943.0,
            },
        ])

        saved_count = await service.save_fund_etf_hist_min_data(test_data)
        assert saved_count == len(test_data)

        stats = await service.get_fund_etf_hist_min_stats()
        assert stats["total_count"] >= len(test_data)

    @pytest.mark.asyncio
    async def test_clear_fund_etf_hist_min_data(self, db_connection):
        """测试清空 ETF 分时行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_connection)

        deleted = await service.clear_fund_etf_hist_min_data()
        assert deleted >= 0

        stats = await service.get_fund_etf_hist_min_stats()
        assert stats["total_count"] == 0


class TestFundETFHistMinAPI:
    """API 端点测试"""

    @pytest.mark.asyncio
    async def test_get_fund_collections_includes_etf_hist_min(self, test_client):
        """集合列表中应包含 ETF 分时行情集合"""
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200

        data = response.json()
        names = [c["name"] for c in data]
        assert "fund_etf_hist_min_em" in names

    @pytest.mark.asyncio
    async def test_get_fund_etf_hist_min_data(self, test_client):
        """测试获取 ETF 分时行情数据列表"""
        response = await test_client.get("/api/funds/collections/fund_etf_hist_min_em")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data

    @pytest.mark.asyncio
    async def test_get_fund_etf_hist_min_stats(self, test_client):
        """测试获取 ETF 分时行情统计信息"""
        response = await test_client.get("/api/funds/collections/fund_etf_hist_min_em/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_count" in data

    @pytest.mark.asyncio
    async def test_refresh_fund_etf_hist_min(self, test_client):
        """测试刷新 ETF 分时行情数据任务创建"""
        # 默认参数：period=5, adjust='hfq' 在服务端使用默认值
        response = await test_client.post(
            "/api/funds/collections/fund_etf_hist_min_em/refresh",
            json={},
        )
        assert response.status_code == 200

        data = response.json()
        assert "task_id" in data

    @pytest.mark.asyncio
    async def test_clear_fund_etf_hist_min_collection(self, test_client):
        """测试通过接口清空 ETF 分时行情集合"""
        response = await test_client.delete("/api/funds/collections/fund_etf_hist_min_em/clear")
        assert response.status_code == 200


class TestFundETFHistMinE2E:
    """端到端测试（基于 Playwright）"""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_etf_hist_min_page(self, page):
        """导航到 ETF 基金分时行情页面"""
        await page.goto("http://localhost:5173")

        # 导航到基金投研 -> 数据集合
        await page.click("text=基金投研")
        await page.click("text=数据集合")

        # 点击 ETF 基金分时行情-东财
        await page.click("text=ETF基金分时行情-东财")

        # 验证页面标题包含关键词
        title = await page.text_content("h1")
        assert "ETF基金分时行情" in (title or "")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_min_overview_display(self, page):
        """测试 ETF 分时行情数据概览显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_min_em")

        # 等待统计卡片
        await page.wait_for_selector(".stats-card")
        assert await page.is_visible(".stats-card")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_min_table_display(self, page):
        """测试 ETF 分时行情数据表格显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_min_em")

        await page.wait_for_selector(".el-table")
        assert await page.is_visible(".el-table")

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_min_buttons(self, page):
        """测试页面顶部按钮是否存在"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_min_em")

        assert await page.query_selector("button:has-text('刷新')") is not None
        assert await page.query_selector("button:has-text('更新数据')") is not None
        assert await page.query_selector("button:has-text('清空数据')") is not None

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_min_update_dialog(self, page):
        """测试更新数据对话框（文件导入、远程同步等区块存在）"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_min_em")

        await page.click("button:has-text('更新数据')")
        await page.wait_for_selector(".el-dialog")

        # 验证基本区块存在
        assert await page.is_visible("text=文件导入")
        assert await page.is_visible("text=远程同步")


# 通用测试 fixture，复用现有 ETF / 基金测试的结构

@pytest.fixture
async def db_connection():
    """数据库连接 fixture"""
    from app.core.database import get_mongo_db

    db = get_mongo_db()
    yield db


@pytest.fixture
async def test_client():
    """HTTPX 异步测试客户端"""
    from httpx import AsyncClient
    from app.main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def page():
    """Playwright 页面 fixture"""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        yield page
        await browser.close()
