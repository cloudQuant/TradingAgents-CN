"""
基金持仓股票-东财服务 (使用基类重构版本)

对比原版本 fund_portfolio_hold_em_service.py（295行），新版本只需要约50行代码。
"""
from typing import Set, Tuple
from app.services.data_sources.base_service import BaseService
from ..providers.fund_portfolio_hold_em_provider_v2 import FundPortfolioHoldEmProviderV2


class FundPortfolioHoldEmServiceV2(BaseService):
    """基金持仓股票-东财服务"""
    
    collection_name = "fund_portfolio_hold_em"
    provider_class = FundPortfolioHoldEmProviderV2
    time_field = "更新时间"
    
    # ===== 批量更新配置 =====
    
    # 从哪个集合获取基金代码列表
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    
    # 需要年份参数，年份范围2010到今年
    batch_use_year = True
    batch_years_range = (2010, None)
    
    # 并发数和进度更新间隔
    batch_concurrency = 3
    batch_progress_interval = 100
    
    # 增量更新检查字段
    incremental_check_fields = ["基金代码", "季度"]
    
    def get_batch_params(self, code: str, year: str) -> dict:
        """构建批量任务的参数"""
        return {"fund_code": code, "year": year}
    
    async def _get_existing_combinations(self) -> Set[Tuple]:
        """
        获取已存在的基金代码+年份组合
        
        从季度字段（如 "2024年1季度"）中提取年份
        """
        existing: Set[Tuple[str, str]] = set()
        cursor = self.collection.find({}, {"基金代码": 1, "季度": 1})
        
        async for doc in cursor:
            fund_code = doc.get("基金代码")
            quarter = str(doc.get("季度", ""))
            
            # 从季度字段提取年份
            if fund_code and len(quarter) >= 4 and quarter[:4].isdigit():
                year = quarter[:4]
                existing.add((fund_code, year))
        
        return existing
