"""
理财型基金实时行情-东方财富数据测试

测试覆盖：
1. 后端数据服务测试（save/clear/stats）
2. API端点测试（collections/data/stats/refresh/clear）
3. 前端E2E测试（Playwright）
"""
import pandas as pd
import pytest
from httpx import AsyncClient


class TestFundFinancialFundDailyDataService:
    """测试 FundDataService 针对 fund_financial_fund_daily_em 的方法"""

    @pytest.mark.asyncio
    async def test_save_fund_financial_fund_daily_data(self, db_instance):
        """测试保存理财型基金实时行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "序号": [1, 2],
                "基金代码": ["000134", "090021"],
                "基金简称": ["信诚理财28日盈A", "大成月添利债券A"],
                "上一期年化收益率": [2.1010, 4.7470],
                "当前交易日-万份收益": [0.4548, 0.5243],
                "当前交易日-7日年华": [1.8150, 1.8540],
                "前一个交易日-万份收益": [0.45, 0.52],
                "前一个交易日-7日年华": [1.80, 1.85],
                "封闭期": ["28天", "1个月"],
                "申购状态": ["限大额", "限大额"],
            }
        )

        # 保存数据
        saved_count = await service.save_fund_financial_fund_daily_data(test_data)

        # 验证
        assert saved_count > 0
        assert saved_count == 2

        # 清理
        await service.clear_fund_financial_fund_daily_data()

    @pytest.mark.asyncio
    async def test_clear_fund_financial_fund_daily_data(self, db_instance):
        """测试清空理财型基金实时行情数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["000134"],
                "基金简称": ["信诚理财28日盈A"],
                "当前交易日-万份收益": [0.4548],
            }
        )

        await service.save_fund_financial_fund_daily_data(test_data)

        # 清空数据
        deleted_count = await service.clear_fund_financial_fund_daily_data()

        # 验证
        assert deleted_count >= 1

    @pytest.mark.asyncio
    async def test_get_fund_financial_fund_daily_stats(self, db_instance):
        """测试获取理财型基金实时行情统计"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["000134", "090021"],
                "基金简称": ["信诚理财28日盈A", "大成月添利债券A"],
                "当前交易日-万份收益": [0.4548, 0.5243],
            }
        )

        await service.save_fund_financial_fund_daily_data(test_data)

        # 获取统计
        stats = await service.get_fund_financial_fund_daily_stats()

        # 验证
        assert stats is not None
        assert "total_count" in stats
        assert stats["total_count"] >= 2

        # 清理
        await service.clear_fund_financial_fund_daily_data()


class TestFundFinancialFundDailyAPI:
    """测试理财型基金实时行情相关API端点"""

    @pytest.mark.asyncio
    async def test_fund_collections_list_includes_fund_financial_fund_daily(
        self, async_client: AsyncClient
    ):
        """测试基金集合列表包含 fund_financial_fund_daily_em"""
        response = await async_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        collection_names = [c["name"] for c in collections]
        assert "fund_financial_fund_daily_em" in collection_names

    @pytest.mark.asyncio
    async def test_get_fund_financial_fund_daily_stats_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试获取理财型基金实时行情统计API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["000134"],
                "基金简称": ["信诚理财28日盈A"],
                "当前交易日-万份收益": [0.4548],
            }
        )
        await service.save_fund_financial_fund_daily_data(test_data)

        # 调用API
        response = await async_client.get(
            "/api/funds/collections/fund_financial_fund_daily_em/stats"
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["total_count"] >= 1

        # 清理
        await service.clear_fund_financial_fund_daily_data()

    @pytest.mark.asyncio
    async def test_clear_fund_financial_fund_daily_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试清空理财型基金实时行情数据API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["000134"],
                "基金简称": ["信诚理财28日盈A"],
                "当前交易日-万份收益": [0.4548],
            }
        )
        await service.save_fund_financial_fund_daily_data(test_data)

        # 调用清空API
        response = await async_client.post(
            "/api/funds/collections/fund_financial_fund_daily_em/clear"
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["deleted_count"] >= 1


class TestFundFinancialFundDailyE2E:
    """理财型基金实时行情前端E2E测试"""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_fund_financial_fund_daily_page(self, page):
        """测试导航到理财型基金实时行情页面"""
        await page.goto("http://localhost:5173/funds/collections/fund_financial_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 验证页面标题
        title = await page.title()
        assert "基金" in title or "Fund" in title
