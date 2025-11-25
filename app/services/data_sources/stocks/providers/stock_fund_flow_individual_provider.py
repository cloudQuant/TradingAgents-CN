"""
Stock Fund Flow Individual数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StockFundFlowIndividualProvider:
    """Stock Fund Flow Individual数据提供者"""
    
    def __init__(self):
        self.collection_name = "stock_fund_flow_individual"
        self.display_name = "Stock Fund Flow Individual"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取Stock Fund Flow Individual数据
        
        Returns:
            DataFrame: Stock Fund Flow Individual数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.stock_fund_flow_individual(**kwargs)
            
            if df is None or df.empty:
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
