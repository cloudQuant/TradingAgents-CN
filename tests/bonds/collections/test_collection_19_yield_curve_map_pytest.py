"""
测试集合: 收益率曲线映射 (pytest版本)
MongoDB Collection: yield_curve_map
Provider Method: save_yield_curve_map

说明：收益率曲线名称和类型的映射表
"""
import pytest
import pandas as pd


class TestYieldCurveMap:
    """收益率曲线映射测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试收益率曲线映射数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取收益率曲线数据...")
        df = await provider.get_yield_curve_data()
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 收益率曲线接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条收益率曲线映射")
            print(f"\n数据样本:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存收益率曲线映射到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_yield_curve_data()
        
        if df.empty:
            print("\n⚠️ 收益率曲线接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条曲线映射数据...")
        saved_count = await bond_service.save_yield_curve_map(df)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询曲线映射数据"""
        print("\n[查询] 查询所有曲线映射")
        
        cursor = bond_service.col_curve_map.find()
        items = await cursor.to_list(length=10)
        count = await bond_service.col_curve_map.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n曲线映射:")
            for i, item in enumerate(items, 1):
                name = item.get('curve_name', 'N/A')
                type_ = item.get('curve_type', 'N/A')
                source = item.get('source', 'N/A')
                print(f"  {i}. {name} ({type_}) - {source}")
        else:
            print("\n⚠️ 集合中暂无数据")
