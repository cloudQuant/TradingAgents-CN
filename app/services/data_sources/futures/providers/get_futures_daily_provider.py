"""
内盘历史行情数据-交易所提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GetFuturesDailyProvider:
    """内盘历史行情数据-交易所提供者"""
    
    def __init__(self):
        self.collection_name = "get_futures_daily"
        self.display_name = "内盘-历史行情数据-交易所"
        self.akshare_func = "get_futures_daily"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            start_date = kwargs.get("start_date", "20200701")
            end_date = kwargs.get("end_date", "20200716")
            market = kwargs.get("market", "DCE")
            
            logger.info(f"Fetching {self.collection_name} data, market={market}")
            df = ak.get_futures_daily(start_date=start_date, end_date=end_date, market=market)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_market'] = market
            df['查询参数_start_date'] = start_date
            df['查询参数_end_date'] = end_date
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["查询参数_market", "symbol", "date"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "symbol", "type": "string", "description": "合约代码"},
            {"name": "date", "type": "string", "description": "日期"},
            {"name": "open", "type": "float", "description": "开盘价"},
            {"name": "high", "type": "float", "description": "最高价"},
            {"name": "low", "type": "float", "description": "最低价"},
            {"name": "close", "type": "float", "description": "收盘价"},
        ]
