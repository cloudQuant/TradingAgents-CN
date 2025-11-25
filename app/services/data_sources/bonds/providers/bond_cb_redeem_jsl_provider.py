"""
可转债强赎-集思录数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCbRedeemJslProvider:
    """可转债强赎-集思录数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cb_redeem_jsl"
        self.display_name = "可转债强赎-集思录"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取可转债强赎数据"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_cb_redeem_jsl()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cb_redeem_jsl'
            df['更新时间'] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "代码", "type": "string", "description": "可转债代码"},
            {"name": "名称", "type": "string", "description": "可转债名称"},
            {"name": "现价", "type": "float", "description": "可转债现价"},
            {"name": "正股代码", "type": "string", "description": "正股代码"},
            {"name": "正股名称", "type": "string", "description": "正股名称"},
            {"name": "规模", "type": "float", "description": "规模(亿)"},
            {"name": "剩余规模", "type": "float", "description": "剩余规模"},
            {"name": "转股起始日", "type": "string", "description": "转股起始日"},
            {"name": "最后交易日", "type": "string", "description": "最后交易日"},
            {"name": "到期日", "type": "string", "description": "到期日"},
            {"name": "转股价", "type": "float", "description": "转股价"},
            {"name": "强赎触发比", "type": "int", "description": "强赎触发比(%)"},
            {"name": "强赎触发价", "type": "float", "description": "强赎触发价"},
            {"name": "正股价", "type": "float", "description": "正股价"},
            {"name": "强赎价", "type": "float", "description": "强赎价"},
            {"name": "强赎天计数", "type": "string", "description": "强赎天计数"},
            {"name": "强赎条款", "type": "string", "description": "强赎条款"},
            {"name": "强赎状态", "type": "string", "description": "强赎状态"},
        ]
