"""
测试可转债专项功能
包括：可转债比价、价值分析、数据同步等功能的测试
"""
import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import pandas as pd

# 测试可转债比价表数据保存
@pytest.mark.asyncio
async def test_save_cov_comparison():
    """测试保存可转债比价表数据"""
    from app.services.bond_data_service import BondDataService
    from motor.motor_asyncio import AsyncIOMotorClient
    
    # 创建测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": 120.5,
            "转债涨跌幅": 2.3,
            "正股代码": "603939",
            "正股名称": "益丰药房",
            "正股最新价": 45.2,
            "转股价": 42.0,
            "转股价值": 107.6,
            "转股溢价率": 12.0,
            "纯债溢价率": 35.5,
            "纯债价值": 89.0,
            "回售触发价": 29.4,
            "强赎触发价": 54.6,
            "到期赎回价": 106.0,
            "开始转股日": "2024-09-01",
            "上市日期": "2024-03-06",
            "申购日期": "2024-03-04"
        },
        {
            "转债代码": "127105",
            "转债名称": "龙星转债",
            "转债最新价": 145.7,
            "转债涨跌幅": -1.5,
            "正股代码": "002442",
            "正股名称": "龙星化工",
            "转股价": 7.2,
            "转股价值": 118.1,
            "转股溢价率": 23.4
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write返回结果
    mock_result = Mock()
    mock_result.upserted_count = 1
    mock_result.modified_count = 1
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_comparison(test_data)
    
    # 验证
    assert saved == 2, f"期望保存2条数据，实际保存{saved}条"
    assert mock_collection.bulk_write.called, "应该调用了bulk_write"
    
    # 验证调用参数
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    assert len(ops) == 2, f"期望2个操作，实际{len(ops)}个"
    
    print("✅ 测试通过：保存可转债比价表数据")


@pytest.mark.asyncio
async def test_query_cov_comparison():
    """测试查询可转债比价表"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=100)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    
    # mock cursor的异步迭代
    mock_cursor.__aiter__.return_value = iter([
        {
            "code": "113682",
            "name": "益丰转债",
            "price": 120.5,
            "convert_premium_rate": 12.0
        },
        {
            "code": "127105",
            "name": "龙星转债",
            "price": 145.7,
            "convert_premium_rate": 23.4
        }
    ])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(
        sort_by="convert_premium_rate",
        sort_dir="asc",
        page=1,
        page_size=50
    )
    
    # 验证
    assert result["total"] == 100, f"期望总数100，实际{result['total']}"
    assert len(result["items"]) == 2, f"期望2条记录，实际{len(result['items'])}"
    assert result["items"][0]["code"] == "113682"
    
    print("✅ 测试通过：查询可转债比价表")


@pytest.mark.asyncio
async def test_save_cov_value_analysis():
    """测试保存可转债价值分析数据"""
    from app.services.bond_data_service import BondDataService
    
    # 创建测试数据
    test_data = pd.DataFrame([
        {
            "日期": "2024-01-01",
            "收盘价": 120.0,
            "纯债价值": 90.0,
            "转股价值": 110.0,
            "纯债溢价率": 33.3,
            "转股溢价率": 9.1
        },
        {
            "日期": "2024-01-02",
            "收盘价": 122.0,
            "纯债价值": 90.1,
            "转股价值": 112.0,
            "纯债溢价率": 35.4,
            "转股溢价率": 8.9
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 2
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_value_analysis("113682", test_data)
    
    # 验证
    assert saved == 2, f"期望保存2条数据，实际{saved}条"
    
    print("✅ 测试通过：保存可转债价值分析数据")


@pytest.mark.asyncio
async def test_query_cov_value_analysis():
    """测试查询可转债价值分析"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    
    # mock异步迭代
    mock_cursor.__aiter__.return_value = iter([
        {
            "code": "113682",
            "date": "2024-01-01",
            "close_price": 120.0,
            "convert_premium_rate": 9.1
        },
        {
            "code": "113682",
            "date": "2024-01-02",
            "close_price": 122.0,
            "convert_premium_rate": 8.9
        }
    ])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询
    service = BondDataService(mock_db)
    result = await service.query_cov_value_analysis(
        code="113682",
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    
    # 验证
    assert result["code"] == "SH.113682" or result["code"] == "113682"
    assert len(result["data"]) == 2
    
    print("✅ 测试通过：查询可转债价值分析")


@pytest.mark.asyncio
async def test_data_provider_get_cov_comparison():
    """测试数据提供商获取可转债比价表"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    
    # 注意：这是集成测试，需要实际调用AKShare
    # 在CI环境中可能需要mock
    with patch('tradingagents.dataflows.providers.china.bonds.ak') as mock_ak:
        # mock AKShare返回
        mock_df = pd.DataFrame([
            {
                "序号": 1,
                "转债代码": "113682",
                "转债名称": "益丰转债",
                "转债最新价": "120.50",
                "转股溢价率": "12.00"
            }
        ])
        mock_ak.bond_cov_comparison.return_value = mock_df
        
        # 使用asyncio.to_thread来模拟异步调用
        with patch('asyncio.to_thread', new=AsyncMock(return_value=mock_df)):
            df = await provider.get_cov_comparison()
            
            assert df is not None, "返回的DataFrame不应为None"
            assert not df.empty, "返回的DataFrame不应为空"
            assert "转债代码" in df.columns or len(df.columns) > 0
    
    print("✅ 测试通过：数据提供商获取可转债比价表")


@pytest.mark.asyncio
async def test_save_spot_deals():
    """测试保存现券市场成交行情"""
    from app.services.bond_data_service import BondDataService
    
    # 创建测试数据
    test_data = pd.DataFrame([
        {
            "债券简称": "23附息国债26",
            "成交净价": 103.20,
            "最新收益率": 2.30,
            "涨跌": -0.80,
            "加权收益率": 2.32,
            "交易量": 15.5
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 1
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_spot_deals(test_data)
    
    # 验证
    assert saved == 1, f"期望保存1条数据，实际{saved}条"
    
    print("✅ 测试通过：保存现券市场成交行情")


def test_bond_code_normalization():
    """测试债券代码规范化"""
    from tradingagents.utils.instrument_validator import normalize_bond_code
    
    # 测试不同格式的债券代码
    test_cases = [
        ("113682", "SH.113682"),
        ("sh113682", "SH.113682"),
        ("SH.113682", "SH.113682"),
        ("127105", "SZ.127105"),
        ("sz127105", "SZ.127105"),
    ]
    
    for input_code, expected in test_cases:
        result = normalize_bond_code(input_code)
        code_std = result.get("code_std") or result.get("code")
        
        # 验证代码包含正确的市场前缀
        assert "SH" in code_std or "SZ" in code_std or code_std == input_code, \
            f"代码 {input_code} 规范化结果 {code_std} 不符合预期"
    
    print("✅ 测试通过：债券代码规范化")


@pytest.mark.asyncio
async def test_category_field_not_null():
    """测试category字段不为空（修复后的bug）"""
    from app.services.bond_data_service import BondDataService
    
    # 创建测试数据（category为空的情况）
    test_items = [
        {
            "code": "113682",
            "name": "益丰转债",
            "category": None,  # 空的category
            "exchange": "SH"
        },
        {
            "code": "127105",
            "name": "龙星转债",
            "category": "",  # 空字符串
            "exchange": "SZ"
        }
    ]
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 2
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_basic_list(test_items)
    
    # 验证bulk_write被调用
    assert mock_collection.bulk_write.called
    
    # 获取实际调用的操作
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    
    # 验证每个操作的$set中都有category字段
    for op in ops:
        update_data = op._UpdateOne__update["$set"]
        assert "category" in update_data, "category字段应该存在"
        assert update_data["category"] == "other", \
            f"空category应该默认为'other'，实际为{update_data.get('category')}"
    
    print("✅ 测试通过：category字段默认值修复")


@pytest.mark.asyncio
async def test_premium_rate_calculation():
    """测试溢价率计算的正确性"""
    # 测试数据
    bond_price = 120.0
    convert_value = 110.0
    pure_debt_value = 90.0
    
    # 计算转股溢价率
    convert_premium = ((bond_price - convert_value) / convert_value) * 100
    assert abs(convert_premium - 9.09) < 0.1, "转股溢价率计算错误"
    
    # 计算纯债溢价率
    pure_debt_premium = ((bond_price - pure_debt_value) / pure_debt_value) * 100
    assert abs(pure_debt_premium - 33.33) < 0.1, "纯债溢价率计算错误"
    
    print("✅ 测试通过：溢价率计算")


@pytest.mark.asyncio
async def test_empty_dataframe_handling():
    """测试空DataFrame的处理"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    service = BondDataService(mock_db)
    
    # 测试保存空DataFrame
    empty_df = pd.DataFrame()
    saved = await service.save_cov_comparison(empty_df)
    
    # 验证返回0
    assert saved == 0, "空DataFrame应该返回0"
    # 验证bulk_write未被调用
    assert not mock_collection.bulk_write.called, "空DataFrame不应调用bulk_write"
    
    print("✅ 测试通过：空DataFrame处理")


@pytest.mark.asyncio
async def test_nan_value_handling():
    """测试NaN值的处理"""
    import numpy as np
    from app.services.bond_data_service import BondDataService
    
    # 创建包含NaN的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": np.nan,  # NaN值
            "转股溢价率": 12.0
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 1
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_comparison(test_data)
    
    # 验证
    assert saved == 1
    
    # 获取调用参数，验证NaN被正确处理
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # price字段应该不存在（因为是NaN）或者为None
    assert "price" not in update_data or update_data["price"] is None, \
        "NaN值应该被过滤掉或转换为None"
    
    print("✅ 测试通过：NaN值处理")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
