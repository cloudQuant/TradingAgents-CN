"""
货币报价时间序列数据提供者
调用 AKShare 的 currency_time_series 接口
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CurrencyTimeSeriesProvider:
    """货币报价时间序列数据提供者"""
    
    def __init__(self):
        self.collection_name = "currency_time_series"
        self.display_name = "货币报价时间序列数据"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取货币报价时间序列数据
        
        Args:
            base: 基础货币，如 "USD"
            start_date: 开始日期，格式 "YYYY-MM-DD"
            end_date: 结束日期，格式 "YYYY-MM-DD"
            symbols: 目标货币，多个用逗号分隔
            api_key: API密钥
            
        Returns:
            DataFrame: 货币报价时间序列数据
        """
        try:
            base = kwargs.get("base", "USD")
            start_date = kwargs.get("start_date")
            end_date = kwargs.get("end_date")
            symbols = kwargs.get("symbols", "")
            api_key = kwargs.get("api_key")
            
            if not api_key:
                raise ValueError("缺少必须参数: api_key")
            if not start_date:
                raise ValueError("缺少必须参数: start_date")
            if not end_date:
                raise ValueError("缺少必须参数: end_date")
            
            logger.info(f"Fetching {self.collection_name} data (base={base}, {start_date} to {end_date})")
            
            df = ak.currency_time_series(
                base=base, 
                start_date=start_date, 
                end_date=end_date, 
                symbols=symbols, 
                api_key=api_key
            )
            
            if df is None or df.empty:
                logger.warning(f"No data returned for base={base}, {start_date} to {end_date}")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = 'currency_time_series'
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "date", "type": "date", "description": "日期"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
            # 动态货币列
        ]
