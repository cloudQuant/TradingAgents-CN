"""
次新股池数据提供者

东方财富网-行情中心-涨停板行情-次新股池
接口: stock_zt_pool_sub_new_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZtPoolSubNewEmProvider(BaseProvider):
    """次新股池数据提供者"""
    
    # 必填属性
    collection_name = "stock_zt_pool_sub_new_em"
    display_name = "次新股池"
    akshare_func = "stock_zt_pool_sub_new_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-涨停板行情-次新股池"
    collection_route = "/stocks/collections/stock_zt_pool_sub_new_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨停价", "type": "float64", "description": "-"},
        {"name": "成交额", "type": "int64", "description": "-"},
        {"name": "流通市值", "type": "float64", "description": "-"},
        {"name": "总市值", "type": "float64", "description": "-"},
        {"name": "转手率", "type": "float64", "description": "注意单位: %"},
        {"name": "开板几日", "type": "int64", "description": "-"},
        {"name": "开板日期", "type": "int64", "description": "-"},
        {"name": "上市日期", "type": "int64", "description": "-"},
        {"name": "是否新高", "type": "int64", "description": "-"},
        {"name": "涨停统计", "type": "object", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
