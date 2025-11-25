"""
现券市场做市报价数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondSpotQuoteProvider:
    """现券市场做市报价数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_spot_quote"
        self.display_name = "现券市场做市报价"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取现券市场做市报价"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_spot_quote()
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_spot_quote'
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
            {"name": "报价机构", "type": "string", "description": "报价机构"},
            {"name": "买入/卖出净价(元)", "type": "string", "description": "买入/卖出净价"},
            {"name": "买入/卖出收益率(%)", "type": "string", "description": "买入/卖出收益率"},
            {"name": "买入/卖出量(万)", "type": "string", "description": "买入/卖出量"},
            {"name": "债券代码", "type": "string", "description": "债券代码"},
            {"name": "更新时间", "type": "string", "description": "更新时间"},
        ]
