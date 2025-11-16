"""
高级查询功能测试
测试可转债查询的各种过滤、排序、分页功能
"""
import pytest
from unittest.mock import Mock, AsyncMock
import pandas as pd


@pytest.mark.asyncio
async def test_query_with_keyword_search():
    """测试关键词搜索功能"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=2)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    
    # mock异步迭代
    mock_cursor.__aiter__.return_value = iter([
        {"code": "SH.113682", "name": "益丰转债", "convert_premium_rate": 12.0},
        {"code": "SZ.127105", "name": "益丰转2", "convert_premium_rate": 15.0}
    ])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(q="益丰")
    
    # 验证
    assert result["total"] == 2
    assert len(result["items"]) == 2
    
    # 验证find被正确调用（包含$or条件）
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "$or" in filter_arg, "应该包含$or搜索条件"
    
    print("✅ 测试通过：关键词搜索")


@pytest.mark.asyncio
async def test_query_with_premium_range():
    """测试溢价率范围过滤"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=5)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    
    # mock异步迭代 - 返回溢价率在0-10%之间的数据
    mock_cursor.__aiter__.return_value = iter([
        {"code": "113682", "convert_premium_rate": 5.0},
        {"code": "127105", "convert_premium_rate": 8.0},
        {"code": "123456", "convert_premium_rate": 9.5}
    ])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（溢价率0-10%）
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(
        min_premium=0.0,
        max_premium=10.0
    )
    
    # 验证
    assert result["total"] == 5
    assert len(result["items"]) == 3
    
    # 验证过滤条件被正确设置
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "convert_premium_rate" in filter_arg, "应该包含溢价率过滤条件"
    assert "$gte" in filter_arg["convert_premium_rate"], "应该包含最小值条件"
    assert "$lte" in filter_arg["convert_premium_rate"], "应该包含最大值条件"
    
    print("✅ 测试通过：溢价率范围过滤")


@pytest.mark.asyncio
async def test_query_with_only_min_premium():
    """测试只设置最小溢价率"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=10)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（只设置最小值）
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(min_premium=20.0)
    
    # 验证过滤条件
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "convert_premium_rate" in filter_arg
    assert "$gte" in filter_arg["convert_premium_rate"]
    assert filter_arg["convert_premium_rate"]["$gte"] == 20.0
    assert "$lte" not in filter_arg["convert_premium_rate"], "不应该有最大值条件"
    
    print("✅ 测试通过：只设置最小溢价率")


@pytest.mark.asyncio
async def test_query_with_only_max_premium():
    """测试只设置最大溢价率"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=15)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（只设置最大值）
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(max_premium=50.0)
    
    # 验证过滤条件
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "convert_premium_rate" in filter_arg
    assert "$lte" in filter_arg["convert_premium_rate"]
    assert filter_arg["convert_premium_rate"]["$lte"] == 50.0
    assert "$gte" not in filter_arg["convert_premium_rate"], "不应该有最小值条件"
    
    print("✅ 测试通过：只设置最大溢价率")


@pytest.mark.asyncio
async def test_query_with_combined_filters():
    """测试组合过滤条件"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=3)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([
        {"code": "113682", "name": "益丰转债", "convert_premium_rate": 8.0}
    ])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（关键词 + 溢价率范围）
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(
        q="益丰",
        min_premium=5.0,
        max_premium=15.0
    )
    
    # 验证
    assert result["total"] == 3
    
    # 验证过滤条件同时包含搜索和溢价率
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "$or" in filter_arg, "应该包含搜索条件"
    assert "convert_premium_rate" in filter_arg, "应该包含溢价率条件"
    
    print("✅ 测试通过：组合过滤条件")


@pytest.mark.asyncio
async def test_query_with_sorting():
    """测试排序功能"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=10)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 测试升序排序
    service = BondDataService(mock_db)
    await service.query_cov_comparison(
        sort_by="convert_premium_rate",
        sort_dir="asc"
    )
    
    # 验证sort被调用且方向为1（升序）
    call_args = mock_cursor.sort.call_args
    sort_spec = call_args[0][0]
    assert sort_spec[0][0] == "convert_premium_rate"
    assert sort_spec[0][1] == 1, "升序应该是1"
    
    # 测试降序排序
    await service.query_cov_comparison(
        sort_by="price",
        sort_dir="desc"
    )
    
    # 验证降序
    call_args = mock_cursor.sort.call_args
    sort_spec = call_args[0][0]
    assert sort_spec[0][0] == "price"
    assert sort_spec[0][1] == -1, "降序应该是-1"
    
    print("✅ 测试通过：排序功能")


