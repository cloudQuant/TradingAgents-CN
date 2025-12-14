"""全球指数历史行情-东财数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class IndexGlobalHistEmProvider(BaseProvider):
    """全球指数历史行情-东财数据提供者"""
    
    collection_name = "index_global_hist_em"
    display_name = "全球指数历史行情-东财"
    akshare_func = "index_global_hist_em"
    unique_keys = ["代码", "日期"]
    
    collection_description = "东方财富网-行情中心-全球指数历史行情数据"
    collection_route = "/indexs/collections/index_global_hist_em"
    collection_order = 31
    
    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "name": "symbol",
    }
    
    # 必填参数
    required_params = ["symbol"]
    
    field_info = [
        {"name": "日期", "type": "string", "description": ""},
        {"name": "代码", "type": "string", "description": "指数代码"},
        {"name": "名称", "type": "string", "description": "指数名称"},
        {"name": "今开", "type": "float", "description": ""},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "振幅", "type": "float", "description": "主要单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
