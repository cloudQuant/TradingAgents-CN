"""
开放式基金实时行情-东方财富数据测试

测试覆盖：
1. 后端数据服务测试（save/clear/stats）
2. API端点测试（collections/data/stats/refresh/clear）
3. 前端E2E测试（Playwright）
"""
import pandas as pd
import pytest
from httpx import AsyncClient


class TestFundOpenFundDailyDataService:
    """测试 FundDataService 针对 fund_open_fund_daily_em 的方法"""

    @pytest.mark.asyncio
    async def test_save_fund_open_fund_daily_data(self, db_instance):
        """测试保存开放式基金实时行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["010407", "161725", "160632"],
                "基金简称": ["安信中债1-3年政策性金融债C", "招商中证白酒指数分级", "鹏华酒分级"],
                "2024-01-01-单位净值": [1.0906, 1.3869, 1.0360],
                "2024-01-01-累计净值": [1.0906, 3.8769, 2.9800],
                "2024-01-01-前交易日-单位净值": [1.0900, 1.3800, 1.0350],
                "2024-01-01-前交易日-累计净值": [1.0900, 3.8700, 2.9750],
                "日增长值": [0.0006, 0.0069, 0.0010],
                "日增长率": [0.055, 0.50, 0.097],
                "申购状态": ["开放申购", "限大额", "开放申购"],
                "赎回状态": ["开放赎回", "开放赎回", "开放赎回"],
                "手续费": ["0.00%", "0.10%", "0.12%"],
            }
        )

        # 保存数据
        saved_count = await service.save_fund_open_fund_daily_data(test_data)

        # 验证
        assert saved_count > 0
        assert saved_count == 3

        # 清理
        await service.clear_fund_open_fund_daily_data()

    @pytest.mark.asyncio
    async def test_clear_fund_open_fund_daily_data(self, db_instance):
        """测试清空开放式基金实时行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["010407"],
                "基金简称": ["安信中债1-3年政策性金融债C"],
                "2024-01-01-单位净值": [1.0906],
                "2024-01-01-累计净值": [1.0906],
                "2024-01-01-前交易日-单位净值": [1.0900],
                "2024-01-01-前交易日-累计净值": [1.0900],
                "日增长值": [0.0006],
                "日增长率": [0.055],
                "申购状态": ["开放申购"],
                "赎回状态": ["开放赎回"],
                "手续费": ["0.00%"],
            }
        )

        await service.save_fund_open_fund_daily_data(test_data)

        # 清空数据
        deleted_count = await service.clear_fund_open_fund_daily_data()

        # 验证
        assert deleted_count >= 1

    @pytest.mark.asyncio
    async def test_get_fund_open_fund_daily_stats(self, db_instance):
        """测试获取开放式基金实时行情统计"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["010407", "161725"],
                "基金简称": ["安信中债1-3年政策性金融债C", "招商中证白酒指数分级"],
                "2024-01-01-单位净值": [1.0906, 1.3869],
                "2024-01-01-累计净值": [1.0906, 3.8769],
                "2024-01-01-前交易日-单位净值": [1.0900, 1.3800],
                "2024-01-01-前交易日-累计净值": [1.0900, 3.8700],
                "日增长值": [0.0006, 0.0069],
                "日增长率": [0.055, 0.50],
                "申购状态": ["开放申购", "限大额"],
                "赎回状态": ["开放赎回", "开放赎回"],
                "手续费": ["0.00%", "0.10%"],
            }
        )

        await service.save_fund_open_fund_daily_data(test_data)

        # 获取统计
        stats = await service.get_fund_open_fund_daily_stats()

        # 验证
        assert stats is not None
        assert "total_count" in stats
        assert stats["total_count"] >= 2
        assert "earliest_date" in stats
        assert "latest_date" in stats

        # 清理
        await service.clear_fund_open_fund_daily_data()


class TestFundOpenFundDailyAPI:
    """测试开放式基金实时行情相关API端点"""

    @pytest.mark.asyncio
    async def test_fund_collections_list_includes_fund_open_fund_daily(
        self, async_client: AsyncClient
    ):
        """测试基金集合列表包含 fund_open_fund_daily_em"""
        response = await async_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        collection_names = [c["name"] for c in collections]
        assert "fund_open_fund_daily_em" in collection_names

    @pytest.mark.asyncio
    async def test_get_fund_open_fund_daily_data(self, async_client: AsyncClient, db_instance):
        """测试获取开放式基金实时行情数据列表"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["010407"],
                "基金简称": ["安信中债1-3年政策性金融债C"],
                "2024-01-01-单位净值": [1.0906],
                "2024-01-01-累计净值": [1.0906],
                "2024-01-01-前交易日-单位净值": [1.0900],
                "2024-01-01-前交易日-累计净值": [1.0900],
                "日增长值": [0.0006],
                "日增长率": [0.055],
                "申购状态": ["开放申购"],
                "赎回状态": ["开放赎回"],
                "手续费": ["0.00%"],
            }
        )
        await service.save_fund_open_fund_daily_data(test_data)

        # 调用API
        response = await async_client.get(
            "/api/funds/collections/fund_open_fund_daily_em/data",
            params={"page": 1, "page_size": 10},
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "total" in data["data"]

        # 清理
        await service.clear_fund_open_fund_daily_data()

    @pytest.mark.asyncio
    async def test_get_fund_open_fund_daily_stats_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试获取开放式基金实时行情统计API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["010407"],
                "基金简称": ["安信中债1-3年政策性金融债C"],
                "2024-01-01-单位净值": [1.0906],
                "2024-01-01-累计净值": [1.0906],
                "2024-01-01-前交易日-单位净值": [1.0900],
                "2024-01-01-前交易日-累计净值": [1.0900],
                "日增长值": [0.0006],
                "日增长率": [0.055],
                "申购状态": ["开放申购"],
                "赎回状态": ["开放赎回"],
                "手续费": ["0.00%"],
            }
        )
        await service.save_fund_open_fund_daily_data(test_data)

        # 调用API
        response = await async_client.get("/api/funds/collections/fund_open_fund_daily_em/stats")

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["total_count"] >= 1

        # 清理
        await service.clear_fund_open_fund_daily_data()

    @pytest.mark.asyncio
    async def test_clear_fund_open_fund_daily_api(self, async_client: AsyncClient, db_instance):
        """测试清空开放式基金实时行情数据API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["010407"],
                "基金简称": ["安信中债1-3年政策性金融债C"],
                "2024-01-01-单位净值": [1.0906],
                "2024-01-01-累计净值": [1.0906],
                "2024-01-01-前交易日-单位净值": [1.0900],
                "2024-01-01-前交易日-累计净值": [1.0900],
                "日增长值": [0.0006],
                "日增长率": [0.055],
                "申购状态": ["开放申购"],
                "赎回状态": ["开放赎回"],
                "手续费": ["0.00%"],
            }
        )
        await service.save_fund_open_fund_daily_data(test_data)

        # 调用清空API
        response = await async_client.post("/api/funds/collections/fund_open_fund_daily_em/clear")

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["deleted_count"] >= 1


class TestFundOpenFundDailyE2E:
    """开放式基金实时行情前端E2E测试"""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_fund_open_fund_daily_page(self, page):
        """测试导航到开放式基金实时行情页面"""
        await page.goto("http://localhost:5173/funds/collections/fund_open_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 验证页面标题
        title = await page.title()
        assert "基金" in title or "Fund" in title

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_open_fund_daily_stats_display(self, page):
        """测试开放式基金实时行情统计信息显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_open_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 等待统计卡片加载
        await page.wait_for_selector(".el-card", timeout=10000)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_open_fund_daily_table_display(self, page):
        """测试开放式基金实时行情数据表格显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_open_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 等待表格加载
        await page.wait_for_selector(".el-table", timeout=10000)

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_open_fund_daily_refresh_button(self, page):
        """测试开放式基金实时行情刷新按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_open_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 查找并点击刷新按钮
        refresh_button = page.locator("button:has-text('刷新')")
        if await refresh_button.count() > 0:
            await refresh_button.first.click()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_open_fund_daily_update_button(self, page):
        """测试开放式基金实时行情更新数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_open_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 查找并点击更新数据按钮
        update_button = page.locator("button:has-text('更新数据')")
        if await update_button.count() > 0:
            await update_button.first.click()

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_fund_open_fund_daily_clear_button(self, page):
        """测试开放式基金实时行情清空数据按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_open_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 查找并点击清空数据按钮
        clear_button = page.locator("button:has-text('清空数据')")
        if await clear_button.count() > 0:
            await clear_button.first.click()
