"""
中美国债收益率数据提供者（重构版）

数据集合名称: bond_zh_us_rate
数据唯一标识: 日期
接口说明: 从东方财富网获取中美国债收益率历史数据，数据从 19901219 开始
"""
from app.services.data_sources.base_provider import BaseProvider

class BondZhUsRateProvider(BaseProvider):
    """中美国债收益率数据提供者"""
    
    collection_name = "bond_zh_us_rate"
    display_name = "中美国债收益率"
    akshare_func = "bond_zh_us_rate"
    unique_keys = ['日期']
    
    collection_description = "中美国债收益率数据"
    collection_route = "/bonds/collections/bond_zh_us_rate"
    collection_order = 27

    # start_date 参数由 service 自动生成，不需要在这里验证
    # required_params = ["start_date"]
    
    field_info = [
        {"name": "日期", "type": "date", "description": "数据日期"},
        {"name": "中国国债收益率2年", "type": "float", "description": "中国2年期国债收益率(%)"}, 
        {"name": "中国国债收益率5年", "type": "float", "description": "中国5年期国债收益率(%)"}, 
        {"name": "中国国债收益率10年", "type": "float", "description": "中国10年期国债收益率(%)"}, 
        {"name": "中国国债收益率30年", "type": "float", "description": "中国30年期国债收益率(%)"}, 
        {"name": "中国国债收益率10年-2年", "type": "float", "description": "中国10年-2年国债利差(%)"}, 
        {"name": "中国GDP年增率", "type": "float", "description": "中国GDP年增率(%)"}, 
        {"name": "美国国债收益率2年", "type": "float", "description": "美国2年期国债收益率(%)"}, 
        {"name": "美国国债收益率5年", "type": "float", "description": "美国5年期国债收益率(%)"}, 
        {"name": "美国国债收益率10年", "type": "float", "description": "美国10年期国债收益率(%)"}, 
        {"name": "美国国债收益率30年", "type": "float", "description": "美国30年期国债收益率(%)"}, 
        {"name": "美国国债收益率10年-2年", "type": "float", "description": "美国10年-2年国债利差(%)"}, 
        {"name": "美国GDP年增率", "type": "float", "description": "美国GDP年增率(%)"}, 
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"}, 
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
