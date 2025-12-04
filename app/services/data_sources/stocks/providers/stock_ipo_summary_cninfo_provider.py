"""
上市相关-巨潮资讯数据提供者

巨潮资讯-个股-上市相关
接口: stock_ipo_summary_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIpoSummaryCninfoProvider(BaseProvider):
    """上市相关-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_ipo_summary_cninfo"
    display_name = "上市相关-巨潮资讯"
    akshare_func = "stock_ipo_summary_cninfo"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "巨潮资讯-个股-上市相关"
    collection_route = "/stocks/collections/stock_ipo_summary_cninfo"
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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "招股公告日期", "type": "object", "description": "-"},
        {"name": "中签率公告日", "type": "object", "description": "-"},
        {"name": "每股面值", "type": "float64", "description": "注意单位: 元"},
        {"name": "总发行数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "发行前每股净资产", "type": "float64", "description": "注意单位: 元"},
        {"name": "摊薄发行市盈率", "type": "float64", "description": "-"},
        {"name": "募集资金净额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "上网发行日期", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "发行价格", "type": "float64", "description": "注意单位: 元"},
        {"name": "发行费用总额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "发行后每股净资产", "type": "float64", "description": "注意单位: 元"},
        {"name": "上网发行中签率", "type": "float64", "description": "注意单位: %"},
        {"name": "主承销商", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
