"""
基金历史行情-新浪数据测试

测试覆盖：
1. 后端数据服务测试（save/clear/stats）
2. API端点测试（collections/data/stats/refresh/clear）
3. 前端E2E测试（Playwright）
"""
import pandas as pd
import pytest
from httpx import AsyncClient


class TestFundHistSinaDataService:
    """测试 FundDataService 针对 fund_hist_sina 的方法"""

    @pytest.mark.asyncio
    async def test_save_fund_hist_sina_data(self, db_instance):
        """测试保存新浪基金历史行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "open": [1.0, 1.1, 1.2],
                "high": [1.05, 1.15, 1.25],
                "low": [0.95, 1.0, 1.1],
                "close": [1.02, 1.12, 1.22],
                "volume": [1000000, 1100000, 1200000],
                "代码": ["sh510050", "sh510050", "sh510050"],
            }
        )

        # 保存数据
        saved_count = await service.save_fund_hist_sina_data(test_data)

        # 验证
        assert saved_count > 0
        assert saved_count == 3

        # 清理
        await service.clear_fund_hist_sina_data()

    @pytest.mark.asyncio
    async def test_clear_fund_hist_sina_data(self, db_instance):
        """测试清空新浪基金历史行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "open": [1.0],
                "high": [1.05],
                "low": [0.95],
                "close": [1.02],
                "volume": [1000000],
                "代码": ["sh510050"],
            }
        )

        await service.save_fund_hist_sina_data(test_data)

        # 清空数据
        deleted_count = await service.clear_fund_hist_sina_data()

        # 验证
        assert deleted_count >= 1

    @pytest.mark.asyncio
    async def test_get_fund_hist_sina_stats(self, db_instance):
        """测试获取新浪基金历史行情统计"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02"],
                "open": [1.0, 1.1],
                "high": [1.05, 1.15],
                "low": [0.95, 1.0],
                "close": [1.02, 1.12],
                "volume": [1000000, 1100000],
                "代码": ["sh510050", "sh510050"],
            }
        )

        await service.save_fund_hist_sina_data(test_data)

        # 获取统计
        stats = await service.get_fund_hist_sina_stats()

        # 验证
        assert stats is not None
        assert "total_count" in stats
        assert stats["total_count"] >= 2
        assert "code_stats" in stats
        assert "earliest_date" in stats
        assert "latest_date" in stats

        # 清理
        await service.clear_fund_hist_sina_data()


class TestFundHistSinaAPI:
    """测试基金历史行情-新浪相关API端点"""

    @pytest.mark.asyncio
    async def test_fund_collections_list_includes_fund_hist_sina(
        self, async_client: AsyncClient
    ):
        """测试基金集合列表包含 fund_hist_sina"""
        response = await async_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        collection_names = [c["name"] for c in collections]
        assert "fund_hist_sina" in collection_names

    @pytest.mark.asyncio
    async def test_get_fund_hist_sina_data(self, async_client: AsyncClient, db_instance):
        """测试获取新浪基金历史行情数据列表"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "open": [1.0],
                "high": [1.05],
                "low": [0.95],
                "close": [1.02],
                "volume": [1000000],
                "代码": ["sh510050"],
            }
        )
        await service.save_fund_hist_sina_data(test_data)

        # 调用API
        response = await async_client.get(
            "/api/funds/collections/fund_hist_sina/data", params={"page": 1, "page_size": 10}
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "total" in data["data"]

        # 清理
        await service.clear_fund_hist_sina_data()

    @pytest.mark.asyncio
    async def test_get_fund_hist_sina_stats_api(self, async_client: AsyncClient, db_instance):
        """测试获取新浪基金历史行情统计API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "open": [1.0],
                "high": [1.05],
                "low": [0.95],
                "close": [1.02],
                "volume": [1000000],
                "代码": ["sh510050"],
            }
        )
        await service.save_fund_hist_sina_data(test_data)

        # 调用API
        response = await async_client.get("/api/funds/collections/fund_hist_sina/stats")

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["total_count"] >= 1

        # 清理
        await service.clear_fund_hist_sina_data()

    @pytest.mark.asyncio
    async def test_clear_fund_hist_sina_api(self, async_client: AsyncClient, db_instance):
        """测试清空新浪基金历史行情数据API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "open": [1.0],
                "high": [1.05],
                "low": [0.95],
                "close": [1.02],
                "volume": [1000000],
                "代码": ["sh510050"],
            }
        )
        await service.save_fund_hist_sina_data(test_data)

        # 调用清空API
        response = await async_client.post("/api/funds/collections/fund_hist_sina/clear")

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["deleted_count"] >= 1


class TestFundHistSinaE2E:
    """基金历史行情-新浪前端E2E测试"""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_fund_hist_sina_page(self, page):
        """测试导航到新浪基金历史行情页面"""
        await page.goto("http://localhost:5173/funds/collections/fund_hist_sina")
        await page.wait_for_load_state("networkidle")
        
        # 验证页面标题
        title = await page.title()
        assert "基金" in title or "Fund" in title

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_hist_sina_stats_display(self, page):
        """测试新浪基金历史行情统计信息显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_hist_sina")
        await page.wait_for_load_state("networkidle")
        
        # 等待统计卡片加载
        await page.wait_for_selector(".el-card", timeout=10000)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_hist_sina_table_display(self, page):
        """测试新浪基金历史行情数据表格显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_hist_sina")
        await page.wait_for_load_state("networkidle")
        
        # 等待表格加载
        await page.wait_for_selector(".el-table", timeout=10000)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_hist_sina_refresh_button(self, page):
        """测试新浪基金历史行情刷新按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_hist_sina")
        await page.wait_for_load_state("networkidle")
        
        # 查找并点击刷新按钮
        refresh_button = page.locator("button:has-text('刷新')")
        if await refresh_button.count() > 0:
            await refresh_button.first.click()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_hist_sina_update_button(self, page):
        """测试新浪基金历史行情更新数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_hist_sina")
        await page.wait_for_load_state("networkidle")
        
        # 查找并点击更新数据按钮
        update_button = page.locator("button:has-text('更新数据')")
        if await update_button.count() > 0:
            await update_button.first.click()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_hist_sina_clear_button(self, page):
        """测试新浪基金历史行情清空数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_hist_sina")
        await page.wait_for_load_state("networkidle")
        
        # 查找并点击清空数据按钮
        clear_button = page.locator("button:has-text('清空数据')")
        if await clear_button.count() > 0:
            await clear_button.first.click()
