"""
财务指标数据提供者

东方财富-港股-核心必读-最新指标
接口: stock_hk_financial_indicator_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkFinancialIndicatorEmProvider(BaseProvider):
    """财务指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_financial_indicator_em"
    display_name = "财务指标"
    akshare_func = "stock_hk_financial_indicator_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-核心必读-最新指标"
    collection_route = "/stocks/collections/stock_hk_financial_indicator_em"
    collection_category = "财务数据"

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
        {"name": "基本每股收益(元)", "type": "object", "description": "-"},
        {"name": "每股净资产(元)", "type": "object", "description": "-"},
        {"name": "法定股本(股)", "type": "object", "description": "-"},
        {"name": "每手股", "type": "object", "description": "-"},
        {"name": "每股股息TTM(港元)", "type": "object", "description": "-"},
        {"name": "派息比率(%)", "type": "object", "description": "-"},
        {"name": "已发行股本(股)", "type": "object", "description": "-"},
        {"name": "已发行股本-H股(股)", "type": "int64", "description": "-"},
        {"name": "每股经营现金流(元)", "type": "object", "description": "-"},
        {"name": "股息率TTM(%)", "type": "object", "description": "-"},
        {"name": "总市值(港元)", "type": "object", "description": "-"},
        {"name": "港股市值(港元)", "type": "object", "description": "-"},
        {"name": "营业总收入", "type": "object", "description": "-"},
        {"name": "营业总收入滚动环比增长(%)", "type": "object", "description": "-"},
        {"name": "销售净利率(%)", "type": "object", "description": "-"},
        {"name": "净利润", "type": "object", "description": "-"},
        {"name": "净利润滚动环比增长(%)", "type": "object", "description": "-"},
        {"name": "股东权益回报率(%)", "type": "object", "description": "-"},
        {"name": "市盈率", "type": "object", "description": "-"},
        {"name": "市净率", "type": "object", "description": "-"},
        {"name": "总资产回报率(%)", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
