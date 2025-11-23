"""
基金实时行情-新浪测试用例

测试内容：
1. 后端数据服务测试
2. API接口测试
3. 前端E2E测试
"""
import pytest
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd


class TestFundSpotSinaBackend:
    """后端单元测试"""
    
    @pytest.mark.asyncio
    async def test_save_fund_spot_sina_data(self):
        """测试保存基金实时行情-新浪数据"""
        from app.core.database import get_mongo_db
        from app.services.fund_data_service import FundDataService
        
        db = get_mongo_db()
        service = FundDataService(db)
        
        # 准备测试数据（包含三种类型）
        test_data = pd.DataFrame([
            {
                "代码": "sz180801",
                "名称": "首钢绿能",
                "最新价": 12.520,
                "涨跌额": 0.008,
                "涨跌幅": 0.064,
                "买入": 12.519,
                "卖出": 12.520,
                "昨收": 12.512,
                "今开": 12.505,
                "最高": 12.530,
                "最低": 12.475,
                "成交量": 839446,
                "成交额": 10510150,
                "基金类型": "封闭式基金"
            },
            {
                "代码": "sh513100",
                "名称": "纳指ETF",
                "最新价": 2.850,
                "涨跌额": 0.010,
                "涨跌幅": 0.35,
                "买入": 2.849,
                "卖出": 2.850,
                "昨收": 2.840,
                "今开": 2.845,
                "最高": 2.855,
                "最低": 2.840,
                "成交量": 1000000,
                "成交额": 28500000,
                "基金类型": "ETF基金"
            },
            {
                "代码": "sz162411",
                "名称": "华宝油气",
                "最新价": 0.850,
                "涨跌额": -0.010,
                "涨跌幅": -1.16,
                "买入": 0.849,
                "卖出": 0.850,
                "昨收": 0.860,
                "今开": 0.855,
                "最高": 0.860,
                "最低": 0.845,
                "成交量": 500000,
                "成交额": 425000,
                "基金类型": "LOF基金"
            }
        ])
        
        # 保存数据
        count = await service.save_fund_spot_sina_data(test_data)
        assert count == 3
        
        # 验证数据已保存
        stats = await service.get_fund_spot_sina_stats()
        assert stats["total_count"] >= 3
        
    @pytest.mark.asyncio
    async def test_get_fund_spot_sina_stats(self):
        """测试获取基金实时行情-新浪统计信息"""
        from app.core.database import get_mongo_db
        from app.services.fund_data_service import FundDataService
        
        db = get_mongo_db()
        service = FundDataService(db)
        
        stats = await service.get_fund_spot_sina_stats()
        
        # 验证统计信息结构
        assert "total_count" in stats
        assert "rise_count" in stats
        assert "fall_count" in stats
        assert "flat_count" in stats
        assert "type_stats" in stats
        assert "top_gainers" in stats
        assert "top_losers" in stats
        assert "top_volume" in stats
        assert "latest_date" in stats
        
    @pytest.mark.asyncio
    async def test_clear_fund_spot_sina_data(self):
        """测试清空基金实时行情-新浪数据"""
        from app.core.database import get_mongo_db
        from app.services.fund_data_service import FundDataService
        
        db = get_mongo_db()
        service = FundDataService(db)
        
        # 清空数据
        deleted_count = await service.clear_fund_spot_sina_data()
        assert deleted_count >= 0


class TestFundSpotSinaAPI:
    """API测试"""
    
    @pytest.mark.asyncio
    async def test_get_fund_collections(self):
        """测试获取基金集合列表"""
        from app.routers.funds import get_fund_collections
        
        collections = await get_fund_collections()
        
        # 验证包含fund_spot_sina
        collection_names = [c["name"] for c in collections]
        assert "fund_spot_sina" in collection_names
        
    @pytest.mark.asyncio
    async def test_get_fund_spot_sina_data(self):
        """测试获取基金实时行情-新浪数据"""
        from app.routers.funds import get_fund_collection_data
        
        result = await get_fund_collection_data(
            collection_name="fund_spot_sina",
            page=1,
            page_size=10
        )
        
        assert result["success"] is True
        assert "data" in result
        assert "items" in result["data"]
        assert "total" in result["data"]
        
    @pytest.mark.asyncio
    async def test_get_fund_spot_sina_stats(self):
        """测试获取基金实时行情-新浪统计信息"""
        from app.routers.funds import get_fund_collection_stats
        
        result = await get_fund_collection_stats(collection_name="fund_spot_sina")
        
        assert result["success"] is True
        assert "data" in result
        
    @pytest.mark.asyncio
    async def test_refresh_fund_spot_sina(self):
        """测试刷新基金实时行情-新浪数据（单个类型）"""
        from app.routers.funds import refresh_fund_collection
        
        # 测试刷新ETF基金
        result = await refresh_fund_collection(
            collection_name="fund_spot_sina",
            params={"symbol": "ETF基金"}
        )
        
        assert result["success"] is True
        assert "task_id" in result["data"]
        
    @pytest.mark.asyncio
    async def test_clear_fund_spot_sina(self):
        """测试清空基金实时行情-新浪数据"""
        from app.routers.funds import clear_fund_collection
        
        result = await clear_fund_collection(collection_name="fund_spot_sina")
        
        assert result["success"] is True


