"""
营业部详情数据-东财数据提供者

东方财富网-数据中心-龙虎榜单-营业部历史交易明细-营业部交易明细
接口: stock_lhb_yyb_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbYybDetailEmProvider(BaseProvider):
    """营业部详情数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_yyb_detail_em"
    display_name = "营业部详情数据-东财"
    akshare_func = "stock_lhb_yyb_detail_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-营业部历史交易明细-营业部交易明细"
    collection_route = "/stocks/collections/stock_lhb_yyb_detail_em"
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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "营业部代码", "type": "object", "description": "-"},
        {"name": "营业部简称", "type": "object", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "买入金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "卖出金额", "type": "float64", "description": "注意单位: 元"},
        {"name": "净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "上榜原因", "type": "object", "description": "-"},
        {"name": "1日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "2日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "3日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "5日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "10日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "20日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "30日后涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
