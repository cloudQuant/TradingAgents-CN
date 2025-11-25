"""
货币基础信息数据提供者
调用 AKShare 的 currency_currencies 接口
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CurrencyCurrenciesProvider:
    """货币基础信息数据提供者"""
    
    def __init__(self):
        self.collection_name = "currency_currencies"
        self.display_name = "货币基础信息查询"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取货币基础信息数据
        
        Args:
            c_type: 货币类型，"fiat"（法定货币）或 "crypto"（加密货币）
            api_key: API密钥
            
        Returns:
            DataFrame: 货币基础信息数据
        """
        try:
            c_type = kwargs.get("c_type", "fiat")
            api_key = kwargs.get("api_key")
            
            if not api_key:
                raise ValueError("缺少必须参数: api_key")
            
            logger.info(f"Fetching {self.collection_name} data (c_type={c_type})")
            
            df = ak.currency_currencies(c_type=c_type, api_key=api_key)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for c_type={c_type}")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = 'currency_currencies'
            df['货币类型'] = c_type
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "id", "type": "int", "description": "ID"},
            {"name": "name", "type": "string", "description": "货币名称"},
            {"name": "short_code", "type": "string", "description": "短代码"},
            {"name": "code", "type": "string", "description": "代码"},
            {"name": "precision", "type": "int", "description": "精度"},
            {"name": "subunit", "type": "int", "description": "子单位"},
            {"name": "symbol", "type": "string", "description": "符号"},
            {"name": "symbol_first", "type": "bool", "description": "符号在前"},
            {"name": "decimal_mark", "type": "string", "description": "小数点"},
            {"name": "thousands_separator", "type": "string", "description": "千位分隔符"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
