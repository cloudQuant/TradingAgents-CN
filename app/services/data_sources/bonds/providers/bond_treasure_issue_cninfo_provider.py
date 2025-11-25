"""
国债发行数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondTreasureIssueCninfoProvider:
    """国债发行数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_treasure_issue_cninfo"
        self.display_name = "国债发行"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取国债发行数据"""
        try:
            start_date = kwargs.get("start_date", "")
            end_date = kwargs.get("end_date", "")
            
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_treasure_issue_cninfo(start_date=start_date, end_date=end_date)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_treasure_issue_cninfo'
            df['更新时间'] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "债券代码", "type": "string", "description": "债券代码"},
            {"name": "债券简称", "type": "string", "description": "债券简称"},
            {"name": "发行起始日", "type": "string", "description": "发行起始日"},
            {"name": "发行终止日", "type": "string", "description": "发行终止日"},
            {"name": "计划发行总量", "type": "float", "description": "计划发行总量(亿元)"},
            {"name": "实际发行总量", "type": "float", "description": "实际发行总量(亿元)"},
            {"name": "发行价格", "type": "float", "description": "发行价格(元)"},
            {"name": "单位面值", "type": "int", "description": "单位面值(元)"},
            {"name": "缴款日", "type": "string", "description": "缴款日"},
            {"name": "增发次数", "type": "int", "description": "增发次数"},
            {"name": "交易市场", "type": "string", "description": "交易市场"},
            {"name": "发行方式", "type": "string", "description": "发行方式"},
            {"name": "发行对象", "type": "string", "description": "发行对象"},
            {"name": "公告日期", "type": "string", "description": "公告日期"},
            {"name": "债券名称", "type": "string", "description": "债券名称"},
        ]
