"""
库存数据-99期货网数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesInventory99Provider:
    """库存数据-99期货网数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_inventory_99"
        self.display_name = "库存数据-99期货网"
        self.akshare_func = "futures_inventory_99"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取库存数据-99期货网数据
        
        Args:
            symbol: 品种名称或代码（必需），如"豆一"
        """
        try:
            symbol = kwargs.get("symbol")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            
            df = ak.futures_inventory_99(symbol=symbol)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for symbol={symbol}")
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_symbol'] = symbol
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键字段"""
        return ["查询参数_symbol", "日期"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "收盘价", "type": "float", "description": "收盘价"},
            {"name": "库存", "type": "float", "description": "库存量"},
        ]
