"""
转股价调整记录-集思录数据提供者（重构版）

数据集合名称: bond_cb_adj_logs_jsl
数据唯一标识: 可转债代码, 股东大会日
"""
from app.services.data_sources.base_provider import BaseProvider


class BondCbAdjLogsJslProvider(BaseProvider):
    """转股价调整记录-集思录数据提供者"""
    
    collection_name = "bond_cb_adj_logs_jsl"
    display_name = "转股价调整记录-集思录"
    akshare_func = "bond_cb_adj_logs_jsl"
    unique_keys = ['代码', '股东大会日']

    collection_description = "转股价调整记录-集思录数据"
    collection_route = "/bonds/collections/bond_cb_adj_logs_jsl"
    collection_order = 25

    # 参数映射与必填项配置
    param_mapping = {
        "symbol": "symbol",
        "债券代码": "symbol",
        "代码": "symbol",
    }
    required_params = ["symbol"]
    add_param_columns = {
        "symbol": "代码",
    }

    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "转债名称", "type": "string", "description": "可转债名称"},
        {"name": "股东大会日", "type": "string", "description": "股东大会日期"},
        {"name": "下修前转股价", "type": "float", "description": "下修前转股价"},
        {"name": "下修后转股价", "type": "float", "description": "下修后转股价"},
        {"name": "新转股价生效日期", "type": "string", "description": "新转股价生效日期"},
        {"name": "下修底价", "type": "float", "description": "下修底价"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
