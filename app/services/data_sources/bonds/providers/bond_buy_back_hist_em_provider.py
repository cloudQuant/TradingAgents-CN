"""
质押式回购历史数据数据提供者（重构版）

数据集合名称: bond_buy_back_hist_em
数据唯一标识: 代码, 日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondBuyBackHistEmProvider(BaseProvider):
    """质押式回购历史数据数据提供者"""
    
    collection_name = "bond_buy_back_hist_em"
    display_name = "质押式回购历史数据"
    akshare_func = "bond_repo_zh_tick"
    unique_keys = ['代码', '日期']
    
    collection_description = "质押式回购历史数据数据"
    collection_route = "/bonds/collections/bond_buy_back_hist_em"
    collection_order = 21
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
