"""
新加坡交易所期货数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesSettlementPriceSgxProvider:
    """新加坡交易所期货数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_settlement_price_sgx"
        self.display_name = "新加坡交易所期货"
        self.akshare_func = "futures_settlement_price_sgx"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            date = kwargs.get("date")
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            
            if date:
                df = ak.futures_settlement_price_sgx(date=date)
            else:
                df = ak.futures_settlement_price_sgx()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            if date:
                df['查询参数_date'] = date
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["合约"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "DATE", "type": "string", "description": "日期"},
            {"name": "COM", "type": "string", "description": "商品"},
            {"name": "OPEN", "type": "float", "description": "开盘价"},
            {"name": "HIGH", "type": "float", "description": "最高价"},
            {"name": "LOW", "type": "float", "description": "最低价"},
            {"name": "CLOSE", "type": "float", "description": "收盘价"},
            {"name": "SETTLE", "type": "float", "description": "结算价"},
        ]
