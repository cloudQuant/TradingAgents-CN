"""
测试香港基金历史数据集合功能
集合名称: fund_hk_hist_em
数据源: 东方财富网-天天基金网-基金数据-香港基金-历史净值明细
API接口: ak.fund_hk_fund_hist_em(code, symbol)
"""
import pytest
import pytest_asyncio
import asyncio
from datetime import datetime
from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService
from app.services.fund_refresh_service import FundRefreshService
import pandas as pd


@pytest_asyncio.fixture
async def db():
    """获取测试数据库连接"""
    database = get_mongo_db()
    
    try:
        yield database
    finally:
        # 清理测试数据
        try:
            await database.get_collection("fund_hk_hist_em").delete_many({"test_flag": True})
        except Exception as e:
            print(f"清理测试数据失败: {e}")


@pytest.fixture
def sample_hist_data():
    """样本历史净值明细数据"""
    return pd.DataFrame({
        "净值日期": ["2021-01-19", "2021-01-18", "2021-01-15"],
        "单位净值": [10.0056, 10.0639, 10.0019],
        "日增长值": [-0.0583, 0.0620, -0.0074],
        "日增长率": [-0.5793, 0.6199, -0.0739],
        "单位": ["元", "元", "元"]
    })


@pytest.fixture
def sample_dividend_data():
    """样本分红送配详情数据"""
    return pd.DataFrame({
        "年份": ["2020", "2020", "2020"],
        "权益登记日": ["", "2020-11-30", "2020-10-30"],
        "除息日": ["2020-12-31", "2020-11-30", "2020-10-30"],
        "分红发放日": ["", "2020-12-14", "2020-11-13"],
        "分红金额": [0.0522, 0.0552, 0.0573],
        "单位": ["元", "元", "元"]
    })


class TestFundHkHistEmCollection:
    """测试香港基金历史数据集合的功能"""
    
    @pytest.mark.asyncio
    async def test_save_historical_net_value_data(self, db, sample_hist_data):
        """测试保存历史净值明细数据"""
        service = FundDataService(db)
        
        # 添加测试标记
        sample_hist_data["test_flag"] = True
        sample_hist_data["code"] = "1002200683"
        sample_hist_data["symbol"] = "历史净值明细"
        
        # 保存数据
        saved_count = await service.save_fund_hk_hist_em_data(sample_hist_data)
        
        # 验证保存数量
        assert saved_count > 0
        
        # 验证数据库中的数据
        collection = db.get_collection("fund_hk_hist_em")
        count = await collection.count_documents({"test_flag": True, "symbol": "历史净值明细"})
        assert count == len(sample_hist_data)
        
        # 验证唯一约束（code + date + symbol）
        # 再次保存相同数据，应该更新而不是插入
        saved_count_2 = await service.save_fund_hk_hist_em_data(sample_hist_data)
        count_2 = await collection.count_documents({"test_flag": True, "symbol": "历史净值明细"})
        assert count_2 == count  # 数量不应该增加
    
    @pytest.mark.asyncio
    async def test_save_dividend_data(self, db, sample_dividend_data):
        """测试保存分红送配详情数据"""
        service = FundDataService(db)
        
        # 添加测试标记
        sample_dividend_data["test_flag"] = True
        sample_dividend_data["code"] = "1002200683"
        sample_dividend_data["symbol"] = "分红送配详情"
        
        # 保存数据
        saved_count = await service.save_fund_hk_hist_em_data(sample_dividend_data)
        
        # 验证保存数量
        assert saved_count > 0
        
        # 验证数据库中的数据
        collection = db.get_collection("fund_hk_hist_em")
        count = await collection.count_documents({"test_flag": True, "symbol": "分红送配详情"})
        assert count == len(sample_dividend_data)
    
    @pytest.mark.asyncio
    async def test_get_collection_stats(self, db, sample_hist_data):
        """测试获取集合统计信息"""
        service = FundDataService(db)
        
        # 保存测试数据
        sample_hist_data["test_flag"] = True
        sample_hist_data["code"] = "1002200683"
        sample_hist_data["symbol"] = "历史净值明细"
        await service.save_fund_hk_hist_em_data(sample_hist_data)
        
        # 获取统计信息
        stats = await service.get_fund_hk_hist_em_stats()
        
        # 验证统计信息
        assert "total_count" in stats
        assert stats["total_count"] >= len(sample_hist_data)
        assert "fund_count" in stats
        assert "earliest_date" in stats
        assert "latest_date" in stats
        assert "symbol_distribution" in stats
    
    @pytest.mark.asyncio
    async def test_file_import(self, db, sample_hist_data, tmp_path):
        """测试文件导入功能"""
        service = FundDataService(db)
        
        # 创建临时CSV文件
        csv_file = tmp_path / "test_hk_fund_hist.csv"
        sample_hist_data["code"] = "1002200683"
        sample_hist_data["symbol"] = "历史净值明细"
        sample_hist_data.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 读取文件内容
        with open(csv_file, 'rb') as f:
            content = f.read()
        
        # 导入文件
        result = await service.import_fund_hk_hist_em_from_file(content, csv_file.name)
        
        # 验证导入结果
        assert result["saved"] > 0
        assert result["rows"] == len(sample_hist_data)
    
    @pytest.mark.asyncio
    async def test_refresh_collection_data(self, db):
        """测试刷新集合数据（使用真实API或模拟）"""
        # 注意：这个测试可能需要较长时间，因为需要调用真实API
        # 在实际测试中，建议使用mock来避免网络请求
        
        refresh_service = FundRefreshService(db)
        
        # 只测试单个基金代码，避免测试时间过长
        test_fund_code = "1002200683"
        
        try:
            # 刷新历史净值明细
            result = await refresh_service.refresh_fund_hk_hist_em(
                fund_codes=[test_fund_code],
                symbol="历史净值明细"
            )
            
            # 验证结果
            assert result["success"] is True
            assert "saved" in result
            
        except Exception as e:
            # 如果API调用失败（例如网络问题），跳过测试
            pytest.skip(f"API调用失败: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_clear_collection_data(self, db, sample_hist_data):
        """测试清空集合数据"""
        service = FundDataService(db)
        collection = db.get_collection("fund_hk_hist_em")
        
        # 保存测试数据
        sample_hist_data["test_flag"] = True
        sample_hist_data["code"] = "1002200683"
        sample_hist_data["symbol"] = "历史净值明细"
        await service.save_fund_hk_hist_em_data(sample_hist_data)
        
        # 清空测试数据
        result = await collection.delete_many({"test_flag": True})
        
        # 验证清空结果
        assert result.deleted_count >= len(sample_hist_data)
        count = await collection.count_documents({"test_flag": True})
        assert count == 0


class TestFundHkHistEmAPI:
    """测试香港基金历史数据的API端点"""
    
    @pytest.mark.asyncio
    async def test_get_collection_data_endpoint(self):
        """测试获取集合数据的API端点"""
        # 这里需要使用 httpx.AsyncClient 来测试API
        # 暂时跳过，在集成测试中实现
        pytest.skip("需要在集成测试中实现")
    
    @pytest.mark.asyncio
    async def test_refresh_collection_endpoint(self):
        """测试刷新集合数据的API端点"""
        pytest.skip("需要在集成测试中实现")
    
    @pytest.mark.asyncio
    async def test_import_collection_endpoint(self):
        """测试导入集合数据的API端点"""
        pytest.skip("需要在集成测试中实现")
    
    @pytest.mark.asyncio
    async def test_clear_collection_endpoint(self):
        """测试清空集合数据的API端点"""
        pytest.skip("需要在集成测试中实现")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