@pytest.mark.asyncio
async def test_query_with_pagination():
    """测试分页功能"""
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
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 测试第2页，每页20条
    service = BondDataService(mock_db)
    await service.query_cov_comparison(page=2, page_size=20)
    
    # 验证skip被正确调用（第2页应该跳过20条）
    call_args = mock_cursor.skip.call_args
    skip_count = call_args[0][0]
    assert skip_count == 20, f"第2页应该跳过20条，实际跳过{skip_count}条"
    
    # 验证limit被正确调用
    call_args = mock_cursor.limit.call_args
    limit_count = call_args[0][0]
    assert limit_count == 20, f"每页应该限制20条，实际限制{limit_count}条"
    
    print("✅ 测试通过：分页功能")


@pytest.mark.asyncio
async def test_query_empty_result():
    """测试空结果处理"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents返回0
    mock_collection.count_documents = AsyncMock(return_value=0)
    
    # 执行查询
    service = BondDataService(mock_db)
    result = await service.query_cov_comparison(q="不存在的债券")
    
    # 验证
    assert result["total"] == 0
    assert result["items"] == []
    
    # 验证find未被调用（因为count=0，提前返回）
    assert not mock_collection.find.called, "count=0时不应调用find"
    
    print("✅ 测试通过：空结果处理")


@pytest.mark.asyncio
async def test_query_value_analysis_with_date_range():
    """测试价值分析的日期范围查询"""
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
        {"code": "SH.113682", "date": "2024-01-01", "close_price": 120.0},
        {"code": "SH.113682", "date": "2024-01-02", "close_price": 121.0}
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
    assert result["code"] in ["SH.113682", "113682"]
    assert len(result["data"]) == 2
    
    # 验证日期范围过滤
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "date" in filter_arg
    assert "$gte" in filter_arg["date"], "应该包含开始日期条件"
    assert "$lte" in filter_arg["date"], "应该包含结束日期条件"
    assert filter_arg["date"]["$gte"] == "2024-01-01"
    assert filter_arg["date"]["$lte"] == "2024-01-31"
    
    print("✅ 测试通过：价值分析日期范围查询")


@pytest.mark.asyncio
async def test_query_value_analysis_only_start_date():
    """测试只设置开始日期"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（只设置开始日期）
    service = BondDataService(mock_db)
    result = await service.query_cov_value_analysis(
        code="113682",
        start_date="2024-01-01"
    )
    
    # 验证过滤条件
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "date" in filter_arg
    assert "$gte" in filter_arg["date"]
    assert filter_arg["date"]["$gte"] == "2024-01-01"
    # 只有开始日期，没有结束日期
    assert "$lte" not in filter_arg["date"]
    
    print("✅ 测试通过：只设置开始日期")


@pytest.mark.asyncio
async def test_query_value_analysis_only_end_date():
    """测试只设置结束日期"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（只设置结束日期）
    service = BondDataService(mock_db)
    result = await service.query_cov_value_analysis(
        code="113682",
        end_date="2024-01-31"
    )
    
    # 验证过滤条件
    call_args = mock_collection.find.call_args
    filter_arg = call_args[0][0]
    assert "date" in filter_arg
    assert "$lte" in filter_arg["date"]
    assert filter_arg["date"]["$lte"] == "2024-01-31"
    # 只有结束日期，没有开始日期
    assert "$gte" not in filter_arg["date"]
    
    print("✅ 测试通过：只设置结束日期")


@pytest.mark.asyncio
async def test_query_negative_page_number():
    """测试负数页码处理"""
    from app.services.bond_data_service import BondDataService
    
    # 创建mock数据库
    mock_db = Mock()
    mock_collection = AsyncMock()
    mock_db.get_collection.return_value = mock_collection
    
    # mock count_documents
    mock_collection.count_documents = AsyncMock(return_value=10)
    
    # mock find返回cursor
    mock_cursor = AsyncMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__aiter__.return_value = iter([])
    
    mock_collection.find.return_value = mock_cursor
    
    # 执行查询（页码为0或负数）
    service = BondDataService(mock_db)
    await service.query_cov_comparison(page=0)  # 页码为0
    
    # 验证skip为0（负数页码会被max(0, ...)处理）
    call_args = mock_cursor.skip.call_args
    skip_count = call_args[0][0]
    assert skip_count == 0, "页码<=1时，skip应该为0"
    
    print("✅ 测试通过：负数页码处理")


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "-s"])
