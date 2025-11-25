"""
自动生成完整的FundRefreshServiceV2，包含所有70个服务
"""
from pathlib import Path

# 所有70个基金集合
FUND_COLLECTIONS = [
    "fund_name_em", "fund_basic_info", "fund_info_index_em", "fund_purchase_status",
    "fund_etf_spot_em", "fund_etf_spot_ths", "fund_lof_spot_em", "fund_spot_sina",
    "fund_etf_hist_min_em", "fund_lof_hist_min_em", "fund_etf_hist_em", "fund_lof_hist_em",
    "fund_hist_sina", "fund_open_fund_daily_em", "fund_open_fund_info_em", "fund_money_fund_daily_em",
    "fund_money_fund_info_em", "fund_financial_fund_daily_em", "fund_financial_fund_info_em",
    "fund_graded_fund_daily_em", "fund_graded_fund_info_em", "fund_etf_fund_daily_em",
    "fund_hk_hist_em", "fund_etf_fund_info_em", "fund_etf_dividend_sina", "fund_fh_em",
    "fund_cf_em", "fund_fh_rank_em", "fund_open_fund_rank_em", "fund_exchange_rank_em",
    "fund_money_rank_em", "fund_lcx_rank_em", "fund_hk_rank_em", "fund_individual_achievement_xq",
    "fund_value_estimation_em", "fund_individual_analysis_xq", "fund_individual_profit_probability_xq",
    "fund_individual_detail_hold_xq", "fund_overview_em", "fund_fee_em",
    "fund_individual_detail_info_xq", "fund_portfolio_hold_em", "fund_portfolio_bond_hold_em",
    "fund_portfolio_industry_allocation_em", "fund_portfolio_change_em", "fund_rating_all_em",
    "fund_rating_sh_em", "fund_rating_zs_em", "fund_rating_ja_em", "fund_manager_em",
    "fund_new_found_em", "fund_scale_open_sina", "fund_scale_close_sina", "fund_scale_structured_sina",
    "fund_aum_em", "fund_aum_trend_em", "fund_aum_hist_em", "reits_realtime_em",
    "reits_hist_em", "fund_report_stock_cninfo", "fund_report_industry_allocation_cninfo",
    "fund_report_asset_allocation_cninfo", "fund_scale_change_em", "fund_hold_structure_em",
    "fund_stock_position_lg", "fund_balance_position_lg", "fund_linghuo_position_lg",
    "fund_announcement_dividend_em", "fund_announcement_report_em", "fund_announcement_personnel_em",
]


def snake_to_camel(snake_str: str) -> str:
    """将蛇形命名转换为驼峰命名"""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def generate_service_v2():
    """生成完整的FundRefreshServiceV2"""
    
    # 生成导入语句
    imports = []
    for collection in FUND_COLLECTIONS:
        class_name = snake_to_camel(collection) + "Service"
        imports.append(f"from app.services.data_sources.funds.services.{collection}_service import {class_name}")
    
    # 生成服务字典注册
    registrations = []
    for collection in FUND_COLLECTIONS:
        class_name = snake_to_camel(collection) + "Service"
        registrations.append(f'            "{collection}": {class_name}(self.db),')
    
    # 生成完整的文件内容
    content = f'''"""
基金数据刷新服务 V2
重构版：使用funds目录中的provider和service模块
包含全部70个基金数据集合
"""
import logging
from typing import Dict, Any
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager

# 导入所有基金服务
{chr(10).join(imports)}

logger = logging.getLogger("webapi")


class FundRefreshServiceV2:
    """基金数据刷新服务 V2"""
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        
        # 初始化所有70个服务
        self.services = {{
{chr(10).join(registrations)}
        }}
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的基金数据集合
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.start_task(task_id)
            self.task_manager.update_progress(task_id, 0, 100, f"开始刷新 {{collection_name}}...")
            
            # 检查服务是否存在
            if collection_name not in self.services:
                raise ValueError(f"未找到集合 {{collection_name}} 的服务")
            
            service = self.services[collection_name]
            
            # 更新进度
            self.task_manager.update_progress(task_id, 10, 100, f"正在获取 {{collection_name}} 数据...")
            
            # 调用服务刷新数据
            result = await service.refresh_data(**(params or {{}}))
            
            if result.get("success"):
                self.task_manager.update_progress(
                    task_id, 100, 100, 
                    f"成功刷新 {{collection_name}}，插入 {{result.get('inserted', 0)}} 条数据"
                )
                self.task_manager.complete_task(task_id)
            else:
                self.task_manager.fail_task(task_id, result.get("message", "刷新失败"))
            
            return result
            
        except Exception as e:
            logger.error(f"刷新 {{collection_name}} 失败: {{e}}", exc_info=True)
            self.task_manager.fail_task(task_id, str(e))
            raise
    
    async def get_collection_overview(self, collection_name: str) -> Dict[str, Any]:
        """获取集合数据概览"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {{collection_name}} 的服务")
        
        service = self.services[collection_name]
        return await service.get_overview()
    
    async def get_collection_data(
        self,
        collection_name: str,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None
    ) -> Dict[str, Any]:
        """获取集合数据"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {{collection_name}} 的服务")
        
        service = self.services[collection_name]
        return await service.get_data(skip=skip, limit=limit, filters=filters)
    
    async def clear_collection(self, collection_name: str) -> Dict[str, Any]:
        """清空集合数据"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {{collection_name}} 的服务")
        
        service = self.services[collection_name]
        return await service.clear_data()
    
    def get_supported_collections(self) -> list:
        """获取支持的所有数据集合列表"""
        return list(self.services.keys())
    
    def get_collection_count(self) -> int:
        """获取支持的数据集合数量"""
        return len(self.services)
'''
    
    return content


def main():
    """主函数"""
    content = generate_service_v2()
    
    # 写入文件
    output_file = Path("app/services/fund_refresh_service_v2.py")
    output_file.write_text(content, encoding='utf-8')
    
    print(f"✅ 成功生成 {output_file}")
    print(f"✅ 包含 {len(FUND_COLLECTIONS)} 个数据集合服务")


if __name__ == "__main__":
    main()
