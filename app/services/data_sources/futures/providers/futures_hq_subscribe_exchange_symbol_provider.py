"""
外盘品种代码表数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesHqSubscribeExchangeSymbolProvider:
    """外盘品种代码表数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_hq_subscribe_exchange_symbol"
        self.display_name = "外盘-品种代码表"
        self.akshare_func = "futures_hq_subscribe_exchange_symbol"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.futures_hq_subscribe_exchange_symbol()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["code"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "symbol", "type": "string", "description": "品种名称"},
            {"name": "code", "type": "string", "description": "品种代码"},
        ]
