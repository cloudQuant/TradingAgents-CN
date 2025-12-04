"""
债券基础信息-中国外汇交易中心服务（重构版：继承BaseService）

需求文档: tests/bonds/requirements/02_债券基础信息-中国外汇交易中心.md
数据唯一标识: 债券代码
批量更新: 从bond_info_cm获取债券简称列表进行批量获取
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_info_detail_cm_provider import BondInfoDetailCmProvider


class BondInfoDetailCmService(BaseService):
    """债券基础信息-中国外汇交易中心服务"""
    
    collection_name = "bond_info_detail_cm"
    provider_class = BondInfoDetailCmProvider
    
    # 批量更新配置：从bond_info_cm获取债券简称列表
    batch_source_collection = "bond_info_cm"
    batch_source_field = "债券简称"  # bond_info_detail_cm需要债券简称作为参数
    batch_concurrency = 3
    
    # 增量更新配置
    incremental_check_fields = ["债券代码"]
