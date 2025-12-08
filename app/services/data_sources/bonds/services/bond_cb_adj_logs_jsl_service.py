"""
转股价调整记录-集思录服务（重构版）

数据集合名称: bond_cb_adj_logs_jsl
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_cb_adj_logs_jsl_provider import BondCbAdjLogsJslProvider


class BondCbAdjLogsJslService(BaseService):
    """转股价调整记录-集思录服务"""
    
    collection_name = "bond_cb_adj_logs_jsl"
    provider_class = BondCbAdjLogsJslProvider

    batch_source_collection = "bond_zh_cov"
    batch_source_field = "债券代码"
    batch_concurrency = 3
