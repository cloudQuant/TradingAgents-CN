"""
自动生成基金数据的providers和services模块
根据fund_refresh_service.py中的_refresh_方法自动创建对应的provider和service文件
"""
import re
import os
from pathlib import Path

# 基金数据集合映射
FUND_COLLECTIONS = {
    "fund_name_em": {
        "akshare_func": "fund_name_em",
        "display_name": "基金基本信息-东财",
        "description": "获取东方财富基金基本信息数据"
    },
    "fund_basic_info": {
        "akshare_func": "fund_individual_basic_info_xq",
        "display_name": "基金基本信息-雪球",
        "description": "获取雪球基金基本信息数据"
    },
    "fund_info_index_em": {
        "akshare_func": "fund_info_index_em",
        "display_name": "指数型基金基本信息-东财",
        "description": "获取指数型基金基本信息数据"
    },
    "fund_purchase_status": {
        "akshare_func": "fund_purchase_em",
        "display_name": "基金申购状态-东财",
        "description": "获取基金申购状态数据"
    },
    "fund_etf_spot_em": {
        "akshare_func": "fund_etf_spot_em",
        "display_name": "ETF实时行情-东财",
        "description": "获取ETF基金实时行情数据"
    },
    "fund_etf_spot_ths": {
        "akshare_func": "fund_etf_spot_ths",
        "display_name": "ETF实时行情-同花顺",
        "description": "获取同花顺ETF实时行情数据"
    },
    "fund_lof_spot_em": {
        "akshare_func": "fund_lof_spot_em",
        "display_name": "LOF实时行情-东财",
        "description": "获取LOF基金实时行情数据"
    },
    "fund_spot_sina": {
        "akshare_func": "fund_spot_em",
        "display_name": "基金实时行情-新浪",
        "description": "获取新浪基金实时行情数据"
    },
    "fund_etf_hist_min_em": {
        "akshare_func": "fund_etf_hist_min_em",
        "display_name": "ETF分时行情-东财",
        "description": "获取ETF基金分时行情数据"
    },
    "fund_lof_hist_min_em": {
        "akshare_func": "fund_lof_hist_min_em",
        "display_name": "LOF分时行情-东财",
        "description": "获取LOF基金分时行情数据"
    },
    "fund_etf_hist_em": {
        "akshare_func": "fund_etf_hist_em",
        "display_name": "ETF历史行情-东财",
        "description": "获取ETF历史行情数据"
    },
    "fund_lof_hist_em": {
        "akshare_func": "fund_lof_hist_em",
        "display_name": "LOF历史行情-东财",
        "description": "获取LOF历史行情数据"
    },
    "fund_hist_sina": {
        "akshare_func": "fund_hist_sina",
        "display_name": "基金历史行情-新浪",
        "description": "获取新浪基金历史行情数据"
    },
    "fund_open_fund_daily_em": {
        "akshare_func": "fund_open_fund_daily_em",
        "display_name": "开放式基金实时行情-东财",
        "description": "获取开放式基金实时行情数据"
    },
    "fund_open_fund_info_em": {
        "akshare_func": "fund_open_fund_info_em",
        "display_name": "开放式基金历史行情-东财",
        "description": "获取开放式基金历史行情数据"
    },
    "fund_money_fund_daily_em": {
        "akshare_func": "fund_money_fund_daily_em",
        "display_name": "货币型基金实时行情-东财",
        "description": "获取货币型基金实时行情数据"
    },
    "fund_money_fund_info_em": {
        "akshare_func": "fund_money_fund_info_em",
        "display_name": "货币型基金历史行情-东财",
        "description": "获取货币型基金历史行情数据"
    },
    "fund_financial_fund_daily_em": {
        "akshare_func": "fund_financial_fund_daily_em",
        "display_name": "理财型基金实时行情-东财",
        "description": "获取理财型基金实时行情数据"
    },
    "fund_financial_fund_info_em": {
        "akshare_func": "fund_financial_fund_info_em",
        "display_name": "理财型基金历史行情-东财",
        "description": "获取理财型基金历史行情数据"
    },
    "fund_graded_fund_daily_em": {
        "akshare_func": "fund_graded_fund_daily_em",
        "display_name": "分级基金实时数据-东财",
        "description": "获取分级基金实时数据"
    },
    "fund_graded_fund_info_em": {
        "akshare_func": "fund_graded_fund_info_em",
        "display_name": "分级基金历史数据-东财",
        "description": "获取分级基金历史数据"
    },
    "fund_etf_fund_daily_em": {
        "akshare_func": "fund_etf_fund_daily_em",
        "display_name": "场内交易基金实时数据-东财",
        "description": "获取场内交易基金实时数据"
    },
    "fund_hk_hist_em": {
        "akshare_func": "fund_hk_hist_em",
        "display_name": "香港基金历史数据-东财",
        "description": "获取香港基金历史数据"
    },
    "fund_etf_fund_info_em": {
        "akshare_func": "fund_etf_fund_info_em",
        "display_name": "场内交易基金历史行情-东财",
        "description": "获取场内交易基金历史行情数据"
    },
    "fund_etf_dividend_sina": {
        "akshare_func": "fund_etf_dividend_sina",
        "display_name": "基金累计分红-新浪",
        "description": "获取基金累计分红数据"
    },
    "fund_fh_em": {
        "akshare_func": "fund_fh_em",
        "display_name": "基金分红-东财",
        "description": "获取基金分红数据"
    },
    "fund_cf_em": {
        "akshare_func": "fund_cf_em",
        "display_name": "基金拆分-东财",
        "description": "获取基金拆分数据"
    },
    "fund_fh_rank_em": {
        "akshare_func": "fund_fh_rank_em",
        "display_name": "基金分红排行-东财",
        "description": "获取基金分红排行数据"
    },
    "fund_open_fund_rank_em": {
        "akshare_func": "fund_open_fund_rank_em",
        "display_name": "开放式基金排行-东财",
        "description": "获取开放式基金排行数据"
    },
    "fund_exchange_rank_em": {
        "akshare_func": "fund_exchange_rank_em",
        "display_name": "场内基金排行-东财",
        "description": "获取场内基金排行数据"
    },
    "fund_money_rank_em": {
        "akshare_func": "fund_money_rank_em",
        "display_name": "货币型基金排行-东财",
        "description": "获取货币型基金排行数据"
    },
    "fund_lcx_rank_em": {
        "akshare_func": "fund_lcx_rank_em",
        "display_name": "理财型基金排行-东财",
        "description": "获取理财型基金排行数据"
    },
    "fund_hk_rank_em": {
        "akshare_func": "fund_hk_rank_em",
        "display_name": "香港基金排行-东财",
        "description": "获取香港基金排行数据"
    },
    "fund_individual_achievement_xq": {
        "akshare_func": "fund_individual_achievement_xq",
        "display_name": "基金业绩表现-雪球",
        "description": "获取雪球基金业绩表现数据"
    },
    "fund_value_estimation_em": {
        "akshare_func": "fund_value_estimation_em",
        "display_name": "基金净值估算-东财",
        "description": "获取基金净值估算数据"
    },
    "fund_individual_analysis_xq": {
        "akshare_func": "fund_individual_analysis_xq",
        "display_name": "基金分析数据-雪球",
        "description": "获取雪球基金分析数据"
    },
    "fund_individual_profit_probability_xq": {
        "akshare_func": "fund_individual_profit_probability_xq",
        "display_name": "基金盈利概率-雪球",
        "description": "获取雪球基金盈利概率数据"
    },
    "fund_individual_detail_hold_xq": {
        "akshare_func": "fund_individual_detail_hold_xq",
        "display_name": "基金持仓明细-雪球",
        "description": "获取雪球基金持仓明细数据"
    },
    "fund_overview_em": {
        "akshare_func": "fund_overview_em",
        "display_name": "基金概况-东财",
        "description": "获取基金概况数据"
    },
    "fund_fee_em": {
        "akshare_func": "fund_fee_em",
        "display_name": "基金费率-东财",
        "description": "获取基金费率数据"
    },
    "fund_individual_detail_info_xq": {
        "akshare_func": "fund_individual_detail_info_xq",
        "display_name": "基金详细信息-雪球",
        "description": "获取雪球基金详细信息数据"
    },
    "fund_portfolio_hold_em": {
        "akshare_func": "fund_portfolio_hold_em",
        "display_name": "基金持仓股票-东财",
        "description": "获取基金持仓股票数据"
    },
    "fund_portfolio_bond_hold_em": {
        "akshare_func": "fund_portfolio_bond_hold_em",
        "display_name": "基金持仓债券-东财",
        "description": "获取基金持仓债券数据"
    },
    "fund_portfolio_industry_allocation_em": {
        "akshare_func": "fund_portfolio_industry_allocation_em",
        "display_name": "基金行业配置-东财",
        "description": "获取基金行业配置数据"
    },
    "fund_portfolio_change_em": {
        "akshare_func": "fund_portfolio_change_em",
        "display_name": "基金持仓变动-东财",
        "description": "获取基金持仓变动数据"
    },
    "fund_rating_all_em": {
        "akshare_func": "fund_rating_all_em",
        "display_name": "基金评级汇总-东财",
        "description": "获取基金评级汇总数据"
    },
    "fund_rating_sh_em": {
        "akshare_func": "fund_rating_sh_em",
        "display_name": "基金评级-上海证券-东财",
        "description": "获取上海证券基金评级数据"
    },
    "fund_rating_zs_em": {
        "akshare_func": "fund_rating_zs_em",
        "display_name": "基金评级-招商证券-东财",
        "description": "获取招商证券基金评级数据"
    },
    "fund_rating_ja_em": {
        "akshare_func": "fund_rating_ja_em",
        "display_name": "基金评级-济安金信-东财",
        "description": "获取济安金信基金评级数据"
    },
    "fund_manager_em": {
        "akshare_func": "fund_manager_em",
        "display_name": "基金经理-东财",
        "description": "获取基金经理数据"
    },
    "fund_new_found_em": {
        "akshare_func": "fund_new_found_em",
        "display_name": "新发基金-东财",
        "description": "获取新发基金数据"
    },
    "fund_scale_open_sina": {
        "akshare_func": "fund_scale_open_sina",
        "display_name": "开放式基金规模-新浪",
        "description": "获取开放式基金规模数据"
    },
    "fund_scale_close_sina": {
        "akshare_func": "fund_scale_close_sina",
        "display_name": "封闭式基金规模-新浪",
        "description": "获取封闭式基金规模数据"
    },
    "fund_scale_structured_sina": {
        "akshare_func": "fund_scale_structured_sina",
        "display_name": "分级基金规模-新浪",
        "description": "获取分级基金规模数据"
    },
    "fund_aum_em": {
        "akshare_func": "fund_aum_em",
        "display_name": "基金管理规模-东财",
        "description": "获取基金管理规模数据"
    },
    "fund_aum_trend_em": {
        "akshare_func": "fund_aum_trend_em",
        "display_name": "基金规模趋势-东财",
        "description": "获取基金规模趋势数据"
    },
    "fund_aum_hist_em": {
        "akshare_func": "fund_aum_hist_em",
        "display_name": "基金规模历史-东财",
        "description": "获取基金规模历史数据"
    },
    "reits_realtime_em": {
        "akshare_func": "reits_realtime_em",
        "display_name": "REITs实时行情-东财",
        "description": "获取REITs实时行情数据"
    },
    "reits_hist_em": {
        "akshare_func": "reits_hist_em",
        "display_name": "REITs历史行情-东财",
        "description": "获取REITs历史行情数据"
    },
    "fund_report_stock_cninfo": {
        "akshare_func": "fund_report_stock_cninfo",
        "display_name": "基金报告持股-巨潮",
        "description": "获取基金报告持股数据"
    },
    "fund_report_industry_allocation_cninfo": {
        "akshare_func": "fund_report_industry_allocation_cninfo",
        "display_name": "基金报告行业配置-巨潮",
        "description": "获取基金报告行业配置数据"
    },
    "fund_report_asset_allocation_cninfo": {
        "akshare_func": "fund_report_asset_allocation_cninfo",
        "display_name": "基金报告资产配置-巨潮",
        "description": "获取基金报告资产配置数据"
    },
    "fund_scale_change_em": {
        "akshare_func": "fund_scale_change_em",
        "display_name": "基金规模变动-东财",
        "description": "获取基金规模变动数据"
    },
    "fund_hold_structure_em": {
        "akshare_func": "fund_hold_structure_em",
        "display_name": "基金持有结构-东财",
        "description": "获取基金持有结构数据"
    },
    "fund_stock_position_lg": {
        "akshare_func": "fund_stock_position_lg",
        "display_name": "股票型基金仓位-理杏仁",
        "description": "获取股票型基金仓位数据"
    },
    "fund_balance_position_lg": {
        "akshare_func": "fund_balance_position_lg",
        "display_name": "平衡型基金仓位-理杏仁",
        "description": "获取平衡型基金仓位数据"
    },
    "fund_linghuo_position_lg": {
        "akshare_func": "fund_linghuo_position_lg",
        "display_name": "灵活配置型基金仓位-理杏仁",
        "description": "获取灵活配置型基金仓位数据"
    },
    "fund_announcement_dividend_em": {
        "akshare_func": "fund_announcement_dividend_em",
        "display_name": "基金分红公告-东财",
        "description": "获取基金分红公告数据"
    },
    "fund_announcement_report_em": {
        "akshare_func": "fund_announcement_report_em",
        "display_name": "基金报告公告-东财",
        "description": "获取基金报告公告数据"
    },
    "fund_announcement_personnel_em": {
        "akshare_func": "fund_announcement_personnel_em",
        "display_name": "基金人事公告-东财",
        "description": "获取基金人事公告数据"
    },
}


