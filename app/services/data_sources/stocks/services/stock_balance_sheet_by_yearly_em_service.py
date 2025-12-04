"""
资产负债表-按年度服务

东方财富-股票-财务分析-资产负债表-按年度
接口: stock_balance_sheet_by_yearly_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_balance_sheet_by_yearly_em_provider import StockBalanceSheetByYearlyEmProvider


class StockBalanceSheetByYearlyEmService(BaseService):
    """资产负债表-按年度服务"""
    
    collection_name = "stock_balance_sheet_by_yearly_em"
    provider_class = StockBalanceSheetByYearlyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
