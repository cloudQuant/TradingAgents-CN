"""
外盘合约详情提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesForeignDetailProvider:
    """外盘合约详情提供者"""
    
    def __init__(self):
        self.collection_name = "futures_foreign_detail"
        self.display_name = "外盘-合约详情"
        self.akshare_func = "futures_foreign_detail"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            df = ak.futures_foreign_detail(symbol=symbol)
            
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
        return ["查询参数_symbol", "交易品种"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "交易品种", "type": "string", "description": "交易品种"},
            {"name": "最小变动价位", "type": "string", "description": "最小变动价位"},
            {"name": "交易时间", "type": "string", "description": "交易时间"},
            {"name": "交易代码", "type": "string", "description": "交易代码"},
        ]
