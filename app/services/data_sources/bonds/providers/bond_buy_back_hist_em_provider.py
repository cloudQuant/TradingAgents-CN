"""
质押式回购历史数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondBuyBackHistEmProvider:
    """质押式回购历史数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_buy_back_hist_em"
        self.display_name = "质押式回购历史数据"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取质押式回购历史数据
        
        Args:
            symbol: 质押式回购代码，如"204001"
            
        Returns:
            DataFrame: 历史行情数据
        """
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data for {symbol}")
            
            df = ak.bond_buy_back_hist_em(symbol=symbol)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['回购代码'] = symbol
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_buy_back_hist_em'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "开盘", "type": "float", "description": "开盘价"},
            {"name": "收盘", "type": "float", "description": "收盘价"},
            {"name": "最高", "type": "float", "description": "最高价"},
            {"name": "最低", "type": "float", "description": "最低价"},
            {"name": "成交量", "type": "float", "description": "成交量"},
            {"name": "成交额", "type": "float", "description": "成交额"},
        ]
