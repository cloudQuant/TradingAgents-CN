"""
期货资讯数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesNewsShmetProvider:
    """期货资讯数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_news_shmet"
        self.display_name = "期货资讯"
        self.akshare_func = "futures_news_shmet"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        try:
            symbol = kwargs.get("symbol", "")
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            
            # 该接口目前可能不可用，返回空DataFrame
            try:
                df = ak.futures_news_shmet(symbol=symbol) if symbol else ak.futures_news_shmet()
            except Exception:
                logger.warning(f"futures_news_shmet 接口可能暂不可用")
                return pd.DataFrame()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            if symbol:
                df['查询参数_symbol'] = symbol
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        return ["发布时间", "内容"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        return [
            {"name": "发布时间", "type": "string", "description": "发布时间"},
            {"name": "内容", "type": "string", "description": "内容"},
        ]
