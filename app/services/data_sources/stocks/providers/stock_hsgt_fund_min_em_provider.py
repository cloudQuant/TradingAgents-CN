"""
沪深港通分时数据数据提供者

东方财富-数据中心-沪深港通-市场概括-分时数据
接口: stock_hsgt_fund_min_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtFundMinEmProvider(BaseProvider):
    """沪深港通分时数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_fund_min_em"
    display_name = "沪深港通分时数据"
    akshare_func = "stock_hsgt_fund_min_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-沪深港通-市场概括-分时数据"
    collection_route = "/stocks/collections/stock_hsgt_fund_min_em"
    collection_category = "沪深港通"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "日期"},
        {"name": "时间", "type": "object", "description": "时间"},
        {"name": "沪股通", "type": "float64", "description": "注意单位: 万元"},
        {"name": "深股通", "type": "float64", "description": "注意单位: 万元"},
        {"name": "北向资金", "type": "float64", "description": "注意单位: 万元"},
        {"name": "日期", "type": "object", "description": "日期"},
        {"name": "时间", "type": "object", "description": "时间"},
        {"name": "港股通(沪)", "type": "float64", "description": "注意单位: 万元"},
        {"name": "港股通(深)", "type": "float64", "description": "注意单位: 万元"},
        {"name": "南向资金", "type": "float64", "description": "注意单位: 万元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
