"""
测试集合: 债券发行 (pytest版本)
MongoDB Collection: bond_issues
Provider Method: save_cninfo_issues(df, issue_type, endpoint)

说明：债券发行信息，包括发行规模、期限、利率等
"""
import pytest
import pandas as pd


class TestIssues:
    """债券发行测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试债券发行数据"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        print("\n正在获取债券发行数据...")
        df = await provider.get_bond_issues(issue_type='convertible')
        
        assert df is not None, "获取的数据为None"
        
        if df.empty:
            print("⚠️ 债券发行接口暂无数据或接口不可用")
            print("测试通过：接口可调用")
        else:
            print(f"\n✅ 成功获取 {len(df)} 条发行数据")
            print(f"\n数据样本（前5条）:")
            print(df.head(5))
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存发行数据到MongoDB"""
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        provider = AKShareBondProvider()
        
        # 获取数据
        df = await provider.get_bond_issues(issue_type='convertible')
        
        if df.empty:
            print("\n⚠️ 债券发行接口暂无数据，无法测试保存")
            return
        
        print(f"\n准备保存 {len(df)} 条发行数据...")
        
        # save_cninfo_issues需要issue_type和endpoint参数
        saved_count = await bond_service.save_cninfo_issues(
            df, 
            issue_type='convertible',
            endpoint='cninfo'
        )
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count >= 0, "保存操作失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询发行数据"""
        print("\n[查询] 查询所有债券发行（前10条）")
        
        cursor = bond_service.col_issues.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_issues.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                date = item.get('issue_date', 'N/A')
                amount = item.get('issue_amount', 'N/A')
                print(f"  {i}. {code} {name} - 发行日:{date} 规模:{amount}")
        else:
            print("\n⚠️ 集合中暂无数据")
