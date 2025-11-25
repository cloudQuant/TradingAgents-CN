"""
内盘实时行情数据(品种)提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesZhRealtimeProvider:
    """内盘实时行情数据(品种)提供者"""
    
    def __init__(self):
        self.collection_name = "futures_zh_realtime"
        self.display_name = "内盘-实时行情数据(品种)"
        self.akshare_func = "futures_zh_realtime"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_zh_realtime(symbol=symbol)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_symbol'] = symbol
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["symbol", "tradedate"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "symbol", "type": "string", "description": "合约代码"},
            {"name": "exchange", "type": "string", "description": "交易所"},
            {"name": "name", "type": "string", "description": "名称"},
            {"name": "trade", "type": "float", "description": "成交价"},
        ]
