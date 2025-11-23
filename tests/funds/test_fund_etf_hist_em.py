"""
ETF基金历史行情-东财 测试用例

测试集合：fund_etf_hist_em
API接口：fund_etf_hist_em(symbol, period, start_date, end_date, adjust)
"""

import pytest
import pandas as pd
from datetime import datetime
from httpx import AsyncClient


class TestFundETFHistDataService:
    """后端数据服务测试"""
    
    @pytest.mark.asyncio
    async def test_save_fund_etf_hist_data(self, fund_data_service):
        """测试保存ETF历史行情数据"""
        # 准备测试数据
        test_data = pd.DataFrame({
            '代码': ['159707', '159707', '513500'],
            '日期': ['2023-01-03', '2023-01-04', '2023-01-03'],
            '开盘': [1.250, 1.247, 1.250],
            '收盘': [1.250, 1.245, 1.250],
            '最高': [1.252, 1.249, 1.252],
            '最低': [1.248, 1.243, 1.248],
            '成交量': [100000, 150000, 200000],
            '成交额': [125000.0, 186750.0, 250000.0],
            '振幅': [0.48, 0.40, 0.48],
            '涨跌幅': [-0.40, -0.40, -0.40],
            '涨跌额': [-0.005, -0.005, -0.005],
            '换手率': [4.49, 1.81, 4.49],
        })
        
        # 保存数据
        saved_count = await fund_data_service.save_fund_etf_hist_data(test_data)
        
        # 验证保存数量
        assert saved_count == len(test_data)
        
        # 验证可以查询到数据
        stats = await fund_data_service.get_fund_etf_hist_stats()
        assert stats['total_count'] >= len(test_data)
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_hist_stats(self, fund_data_service):
        """测试获取ETF历史行情统计"""
        stats = await fund_data_service.get_fund_etf_hist_stats()
        
        # 验证返回的统计信息结构
        assert 'total_count' in stats
        assert 'code_stats' in stats
        assert 'earliest_date' in stats
        assert 'latest_date' in stats
        
        # 如果有数据，验证统计详情
        if stats['total_count'] > 0:
            assert isinstance(stats['code_stats'], list)
            assert len(stats['code_stats']) > 0
    
    @pytest.mark.asyncio
    async def test_clear_fund_etf_hist_data(self, fund_data_service):
        """测试清空ETF历史行情数据"""
        # 先保存一些测试数据
        test_data = pd.DataFrame({
            '代码': ['159707'],
            '日期': ['2023-01-03'],
            '开盘': [1.250],
            '收盘': [1.250],
            '最高': [1.252],
            '最低': [1.248],
            '成交量': [100000],
            '成交额': [125000.0],
            '振幅': [0.48],
            '涨跌幅': [-0.40],
            '涨跌额': [-0.005],
            '换手率': [4.49],
        })
        await fund_data_service.save_fund_etf_hist_data(test_data)
        
        # 清空数据
        deleted_count = await fund_data_service.clear_fund_etf_hist_data()
        
        # 验证清空结果
        assert deleted_count >= 0
        
        # 验证数据已清空
        stats = await fund_data_service.get_fund_etf_hist_stats()
        assert stats['total_count'] == 0


class TestFundETFHistAPI:
    """API端点测试"""
    
    @pytest.mark.asyncio
    async def test_get_fund_collections_includes_etf_hist(self, test_client):
        """测试基金集合列表包含ETF历史行情"""
        response = await test_client.get("/api/funds/collections")
        assert response.status_code == 200
        
        data = response.json()
        collection_names = [c['name'] for c in data]
        assert 'fund_etf_hist_em' in collection_names
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_hist_data(self, test_client):
        """测试获取ETF历史行情数据"""
        response = await test_client.get("/api/funds/collections/fund_etf_hist_em")
        assert response.status_code == 200
        
        data = response.json()
        assert 'items' in data
        assert 'total' in data
    
    @pytest.mark.asyncio
    async def test_get_fund_etf_hist_stats(self, test_client):
        """测试获取ETF历史行情统计"""
        response = await test_client.get("/api/funds/collections/fund_etf_hist_em/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert 'total_count' in data
    
    @pytest.mark.asyncio
    async def test_refresh_fund_etf_hist(self, test_client):
        """测试刷新ETF历史行情数据"""
        response = await test_client.post(
            "/api/funds/collections/fund_etf_hist_em/refresh",
            json={}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert 'task_id' in data
    
    @pytest.mark.asyncio
    async def test_clear_fund_etf_hist(self, test_client):
        """测试清空ETF历史行情数据"""
        response = await test_client.delete("/api/funds/collections/fund_etf_hist_em/clear")
        assert response.status_code == 200


class TestFundETFHistE2E:
    """端到端测试（基于Playwright）"""
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_navigate_to_etf_hist_page(self, page):
        """测试导航到ETF历史行情页面"""
        await page.goto("http://localhost:5173")
        
        # 等待页面加载
        await page.wait_for_selector(".main-container", timeout=5000)
        
        # 点击基金菜单
        await page.click("text=基金数据")
        
        # 等待并点击ETF历史行情
        await page.wait_for_selector("text=ETF基金历史行情-东财", timeout=3000)
        await page.click("text=ETF基金历史行情-东财")
        
        # 验证页面已导航到正确路由
        await page.wait_for_url("**/funds/collections/fund_etf_hist_em", timeout=3000)
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_page_displays_stats_and_table(self, page):
        """测试ETF历史行情页面显示统计和表格"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_em")
        
        # 等待统计卡片加载
        await page.wait_for_selector(".stats-card", timeout=5000)
        
        # 验证统计信息存在
        stats_card = await page.query_selector(".stats-card")
        assert stats_card is not None
        
        # 验证数据表格存在
        table = await page.query_selector(".el-table")
        assert table is not None
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_refresh_button(self, page):
        """测试ETF历史行情刷新按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_em")
        
        # 等待页面加载
        await page.wait_for_selector(".stats-card", timeout=5000)
        
        # 查找并点击刷新按钮
        refresh_button = await page.query_selector("button:has-text('刷新')")
        assert refresh_button is not None
        
        await refresh_button.click()
        
        # 等待刷新完成（简单等待，实际可能需要更复杂的逻辑）
        await page.wait_for_timeout(1000)
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_update_data_dialog(self, page):
        """测试ETF历史行情更新数据对话框"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_em")
        
        # 等待页面加载
        await page.wait_for_selector(".stats-card", timeout=5000)
        
        # 点击更新数据按钮
        update_button = await page.query_selector("button:has-text('更新数据')")
        if update_button:
            await update_button.click()
            
            # 等待对话框出现
            await page.wait_for_selector(".el-dialog", timeout=3000)
            
            # 验证对话框中包含文件导入和远程同步选项
            dialog = await page.query_selector(".el-dialog")
            dialog_text = await dialog.inner_text()
            
            assert "文件导入" in dialog_text
            assert "远程同步" in dialog_text
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_etf_hist_clear_button(self, page):
        """测试ETF历史行情清空按钮"""
        await page.goto("http://localhost:5173/funds/collections/fund_etf_hist_em")
        
        # 等待页面加载
        await page.wait_for_selector(".stats-card", timeout=5000)
        
        # 查找清空按钮
        clear_button = await page.query_selector("button:has-text('清空数据')")
        assert clear_button is not None
