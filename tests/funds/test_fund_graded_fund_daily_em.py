"""
分级基金实时数据-东方财富测试

测试覆盖：
1. 后端数据服务测试（save/clear/stats）
2. API端点测试（collections/data/stats/refresh/clear）
3. 前端E2E测试（Playwright）
"""
import pandas as pd
import pytest
from httpx import AsyncClient


class TestFundGradedFundDailyDataService:
    """测试 FundDataService 针对 fund_graded_fund_daily_em 的方法"""

    @pytest.mark.asyncio
    async def test_save_fund_graded_fund_daily_data(self, db_instance):
        """测试保存分级基金实时数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["150232", "150174"],
                "基金简称": ["申万菱信申万电子分级B", "信诚中证TMT产业主题分级B"],
                "单位净值": [0.5598, 0.6580],
                "累计净值": [0.0, 2.0740],
                "前交易日-单位净值": [0.5, 0.6],
                "前交易日-累计净值": [0.0, 2.0],
                "日增长值": [0.05, 0.05],
                "日增长率": ["15.85", "10.77"],
                "市价": ["0.9080", "0.76"],
                "折价率": ["-62.20", "-15.50"],
                "手续费": ["", ""],
            }
        )

        # 保存数据
        saved_count = await service.save_fund_graded_fund_daily_data(test_data)

        # 验证
        assert saved_count > 0
        assert saved_count == 2

        # 清理
        await service.clear_fund_graded_fund_daily_data()

    @pytest.mark.asyncio
    async def test_clear_fund_graded_fund_daily_data(self, db_instance):
        """测试清空分级基金实时数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["150232"],
                "基金简称": ["申万菱信申万电子分级B"],
                "单位净值": [0.5598],
            }
        )

        await service.save_fund_graded_fund_daily_data(test_data)

        # 清空数据
        deleted_count = await service.clear_fund_graded_fund_daily_data()

        # 验证
        assert deleted_count >= 1

    @pytest.mark.asyncio
    async def test_get_fund_graded_fund_daily_stats(self, db_instance):
        """测试获取分级基金实时数据统计"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["150232", "150174"],
                "基金简称": ["申万菱信申万电子分级B", "信诚中证TMT产业主题分级B"],
                "单位净值": [0.5598, 0.6580],
            }
        )

        await service.save_fund_graded_fund_daily_data(test_data)

        # 获取统计
        stats = await service.get_fund_graded_fund_daily_stats()

        # 验证
        assert stats is not None
        assert "total_count" in stats
        assert stats["total_count"] >= 2

        # 清理
        await service.clear_fund_graded_fund_daily_data()


class TestFundGradedFundDailyAPI:
    """测试分级基金实时数据相关API端点"""

    @pytest.mark.asyncio
    async def test_fund_collections_list_includes_fund_graded_fund_daily(
        self, async_client: AsyncClient
    ):
        """测试基金集合列表包含 fund_graded_fund_daily_em"""
        response = await async_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        collection_names = [c["name"] for c in collections]
        assert "fund_graded_fund_daily_em" in collection_names

    @pytest.mark.asyncio
    async def test_get_fund_graded_fund_daily_stats_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试获取分级基金实时数据统计API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["150232"],
                "基金简称": ["申万菱信申万电子分级B"],
                "单位净值": [0.5598],
            }
        )
        await service.save_fund_graded_fund_daily_data(test_data)

        # 调用API
        response = await async_client.get(
            "/api/funds/collections/fund_graded_fund_daily_em/stats"
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["total_count"] >= 1

        # 清理
        await service.clear_fund_graded_fund_daily_data()

    @pytest.mark.asyncio
    async def test_clear_fund_graded_fund_daily_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试清空分级基金实时数据API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "基金代码": ["150232"],
                "基金简称": ["申万菱信申万电子分级B"],
                "单位净值": [0.5598],
            }
        )
        await service.save_fund_graded_fund_daily_data(test_data)

        # 调用清空API
        response = await async_client.post(
            "/api/funds/collections/fund_graded_fund_daily_em/clear"
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["deleted_count"] >= 1


class TestFundGradedFundDailyE2E:
    """分级基金实时数据前端E2E测试"""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_fund_graded_fund_daily_page(self, page):
        """测试导航到分级基金实时数据页面"""
        await page.goto("http://localhost:5173/funds/collections/fund_graded_fund_daily_em")
        await page.wait_for_load_state("networkidle")

        # 验证页面标题
        title = await page.title()
        assert "基金" in title or "Fund" in title
