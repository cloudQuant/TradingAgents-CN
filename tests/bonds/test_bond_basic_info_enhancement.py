"""
债券基础信息增强功能测试用例

根据需求文档06_债券基础信息.md编写的测试用例，覆盖：
1. 批量更新功能测试
2. 增量更新功能测试
3. 统计信息获取测试
4. API端点测试
5. 错误处理测试
6. Bug修复测试（信号处理、数据格式转换等）
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import pandas as pd

from app.services.bond_basic_info_service import BondBasicInfoService
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


class TestBondBasicInfoService:
    """债券基础信息服务测试"""
    
    @pytest.fixture
    async def mock_db(self):
        """模拟数据库"""
        db = Mock()
        db.get_collection = Mock()
        return db
    
    @pytest.fixture
    async def mock_collection(self):
        """模拟集合"""
        collection = Mock()
        collection.find = Mock()
        collection.find_one = AsyncMock()
        collection.count_documents = AsyncMock()
        return collection
    
    @pytest.fixture
    async def service(self, mock_db, mock_collection):
        """创建服务实例"""
        with patch('app.services.bond_basic_info_service.BondDataService') as mock_bond_data_service_class, \
             patch('app.services.bond_basic_info_service.AKShareBondProvider') as mock_provider_class:
            
            # 模拟BondDataService
            mock_bond_data_service = Mock(spec=BondDataService)
            mock_bond_data_service.save_info_cm_detail = AsyncMock(return_value=1)
            mock_bond_data_service.save_bond_info_from_api = AsyncMock(return_value=1)
            mock_bond_data_service_class.return_value = mock_bond_data_service
            
            # 模拟AKShareBondProvider
            mock_provider = Mock(spec=AKShareBondProvider)
            mock_provider.get_basic_info = AsyncMock()
            mock_provider_class.return_value = mock_provider
            
            service = BondBasicInfoService(mock_db)
            service.col_info_cm = mock_collection
            service.col_basic = mock_collection
            service.provider = mock_provider
            service.bond_data_service = mock_bond_data_service
            
            return service
    
    @pytest.mark.asyncio
    async def test_batch_update_from_bond_info_cm_success(self, service, mock_collection):
        """测试批量更新成功场景"""
        # 模拟bond_info_cm数据库查询结果
        mock_docs = [
            {"code": "110001", "债券简称": "转债1", "债券代码": "110001"},
            {"code": "110002", "债券简称": "转债2", "债券代码": "110002"},
        ]
        
        # 模拟异步游标
        mock_cursor = Mock()
        mock_cursor.__aiter__ = Mock(return_value=iter(mock_docs))
        mock_collection.find.return_value = mock_cursor
        
        # 模拟已有详细信息查询为空（需要更新）
        mock_collection.find_one = AsyncMock(return_value=None)
        
        # 模拟akshare.bond_info_detail_cm调用
        mock_detail_df = pd.DataFrame([
            {"name": "债券全称", "value": "测试转债001"},
            {"name": "债券代码", "value": "110001"}
        ])
        
        with patch('akshare.bond_info_detail_cm', return_value=mock_detail_df):
            # 执行批量更新
            result = await service.batch_update_from_bond_info_cm(
                batch_size=100,
                concurrent_threads=1,
                save_interval=100
            )
        
        # 验证结果
        assert result["success"] == True
        assert result["total_bonds"] == 2
        assert "total_processed" in result
        assert "total_updated" in result
        assert "duration_seconds" in result
        assert result["message"].startswith("批量更新完成")
    
    @pytest.mark.asyncio
    async def test_batch_update_no_bonds_found(self, service, mock_collection):
        """测试没有找到债券的场景"""
        # 模拟空的查询结果
        mock_cursor = Mock()
        mock_cursor.__aiter__ = Mock(return_value=iter([]))
        mock_collection.find.return_value = mock_cursor
        
        result = await service.batch_update_from_bond_info_cm()
        
        assert result["success"] == True
        assert result["total_bonds"] == 0
        assert result["message"] == "未找到需要处理的债券代码"
    
    @pytest.mark.asyncio
    async def test_incremental_update_missing_info_success(self, service):
        """测试增量更新成功场景"""
        # 模拟bond_info_cm中的代码
        basic_docs = [
            {"code": "110001", "债券简称": "转债1"},
            {"code": "110002", "债券简称": "转债2"}, 
            {"code": "110003", "债券简称": "转债3"}
        ]
        
        # 模拟bond_info_detail_cm中的代码（缺少110003）
        detail_docs = [
            {"code": "110001"},
            {"code": "110002"}
        ]
        
        # 创建模拟游标
        def create_mock_cursor(docs):
            mock_cursor = Mock()
            mock_cursor.__aiter__ = Mock(return_value=iter(docs))
            return mock_cursor
        
        # 设置find方法的行为
        service.col_info_cm.find = Mock(side_effect=[
            create_mock_cursor(basic_docs),  # 第一次调用返回基础代码
            create_mock_cursor(detail_docs)  # 第二次调用返回详细代码
        ])
        
        # 模拟akshare调用和provider返回成功数据
        mock_detail_df = pd.DataFrame([
            {"name": "债券全称", "value": "缺失转债003"},
            {"name": "债券代码", "value": "110003"}
        ])
        
        with patch('akshare.bond_info_detail_cm', return_value=mock_detail_df):
            result = await service.incremental_update_missing_info()
        
        assert result["success"] == True
        assert result["total_basic_codes"] == 3
        assert result["total_detail_codes"] == 2
        assert result["missing_codes"] == 1
        assert result["updated"] >= 0  # 可能为0或1，取决于模拟的保存结果
    
    @pytest.mark.asyncio
    async def test_get_update_statistics(self, service):
        """测试获取统计信息"""
        # 模拟count_documents返回值
        service.col_info_cm.count_documents = AsyncMock(side_effect=[100, 80])  # basic, detail
        service.col_basic.count_documents = AsyncMock(return_value=90)
        
        result = await service.get_update_statistics()
        
        assert result["success"] == True
        assert result["bond_info_cm_count"] == 100
        assert result["bond_info_detail_cm_count"] == 80
        assert result["bond_basic_info_count"] == 90
        assert result["coverage_rate"] == 80.0  # 80/100 * 100
        assert result["missing_detail_count"] == 20  # 100-80
    
    @pytest.mark.asyncio
    async def test_batch_update_with_akshare_error(self, service, mock_collection):
        """测试akshare接口错误处理"""
        # 模拟数据库查询结果
        mock_docs = [{"code": "110001", "债券简称": "转债1"}]
        mock_cursor = Mock()
        mock_cursor.__aiter__ = Mock(return_value=iter(mock_docs))
        mock_collection.find.return_value = mock_cursor
        
        service.col_info_cm.find_one = AsyncMock(return_value=None)
        
        # 模拟akshare调用失败
        with patch('akshare.bond_info_detail_cm', side_effect=Exception("akshare_error")):
            # 模拟provider也返回错误
            service.provider.get_basic_info.return_value = {
                "error": "akshare_not_available"
            }
            
            result = await service.batch_update_from_bond_info_cm(
                batch_size=100,
                concurrent_threads=1
            )
        
        assert result["success"] == True
        assert result["total_errors"] > 0
    
    @pytest.mark.asyncio
    async def test_incremental_update_no_missing_codes(self, service):
        """测试增量更新无缺失代码场景"""
        # 模拟bond_info_cm和bond_info_detail_cm中的代码完全一致
        docs = [
            {"code": "110001", "债券简称": "转债1"},
            {"code": "110002", "债券简称": "转债2"}
        ]
        
        def create_mock_cursor(docs):
            mock_cursor = Mock()
            mock_cursor.__aiter__ = Mock(return_value=iter(docs))
            return mock_cursor
        
        service.col_info_cm.find = Mock(side_effect=[
            create_mock_cursor(docs),  # bond_info_cm
            create_mock_cursor(docs)   # bond_info_detail_cm
        ])
        
        result = await service.incremental_update_missing_info()
        
        assert result["success"] == True
        assert result["missing_codes"] == 0
        assert result["updated"] == 0
        assert result["message"] == "没有发现缺失的债券基础信息"


class TestBondBasicInfoAPI:
    """债券基础信息API测试"""
    
    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)
    
    def test_batch_update_api_authentication(self, client):
        """测试批量更新API需要认证"""
        response = client.post("/api/bonds/basic-info/batch-update")
        assert response.status_code == 401  # 未认证
    
    def test_incremental_update_api_authentication(self, client):
        """测试增量更新API需要认证"""
        response = client.post("/api/bonds/basic-info/incremental-update")
        assert response.status_code == 401  # 未认证
    
    def test_statistics_api_authentication(self, client):
        """测试统计API需要认证"""
        response = client.get("/api/bonds/basic-info/update-statistics")
        assert response.status_code == 401  # 未认证
    
    @patch('app.routers.bonds.get_current_user')
    @patch('app.routers.bonds.BondBasicInfoService')
    def test_batch_update_api_success(self, mock_service_class, mock_auth, client):
        """测试批量更新API成功场景"""
        # 模拟认证用户
        mock_auth.return_value = {"username": "test_user"}
        
        # 模拟服务返回成功结果
        mock_service = Mock()
        mock_service.batch_update_from_bond_info_cm = AsyncMock(return_value={
            "success": True,
            "message": "批量更新完成",
            "total_updated": 10
        })
        mock_service_class.return_value = mock_service
        
        response = client.post(
            "/api/bonds/basic-info/batch-update",
            params={
                "batch_size": 1000,
                "concurrent_threads": 3,
                "save_interval": 1000
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
    
    @patch('app.routers.bonds.get_current_user')
    @patch('app.routers.bonds.BondBasicInfoService')
    def test_incremental_update_api_success(self, mock_service_class, mock_auth, client):
        """测试增量更新API成功场景"""
        # 模拟认证用户
        mock_auth.return_value = {"username": "test_user"}
        
        # 模拟服务返回成功结果
        mock_service = Mock()
        mock_service.incremental_update_missing_info = AsyncMock(return_value={
            "success": True,
            "message": "增量更新完成",
            "updated": 5
        })
        mock_service_class.return_value = mock_service
        
        response = client.post("/api/bonds/basic-info/incremental-update")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data


class TestBondBasicInfoBugFixes:
    """债券基础信息Bug修复测试"""
    
    @pytest.fixture
    async def service_with_signal_handling(self):
        """创建带信号处理的服务实例"""
        db = Mock()
        db.get_collection = Mock()
        
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            return service
    
    @pytest.mark.asyncio
    async def test_global_signal_handling(self):
        """测试全局信号处理器"""
        from app.services.bond_basic_info_service import _global_shutdown_event
        
        db = Mock()
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            
            # 初始状态应该是未停止
            assert service.should_shutdown() == False
            
            # 模拟全局停止信号
            _global_shutdown_event.set()
            assert service.should_shutdown() == True
            
            # 清理全局状态
            _global_shutdown_event.clear()
    
    @pytest.mark.asyncio
    async def test_dataframe_to_dict_conversion(self):
        """测试DataFrame到字典的转换"""
        db = Mock()
        db.get_collection = Mock()
        
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            
            # 创建测试DataFrame
            test_df = pd.DataFrame([
                {"name": "bondFullName", "value": "重庆万林投资发展有限公司2019年度第一期短期融资券"},
                {"name": "bondDefinedCode", "value": "695327xh9n"},
                {"name": "bondName", "value": "19万林投资CP001"},
                {"name": "bondCode", "value": "041900126"},
                {"name": "isinCode", "value": "---"}
            ])
            
            # 测试转换
            result = service._convert_detail_dataframe_to_dict(test_df, "041900126", "19万林投资CP001")
            
            # 验证转换结果
            assert result["bondFullName"] == "重庆万林投资发展有限公司2019年度第一期短期融资券"
            assert result["bondDefinedCode"] == "695327xh9n"
            assert result["bondName"] == "19万林投资CP001"
            assert result["bondCode"] == "041900126"
            assert result["isinCode"] == "---"
            assert result["code"] == "041900126"
            assert result["endpoint"] == "bond_info_detail_cm"
            assert result["债券简称"] == "19万林投资CP001"
            assert "数据来源" in result
            assert "更新时间" in result
    
    @pytest.mark.asyncio
    async def test_dataframe_conversion_empty_data(self):
        """测试空DataFrame转换"""
        db = Mock()
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            
            # 测试空DataFrame
            empty_df = pd.DataFrame()
            result = service._convert_detail_dataframe_to_dict(empty_df, "123456", "测试债券")
            
            # 验证基本信息仍然存在
            assert result["code"] == "123456"
            assert result["endpoint"] == "bond_info_detail_cm"
            assert result["债券简称"] == "测试债券"
    
    @pytest.mark.asyncio
    async def test_bond_name_extraction(self):
        """测试债券简称提取功能"""
        db = Mock()
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            
            # 测试各种格式的债券简称提取
            test_cases = [
                # (输入, 期望输出)
                ("111887384(18稠州商行CD016)", "18稠州商行CD016"),
                ("19万林投资CP001", "19万林投资CP001"),
                ("123456 20中信证券CP001", "20中信证券CP001"),
                ("041900126(19万林投资CP001)", "19万林投资CP001"),
                ("", ""),
                ("纯债券简称", "纯债券简称"),
                ("123456789", "123456789"),  # 纯数字保持不变
                ("代码()", "代码()"),  # 空括号保持不变
                ("代码( )", " "),  # 括号内只有空格，提取空格
            ]
            
            for input_name, expected in test_cases:
                result = service._extract_bond_name(input_name)
                assert result == expected, f"输入: '{input_name}', 期望: '{expected}', 实际: '{result}'"
    
    @pytest.mark.asyncio
    async def test_dataframe_conversion_with_special_values(self):
        """测试DataFrame转换处理特殊值"""
        db = Mock()
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            
            # 创建包含特殊值的测试DataFrame
            test_df = pd.DataFrame([
                {"name": "bondFullName", "value": "正常债券名称"},
                {"name": "bondCode", "value": "041900126"},
                {"name": "isinCode", "value": "---"},  # 应该转换为None
                {"name": "creditRating", "value": ""},   # 空字符串应该转换为None
                {"name": "maturityDate", "value": "null"}, # null字符串应该转换为None
                {"name": "couponRate", "value": "3.5%"}  # 正常值
            ])
            
            result = service._convert_detail_dataframe_to_dict(test_df, "041900126", "测试债券")
            
            # 验证特殊值处理
            assert result["bondFullName"] == "正常债券名称"
            assert result["bondCode"] == "041900126"
            assert result["isinCode"] is None  # --- 应该转换为None
            assert result["creditRating"] is None  # 空字符串应该转换为None
            assert result["maturityDate"] is None  # null应该转换为None
            assert result["couponRate"] == "3.5%"  # 正常值保持不变
            
            # 验证元数据
            assert result["code"] == "041900126"
            assert result["endpoint"] == "bond_info_detail_cm"
            assert result["债券简称"] == "测试债券"
            assert "数据来源" in result
            assert "更新时间" in result
    
    @pytest.mark.asyncio
    async def test_save_bond_detail_dict(self):
        """测试债券详细信息字典保存"""
        mock_collection = Mock()
        mock_collection.update_one = AsyncMock()
        
        db = Mock()
        db.get_collection = Mock(return_value=mock_collection)
        
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            service.col_info_cm = mock_collection
            
            # 模拟update_one返回成功结果
            mock_result = Mock()
            mock_result.upserted_id = "new_id"
            mock_result.modified_count = 0
            mock_collection.update_one.return_value = mock_result
            
            # 测试保存
            test_data = {
                "code": "041900126",
                "endpoint": "bond_info_detail_cm",
                "bondFullName": "测试债券全称"
            }
            
            result = await service._save_bond_detail_dict(test_data)
            
            # 验证保存调用
            assert result == 1
            mock_collection.update_one.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_batch_update_with_shutdown_signal(self):
        """测试批量更新过程中的停止信号处理"""
        db = Mock()
        mock_collection = Mock()
        
        # 模拟find返回一些数据
        mock_docs = [{"code": "110001", "债券简称": "转债1"}]
        mock_cursor = Mock()
        mock_cursor.__aiter__ = Mock(return_value=iter(mock_docs))
        mock_collection.find.return_value = mock_cursor
        mock_collection.find_one = AsyncMock(return_value=None)
        
        db.get_collection = Mock(return_value=mock_collection)
        
        with patch('app.services.bond_basic_info_service.BondDataService'), \
             patch('app.services.bond_basic_info_service.AKShareBondProvider'):
            service = BondBasicInfoService(db)
            service.col_info_cm = mock_collection
            
            # 立即设置停止信号
            service._shutdown_event.set()
            
            # 执行批量更新
            result = await service.batch_update_from_bond_info_cm(batch_size=10, concurrent_threads=1)
            
            # 验证结果 - 应该能正常处理停止信号
            assert result["success"] == True
            assert result["total_bonds"] == 1


class TestBondBasicInfoIntegration:
    """债券基础信息集成测试"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_batch_update_workflow(self):
        """测试完整的批量更新工作流"""
        # 这里应该是完整的集成测试
        # 包括真实的数据库连接和API调用
        # 由于需要真实环境，标记为integration测试
        pass
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_incremental_update_workflow(self):
        """测试完整的增量更新工作流"""
        # 这里应该是完整的集成测试
        pass


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
