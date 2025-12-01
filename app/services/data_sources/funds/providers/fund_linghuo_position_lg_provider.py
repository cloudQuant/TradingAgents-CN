"""
灵活配置型基金仓位-乐咕乐股数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundLinghuoPositionLgProvider(SimpleProvider):
    """灵活配置型基金仓位-乐咕乐股数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "乐咕乐股-基金仓位-灵活配置型基金仓位（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_linghuo_position_lg"
    collection_order = 68

    collection_name = "fund_linghuo_position_lg"
    display_name = "灵活配置型基金仓位-乐咕乐股"
    akshare_func = "fund_linghuo_position_lg"
    unique_keys = ["date"]  # 以date为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_linghuo_position_lg 接口不需要参数）
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
        {"name": "close", "type": "float", "description": "沪深300收盘价"},
        {"name": "position", "type": "float", "description": "持仓比例（%）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_linghuo_position_lg"},
    ]
