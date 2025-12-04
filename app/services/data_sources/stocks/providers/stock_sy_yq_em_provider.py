"""
商誉减值预期明细数据提供者

东方财富网-数据中心-特色数据-商誉-商誉减值预期明细
接口: stock_sy_yq_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSyYqEmProvider(BaseProvider):
    """商誉减值预期明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_sy_yq_em"
    display_name = "商誉减值预期明细"
    akshare_func = "stock_sy_yq_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-商誉-商誉减值预期明细"
    collection_route = "/stocks/collections/stock_sy_yq_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "业绩变动原因", "type": "object", "description": "-"},
        {"name": "最新商誉报告期", "type": "object", "description": "-"},
        {"name": "最新一期商誉", "type": "float64", "description": "主要单位: 元"},
        {"name": "上年商誉", "type": "float64", "description": "主要单位: 元"},
        {"name": "预计净利润-下限", "type": "int64", "description": "主要单位: 元"},
        {"name": "预计净利润-上限", "type": "int64", "description": "主要单位: 元"},
        {"name": "业绩变动幅度-下限", "type": "float64", "description": "主要单位: %"},
        {"name": "业绩变动幅度-上限", "type": "float64", "description": "主要单位: %"},
        {"name": "上年度同期净利润", "type": "float64", "description": "主要单位: 元"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "交易市场", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
