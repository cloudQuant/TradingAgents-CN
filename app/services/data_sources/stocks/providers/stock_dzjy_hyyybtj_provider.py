"""
活跃营业部统计数据提供者

东方财富网-数据中心-大宗交易-活跃营业部统计
接口: stock_dzjy_hyyybtj
"""
from app.services.data_sources.base_provider import BaseProvider


class StockDzjyHyyybtjProvider(BaseProvider):
    """活跃营业部统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_dzjy_hyyybtj"
    display_name = "活跃营业部统计"
    akshare_func = "stock_dzjy_hyyybtj"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-大宗交易-活跃营业部统计"
    collection_route = "/stocks/collections/stock_dzjy_hyyybtj"
    collection_category = "默认"

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "最近上榜日", "type": "object", "description": "-"},
        {"name": "次数总计-买入", "type": "float64", "description": "-"},
        {"name": "次数总计-卖出", "type": "float64", "description": "注意单位: %"},
        {"name": "成交金额统计-买入", "type": "float64", "description": "注意单位: 万元"},
        {"name": "成交金额统计-卖出", "type": "float64", "description": "注意单位: 万元"},
        {"name": "成交金额统计-净买入额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "买入的股票", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
