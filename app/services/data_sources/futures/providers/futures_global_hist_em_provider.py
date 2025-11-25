"""
外盘历史行情数据-东财提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesGlobalHistEmProvider:
    """外盘历史行情数据-东财提供者"""
    
    def __init__(self):
        self.collection_name = "futures_global_hist_em"
        self.display_name = "外盘-历史行情数据-东财"
        self.akshare_func = "futures_global_hist_em"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            start_date = kwargs.get("start_date", "19700101")
            end_date = kwargs.get("end_date", "20500101")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_global_hist_em(symbol=symbol, start_date=start_date, end_date=end_date)
            
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
        return ["查询参数_symbol", "日期"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "代码", "type": "string", "description": "代码"},
            {"name": "名称", "type": "string", "description": "名称"},
            {"name": "开盘", "type": "float", "description": "开盘价"},
            {"name": "最新价", "type": "float", "description": "最新价"},
        ]
