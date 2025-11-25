"""可转债价值分析服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_cov_value_analysis_provider import BondZhCovValueAnalysisProvider


class BondZhCovValueAnalysisService(BaseBondService):
    """可转债价值分析服务 - 按可转债代码和日期唯一"""
    
    def __init__(self, db):
        super().__init__(
            db, 
            "bond_zh_cov_value_analysis", 
            BondZhCovValueAnalysisProvider(), 
            unique_keys=["可转债代码", "日期"]  # 每个可转债每天一条记录
        )
