"""
货币型基金排行-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundMoneyRankEmProvider(SimpleProvider):
    """货币型基金排行-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-数据中心-货币型基金排行，每个交易日17点后更新"
    collection_route = "/funds/collections/fund_money_rank_em"
    collection_order = 32

    collection_name = "fund_money_rank_em"
    display_name = "货币型基金排行-东财"
    akshare_func = "fund_money_rank_em"
    unique_keys = ["基金代码", "日期"]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_money_rank_em 接口不需要参数）
            df = self._call_akshare(self.akshare_func)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise

    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
        {"name": "万份收益", "type": "string", "description": ""},
        {"name": "年化收益率7日", "type": "string", "description": ""},
        {"name": "年化收益率14日", "type": "string", "description": ""},
        {"name": "年化收益率28日", "type": "string", "description": ""},
        {"name": "近1月", "type": "string", "description": ""},
        {"name": "近3月", "type": "string", "description": ""},
        {"name": "近6月", "type": "string", "description": ""},
        {"name": "近1年", "type": "string", "description": ""},
        {"name": "近2年", "type": "string", "description": ""},
        {"name": "近3年", "type": "string", "description": ""},
        {"name": "近5年", "type": "string", "description": ""},
        {"name": "今年来", "type": "string", "description": ""},
        {"name": "成立来", "type": "string", "description": ""},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_money_rank_em"},
    ]
