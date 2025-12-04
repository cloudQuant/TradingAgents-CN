"""
中债新综合指数数据提供者（重构版）

需求文档: tests/bonds/requirements/33_中债新综合指数.md
数据唯一标识: 指标类型、期限和日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondNewCompositeIndexCbondProvider(BaseProvider):
    """中债新综合指数数据提供者"""
    
    collection_name = "bond_new_composite_index_cbond"
    display_name = "中债新综合指数"
    akshare_func = "bond_new_composite_index_cbond"
    unique_keys = ["指标类型", "期限", "date"]
    
    # 默认参数（SimpleProvider不支持参数，所以使用BaseProvider）
    add_param_columns = {"indicator": "指标类型", "period": "期限"}
    
    collection_description = "中债新综合指数历史数据"
    collection_route = "/bonds/collections/bond_new_composite_index_cbond"
    collection_order = 33
    
    field_info = [
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "value", "type": "float", "description": "指数值"},
        {"name": "指标类型", "type": "string", "description": "指标类型"},
        {"name": "期限", "type": "string", "description": "期限"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
