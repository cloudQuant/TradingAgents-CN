"""
分级基金历史数据-东方财富测试

测试覆盖：
1. 后端数据服务测试（save/clear/stats）
2. API端点测试（collections/data/stats/refresh/clear）
3. 前端E2E测试（Playwright）
"""
import pandas as pd
import pytest
from httpx import AsyncClient


class TestFundGradedFundInfoDataService:
    """测试 FundDataService 针对 fund_graded_fund_info_em 的方法"""

    @pytest.mark.asyncio
    async def test_save_fund_graded_fund_info_data(self, db_instance):
        """测试保存分级基金历史数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "净值日期": ["2024-01-01", "2024-01-02"],
                "单位净值": [1.0000, 0.9997],
                "累计净值": [1.0000, 0.9997],
                "日增长率": [0.0, -0.03],
                "申购状态": ["封闭期", "封闭期"],
                "赎回状态": ["封闭期", "封闭期"],
            }
        )

        # 保存数据
        saved_count = await service.save_fund_graded_fund_info_data(
            df=test_data, fund_code="150232"
        )

        # 验证
        assert saved_count > 0
        assert saved_count == 2

        # 清理
        await service.clear_fund_graded_fund_info_data()

    @pytest.mark.asyncio
    async def test_clear_fund_graded_fund_info_data(self, db_instance):
        """测试清空分级基金历史数据"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "净值日期": ["2024-01-01"],
                "单位净值": [1.0000],
                "累计净值": [1.0000],
            }
        )

        await service.save_fund_graded_fund_info_data(df=test_data, fund_code="150232")

        # 清空数据
        deleted_count = await service.clear_fund_graded_fund_info_data()

        # 验证
        assert deleted_count >= 1

    @pytest.mark.asyncio
    async def test_get_fund_graded_fund_info_stats(self, db_instance):
        """测试获取分级基金历史数据统计"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "净值日期": ["2024-01-01", "2024-01-02"],
                "单位净值": [1.0000, 0.9997],
                "累计净值": [1.0000, 0.9997],
            }
        )

        await service.save_fund_graded_fund_info_data(df=test_data, fund_code="150232")

        # 获取统计
        stats = await service.get_fund_graded_fund_info_stats()

        # 验证
        assert stats is not None
        assert "total_count" in stats
        assert stats["total_count"] >= 2
        assert "fund_code_stats" in stats

        # 清理
        await service.clear_fund_graded_fund_info_data()


class TestFundGradedFundInfoAPI:
    """测试分级基金历史数据相关API端点"""

    @pytest.mark.asyncio
    async def test_fund_collections_list_includes_fund_graded_fund_info(
        self, async_client: AsyncClient
    ):
        """测试基金集合列表包含 fund_graded_fund_info_em"""
        response = await async_client.get("/api/funds/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        collections = data["data"]
        collection_names = [c["name"] for c in collections]
        assert "fund_graded_fund_info_em" in collection_names

    @pytest.mark.asyncio
    async def test_get_fund_graded_fund_info_stats_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试获取分级基金历史数据统计API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "净值日期": ["2024-01-01"],
                "单位净值": [1.0000],
            }
        )
        await service.save_fund_graded_fund_info_data(df=test_data, fund_code="150232")

        # 调用API
        response = await async_client.get(
            "/api/funds/collections/fund_graded_fund_info_em/stats"
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["total_count"] >= 1

        # 清理
        await service.clear_fund_graded_fund_info_data()

    @pytest.mark.asyncio
    async def test_clear_fund_graded_fund_info_api(
        self, async_client: AsyncClient, db_instance
    ):
        """测试清空分级基金历史数据API"""
        from app.services.fund_data_service import FundDataService

        service = FundDataService(db_instance)

        # 准备测试数据
        test_data = pd.DataFrame(
            {
                "净值日期": ["2024-01-01"],
                "单位净值": [1.0000],
            }
        )
        await service.save_fund_graded_fund_info_data(df=test_data, fund_code="150232")

        # 调用清空API
        response = await async_client.post(
            "/api/funds/collections/fund_graded_fund_info_em/clear"
        )

        # 验证
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["deleted_count"] >= 1


class TestFundGradedFundInfoE2E:
    """分级基金历史数据前端E2E测试"""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_fund_graded_fund_info_page(self, page):
        """测试导航到分级基金历史数据页面"""
        await page.goto("http://localhost:5173/funds/collections/fund_graded_fund_info_em")
        await page.wait_for_load_state("networkidle")

        # 验证页面标题
        title = await page.title()
        assert "基金" in title or "Fund" in title
