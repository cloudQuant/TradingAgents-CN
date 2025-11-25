"""
基金分红-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundFhEmProvider:
    """基金分红-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_fh_em"
        self.display_name = "基金分红-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取基金分红数据
        
        Args:
            year/date: 年份（必填，如 "2024"）
        
        Returns:
            DataFrame: 基金分红-东财数据
        """
        try:
            # 处理参数名称映射
            date = kwargs.get("year") or kwargs.get("date")
            
            if not date:
                raise ValueError("缺少必须参数: year/date")
            
            logger.info(f"Fetching {self.collection_name} data for date={date}")
            df = ak.fund_fh_em(date=str(date))
            
            if df is None or df.empty:
                logger.warning(f"No data returned for date={date}")
                return pd.DataFrame()
            
            # 添加年份字段
            df['年份'] = str(date)
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for date={date}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "基金代码", "type": "string", "description": "基金代码"},
            {"name": "基金简称", "type": "string", "description": "基金简称"},
            {"name": "权益登记日", "type": "string", "description": "权益登记日"},
            {"name": "除息日", "type": "string", "description": "除息日"},
            {"name": "每份分红", "type": "float", "description": "每份分红"},
            {"name": "分红发放日", "type": "string", "description": "分红发放日"},
            {"name": "年份", "type": "string", "description": "年份"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
