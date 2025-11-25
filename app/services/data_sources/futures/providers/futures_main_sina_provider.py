"""
期货连续合约数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesMainSinaProvider:
    """期货连续合约数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_main_sina"
        self.display_name = "期货连续合约"
        self.akshare_func = "futures_main_sina"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_main_sina(symbol=symbol)
            
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
        return ["查询参数_symbol", "date"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "开盘价", "type": "float", "description": "开盘价"},
            {"name": "最高价", "type": "float", "description": "最高价"},
            {"name": "最低价", "type": "float", "description": "最低价"},
            {"name": "收盘价", "type": "float", "description": "收盘价"},
            {"name": "成交量", "type": "int", "description": "成交量"},
            {"name": "持仓量", "type": "int", "description": "持仓量"},
        ]
