"""
测试债券功能的Bug修复
验证已修复的bug不会再次出现
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import pandas as pd
import numpy as np


@pytest.mark.asyncio
async def test_zero_value_not_filtered():
    """
    Bug修复测试：0值不应被过滤掉
    
    问题：之前使用 `float(value or 0)` 会将0值判断为False
    修复：使用safe_float函数正确处理0值
    """
    from app.services.bond_data_service import BondDataService
    
    # 创建包含0值的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": 0.0,  # 价格为0（虽然不常见，但应该被保存）
            "转债涨跌幅": 0.0,  # 涨跌幅为0（很常见）
            "转股溢价率": 0.0,  # 溢价率为0（表示等价）
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
    
    # 验证保存成功
    assert saved == 1
    
    # 获取实际调用的数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # 关键验证：0值应该被保存
    assert "price" in update_data, "price字段应该存在"
    assert update_data["price"] == 0.0, f"price应该是0.0，实际是{update_data.get('price')}"
    
    assert "change_pct" in update_data, "change_pct字段应该存在"
    assert update_data["change_pct"] == 0.0, f"change_pct应该是0.0，实际是{update_data.get('change_pct')}"
    
    assert "convert_premium_rate" in update_data, "convert_premium_rate字段应该存在"
    assert update_data["convert_premium_rate"] == 0.0, \
        f"convert_premium_rate应该是0.0，实际是{update_data.get('convert_premium_rate')}"
    
    print("✅ Bug修复验证通过：0值被正确保存")


@pytest.mark.asyncio
async def test_nan_value_correctly_filtered():
    """
    Bug修复测试：NaN值应被正确过滤
    
    验证：NaN值应该被转换为None并过滤掉
    """
    from app.services.bond_data_service import BondDataService
    
    # 创建包含NaN的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": np.nan,  # NaN值
            "转债涨跌幅": 2.5,
            "转股溢价率": np.nan,  # NaN值
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
    
    # 验证保存成功
    assert saved == 1
    
    # 获取实际调用的数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # 关键验证：NaN值应该被过滤掉
    assert "price" not in update_data, "NaN的price字段不应该存在"
    assert "convert_premium_rate" not in update_data, "NaN的convert_premium_rate字段不应该存在"
    
    # 有效值应该被保存
    assert "change_pct" in update_data, "有效的change_pct字段应该存在"
    assert update_data["change_pct"] == 2.5
    
    print("✅ Bug修复验证通过：NaN值被正确过滤")


@pytest.mark.asyncio
async def test_negative_values_preserved():
    """
    Bug修复测试：负值应该被正确保存
    
    验证：负的涨跌幅、负的溢价率等应该被保存
    """
    from app.services.bond_data_service import BondDataService
    
    # 创建包含负值的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债涨跌幅": -5.5,  # 负的涨跌幅
            "转股溢价率": -2.0,  # 负的溢价率（折价）
            "涨跌": -0.8,  # 负的涨跌
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
    
    # 验证保存成功
    assert saved == 1
    
    # 获取实际调用的数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # 关键验证：负值应该被保存
    assert update_data["change_pct"] == -5.5, f"change_pct应该是-5.5，实际是{update_data.get('change_pct')}"
    assert update_data["convert_premium_rate"] == -2.0, \
        f"convert_premium_rate应该是-2.0，实际是{update_data.get('convert_premium_rate')}"
    
    print("✅ Bug修复验证通过：负值被正确保存")


@pytest.mark.asyncio
async def test_invalid_string_to_float():
    """
    Bug修复测试：无效字符串转换为float应返回None
    
    验证：safe_float函数能正确处理无法转换的字符串
    """
    from app.services.bond_data_service import BondDataService
    
    # 创建包含无效字符串的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": "N/A",  # 无效字符串
            "转债涨跌幅": "--",  # 无效字符串
            "转股溢价率": 12.5,  # 有效数值
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
    
    # 验证保存成功
    assert saved == 1
    
    # 获取实际调用的数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # 关键验证：无效字符串应该被过滤掉
    assert "price" not in update_data, "无效的price字段不应该存在"
    assert "change_pct" not in update_data, "无效的change_pct字段不应该存在"
    
    # 有效值应该被保存
    assert "convert_premium_rate" in update_data
    assert update_data["convert_premium_rate"] == 12.5
    
    print("✅ Bug修复验证通过：无效字符串被正确处理")


@pytest.mark.asyncio
async def test_empty_string_not_saved():
    """
    Bug修复测试：空字符串不应被保存
    
    验证：空字符串应该被过滤掉
    """
    from app.services.bond_data_service import BondDataService
    
    # 创建包含空字符串的测试数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "开始转股日": "",  # 空字符串
            "上市日期": "2024-03-06",  # 有效日期
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
    
    # 验证保存成功
    assert saved == 1
    
    # 获取实际调用的数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # 关键验证：空字符串应该被过滤掉
    assert "start_convert_date" not in update_data, "空字符串的start_convert_date不应该存在"
    
    # 有效字符串应该被保存
    assert "list_date" in update_data
    assert update_data["list_date"] == "2024-03-06"
    
    print("✅ Bug修复验证通过：空字符串被正确过滤")


@pytest.mark.asyncio
async def test_mixed_valid_invalid_data():
    """
    综合测试：混合有效和无效数据
    
    验证：能正确处理包含各种情况的混合数据
    """
    from app.services.bond_data_service import BondDataService
    
    # 创建混合数据
    test_data = pd.DataFrame([
        {
            "转债代码": "113682",
            "转债名称": "益丰转债",
            "转债最新价": 120.5,  # 有效
            "转债涨跌幅": 0.0,  # 0值
            "转股溢价率": np.nan,  # NaN
            "纯债溢价率": -5.0,  # 负值
            "开始转股日": "",  # 空字符串
            "上市日期": "2024-03-06",  # 有效
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
    
    # 验证保存成功
    assert saved == 1
    
    # 获取实际调用的数据
    call_args = mock_collection.bulk_write.call_args
    ops = call_args[0][0]
    update_data = ops[0]._UpdateOne__update["$set"]
    
    # 验证结果
    assert update_data["price"] == 120.5, "有效值应该被保存"
    assert update_data["change_pct"] == 0.0, "0值应该被保存"
    assert "convert_premium_rate" not in update_data, "NaN应该被过滤"
    assert update_data["pure_debt_premium_rate"] == -5.0, "负值应该被保存"
    assert "start_convert_date" not in update_data, "空字符串应该被过滤"
    assert update_data["list_date"] == "2024-03-06", "有效字符串应该被保存"
    
    print("✅ 综合测试通过：混合数据被正确处理")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
