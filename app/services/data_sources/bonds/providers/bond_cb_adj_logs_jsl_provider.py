"""
转股价调整记录-集思录数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCbAdjLogsJslProvider:
    """转股价调整记录-集思录数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cb_adj_logs_jsl"
        self.display_name = "转股价调整记录-集思录"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取转股价调整记录"""
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data for {symbol}")
            
            df = ak.bond_cb_adj_logs_jsl(symbol=symbol)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['可转债代码'] = symbol
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cb_adj_logs_jsl'
            df['更新时间'] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "转债名称", "type": "string", "description": "可转债名称"},
            {"name": "股东大会日", "type": "string", "description": "股东大会日期"},
            {"name": "下修前转股价", "type": "float", "description": "下修前转股价"},
            {"name": "下修后转股价", "type": "float", "description": "下修后转股价"},
            {"name": "新转股价生效日期", "type": "string", "description": "新转股价生效日期"},
            {"name": "下修底价", "type": "float", "description": "下修底价"},
        ]
