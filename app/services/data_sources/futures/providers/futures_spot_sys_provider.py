"""
现期图数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesSpotSysProvider:
    """现期图数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_spot_sys"
        self.display_name = "现期图"
        self.akshare_func = "futures_spot_sys"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取现期图数据
        
        Args:
            symbol: 品种代码（必需）
            indicator: 合约代码/指标（必需）
        """
        try:
            symbol = kwargs.get("symbol")
            indicator = kwargs.get("indicator") or kwargs.get("contract")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            if not indicator:
                raise ValueError("缺少必须参数: indicator")
            
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}, indicator={indicator}")
            
            df = ak.futures_spot_sys(symbol=symbol, contract=indicator)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for symbol={symbol}, indicator={indicator}")
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_symbol'] = symbol
            df['查询参数_indicator'] = indicator
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["日期", "查询参数_symbol", "查询参数_indicator"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "日期", "type": "string", "description": "日期"},
            {"name": "主力基差", "type": "float", "description": "主力基差"},
        ]
