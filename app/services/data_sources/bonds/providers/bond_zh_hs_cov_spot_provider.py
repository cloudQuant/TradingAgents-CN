"""
可转债实时行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhHsCovSpotProvider:
    """可转债实时行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_hs_cov_spot"
        self.display_name = "可转债实时行情"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取可转债实时行情数据"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_zh_hs_cov_spot()
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_hs_cov_spot'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "代码", "type": "string", "description": "可转债代码"},
            {"name": "名称", "type": "string", "description": "可转债名称"},
            {"name": "最新价", "type": "float", "description": "最新价"},
            {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
            {"name": "涨跌额", "type": "float", "description": "涨跌额"},
            {"name": "成交量", "type": "float", "description": "成交量(手)"},
            {"name": "成交额", "type": "float", "description": "成交额"},
            {"name": "今开", "type": "float", "description": "今日开盘价"},
            {"name": "昨收", "type": "float", "description": "昨日收盘价"},
            {"name": "最高", "type": "float", "description": "最高价"},
            {"name": "最低", "type": "float", "description": "最低价"},
            {"name": "申买价", "type": "float", "description": "申买价"},
            {"name": "申卖价", "type": "float", "description": "申卖价"},
        ]
