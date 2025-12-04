"""
龙虎榜-营业上榜统计数据提供者

新浪财经-龙虎榜-营业上榜统计
接口: stock_lhb_yytj_sina
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbYytjSinaProvider(BaseProvider):
    """龙虎榜-营业上榜统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_yytj_sina"
    display_name = "龙虎榜-营业上榜统计"
    akshare_func = "stock_lhb_yytj_sina"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-龙虎榜-营业上榜统计"
    collection_route = "/stocks/collections/stock_lhb_yytj_sina"
    collection_category = "龙虎榜"

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
        {"name": "上榜次数", "type": "int64", "description": "-"},
        {"name": "累积购买额", "type": "float64", "description": "注意单位: 万"},
        {"name": "买入席位数", "type": "int64", "description": "-"},
        {"name": "累积卖出额", "type": "float64", "description": "注意单位: 万"},
        {"name": "卖出席位数", "type": "int64", "description": "-"},
        {"name": "买入前三股票", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
