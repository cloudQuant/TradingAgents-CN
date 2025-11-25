"""
现货与股票数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesSpotStockProvider:
    """现货与股票数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_spot_stock"
        self.display_name = "现货与股票"
        self.akshare_func = "futures_spot_stock"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_spot_stock(symbol=symbol)
            
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
            {"name": "商品名称", "type": "string", "description": "商品名称"},
            {"name": "最新价", "type": "float", "description": "最新价"},
            {"name": "近半年涨跌幅", "type": "string", "description": "近半年涨跌幅"},
        ]
