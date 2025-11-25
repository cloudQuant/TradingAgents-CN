"""
债券成交概览数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondDealSummarySseProvider:
    """债券成交概览数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_deal_summary_sse"
        self.display_name = "债券成交概览"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取债券成交概览"""
        try:
            date = kwargs.get("date")
            if not date:
                date = datetime.now().strftime("%Y%m%d")
            else:
                date = str(date).replace("-", "")
            
            logger.info(f"Fetching {self.collection_name} data for {date}")
            
            df = ak.bond_deal_summary_sse(date=date)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {date}")
                return pd.DataFrame()
            
            df['查询日期'] = date
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_deal_summary_sse'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for {date}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "品种", "type": "string", "description": "债券品种"},
            {"name": "当日成交金额(亿元)", "type": "float", "description": "当日成交金额"},
            {"name": "今年累计成交金额(亿元)", "type": "float", "description": "今年累计成交金额"},
            {"name": "上市债券只数", "type": "int", "description": "上市债券只数"},
            {"name": "历年成交金额(亿元)", "type": "float", "description": "历年成交金额"},
        ]
