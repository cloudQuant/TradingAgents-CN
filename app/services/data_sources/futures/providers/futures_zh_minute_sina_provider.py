"""
内盘分时行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesZhMinuteSinaProvider:
    """内盘分时行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_zh_minute_sina"
        self.display_name = "内盘-分时行情数据"
        self.akshare_func = "futures_zh_minute_sina"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            period = kwargs.get("period", "1")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}, period={period}")
            df = ak.futures_zh_minute_sina(symbol=symbol, period=period)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_symbol'] = symbol
            df['查询参数_period'] = period
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["查询参数_symbol", "查询参数_period", "datetime"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "datetime", "type": "string", "description": "时间"},
            {"name": "open", "type": "float", "description": "开盘价"},
            {"name": "high", "type": "float", "description": "最高价"},
            {"name": "low", "type": "float", "description": "最低价"},
            {"name": "close", "type": "float", "description": "收盘价"},
            {"name": "volume", "type": "int", "description": "成交量"},
        ]
