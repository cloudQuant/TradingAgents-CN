"""
可转债历史行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhHsCovDailyProvider:
    """可转债历史行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_hs_cov_daily"
        self.display_name = "可转债历史行情"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取可转债历史行情数据"""
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data for {symbol}")
            
            df = ak.bond_zh_hs_cov_daily(symbol=symbol)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {symbol}")
                return pd.DataFrame()
            
            df['可转债代码'] = symbol
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_hs_cov_daily'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "date", "type": "string", "description": "日期"},
            {"name": "open", "type": "float", "description": "开盘价"},
            {"name": "high", "type": "float", "description": "最高价"},
            {"name": "low", "type": "float", "description": "最低价"},
            {"name": "close", "type": "float", "description": "收盘价"},
            {"name": "volume", "type": "float", "description": "成交量"},
        ]
