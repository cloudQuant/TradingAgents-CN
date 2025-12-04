"""
券商业绩月报数据提供者

东方财富网-数据中心-特色数据-券商业绩月报
接口: stock_qsjy_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockQsjyEmProvider(BaseProvider):
    """券商业绩月报数据提供者"""
    
    # 必填属性
    collection_name = "stock_qsjy_em"
    display_name = "券商业绩月报"
    akshare_func = "stock_qsjy_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-券商业绩月报"
    collection_route = "/stocks/collections/stock_qsjy_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "当月净利润-净利润", "type": "float64", "description": "注意单位: 万元"},
        {"name": "当月净利润-同比增长", "type": "float64", "description": "-"},
        {"name": "当月净利润-环比增长", "type": "float64", "description": "-"},
        {"name": "当年累计净利润-累计净利润", "type": "float64", "description": "注意单位: 万元"},
        {"name": "当年累计净利润-同比增长", "type": "float64", "description": "-"},
        {"name": "当月营业收入-营业收入", "type": "float64", "description": "注意单位: 万元"},
        {"name": "当月营业收入-环比增长", "type": "float64", "description": "-"},
        {"name": "当月营业收入-同比增长", "type": "float64", "description": "-"},
        {"name": "当年累计营业收入-累计营业收入", "type": "float64", "description": "注意单位: 万元"},
        {"name": "当年累计营业收入-同比增长", "type": "float64", "description": "-"},
        {"name": "净资产-净资产", "type": "float64", "description": "注意单位: 万元"},
        {"name": "净资产-同比增长", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
