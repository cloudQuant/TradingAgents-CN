"""
债券基础信息详情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondInfoDetailCmProvider:
    """债券基础信息详情数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_info_detail_cm"
        self.display_name = "债券基础信息"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取债券基础信息详情"""
        try:
            bond_code = kwargs.get("bond_code") or kwargs.get("symbol")
            if not bond_code:
                raise ValueError("缺少必须参数: bond_code")
            
            logger.info(f"Fetching {self.collection_name} data for {bond_code}")
            
            df = ak.bond_info_detail_cm(symbol=str(bond_code))
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {bond_code}")
                return pd.DataFrame()
            
            df['查询代码'] = bond_code
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_info_detail_cm'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched data for {bond_code}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息（完整的债券基础信息字段）"""
        return [
            {"name": "债券简称", "type": "string", "description": "债券简称"},
            {"name": "债券全称", "type": "string", "description": "债券全称"},
            {"name": "债券类型", "type": "string", "description": "债券类型"},
            {"name": "发行人/受托机构", "type": "string", "description": "发行人"},
            {"name": "计息方式", "type": "string", "description": "计息方式"},
            {"name": "计息基准", "type": "string", "description": "计息基准"},
            {"name": "付息频率", "type": "string", "description": "付息频率"},
            {"name": "起息日", "type": "string", "description": "起息日"},
            {"name": "到期日", "type": "string", "description": "到期日"},
            {"name": "票面利率(%)", "type": "float", "description": "票面利率"},
            {"name": "参考收益率(%)", "type": "float", "description": "参考收益率"},
            {"name": "发行价格", "type": "float", "description": "发行价格"},
            {"name": "面值(元)", "type": "float", "description": "面值"},
            {"name": "发行总量(亿元)", "type": "float", "description": "发行总量"},
            {"name": "债项评级", "type": "string", "description": "债项评级"},
            {"name": "主体评级", "type": "string", "description": "主体评级"},
            {"name": "评级机构", "type": "string", "description": "评级机构"},
            {"name": "主承销商", "type": "string", "description": "主承销商"},
            {"name": "托管机构", "type": "string", "description": "托管机构"},
            {"name": "交易市场", "type": "string", "description": "交易市场"},
        ]
