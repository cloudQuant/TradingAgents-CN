"""
沪深港通历史数据数据提供者

东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据
接口: stock_hsgt_hist_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtHistEmProvider(BaseProvider):
    """沪深港通历史数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_hist_em"
    display_name = "沪深港通历史数据"
    akshare_func = "stock_hsgt_hist_em"
    unique_keys = ['日期']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据"
    collection_route = "/stocks/collections/stock_hsgt_hist_em"
    collection_category = "历史行情"

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
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "当日成交净买额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "买入成交额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "卖出成交额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "历史累计净买额", "type": "float64", "description": "注意单位: 万亿元"},
        {"name": "当日资金流入", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "当日余额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "领涨股", "type": "object", "description": "-"},
        {"name": "领涨股-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "沪深300", "type": "float64", "description": "-"},
        {"name": "沪深300-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "领涨股-代码", "type": "object", "description": "-"},
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "当日成交净买额", "type": "float64", "description": "注意单位: 亿港元"},
        {"name": "买入成交额", "type": "float64", "description": "注意单位: 亿港元"},
        {"name": "卖出成交额", "type": "float64", "description": "注意单位: 亿港元"},
        {"name": "历史累计净买额", "type": "float64", "description": "注意单位: 万亿元"},
        {"name": "当日资金流入", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "当日余额", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "领涨股", "type": "object", "description": "-"},
        {"name": "领涨股-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "恒生指数", "type": "float64", "description": "-"},
        {"name": "恒生指数-涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "领涨股-代码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
