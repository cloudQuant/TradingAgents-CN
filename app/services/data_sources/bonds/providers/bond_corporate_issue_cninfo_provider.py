"""
企业债发行数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCorporateIssueCninfoProvider:
    """企业债发行数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_corporate_issue_cninfo"
        self.display_name = "企业债发行"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取企业债发行数据"""
        try:
            start_date = kwargs.get("start_date", "")
            end_date = kwargs.get("end_date", "")
            
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_corporate_issue_cninfo(start_date=start_date, end_date=end_date)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_corporate_issue_cninfo'
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
            {"name": "公告日期", "type": "string", "description": "公告日期"},
            {"name": "交易所网上发行起始日", "type": "string", "description": "网上发行起始日"},
            {"name": "交易所网上发行终止日", "type": "string", "description": "网上发行终止日"},
            {"name": "计划发行总量", "type": "float", "description": "计划发行总量(万元)"},
            {"name": "实际发行总量", "type": "float", "description": "实际发行总量(万元)"},
            {"name": "发行面值", "type": "float", "description": "发行面值"},
            {"name": "发行价格", "type": "int", "description": "发行价格(元)"},
            {"name": "发行方式", "type": "string", "description": "发行方式"},
            {"name": "发行对象", "type": "string", "description": "发行对象"},
            {"name": "发行范围", "type": "string", "description": "发行范围"},
            {"name": "承销方式", "type": "string", "description": "承销方式"},
            {"name": "最小认购单位", "type": "float", "description": "最小认购单位(万元)"},
            {"name": "募资用途说明", "type": "string", "description": "募资用途说明"},
            {"name": "最低认购额", "type": "float", "description": "最低认购额(万元)"},
            {"name": "债券名称", "type": "string", "description": "债券名称"},
        ]
