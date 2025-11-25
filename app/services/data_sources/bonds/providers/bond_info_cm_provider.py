"""
债券信息查询-中国外汇交易中心数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondInfoCmProvider:
    """债券信息查询-中国外汇交易中心数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_info_cm"
        self.display_name = "债券信息查询"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取债券信息查询数据
        
        Args:
            bond_name: 债券名称
            bond_code: 债券代码
            bond_issue: 发行人
            bond_type: 债券类型
            coupon_type: 付息方式
            issue_year: 发行年份
            underwriter: 承销商
            grade: 评级
            
        Returns:
            DataFrame: 债券信息数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data, kwargs={kwargs}")
            
            # 提取参数
            bond_name = kwargs.get("bond_name", "")
            bond_code = kwargs.get("bond_code", "")
            bond_issue = kwargs.get("bond_issue", "")
            bond_type = kwargs.get("bond_type", "")
            coupon_type = kwargs.get("coupon_type", "")
            issue_year = kwargs.get("issue_year", "")
            underwriter = kwargs.get("underwriter", "")
            grade = kwargs.get("grade", "")
            
            # 调用AKShare接口
            df = ak.bond_info_cm(
                bond_name=bond_name,
                bond_code=bond_code,
                bond_issue=bond_issue,
                bond_type=bond_type,
                coupon_type=coupon_type,
                issue_year=issue_year,
                underwriter=underwriter,
                grade=grade
            )
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 添加元数据
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_info_cm'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "债券代码", "type": "string", "description": "债券代码"},
            {"name": "债券简称", "type": "string", "description": "债券简称"},
            {"name": "债券类型", "type": "string", "description": "债券类型"},
            {"name": "发行人/受托机构", "type": "string", "description": "发行人"},
            {"name": "发行日期", "type": "string", "description": "发行日期"},
            {"name": "最新债项评级", "type": "string", "description": "最新债项评级"},
            {"name": "更新时间", "type": "datetime", "description": "更新时间"},
        ]
