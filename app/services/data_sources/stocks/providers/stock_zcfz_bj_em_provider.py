"""
资产负债表-北交所数据提供者

东方财富-数据中心-年报季报-业绩快报-资产负债表
接口: stock_zcfz_bj_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZcfzBjEmProvider(BaseProvider):
    """资产负债表-北交所数据提供者"""
    
    # 必填属性
    collection_name = "stock_zcfz_bj_em"
    display_name = "资产负债表-北交所"
    akshare_func = "stock_zcfz_bj_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-年报季报-业绩快报-资产负债表"
    collection_route = "/stocks/collections/stock_zcfz_bj_em"
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
        {"name": "资产-货币资金", "type": "float64", "description": "注意单位: 元"},
        {"name": "资产-应收账款", "type": "float64", "description": "注意单位: 元"},
        {"name": "资产-存货", "type": "float64", "description": "注意单位: 元"},
        {"name": "资产-总资产", "type": "float64", "description": "注意单位: 元"},
        {"name": "资产-总资产同比", "type": "float64", "description": "注意单位: %"},
        {"name": "负债-应付账款", "type": "float64", "description": "注意单位: 元"},
        {"name": "负债-总负债", "type": "float64", "description": "注意单位: 元"},
        {"name": "负债-预收账款", "type": "float64", "description": "注意单位: 元"},
        {"name": "负债-总负债同比", "type": "float64", "description": "注意单位: %"},
        {"name": "资产负债率", "type": "float64", "description": "注意单位: %"},
        {"name": "股东权益合计", "type": "float64", "description": "注意单位: 元"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
