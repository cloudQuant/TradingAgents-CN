"""
可转债转股数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCovStockIssueCninfoProvider:
    """可转债转股数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cov_stock_issue_cninfo"
        self.display_name = "可转债转股"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取可转债转股数据
        
        注意: 该接口无需参数，返回所有可转债转股数据
        
        Returns:
            DataFrame: 所有可转债转股数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_cov_stock_issue_cninfo()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cov_stock_issue_cninfo'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "债券代码", "type": "string", "description": "债券代码"},
            {"name": "债券简称", "type": "string", "description": "债券简称"},
            {"name": "公告日期", "type": "string", "description": "公告日期"},
            {"name": "转股代码", "type": "string", "description": "转股代码"},
            {"name": "转股简称", "type": "string", "description": "转股简称"},
            {"name": "转股价格", "type": "float", "description": "转股价格(元)"},
            {"name": "自愿转换期起始日", "type": "string", "description": "自愿转换期起始日"},
            {"name": "自愿转换期终止日", "type": "string", "description": "自愿转换期终止日"},
            {"name": "标的股票", "type": "string", "description": "标的股票"},
            {"name": "债券名称", "type": "string", "description": "债券名称"},
        ]
