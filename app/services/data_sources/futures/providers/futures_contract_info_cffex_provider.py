"""
中国金融期货交易所合约信息数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesContractInfoCffexProvider:
    """中国金融期货交易所合约信息数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_contract_info_cffex"
        self.display_name = "合约信息-中国金融期货交易所"
        self.akshare_func = "futures_contract_info_cffex"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            date = kwargs.get("date")
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            df = ak.futures_contract_info_cffex(date=date)
            
            if df is None or df.empty:
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
        return ["合约代码"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "合约代码", "type": "string", "description": "合约代码"},
            {"name": "合约月份", "type": "string", "description": "合约月份"},
            {"name": "挂盘基准价", "type": "float", "description": "挂盘基准价"},
        ]
