"""
投资评级数据提供者

巨潮资讯-数据中心-评级预测-投资评级
接口: stock_rank_forecast_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRankForecastCninfoProvider(BaseProvider):
    """投资评级数据提供者"""
    
    # 必填属性
    collection_name = "stock_rank_forecast_cninfo"
    display_name = "投资评级"
    akshare_func = "stock_rank_forecast_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-评级预测-投资评级"
    collection_route = "/stocks/collections/stock_rank_forecast_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "发布日期", "type": "object", "description": "-"},
        {"name": "研究机构简称", "type": "object", "description": "-"},
        {"name": "投资评级", "type": "object", "description": "-"},
        {"name": "是否首次评级", "type": "object", "description": "-"},
        {"name": "评级变化", "type": "object", "description": "-"},
        {"name": "前一次投资评级", "type": "object", "description": "-"},
        {"name": "目标价格-下限", "type": "float64", "description": "-"},
        {"name": "目标价格-上限", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
