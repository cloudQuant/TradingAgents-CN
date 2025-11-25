"""
内盘实时行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesZhSpotProvider:
    """内盘实时行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_zh_spot"
        self.display_name = "内盘-实时行情数据"
        self.akshare_func = "futures_zh_spot"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol")
            market = kwargs.get("market", "CF")
            adjust = kwargs.get("adjust", "0")
            
            logger.info(f"Fetching {self.collection_name} data, market={market}")
            df = ak.futures_zh_spot(subscribe_list=symbol, market=market, adjust=adjust)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_market'] = market
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["symbol", "time"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "symbol", "type": "string", "description": "合约代码"},
            {"name": "time", "type": "string", "description": "时间"},
            {"name": "open", "type": "float", "description": "开盘价"},
            {"name": "high", "type": "float", "description": "最高价"},
            {"name": "low", "type": "float", "description": "最低价"},
            {"name": "current_price", "type": "float", "description": "当前价"},
            {"name": "volume", "type": "int", "description": "成交量"},
        ]
