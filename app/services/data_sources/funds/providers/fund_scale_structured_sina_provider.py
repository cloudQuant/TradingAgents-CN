"""
分级基金规模-新浪数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundScaleStructuredSinaProvider:
    """分级基金规模-新浪数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_scale_structured_sina"
        self.display_name = "分级基金规模-新浪"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取分级基金规模数据
        
        Returns:
            DataFrame: 分级基金规模-新浪数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.fund_scale_structured_sina(**kwargs)
            
            if df.empty:
                logger.warning(f"No data returned")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
