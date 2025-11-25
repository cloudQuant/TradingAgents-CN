"""
生猪市场价格指数数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class IndexHogSpotPriceProvider:
    """生猪市场价格指数数据提供者"""
    
    def __init__(self):
        self.collection_name = "index_hog_spot_price"
        self.display_name = "生猪市场价格指数"
        self.akshare_func = "index_hog_spot_price"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.index_hog_spot_price()
            
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
        return ["日期"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "指数", "type": "float", "description": "指数"},
            {"name": "预售均价", "type": "float", "description": "预售均价"},
            {"name": "成交均价", "type": "float", "description": "成交均价"},
            {"name": "成交均重", "type": "float", "description": "成交均重"},
        ]
