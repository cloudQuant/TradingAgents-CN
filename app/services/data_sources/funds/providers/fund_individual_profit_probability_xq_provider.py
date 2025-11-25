"""
基金盈利概率-雪球数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundIndividualProfitProbabilityXqProvider:
    """基金盈利概率-雪球数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_individual_profit_probability_xq"
        self.display_name = "基金盈利概率-雪球"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取雪球基金盈利概率数据
        
        Returns:
            DataFrame: 基金盈利概率-雪球数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            df = ak.fund_individual_profit_probability_xq(**kwargs)
            
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
