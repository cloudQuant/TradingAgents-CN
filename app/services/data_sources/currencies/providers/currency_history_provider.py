"""
货币报价历史数据提供者
调用 AKShare 的 currency_history 接口
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CurrencyHistoryProvider:
    """货币报价历史数据提供者"""
    
    def __init__(self):
        self.collection_name = "currency_history"
        self.display_name = "货币报价历史数据"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取货币报价历史数据
        
        Args:
            base: 基础货币，如 "USD"
            date: 日期，格式 "YYYY-MM-DD"
            symbols: 目标货币，多个用逗号分隔
            api_key: API密钥
            
        Returns:
            DataFrame: 货币报价历史数据
        """
        try:
            base = kwargs.get("base", "USD")
            date = kwargs.get("date")
            symbols = kwargs.get("symbols", "")
            api_key = kwargs.get("api_key")
            
            if not api_key:
                raise ValueError("缺少必须参数: api_key")
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data (base={base}, date={date})")
            
            df = ak.currency_history(base=base, date=date, symbols=symbols, api_key=api_key)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for base={base}, date={date}")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = 'currency_history'
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "currency", "type": "string", "description": "货币代码"},
            {"name": "date", "type": "date", "description": "日期"},
            {"name": "base", "type": "string", "description": "基础货币"},
            {"name": "rates", "type": "float", "description": "汇率"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
