"""
中债综合指数数据提供者（重构版）

数据集合名称: bond_composite_index_cbond
数据唯一标识: 指标类型, 期限, date
数据来源: 中国债券信息网
"""
from app.services.data_sources.base_provider import BaseProvider


class BondCompositeIndexCbondProvider(BaseProvider):
    """中债综合指数数据提供者"""
    
    collection_name = "bond_composite_index_cbond"
    display_name = "中债综合指数"
    akshare_func = "bond_composite_index_cbond"
    unique_keys = ['指标类型', '期限', 'date']
    
    # 将参数写回到结果中
    add_param_columns = {"indicator": "指标类型", "period": "期限"}
    
    collection_description = "中债综合指数数据"
    collection_route = "/bonds/collections/bond_composite_index_cbond"
    collection_order = 34
    
    field_info = [
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "value", "type": "float", "description": "指数值"},
        {"name": "指标类型", "type": "string", "description": "指标类型（全价、净价、财富等）"},
        {"name": "期限", "type": "string", "description": "期限（总值、1年以下、1-3年等）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
