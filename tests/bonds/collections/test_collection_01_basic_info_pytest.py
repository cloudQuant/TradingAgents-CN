"""
测试集合: 债券基础信息 (pytest版本)
MongoDB Collection: bond_basic_info
AkShare Interface: bond_zh_hs_cov_spot
Provider Method: get_symbol_list
"""
import pytest
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestBondBasicInfo:
    """债券基础信息测试类"""
    
    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """测试从AkShare获取数据 - bond_zh_hs_cov_spot接口
        
        Expected fields based on AkShare docs:
        - symbol: str (交易代码)
        - name: str (债券名称)
        - trade: float (最新价)
        - pricechange: float (涨跌额)
        - changepercent: float (涨跌幅%)
        - buy: float (买入价)
        - sell: float (卖出价)
        - settlement: float (昨收)
        - open: float (开盘)
        - high: float (最高)
        - low: float (最低)
        - volume: int (成交量)
        - amount: float (成交额)
        - code: str (债券代码)
        - ticktime: str (时间)
        """
        provider = AKShareBondProvider()
        data = await provider.get_symbol_list()
        
        # 验证数据不为空
        assert data is not None, "获取的数据为None"
        assert len(data) > 0, "获取的数据为空列表"
        
        print(f"\n[PASS] 成功获取 {len(data)} 条债券数据")
        
        # 验证数据结构
        first_item = data[0]
        assert 'code' in first_item, "数据缺少code字段"
        assert 'name' in first_item, "数据缺少name字段"
        assert 'category' in first_item, "数据缺少category字段"
        
        # 验证字段类型（检查前10条有效数据）
        valid_count = 0
        type_errors = []
        
        for i, item in enumerate(data[:50]):  # 检查前50条
            code = item.get('code')
            name = item.get('name')
            
            # 跳过无效数据
            if not code or str(code) == 'None' or str(code).strip() == '':
                continue
            if not name or str(name) == 'nan' or str(name).strip() == '':
                continue
            
            valid_count += 1
            
            # 验证code类型（应该是字符串）
            if not isinstance(code, str):
                type_errors.append(f"Item {i}: code应为str, 实际为{type(code).__name__}")
            
            # 验证name类型（应该是字符串）
            if not isinstance(name, str):
                type_errors.append(f"Item {i}: name应为str, 实际为{type(name).__name__}")
            
            # 验证category类型（应该是字符串）
            category = item.get('category')
            if category is not None and not isinstance(category, str):
                type_errors.append(f"Item {i}: category应为str, 实际为{type(category).__name__}")
            
            if valid_count >= 10:  # 只检查前10条有效数据
                break
        
        if type_errors:
            print(f"\n[WARN] 发现字段类型问题:")
            for error in type_errors[:5]:  # 只显示前5个错误
                print(f"  - {error}")
        else:
            print(f"\n[PASS] 字段类型验证通过 (检查了{valid_count}条有效数据)")
        
        # 打印数据样本
        print(f"\n数据样本（前3条）:")
        for i, item in enumerate(data[:3], 1):
            code = item.get('code', 'N/A')
            name = item.get('name', 'N/A')
            category = item.get('category', 'N/A')
            print(f"  {i}. 代码:{code} 名称:{name} 分类:{category}")
        
        # 统计分类
        categories = {}
        valid_count = 0
        for item in data:
            code = item.get('code')
            if code and str(code).strip() and str(code) != 'None':
                valid_count += 1
            cat = item.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n分类统计:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}条")
        
        print(f"\n有效数据（有代码）: {valid_count}条")
        
        # 验证至少有一些有效数据
        assert valid_count > 100, f"有效数据太少: {valid_count}条，预期至少100条"
    
    @pytest.mark.asyncio
    async def test_save_data(self, bond_service):
        """测试保存数据到MongoDB"""
        provider = AKShareBondProvider()
        
        # 获取数据
        data = await provider.get_symbol_list()
        assert data is not None and len(data) > 0, "无数据可保存"
        
        print(f"\n准备保存 {len(data)} 条数据...")
        
        # 保存数据
        saved_count = await bond_service.save_basic_list(data)
        print(f"✅ 成功保存 {saved_count} 条数据")
        
        assert saved_count > 0, "保存数据失败，保存数量为0"
        
        # 验证保存
        result = await bond_service.query_basic_list(page=1, page_size=1)
        total = result.get('total', 0)
        
        assert total > 0, "保存后数据库为空"
        print(f"💾 数据库当前共有 {total} 条债券记录")
    
    @pytest.mark.asyncio
    async def test_query_data(self, bond_service):
        """测试从MongoDB查询数据"""
        # 测试1: 查询全部数据
        print("\n[查询1] 查询前5条数据")
        result = await bond_service.query_basic_list(page=1, page_size=5)
        
        assert result is not None, "查询结果为None"
        assert result.get('total', 0) > 0, "未能查询到数据"
        
        total = result['total']
        items = result.get('items', [])
        
        print(f"✅ 查询成功，共 {total} 条数据")
        for i, item in enumerate(items, 1):
            code = item.get('code', 'N/A')
            name = item.get('name', 'N/A')
            category = item.get('category', 'N/A')
            print(f"  {i}. {code} - {name} ({category})")
        
        # 测试2: 按分类查询
        print("\n[查询2] 按分类查询可转债 (convertible)")
        result_conv = await bond_service.query_basic_list(
            category='convertible', 
            page=1, 
            page_size=3
        )
        
        if result_conv.get('total', 0) > 0:
            print(f"✅ 查询到 {result_conv['total']} 条可转债")
            for i, item in enumerate(result_conv.get('items', []), 1):
                print(f"  {i}. {item.get('code')} - {item.get('name')}")
        
        # 测试3: 关键词搜索
        print("\n[查询3] 关键词搜索 '转债'")
        result_search = await bond_service.query_basic_list(
            q='转债', 
            page=1, 
            page_size=3
        )
        
        if result_search.get('total', 0) > 0:
            print(f"✅ 搜索到 {result_search['total']} 条结果")
        
        # 至少一个查询有结果
        assert total > 0, "所有查询都失败"
    
    @pytest.mark.asyncio
    async def test_data_quality(self):
        """测试数据质量"""
        provider = AKShareBondProvider()
        data = await provider.get_symbol_list()
        
        assert data is not None and len(data) > 0
        
        # 检查数据质量
        valid_data = []
        for item in data:
            code = item.get('code')
            name = item.get('name')
            
            # 跳过无效数据
            if not code or str(code) == 'None' or str(code).strip() == '':
                continue
            if not name or str(name) == 'nan' or str(name).strip() == '':
                continue
            
            valid_data.append(item)
        
        print(f"\n数据质量检查:")
        print(f"  总数据: {len(data)}")
        print(f"  有效数据: {len(valid_data)}")
        print(f"  无效数据: {len(data) - len(valid_data)}")
        print(f"  有效率: {len(valid_data)/len(data)*100:.1f}%")
        
        # 应该至少有50%的有效数据
        assert len(valid_data) >= len(data) * 0.5, \
            f"有效数据比例过低: {len(valid_data)}/{len(data)}"
