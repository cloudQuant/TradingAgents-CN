"""
银行间市场债券发行数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondDebtNafmiiProvider:
    """银行间市场债券发行数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_debt_nafmii"
        self.display_name = "银行间市场债券发行"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取银行间市场债券发行数据"""
        try:
            page = kwargs.get("page", "1")
            logger.info(f"Fetching {self.collection_name} data, page={page}")
            
            df = ak.bond_debt_nafmii(page=str(page))
            
            if df is None or df.empty:
                logger.warning(f"No data returned for page {page}")
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_debt_nafmii'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "注册通知书文号", "type": "string", "description": "注册通知书文号"},
            {"name": "企业名称", "type": "string", "description": "发行企业名称"},
            {"name": "注册金额(亿元)", "type": "float", "description": "注册金额"},
            {"name": "产品类型", "type": "string", "description": "产品类型"},
            {"name": "主承销商/簿记管理人", "type": "string", "description": "主承销商"},
            {"name": "通知书日期", "type": "string", "description": "通知书日期"},
            {"name": "注册有效期截至日", "type": "string", "description": "注册有效期截至日"},
        ]
