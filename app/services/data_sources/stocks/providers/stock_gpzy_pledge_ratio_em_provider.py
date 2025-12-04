"""
上市公司质押比例数据提供者

东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
接口: stock_gpzy_pledge_ratio_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGpzyPledgeRatioEmProvider(BaseProvider):
    """上市公司质押比例数据提供者"""
    
    # 必填属性
    collection_name = "stock_gpzy_pledge_ratio_em"
    display_name = "上市公司质押比例"
    akshare_func = "stock_gpzy_pledge_ratio_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股权质押-上市公司质押比例"
    collection_route = "/stocks/collections/stock_gpzy_pledge_ratio_em"
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
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "质押比例", "type": "float64", "description": "注意单位: %"},
        {"name": "质押股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "质押市值", "type": "float64", "description": "注意单位: 万元"},
        {"name": "质押笔数", "type": "float64", "description": "-"},
        {"name": "无限售股质押数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "限售股质押数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "近一年涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "所属行业代码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
