"""
货币报价最新数据提供者
调用 AKShare 的 currency_latest 接口
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CurrencyLatestProvider:
    """货币报价最新数据提供者"""
    
    def __init__(self):
        self.collection_name = "currency_latest"
        self.display_name = "货币报价最新数据"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取货币报价最新数据
        
        Args:
            base: 基础货币，如 "USD"
            symbols: 目标货币，多个用逗号分隔，如 "CNY,EUR"
            api_key: API密钥
            
        Returns:
            DataFrame: 货币报价数据
        """
        try:
            base = kwargs.get("base", "USD")
            symbols = kwargs.get("symbols", "")
            api_key = kwargs.get("api_key")
            
            if not api_key:
                raise ValueError("缺少必须参数: api_key")
            
            logger.info(f"Fetching {self.collection_name} data (base={base})")
            
            df = ak.currency_latest(base=base, symbols=symbols, api_key=api_key)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for base={base}")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = 'currency_latest'
            
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
