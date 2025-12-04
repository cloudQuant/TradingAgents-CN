"""
跌停股池数据提供者

东方财富网-行情中心-涨停板行情-跌停股池
接口: stock_zt_pool_dtgc_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZtPoolDtgcEmProvider(BaseProvider):
    """跌停股池数据提供者"""
    
    # 必填属性
    collection_name = "stock_zt_pool_dtgc_em"
    display_name = "跌停股池"
    akshare_func = "stock_zt_pool_dtgc_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-涨停板行情-跌停股池"
    collection_route = "/stocks/collections/stock_zt_pool_dtgc_em"
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
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "成交额", "type": "int64", "description": "-"},
        {"name": "流通市值", "type": "float64", "description": "-"},
        {"name": "总市值", "type": "float64", "description": "-"},
        {"name": "动态市盈率", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "封单资金", "type": "int64", "description": "-"},
        {"name": "最后封板时间", "type": "object", "description": "注意格式: 09:25:00"},
        {"name": "板上成交额", "type": "int64", "description": "-"},
        {"name": "连续跌停", "type": "int64", "description": "-"},
        {"name": "开板次数", "type": "int64", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
