"""
中美国债收益率数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhUsRateProvider:
    """中美国债收益率数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_us_rate"
        self.display_name = "中美国债收益率"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取中美国债收益率历史数据
        
        Args:
            start_date: 开始日期，如"19901219"，数据从19901219开始
            
        Returns:
            DataFrame: 中美国债收益率历史数据
        """
        try:
            start_date = kwargs.get("start_date", "19901219")
            
            logger.info(f"Fetching {self.collection_name} data from {start_date}")
            
            df = ak.bond_zh_us_rate(start_date=start_date)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_us_rate'
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
            {"name": "中国国债收益率2年", "type": "float", "description": "中国国债2年期收益率"},
            {"name": "中国国债收益率5年", "type": "float", "description": "中国国债5年期收益率"},
            {"name": "中国国债收益率10年", "type": "float", "description": "中国国债10年期收益率"},
            {"name": "中国国债收益率30年", "type": "float", "description": "中国国债30年期收益率"},
            {"name": "中国国债收益率10年-2年", "type": "float", "description": "中国国债10年-2年利差"},
            {"name": "中国GDP年增率", "type": "float", "description": "中国GDP年增率"},
            {"name": "美国国债收益率2年", "type": "float", "description": "美国国债2年期收益率"},
            {"name": "美国国债收益率5年", "type": "float", "description": "美国国债5年期收益率"},
            {"name": "美国国债收益率10年", "type": "float", "description": "美国国债10年期收益率"},
            {"name": "美国国债收益率30年", "type": "float", "description": "美国国债30年期收益率"},
            {"name": "美国国债收益率10年-2年", "type": "float", "description": "美国国债10年-2年利差"},
            {"name": "美国GDP年增率", "type": "float", "description": "美国GDP年增率"},
        ]
