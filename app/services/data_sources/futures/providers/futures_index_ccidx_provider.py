"""
中证商品指数数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesIndexCcidxProvider:
    """中证商品指数数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_index_ccidx"
        self.display_name = "中证商品指数"
        self.akshare_func = "futures_index_ccidx"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_index_ccidx(symbol=symbol)
            
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
            {"name": "指数代码", "type": "string", "description": "指数代码"},
            {"name": "收盘点位", "type": "float", "description": "收盘点位"},
            {"name": "结算点位", "type": "float", "description": "结算点位"},
        ]
