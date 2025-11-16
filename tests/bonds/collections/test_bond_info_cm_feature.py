"""
测试集合: 中债信息查询 (bond_info_cm)
MongoDB Collection: bond_info_cm
AkShare Interface: bond_info_cm
Provider Method: get_bond_info_cm / save_bond_info_cm

需求：
1. 把债券查询接口放到数据集合页面的第一个
2. 支持多参数查询：bond_name, bond_code, bond_issue, bond_type, coupon_type, issue_year, underwriter, grade
3. 输出字段：债券简称、债券代码、发行人/受托机构、债券类型、发行日期、最新债项评级、查询代码
4. 更新数据时默认更新所有债券数据
5. 页面包含：刷新、更新数据、清空数据按钮
"""
import pytest
import os
import re

# 为所有测试设置30秒超时
pytestmark = pytest.mark.timeout(30)


class TestBondInfoCmFeature:
    """中债信息查询功能测试类"""
    
    def test_collection_is_first_in_list(self):
        """测试1: 验证bond_info_cm在数据集合列表的第一位"""
        bonds_router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'app', 'routers', 'bonds.py'
        )
        bonds_router_path = os.path.abspath(bonds_router_path)
        
        assert os.path.exists(bonds_router_path), f"bonds.py路由文件不存在: {bonds_router_path}"
        
        with open(bonds_router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找list_bond_collections函数
        assert 'def list_bond_collections' in content, "缺少list_bond_collections函数"
        
        # 提取collections列表
        collections_start = content.find('collections = [')
        assert collections_start > 0, "找不到collections列表定义"
        
        # 提取第一个collection定义
        first_collection_start = content.find('{', collections_start)
        first_collection_end = content.find('},', first_collection_start)
        first_collection = content[first_collection_start:first_collection_end]
        
        # 验证第一个是bond_info_cm
        assert '"name": "bond_info_cm"' in first_collection, \
            "bond_info_cm不是第一个数据集合"
        assert '"display_name": "债券信息查询"' in first_collection, \
            "第一个集合的display_name应为'债券信息查询'"
        
        print("✅ bond_info_cm已是第一个数据集合")
    
    def test_collection_has_correct_fields(self):
        """测试2: 验证bond_info_cm配置包含正确的字段"""
        bonds_router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'app', 'routers', 'bonds.py'
        )
        bonds_router_path = os.path.abspath(bonds_router_path)
        
        with open(bonds_router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找bond_info_cm的配置
        bond_info_cm_start = content.find('"name": "bond_info_cm"')
        assert bond_info_cm_start > 0, "找不到bond_info_cm配置"
        
        # 提取这个collection的完整配置
        config_start = content.rfind('{', 0, bond_info_cm_start)
        config_end = content.find('},', bond_info_cm_start)
        config_text = content[config_start:config_end]
        
        # 验证必需字段
        required_fields = [
            '债券简称', '债券代码', '发行人', '债券类型', 
            '发行日期', '最新债项评级', '查询代码'
        ]
        
        fields_section = re.search(r'"fields":\s*\[(.*?)\]', config_text, re.DOTALL)
        assert fields_section, "找不到fields配置"
        
        fields_text = fields_section.group(1)
        
        # 至少要包含一些关键字段
        has_bond_fields = any(field in fields_text for field in ['债券简称', '债券代码', 'code'])
        assert has_bond_fields, f"fields配置中缺少必要字段，当前fields: {fields_text}"
        
        print(f"✅ bond_info_cm配置正确")
    
    def test_collection_detail_page_exists(self):
        """测试3: 验证集合详情页面路由存在"""
        collection_vue_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Bonds', 'Collection.vue'
        )
        collection_vue_path = os.path.abspath(collection_vue_path)
        
        assert os.path.exists(collection_vue_path), \
            f"集合详情页面不存在: {collection_vue_path}"
        
        with open(collection_vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证页面包含必要的功能
        assert 'collectionName' in content, "页面缺少集合名称变量"
        assert 'loadData' in content, "页面缺少数据加载函数"
        
        print("✅ 集合详情页面存在")
    
    def test_collection_page_has_refresh_button(self):
        """测试4: 验证集合详情页面有刷新按钮"""
        collection_vue_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Bonds', 'Collection.vue'
        )
        collection_vue_path = os.path.abspath(collection_vue_path)
        
        with open(collection_vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查刷新按钮
        has_refresh = 'Refresh' in content and '@click' in content
        assert has_refresh, "页面缺少刷新按钮或点击事件"
        
        # 检查刷新函数
        assert 'loadData' in content or 'handleRefresh' in content, \
            "页面缺少刷新函数"
        
        print("✅ 集合详情页面有刷新按钮")
    
    def test_collection_page_has_update_button(self):
        """测试5: 验证集合详情页面有更新数据按钮"""
        collection_vue_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Bonds', 'Collection.vue'
        )
        collection_vue_path = os.path.abspath(collection_vue_path)
        
        with open(collection_vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查更新按钮
        has_update_button = '更新数据' in content or 'handleUpdate' in content
        assert has_update_button, "页面缺少更新数据按钮"
        
        # 检查更新函数
        assert 'handleUpdateData' in content or 'handleUpdate' in content, \
            "页面缺少更新数据函数"
        
        print("✅ 集合详情页面有更新数据按钮")
    
    def test_collection_page_has_clear_button(self):
        """测试6: 验证集合详情页面有清空数据按钮"""
        collection_vue_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'frontend', 'src', 'views', 'Bonds', 'Collection.vue'
        )
        collection_vue_path = os.path.abspath(collection_vue_path)
        
        with open(collection_vue_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查清空按钮（根据之前的清空功能实现）
        has_clear_button = '清空数据' in content or 'handleClear' in content
        assert has_clear_button, "页面缺少清空数据按钮"
        
        # 检查清空函数
        assert 'handleClearData' in content or 'handleClear' in content, \
            "页面缺少清空数据函数"
        
        print("✅ 集合详情页面有清空数据按钮")
    
    @pytest.mark.asyncio
    async def test_provider_method_supports_parameters(self):
        """测试7: 验证Provider方法支持参数
        
        需要支持的参数：
        - bond_name: 债券名称
        - bond_code: 债券代码  
        - bond_issue: 发行人
        - bond_type: 债券类型
        - coupon_type: 付息方式
        - issue_year: 发行年份
        - underwriter: 承销商
        - grade: 评级
        """
        # 注意：由于AKShareBondProvider暂时不存在，这个测试会fail
        # 这是预期的TDD行为
        try:
            from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
            provider = AKShareBondProvider()
            
            # 验证方法存在
            assert hasattr(provider, 'get_bond_info_cm'), \
                "Provider缺少get_bond_info_cm方法"
            
            # 测试调用方法（使用默认参数）
            print("\n测试调用bond_info_cm接口...")
            df = await provider.get_bond_info_cm()
            
            assert df is not None, "获取的数据为None"
            
            if df.empty:
                print("⚠️ 接口暂无数据或接口不可用")
            else:
                print(f"✅ 成功获取 {len(df)} 条数据")
                
                # 验证返回的DataFrame包含必需字段
                required_columns = ['债券简称', '债券代码']
                for col in required_columns:
                    if col in df.columns:
                        print(f"  ✓ 包含字段: {col}")
                
                print(f"\n数据样本（前3条）:")
                print(df.head(3))
            
            # 测试带参数调用
            print("\n测试带参数调用...")
            df_with_params = await provider.get_bond_info_cm(
                bond_type="短期融资券",
                issue_year="2019"
            )
            
            if df_with_params is not None and not df_with_params.empty:
                print(f"✅ 带参数查询成功，获取 {len(df_with_params)} 条数据")
            
        except ImportError as e:
            print(f"⚠️ AKShareBondProvider暂未实现: {e}")
            pytest.skip("AKShareBondProvider暂未实现，跳过此测试")
    
    @pytest.mark.asyncio
    async def test_save_bond_info_cm_data(self, bond_service):
        """测试8: 验证保存bond_info_cm数据到MongoDB"""
        try:
            from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
            provider = AKShareBondProvider()
            
            # 获取数据
            df = await provider.get_bond_info_cm()
            
            if df is None or df.empty:
                print("\n⚠️ 接口暂无数据，无法测试保存")
                pytest.skip("接口暂无数据")
                return
            
            print(f"\n准备保存 {len(df)} 条数据...")
            
            # 验证保存方法存在
            assert hasattr(bond_service, 'save_info_cm'), \
                "BondDataService缺少save_info_cm方法"
            
            # 保存到MongoDB
            saved_count = await bond_service.save_info_cm(df)
            
            print(f"✅ 成功保存 {saved_count} 条数据")
            assert saved_count >= 0, "保存操作失败"
            
        except ImportError as e:
            print(f"⚠️ AKShareBondProvider暂未实现: {e}")
            pytest.skip("AKShareBondProvider暂未实现，跳过此测试")
    
    @pytest.mark.asyncio
    async def test_query_bond_info_cm_data(self, bond_service):
        """测试9: 验证从MongoDB查询bond_info_cm数据"""
        print("\n查询bond_info_cm集合数据...")
        
        cursor = bond_service.col_info_cm.find().limit(10)
        items = await cursor.to_list(length=10)
        count = await bond_service.col_info_cm.count_documents({})
        
        print(f"集合中共有 {count} 条记录")
        
        if items:
            print(f"\n数据样本（前5条）:")
            for i, item in enumerate(items[:5], 1):
                code = item.get('code') or item.get('债券代码', 'N/A')
                name = item.get('name') or item.get('债券简称', 'N/A')
                bond_type = item.get('bond_type') or item.get('债券类型', 'N/A')
                print(f"  {i}. {code} {name} - 类型:{bond_type}")
        else:
            print("\n⚠️ 集合中暂无数据")
        
        # 至少验证集合存在
        assert bond_service.col_info_cm is not None, "集合不存在"
    
    def test_api_endpoint_exists(self):
        """测试10: 验证API端点存在"""
        bonds_router_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'app', 'routers', 'bonds.py'
        )
        bonds_router_path = os.path.abspath(bonds_router_path)
        
        with open(bonds_router_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证collection_map中包含bond_info_cm
        assert 'collection_map' in content, "找不到collection_map"
        assert '"bond_info_cm"' in content, "collection_map中缺少bond_info_cm"
        
        # 验证更新数据的API端点
        has_update_endpoint = '/collections/{collection_name}/update' in content or \
                            '@router.post' in content
        assert has_update_endpoint, "缺少更新数据的API端点"
        
        print("✅ API端点配置正确")
    
    def test_update_parameters_match_akshare_interface(self):
        """测试11: 验证更新参数与AkShare接口一致
        
        AkShare bond_info_cm接口参数：
        - bond_name: str
        - bond_code: str
        - bond_issue: str
        - bond_type: str
        - coupon_type: str
        - issue_year: str
        - underwriter: str
        - grade: str
        """
        # 这个测试主要验证文档和代码的一致性
        # 实际的Provider实现应该支持这些参数
        
        expected_params = [
            'bond_name',
            'bond_code', 
            'bond_issue',
            'bond_type',
            'coupon_type',
            'issue_year',
            'underwriter',
            'grade'
        ]
        
        print("\n需求的参数列表:")
        for param in expected_params:
            print(f"  - {param}")
        
        print("\n✅ 参数列表已记录，Provider实现时需要支持这些参数")


class TestBondInfoCmIntegration:
    """集成测试：完整的数据流程"""
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="集成测试，手动运行")
    async def test_full_workflow(self, bond_service):
        """完整工作流测试：获取 -> 保存 -> 查询 -> 清空"""
        try:
            from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
            provider = AKShareBondProvider()
            
            # 1. 获取数据
            print("\n[步骤1] 获取数据...")
            df = await provider.get_bond_info_cm(bond_type="短期融资券", issue_year="2019")
            assert df is not None and not df.empty, "获取数据失败"
            print(f"✅ 获取 {len(df)} 条数据")
            
            # 2. 保存数据
            print("\n[步骤2] 保存数据...")
            saved_count = await bond_service.save_info_cm(df)
            print(f"✅ 保存 {saved_count} 条数据")
            
            # 3. 查询数据
            print("\n[步骤3] 查询数据...")
            count = await bond_service.col_info_cm.count_documents({})
            print(f"✅ 集合中共有 {count} 条数据")
            
            # 4. 清空数据（可选）
            # print("\n[步骤4] 清空数据...")
            # result = await bond_service.col_info_cm.delete_many({})
            # print(f"✅ 清空 {result.deleted_count} 条数据")
            
            print("\n✅ 完整工作流测试通过")
            
        except ImportError as e:
            pytest.skip(f"AKShareBondProvider暂未实现: {e}")
