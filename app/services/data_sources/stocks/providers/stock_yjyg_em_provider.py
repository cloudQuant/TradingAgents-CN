"""
业绩预告数据提供者

东方财富-数据中心-年报季报-业绩预告
接口: stock_yjyg_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockYjygEmProvider(BaseProvider):
    """业绩预告数据提供者"""
    
    # 必填属性
    collection_name = "stock_yjyg_em"
    display_name = "业绩预告"
    akshare_func = "stock_yjyg_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-年报季报-业绩预告"
    collection_route = "/stocks/collections/stock_yjyg_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "预测指标", "type": "float64", "description": "-"},
        {"name": "业绩变动", "type": "float64", "description": "-"},
        {"name": "预测数值", "type": "float64", "description": "注意单位: 元"},
        {"name": "业绩变动幅度", "type": "float64", "description": "注意单位: %"},
        {"name": "业绩变动原因", "type": "float64", "description": "-"},
        {"name": "预告类型", "type": "float64", "description": "-"},
        {"name": "上年同期值", "type": "float64", "description": "注意单位: 元"},
        {"name": "公告日期", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
