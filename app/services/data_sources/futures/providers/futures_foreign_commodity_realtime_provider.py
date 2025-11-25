"""
外盘实时行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesForeignCommodityRealtimeProvider:
    """外盘实时行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_foreign_commodity_realtime"
        self.display_name = "外盘-实时行情数据"
        self.akshare_func = "futures_foreign_commodity_realtime"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_foreign_commodity_realtime(symbol=symbol)
            
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
        return ["名称"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "名称", "type": "string", "description": "名称"},
            {"name": "最新价", "type": "float", "description": "最新价"},
            {"name": "人民币报价", "type": "float", "description": "人民币报价"},
            {"name": "涨跌额", "type": "float", "description": "涨跌额"},
            {"name": "涨跌幅", "type": "string", "description": "涨跌幅"},
        ]
