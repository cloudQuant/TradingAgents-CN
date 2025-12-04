"""
互动易-提问数据提供者

互动易-提问
接口: stock_irm_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIrmCninfoProvider(BaseProvider):
    """互动易-提问数据提供者"""
    
    # 必填属性
    collection_name = "stock_irm_cninfo"
    display_name = "互动易-提问"
    akshare_func = "stock_irm_cninfo"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "互动易-提问"
    collection_route = "/stocks/collections/stock_irm_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "公司简称", "type": "object", "description": "-"},
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "行业代码", "type": "object", "description": "-"},
        {"name": "问题", "type": "object", "description": "-"},
        {"name": "提问者", "type": "object", "description": "-"},
        {"name": "来源", "type": "object", "description": "-"},
        {"name": "提问时间", "type": "datetime64[ns]", "description": "-"},
        {"name": "更新时间", "type": "datetime64[ns]", "description": "-"},
        {"name": "提问者编号", "type": "object", "description": "-"},
        {"name": "问题编号", "type": "object", "description": "-"},
        {"name": "回答ID", "type": "object", "description": "-"},
        {"name": "回答内容", "type": "object", "description": "-"},
        {"name": "回答者", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
