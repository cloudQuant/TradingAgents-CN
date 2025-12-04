"""
关键指标-同花顺数据提供者

同花顺-财务指标-主要指标
接口: stock_financial_abstract_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialAbstractThsProvider(BaseProvider):
    """关键指标-同花顺数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_abstract_ths"
    display_name = "关键指标-同花顺"
    akshare_func = "stock_financial_abstract_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-财务指标-主要指标"
    collection_route = "/stocks/collections/stock_financial_abstract_ths"
    collection_category = "财务数据"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "报告期", "type": "object", "description": "-"},
        {"name": "净利润", "type": "object", "description": "-"},
        {"name": "净利润同比增长率", "type": "object", "description": "-"},
        {"name": "扣非净利润", "type": "object", "description": "-"},
        {"name": "扣非净利润同比增长率", "type": "object", "description": "-"},
        {"name": "营业总收入", "type": "object", "description": "-"},
        {"name": "营业总收入同比增长率", "type": "object", "description": "-"},
        {"name": "基本每股收益", "type": "object", "description": "-"},
        {"name": "每股净资产", "type": "object", "description": "-"},
        {"name": "每股资本公积金", "type": "object", "description": "-"},
        {"name": "每股未分配利润", "type": "object", "description": "-"},
        {"name": "每股经营现金流", "type": "object", "description": "-"},
        {"name": "销售净利率", "type": "object", "description": "-"},
        {"name": "销售毛利率", "type": "object", "description": "-"},
        {"name": "净资产收益率", "type": "object", "description": "-"},
        {"name": "净资产收益率-摊薄", "type": "object", "description": "-"},
        {"name": "营业周期", "type": "object", "description": "-"},
        {"name": "存货周转率", "type": "object", "description": "-"},
        {"name": "存货周转天数", "type": "object", "description": "-"},
        {"name": "应收账款周转天数", "type": "object", "description": "-"},
        {"name": "流动比率", "type": "object", "description": "-"},
        {"name": "速动比率", "type": "object", "description": "-"},
        {"name": "保守速动比率", "type": "object", "description": "-"},
        {"name": "产权比率", "type": "object", "description": "-"},
        {"name": "资产负债率", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
