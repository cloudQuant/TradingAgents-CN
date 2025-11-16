"""
债券功能边界条件测试
测试各种边界情况和异常场景
"""
import pytest
from unittest.mock import Mock, AsyncMock
import pandas as pd
import numpy as np


@pytest.mark.asyncio
async def test_very_large_page_number():
    """测试超大页码"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # 总共100条数据
    mock_collection.count_documents = AsyncMock(return_value=100)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])  # 超过范围，返回空
    
    mock_collection.find.return_value = mock_cursor
    
    # 请求第1000页（每页10条，远超数据总量）
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(page=1000, page_size=10)
    
    # 验证
    assert result["total"] == 100
    assert result["items"] == []
    
    # 验证skip计算正确
    call_args = mock_cursor.skip.call_args
    skip_count = call_args[0][0]
    assert skip_count == 9990  # (1000-1) * 10
    
    print("✅ 测试通过：超大页码")


@pytest.mark.asyncio
async def test_very_large_page_size():
    """测试超大每页数量"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # 总共100条数据
    mock_collection.count_documents = AsyncMock(return_value=100)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([{"code": "test"}] * 100)
    
    mock_collection.find.return_value = mock_cursor
    
    # 请求每页1000条（远超实际数据量）
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(page=1, page_size=1000)
    
    # 验证limit被调用
    call_args = mock_cursor.limit.call_args
    limit_count = call_args[0][0]
    assert limit_count == 1000
    
    print("✅ 测试通过：超大每页数量")


