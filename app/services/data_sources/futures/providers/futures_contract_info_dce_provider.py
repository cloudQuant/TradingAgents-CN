"""
大连商品交易所合约信息数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesContractInfoDceProvider:
    """大连商品交易所合约信息数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_contract_info_dce"
        self.display_name = "合约信息-大连商品交易所"
        self.akshare_func = "futures_contract_info_dce"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.futures_contract_info_dce()
            
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
        return ["合约代码"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "品种", "type": "string", "description": "品种"},
            {"name": "合约代码", "type": "string", "description": "合约代码"},
            {"name": "交易单位", "type": "string", "description": "交易单位"},
            {"name": "最小变动价位", "type": "float", "description": "最小变动价位"},
        ]
