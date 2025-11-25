"""可转债详情-东财服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_cov_info_provider import BondZhCovInfoProvider


class BondZhCovInfoService(BaseBondService):
    """可转债详情服务 - 支持不同indicator查询"""
    
    def __init__(self, db):
        super().__init__(
            db, 
            "bond_zh_cov_info", 
            BondZhCovInfoProvider(), 
            unique_keys=["可转债代码", "查询指标"]  # 每个可转债每种指标类型一条记录
        )
