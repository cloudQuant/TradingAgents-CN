"""
现券市场成交行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondSpotDealProvider:
    """现券市场成交行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_spot_deal"
        self.display_name = "现券市场成交行情"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取现券市场成交行情"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_spot_deal()
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_spot_deal'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "债券简称", "type": "string", "description": "债券简称"},
            {"name": "债券代码", "type": "string", "description": "债券代码"},
            {"name": "成交净价(元)", "type": "float", "description": "成交净价"},
            {"name": "最新收益率(%)", "type": "float", "description": "最新收益率"},
            {"name": "涨跌(BP)", "type": "float", "description": "涨跌BP"},
            {"name": "加权收益率(%)", "type": "float", "description": "加权收益率"},
            {"name": "交易量(亿)", "type": "float", "description": "交易量"},
        ]
