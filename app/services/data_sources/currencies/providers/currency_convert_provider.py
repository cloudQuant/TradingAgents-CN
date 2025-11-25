"""
货币转换数据提供者
调用 AKShare 的 currency_convert 接口
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CurrencyConvertProvider:
    """货币转换数据提供者"""
    
    def __init__(self):
        self.collection_name = "currency_convert"
        self.display_name = "货币转换"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取货币转换数据
        
        Args:
            base: 基础货币，如 "USD"
            to: 目标货币，如 "CNY"
            amount: 金额
            api_key: API密钥
            
        Returns:
            DataFrame: 货币转换数据
        """
        try:
            base = kwargs.get("base", "USD")
            to = kwargs.get("to", "CNY")
            amount = kwargs.get("amount", "1")
            api_key = kwargs.get("api_key")
            
            if not api_key:
                raise ValueError("缺少必须参数: api_key")
            
            logger.info(f"Fetching {self.collection_name} data ({amount} {base} -> {to})")
            
            df = ak.currency_convert(base=base, to=to, amount=str(amount), api_key=api_key)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {base} -> {to}")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = 'currency_convert'
            
            logger.info(f"Successfully fetched conversion result")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "date", "type": "date", "description": "日期"},
            {"name": "base", "type": "string", "description": "基础货币"},
            {"name": "to", "type": "string", "description": "目标货币"},
            {"name": "amount", "type": "float", "description": "原始金额"},
            {"name": "value", "type": "float", "description": "转换后金额"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