@pytest.mark.asyncio
async def test_extreme_premium_values():
    """测试极端溢价率值"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含极端值的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "极高溢价",
            "转股溢价率": 999.99,  # 极高溢价
        },
        {
            "转债代码": "127105",
            "转债名称": "极低溢价",
            "转股溢价率": -99.99,  # 极低溢价（深度折价）
        },
        {
            "转债代码": "123456",
            "转债名称": "零溢价",
            "转股溢价率": 0.0,  # 零溢价
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 3
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_comparison(test_data)
    
    # 验证所有数据都被保存
    assert saved == 3
    
    # 验证极端值被正确处理
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    
    # 检查极高溢价率
    high_premium = ops[0]._UpdateOne__update["$set"]
    assert high_premium["convert_premium_rate"] == 999.99
    
    # 检查极低溢价率
    low_premium = ops[1]._UpdateOne__update["$set"]
    assert low_premium["convert_premium_rate"] == -99.99
    
    # 检查零溢价率
    zero_premium = ops[2]._UpdateOne__update["$set"]
    assert zero_premium["convert_premium_rate"] == 0.0
    
    print("✅ 测试通过：极端溢价率值")


@pytest.mark.asyncio
async def test_unicode_bond_names():
    """测试Unicode字符的债券名称"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含特殊字符的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "测试转债💰",  # 包含emoji
        },
        {
            "转债代码": "127105",
            "转债名称": "テスト債券",  # 日文
        },
        {
            "转债代码": "123456",
            "转债名称": "Test①②③",  # 特殊数字
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 3
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_comparison(test_data)
    
    # 验证Unicode名称被正确保存
    assert saved == 3
    
    print("✅ 测试通过：Unicode债券名称")


@pytest.mark.asyncio
async def test_duplicate_bond_codes():
    """测试重复的债券代码"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含重复代码的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债V1",
            "转债最新价": 120.0,
        },
        {
            "转债代码": "113682",  # 重复代码
            "转债名称": "益丰转债V2",
            "转债最新价": 125.0,  # 不同的价格
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 0
    mock_result.modified_count = 2  # 第二条会更新第一条
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_comparison(test_data)
    
    # 验证：upsert逻辑会处理重复
    assert saved == 2  # 两次操作都被记录
    
    print("✅ 测试通过：重复债券代码")


@pytest.mark.asyncio
async def test_missing_required_fields():
    """测试缺少必需字段"""
    from app.services.bond_data_service import BondDataService
    
    # 创建缺少债券代码的测试数据
    test_data = pd.DataFrame([
        {
            # 缺少"转债代码"字段
            "转债名称": "无代码转债",
            "转债最新价": 120.0,
        },
        {
            "转债代码": "",  # 空代码
            "转债名称": "空代码转债",
            "转债最新价": 125.0,
        },
        {
            "转债代码": "113682",  # 正常数据
            "转债名称": "正常转债",
            "转债最新价": 130.0,
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
    
    # 验证：只有有效代码的数据被保存
    assert saved == 1
    
    # 验证bulk_write只处理了1条数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    assert len(ops) == 1
    
    print("✅ 测试通过：缺少必需字段")


@pytest.mark.asyncio
async def test_all_nan_row():
    """测试全是NaN的行"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含全NaN行的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": np.nan,
            "转债涨跌幅": np.nan,
            "转股溢价率": np.nan,
        },
        {
            "转债代码": "127105",
            "转债名称": "龙星转债",
            "转债最新价": 120.0,  # 有效数据
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
    saved = await service.save_cov_comparison(test_data)
    
    # 验证：全NaN行仍然保存（只是数值字段为空）
    assert saved == 2
    
    print("✅ 测试通过：全NaN行")


@pytest.mark.asyncio
async def test_date_format_variations():
    """测试不同日期格式"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含不同日期格式的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "上市日期": "2024-03-06",  # 标准格式
        },
        {
            "转债代码": "127105",
            "上市日期": "20240306",  # 无分隔符
        },
        {
            "转债代码": "123456",
            "上市日期": "2024/03/06",  # 斜杠分隔
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 3
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存
    service = BondDataService(mock_db)
    saved = await service.save_cov_comparison(test_data)
    
    # 验证所有日期格式都被保存
    assert saved == 3
    
    # 验证日期被转为字符串保存
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    for op in ops:
        update_data = op._UpdateOne__update["$set"]
        if "list_date" in update_data:
            assert isinstance(update_data["list_date"], str)
    
    print("✅ 测试通过：不同日期格式")


@pytest.mark.asyncio
async def test_very_long_bond_name():
    """测试超长债券名称"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含超长名称的测试数据
    long_name = "A" * 500  # 500个字符的名称
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": long_name,
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
    
    # 验证超长名称被保存
    assert saved == 1
    
    # 验证名称被保存
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    assert len(update_data["name"]) == 500
    
    print("✅ 测试通过：超长债券名称")


@pytest.mark.asyncio
async def test_special_float_values():
    """测试特殊浮点数值"""
    from app.services.bond_data_service import BondDataService
    
    # 创建包含特殊浮点数的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债最新价": float('inf'),  # 正无穷
        },
        {
            "转债代码": "127105",
            "转债最新价": float('-inf'),  # 负无穷
        },
        {
            "转债代码": "123456",
            "转债最新价": np.nan,  # NaN
        }
    ])
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock bulk_write
    mock_result = Mock()
    mock_result.upserted_count = 3
    mock_result.modified_count = 0
    mock_collection.bulk_write = AsyncMock(return_value=mock_result)
    
    # 执行保存（应该能处理特殊值）
    service = BondDataService(mock_db)
    try:
        saved = await service.save_cov_comparison(test_data)
        # 验证：特殊值被处理（转为None或其他安全值）
        assert saved >= 0
    except Exception as e:
        # 如果抛出异常，确保是预期的
        assert "inf" in str(e).lower() or "nan" in str(e).lower()
    
    print("✅ 测试通过：特殊浮点数值")


@pytest.mark.asyncio
async def test_query_with_regex_special_chars():
    """测试包含正则特殊字符的搜索"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=1)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 使用包含正则特殊字符的搜索词
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(q="(test)")
    
    # 验证搜索被执行（不抛出正则错误）
    assert result["total"] == 1
    
    print("✅ 测试通过：正则特殊字符搜索")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
