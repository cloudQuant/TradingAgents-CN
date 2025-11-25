"""
内盘历史行情数据-东财提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesHistEmProvider:
    """内盘历史行情数据-东财提供者"""
    
    def __init__(self):
        self.collection_name = "futures_hist_em"
        self.display_name = "内盘-历史行情数据-东财"
        self.akshare_func = "futures_hist_em"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            period = kwargs.get("period", "daily")
            start_date = kwargs.get("start_date", "19900101")
            end_date = kwargs.get("end_date", "20500101")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}, period={period}")
            df = ak.futures_hist_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
            
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
        return ["查询参数_symbol", "查询参数_period", "时间"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "时间", "type": "string", "description": "时间"},
            {"name": "开盘", "type": "float", "description": "开盘价"},
            {"name": "最高", "type": "float", "description": "最高价"},
            {"name": "最低", "type": "float", "description": "最低价"},
            {"name": "收盘", "type": "float", "description": "收盘价"},
            {"name": "成交量", "type": "int", "description": "成交量"},
        ]
