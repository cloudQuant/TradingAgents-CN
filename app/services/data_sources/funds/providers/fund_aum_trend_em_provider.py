"""
基金规模趋势-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundAumTrendEmProvider(SimpleProvider):
    """基金规模趋势-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-基金数据-基金规模走势（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_aum_trend_em"
    collection_order = 57

    collection_name = "fund_aum_trend_em"
    display_name = "基金规模走势-东财"
    akshare_func = "fund_aum_trend_em"
    unique_keys = ["date"]  # 以date为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_aum_trend_em 接口不需要参数）
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
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "value", "type": "float", "description": "基金规模值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_aum_trend_em"},
    ]
