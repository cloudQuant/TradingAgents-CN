"""
持续缩量数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StockRankCxslThsProvider:
    """持续缩量数据提供者"""
    
    def __init__(self):
        self.collection_name = "stock_rank_cxsl_ths"
        self.display_name = "持续缩量"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取持续缩量数据
        
        Returns:
            DataFrame: 持续缩量数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.stock_rank_cxsl_ths(**kwargs)
            
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
        # 这里需要根据实际API返回的字段来定义
        return [
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
