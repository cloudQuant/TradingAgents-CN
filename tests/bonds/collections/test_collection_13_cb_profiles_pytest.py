"""
测试集合: 可转债基本资料 (pytest版本)
MongoDB Collection: bond_cb_profiles
AkShare Interface: 通过get_basic_info构建
Provider Method: 从get_symbol_list + get_basic_info构建profiles

说明：可转债基本资料通过获取可转债列表，然后逐个获取详细信息构建
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestCbProfiles:
    """可转债基本资料测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试构建可转债基本资料
        
        方案：从get_symbol_list获取可转债列表，提取基本信息构建profile
        """
        provider = AKShareBondProvider()
        
        print("\n正在获取可转债列表...")
        all_bonds = await provider.get_symbol_list()
        
        # 筛选可转债
        cov_bonds = [b for b in all_bonds if b.get('category') == 'convertible']
        
        assert len(cov_bonds) > 0, "未找到可转债"
        
        print(f"\n✅ 找到 {len(cov_bonds)} 只可转债")
        
        # 构建profiles（从symbol_list中提取关键字段）
        profiles = []
        for bond in cov_bonds[:10]:  # 只取前10个作为测试
            profile = {
                'code': bond.get('code'),
                'name': bond.get('name'),
                'category': bond.get('category'),
                'exchange': bond.get('exchange', ''),
                'source': 'akshare',
            }
            if profile['code'] and profile['name']:
                profiles.append(profile)
        
        print(f"\n构建profile数据: {len(profiles)} 条")
        print(f"\n数据样本（前3条）:")
        for i, p in enumerate(profiles[:3], 1):
            print(f"  {i}. {p['code']} {p['name']} ({p['category']})")
        
        assert len(profiles) > 0, "未能构建profile数据"
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存可转债基本资料到MongoDB"""
        provider = AKShareBondProvider()
        
        # 获取可转债列表
        all_bonds = await provider.get_symbol_list()
        cov_bonds = [b for b in all_bonds if b.get('category') == 'convertible']
        
        # 构建profiles
        profiles = []
        for bond in cov_bonds[:20]:  # 取前20个测试
            profile = {
                'code': bond.get('code'),
                'name': bond.get('name'),
                'category': bond.get('category'),
                'exchange': bond.get('exchange', ''),
                'trade': bond.get('trade'),  # 最新价
                'changepercent': bond.get('changepercent'),  # 涨跌幅
                'source': 'akshare',
            }
            if profile['code'] and profile['name']:
                profiles.append(profile)
        
        assert len(profiles) > 0, "无profile数据可保存"
        
        print(f"\n准备保存 {len(profiles)} 条可转债基本资料...")
        
        # 保存到MongoDB
        saved_count = await bond_service.save_cb_profiles(profiles)
        
        print(f"✅ 成功保存 {saved_count} 条数据")
        assert saved_count > 0, "保存失败"
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询可转债基本资料"""
        print("\n[查询1] 查询所有可转债基本资料（前10条）")
        
        cursor = bond_service.col_cb_profiles.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_cb_profiles.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code', 'N/A')
                name = item.get('name', 'N/A')
                category = item.get('category', 'N/A')
                exchange = item.get('exchange', 'N/A')
                print(f"  {i}. {code} {name} - 类型:{category} 交易所:{exchange}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 测试按code查询
        if count > 0:
            print("\n[查询2] 查询特定可转债")
            first_item = items[0] if items else None
            if first_item and first_item.get('code'):
                test_code = first_item['code']
                result = await bond_service.col_cb_profiles.find_one({'code': test_code})
                if result:
                    print(f"✅ 成功查询到 {test_code}: {result.get('name', 'N/A')}")
                else:
                    print(f"⚠️ 未找到 {test_code}")
