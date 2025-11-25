"""
上海期货交易所期转现数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesToSpotShfeProvider:
    """上海期货交易所期转现数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_to_spot_shfe"
        self.display_name = "期转现-上期所"
        self.akshare_func = "futures_to_spot_shfe"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取上海期货交易所期转现数据
        
        Args:
            date: 交易月份（必需），格式YYYYMM
        """
        try:
            date = kwargs.get("date")
            
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            
            df = ak.futures_to_spot_shfe(date=date)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for date={date}")
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_date'] = date
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["日期", "合约"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "合约", "type": "string", "description": "合约"},
            {"name": "交割量", "type": "int", "description": "交割量"},
            {"name": "期转现量", "type": "int", "description": "期转现量"},
        ]