class TestFundSpotSinaE2E:
    """端到端测试（基于Playwright）"""
    
    @pytest.mark.asyncio
    async def test_navigate_to_fund_spot_sina(self, page):
        """测试导航到基金实时行情-新浪页面"""
        # 登录
        await page.goto("http://localhost:5173/login")
        await page.fill('input[type="text"]', "admin")
        await page.fill('input[type="password"]', "admin123")
        await page.click('button[type="submit"]')
        
        # 等待登录成功
        await page.wait_for_url("http://localhost:5173/")
        
        # 导航到基金数据集合
        await page.click('text=基金投研')
        await page.click('text=数据集合')
        
        # 选择基金实时行情-新浪
        await page.click('text=基金实时行情-新浪')
        
        # 验证页面加载成功
        assert await page.title() == "基金投研系统"
        
    @pytest.mark.asyncio
    async def test_fund_spot_sina_overview(self, page):
        """测试数据概览"""
        # 导航到页面（假设已登录）
        await page.goto("http://localhost:5173/funds/collections/fund_spot_sina")
        
        # 等待数据加载
        await page.wait_for_selector('.stat-card')
        
        # 验证统计卡片
        cards = await page.query_selector_all('.stat-card')
        assert len(cards) >= 3  # 至少有上涨、下跌、平盘统计
        
    @pytest.mark.asyncio
    async def test_fund_spot_sina_table(self, page):
        """测试数据表格"""
        await page.goto("http://localhost:5173/funds/collections/fund_spot_sina")
        
        # 等待表格加载
        await page.wait_for_selector('.el-table')
        
        # 验证表格有数据
        rows = await page.query_selector_all('.el-table tbody tr')
        assert len(rows) > 0
        
    @pytest.mark.asyncio
    async def test_fund_spot_sina_buttons(self, page):
        """测试按钮功能"""
        await page.goto("http://localhost:5173/funds/collections/fund_spot_sina")
        
        # 验证刷新按钮
        refresh_btn = await page.query_selector('button:has-text("刷新")')
        assert refresh_btn is not None
        
        # 验证更新数据按钮
        update_btn = await page.query_selector('button:has-text("更新数据")')
        assert update_btn is not None
        
        # 验证清空数据按钮
        clear_btn = await page.query_selector('button:has-text("清空数据")')
        assert clear_btn is not None
        
    @pytest.mark.asyncio
    async def test_fund_spot_sina_charts(self, page):
        """测试图表显示"""
        await page.goto("http://localhost:5173/funds/collections/fund_spot_sina")
        
        # 等待图表加载
        await page.wait_for_selector('.chart-wrapper-medium', timeout=5000)
        
        # 验证图表存在
        charts = await page.query_selector_all('.chart-wrapper-medium')
        assert len(charts) >= 2  # 至少有涨跌分布和类型分布图表
        
    @pytest.mark.asyncio
    async def test_fund_spot_sina_update_dialog(self, page):
        """测试更新数据对话框"""
        await page.goto("http://localhost:5173/funds/collections/fund_spot_sina")
        
        # 点击更新数据按钮
        await page.click('button:has-text("更新数据")')
        
        # 等待对话框显示
        await page.wait_for_selector('.el-dialog')
        
        # 验证有类型选择器
        type_selector = await page.query_selector('select, .el-select')
        assert type_selector is not None
        
        # 验证有"全部更新"选项
        all_update_option = await page.query_selector('text=全部更新')
        assert all_update_option is not None
