"""
外盘实时行情数据-东财提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesGlobalSpotEmProvider:
    """外盘实时行情数据-东财提供者"""
    
    def __init__(self):
        self.collection_name = "futures_global_spot_em"
        self.display_name = "外盘-实时行情数据-东财"
        self.akshare_func = "futures_global_spot_em"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.futures_global_spot_em()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["代码"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "序号", "type": "int", "description": "序号"},
            {"name": "代码", "type": "string", "description": "代码"},
            {"name": "名称", "type": "string", "description": "名称"},
            {"name": "最新价", "type": "float", "description": "最新价"},
            {"name": "涨跌额", "type": "float", "description": "涨跌额"},
            {"name": "涨跌幅", "type": "string", "description": "涨跌幅"},
        ]
