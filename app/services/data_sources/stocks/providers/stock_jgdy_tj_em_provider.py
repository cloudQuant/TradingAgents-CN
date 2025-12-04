"""
机构调研-统计数据提供者

东方财富网-数据中心-特色数据-机构调研-机构调研统计
接口: stock_jgdy_tj_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockJgdyTjEmProvider(BaseProvider):
    """机构调研-统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_jgdy_tj_em"
    display_name = "机构调研-统计"
    akshare_func = "stock_jgdy_tj_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-机构调研-机构调研统计"
    collection_route = "/stocks/collections/stock_jgdy_tj_em"
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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "接待机构数量", "type": "int64", "description": "-"},
        {"name": "接待方式", "type": "object", "description": "-"},
        {"name": "接待人员", "type": "object", "description": "-"},
        {"name": "接待地点", "type": "object", "description": "-"},
        {"name": "接待日期", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