def snake_to_camel(snake_str: str) -> str:
    """将蛇形命名转换为驼峰命名"""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def generate_provider_file(collection_name: str, info: dict) -> str:
    """生成provider文件内容"""
    class_name = snake_to_camel(collection_name) + "Provider"
    
    return f'''"""
{info['display_name']}数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class {class_name}:
    """{info['display_name']}数据提供者"""
    
    def __init__(self):
        self.collection_name = "{collection_name}"
        self.display_name = "{info['display_name']}"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        {info['description']}
        
        Returns:
            DataFrame: {info['display_name']}数据
        """
        try:
            logger.info(f"Fetching {{self.collection_name}} data")
            df = ak.{info['akshare_func']}(**kwargs)
            
            if df.empty:
                logger.warning(f"No data returned")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {{len(df)}} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {{self.collection_name}} data: {{e}}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {{"name": "scraped_at", "type": "datetime", "description": "抓取时间"}},
        ]
'''


def generate_service_file(collection_name: str, info: dict) -> str:
    """生成service文件内容"""
    class_name = snake_to_camel(collection_name) + "Service"
    provider_class = snake_to_camel(collection_name) + "Provider"
    provider_file = collection_name + "_provider"
    
    return f'''"""
{info['display_name']}服务
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.{provider_file} import {provider_class}

logger = logging.getLogger(__name__)


class {class_name}:
    """{info['display_name']}服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db.funds.{collection_name}
        self.provider = {provider_class}()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({{}})
        
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        return {{
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
        }}
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {{}}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("scraped_at", -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {{
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }}
    
    async def refresh_data(self, **kwargs) -> Dict[str, Any]:
        """刷新数据"""
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {{
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }}
            
            records = df.to_dict('records')
            
            # 批量插入
            if records:
                result = await self.collection.insert_many(records)
                return {{
                    "success": True,
                    "message": "Data refreshed successfully",
                    "inserted": len(result.inserted_ids),
                }}
            
            return {{
                "success": True,
                "message": "No operations performed",
                "inserted": 0,
            }}
            
        except Exception as e:
            logger.error(f"Error refreshing data: {{e}}")
            return {{
                "success": False,
                "message": str(e),
                "inserted": 0,
            }}
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空数据"""
        result = await self.collection.delete_many({{}})
        return {{
            "success": True,
            "message": f"Deleted {{result.deleted_count}} records",
            "deleted": result.deleted_count,
        }}
'''


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    funds_dir = project_root / "app" / "services" / "data_sources" / "funds"
    
    providers_dir = funds_dir / "providers"
    services_dir = funds_dir / "services"
    
    # 确保目录存在
    providers_dir.mkdir(parents=True, exist_ok=True)
    services_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建__init__.py文件
    (providers_dir / "__init__.py").write_text('"""\n基金数据提供者模块\n"""\n', encoding='utf-8')
    (services_dir / "__init__.py").write_text('"""\n基金数据服务模块\n"""\n', encoding='utf-8')
    
    # 生成所有provider和service文件
    for collection_name, info in FUND_COLLECTIONS.items():
        # 生成provider文件
        provider_file = providers_dir / f"{collection_name}_provider.py"
        provider_content = generate_provider_file(collection_name, info)
        provider_file.write_text(provider_content, encoding='utf-8')
        print(f"Created: {provider_file}")
        
        # 生成service文件
        service_file = services_dir / f"{collection_name}_service.py"
        service_content = generate_service_file(collection_name, info)
        service_file.write_text(service_content, encoding='utf-8')
        print(f"Created: {service_file}")
    
    print(f"\n成功生成 {len(FUND_COLLECTIONS)} 个provider和service文件！")


if __name__ == "__main__":
    main()
