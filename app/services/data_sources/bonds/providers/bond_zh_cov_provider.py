"""
可转债数据一览表数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhCovProvider:
    """可转债数据一览表数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_cov"
        self.display_name = "可转债数据一览表"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取可转债数据一览表"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_zh_cov()
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_cov'
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
            {"name": "债券简称", "type": "string", "description": "可转债名称"},
            {"name": "申购日期", "type": "string", "description": "申购日期"},
            {"name": "申购代码", "type": "string", "description": "申购代码"},
            {"name": "申购上限", "type": "float", "description": "申购上限(万元)"},
            {"name": "正股代码", "type": "string", "description": "正股代码"},
            {"name": "正股简称", "type": "string", "description": "正股名称"},
            {"name": "正股价", "type": "float", "description": "正股价格"},
            {"name": "转股价", "type": "float", "description": "转股价"},
            {"name": "转股价值", "type": "float", "description": "转股价值"},
            {"name": "债现价", "type": "float", "description": "债券现价"},
            {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
            {"name": "原股东配售-股权登记日", "type": "string", "description": "原股东配售股权登记日"},
            {"name": "原股东配售-每股配售额", "type": "string", "description": "每股配售额"},
            {"name": "发行规模", "type": "float", "description": "发行规模(亿元)"},
            {"name": "中签号发布日", "type": "string", "description": "中签号发布日"},
            {"name": "中签率", "type": "float", "description": "中签率(%)"},
            {"name": "上市时间", "type": "string", "description": "上市时间"},
            {"name": "信用评级", "type": "string", "description": "信用评级"},
        ]
