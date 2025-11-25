"""
可转债详情-同花顺数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhCovInfoThsProvider:
    """可转债详情-同花顺数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_cov_info_ths"
        self.display_name = "可转债详情-同花顺"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取可转债详情（同花顺）
        
        注意: 该接口无需参数，单次返回所有数据
        
        Returns:
            DataFrame: 所有可转债详情数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_zh_cov_info_ths()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_cov_info_ths'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "债券代码", "type": "string", "description": "可转债代码"},
            {"name": "债券简称", "type": "string", "description": "可转债简称"},
            {"name": "申购日期", "type": "string", "description": "申购日期"},
            {"name": "申购代码", "type": "string", "description": "申购代码"},
            {"name": "原股东配售码", "type": "string", "description": "原股东配售码"},
            {"name": "每股获配额", "type": "float", "description": "每股获配额"},
            {"name": "计划发行量", "type": "float", "description": "计划发行量"},
            {"name": "实际发行量", "type": "float", "description": "实际发行量"},
            {"name": "中签公布日", "type": "string", "description": "中签公布日"},
            {"name": "中签号", "type": "string", "description": "中签号"},
            {"name": "上市日期", "type": "string", "description": "上市日期"},
            {"name": "正股代码", "type": "string", "description": "正股代码"},
            {"name": "正股简称", "type": "string", "description": "正股简称"},
            {"name": "转股价格", "type": "float", "description": "转股价格"},
            {"name": "到期时间", "type": "string", "description": "到期时间"},
            {"name": "中签率", "type": "string", "description": "中签率(%)"},
        ]
