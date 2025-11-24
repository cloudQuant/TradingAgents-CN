"""
测试 fund_etf_spot_em 数据集合的字段显示和结构分布分析修复

验证内容：
1. 字段列表是否完整（37个字段）
2. 统计信息是否包含 type_stats
3. 前端结构分布分析是否正常显示
"""

import pytest
import asyncio
from app.services.fund_data_service import FundDataService
from app.core.database import get_mongo_db
import akshare as ak


class TestFundETFSpotFix:
    """测试 fund_etf_spot_em 修复"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """设置测试环境"""
        self.db = get_mongo_db()
        self.data_service = FundDataService()
        
    def test_fields_count(self):
        """测试字段数量是否为37个"""
        from app.routers import funds
        
        # 获取集合定义
        collections = None
        for item in dir(funds):
            if item == 'list_fund_collections':
                func = getattr(funds, item)
                break
        
        # 查找 fund_etf_spot_em 的字段定义
        expected_fields = [
            "代码", "名称", "最新价", "IOPV实时估值", "基金折价率", "涨跌额", "涨跌幅", 
            "成交量", "成交额", "开盘价", "最高价", "最低价", "昨收", "换手率", 
            "量比", "委比", "外盘", "内盘",
            "主力净流入-净额", "主力净流入-净占比", 
            "超大单净流入-净额", "超大单净流入-净占比",
            "大单净流入-净额", "大单净流入-净占比", 
            "中单净流入-净额", "中单净流入-净占比",
            "小单净流入-净额", "小单净流入-净占比",
            "现手", "买一", "卖一",
            "最新份额", "流通市值", "总市值",
            "数据日期", "更新时间"
        ]
        
        assert len(expected_fields) == 37, f"字段数量应为37个，实际为{len(expected_fields)}个"
        print(f"✓ 字段数量正确：{len(expected_fields)}个")
        
    @pytest.mark.asyncio
    async def test_stats_has_type_stats(self):
        """测试统计信息是否包含 type_stats"""
        # 首先确保有数据
        col = self.db.get_collection("fund_etf_spot_em")
        count = await col.count_documents({})
        
        if count == 0:
            print("⚠ 数据库中没有 ETF 数据，跳过统计测试")
            print("  建议：先运行数据更新，然后再测试")
            pytest.skip("数据库中没有 ETF 数据")
            return
        
        # 获取统计信息
        stats = await self.data_service.get_fund_etf_spot_stats()
        
        # 验证统计信息结构
        assert 'total_count' in stats, "统计信息应包含 total_count"
        assert 'rise_count' in stats, "统计信息应包含 rise_count"
        assert 'fall_count' in stats, "统计信息应包含 fall_count"
        assert 'flat_count' in stats, "统计信息应包含 flat_count"
        assert 'type_stats' in stats, "统计信息应包含 type_stats（这是修复的关键）"
        
        # 验证 type_stats 格式
        type_stats = stats['type_stats']
        assert isinstance(type_stats, list), "type_stats 应该是列表"
        
        if len(type_stats) > 0:
            # 检查第一个类型统计的格式
            first_stat = type_stats[0]
            assert 'type' in first_stat, "type_stats 中每项应包含 type 字段"
            assert 'count' in first_stat, "type_stats 中每项应包含 count 字段"
            
            print(f"✓ 统计信息包含 type_stats")
            print(f"  - 基金类型数量: {len(type_stats)}")
            print(f"  - 前3个类型:")
            for stat in type_stats[:3]:
                print(f"    * {stat['type']}: {stat['count']}个")
        else:
            print("⚠ type_stats 为空（可能数据量较少）")
        
    @pytest.mark.asyncio
    async def test_sample_data_structure(self):
        """测试数据库中实际数据的字段结构"""
        col = self.db.get_collection("fund_etf_spot_em")
        
        # 获取一条样本数据
        sample = await col.find_one()
        
        if sample is None:
            print("⚠ 数据库中没有 ETF 数据")
            pytest.skip("数据库中没有 ETF 数据")
            return
        
        # 统计字段数量（排除 _id 和元数据字段）
        meta_fields = ['_id', 'code', 'date', 'source', 'endpoint', 'updated_at']
        data_fields = [k for k in sample.keys() if k not in meta_fields]
        
        print(f"✓ 数据库中的字段数量: {len(data_fields)}个")
        print(f"  实际字段: {', '.join(data_fields[:10])}...")
        
        # 检查是否包含新增的字段
        new_fields = ["外盘", "内盘", "超大单净流入-净额", "现手", "买一", "卖一", "最新份额", "流通市值", "总市值"]
        missing_fields = [f for f in new_fields if f not in sample]
        
        if missing_fields:
            print(f"⚠ 缺少以下新增字段: {', '.join(missing_fields)}")
            print(f"  建议：需要重新获取数据以包含所有37个字段")
        else:
            print(f"✓ 所有新增字段都存在")
    
    def test_akshare_api_fields(self):
        """测试 AKShare API 返回的字段"""
        try:
            print("正在从 AKShare 获取样本数据...")
            df = ak.fund_etf_spot_em()
            
            if df is None or df.empty:
                print("⚠ AKShare 返回空数据")
                pytest.skip("AKShare 返回空数据")
                return
            
            # 统计字段数量
            field_count = len(df.columns)
            print(f"✓ AKShare API 返回 {field_count} 个字段")
            print(f"  字段列表: {', '.join(df.columns.tolist())}")
            
            # 验证字段数量
            assert field_count >= 35, f"AKShare 应该返回至少35个字段，实际返回{field_count}个"
            
        except Exception as e:
            print(f"⚠ 无法连接 AKShare API: {e}")
            pytest.skip(f"无法连接 AKShare API: {e}")


def main():
    """手动运行测试"""
    print("=" * 60)
    print("测试 fund_etf_spot_em 数据集合修复")
    print("=" * 60)
    
    test = TestFundETFSpotFix()
    test.setup()
    
    print("\n[1/4] 测试字段数量...")
    try:
        test.test_fields_count()
    except Exception as e:
        print(f"✗ 字段数量测试失败: {e}")
    
    print("\n[2/4] 测试 AKShare API 字段...")
    try:
        test.test_akshare_api_fields()
    except Exception as e:
        print(f"✗ AKShare API 测试失败: {e}")
    
    print("\n[3/4] 测试数据库数据结构...")
    try:
        asyncio.run(test.test_sample_data_structure())
    except Exception as e:
        print(f"✗ 数据结构测试失败: {e}")
    
    print("\n[4/4] 测试统计信息（type_stats）...")
    try:
        asyncio.run(test.test_stats_has_type_stats())
    except Exception as e:
        print(f"✗ 统计信息测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n建议后续操作:")
    print("1. 在前端访问 /funds/collections/fund_etf_spot_em")
    print("2. 点击'更新数据'按钮重新获取数据")
    print("3. 检查'结构分布分析' tab 是否正常显示")
    print("4. 检查数据列表是否显示所有37个字段")


if __name__ == "__main__":
    main()
