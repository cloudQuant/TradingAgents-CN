"""
可转债价值分析数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhCovValueAnalysisProvider:
    """可转债价值分析数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_cov_value_analysis"
        self.display_name = "可转债价值分析"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取可转债价值分析数据
        
        Args:
            symbol: 可转债代码，如"113527"
            
        Returns:
            DataFrame: 可转债价值分析历史数据
        """
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data for {symbol}")
            
            df = ak.bond_zh_cov_value_analysis(symbol=symbol)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['可转债代码'] = symbol
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_cov_value_analysis'
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
            {"name": "收盘价", "type": "float", "description": "收盘价(元)"},
            {"name": "纯债价值", "type": "float", "description": "纯债价值(元)"},
            {"name": "转股价值", "type": "float", "description": "转股价值(元)"},
            {"name": "纯债溢价率", "type": "float", "description": "纯债溢价率(%)"},
            {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
        ]
