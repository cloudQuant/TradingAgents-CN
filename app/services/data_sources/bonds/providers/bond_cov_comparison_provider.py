"""
可转债比价表数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCovComparisonProvider:
    """可转债比价表数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cov_comparison"
        self.display_name = "可转债比价表"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取可转债比价表"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_cov_comparison()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cov_comparison'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "序号", "type": "int", "description": "序号"},
            {"name": "转债代码", "type": "string", "description": "可转债代码"},
            {"name": "转债名称", "type": "string", "description": "可转债名称"},
            {"name": "转债最新价", "type": "float", "description": "转债最新价"},
            {"name": "转债涨跌幅", "type": "float", "description": "转债涨跌幅(%)"},
            {"name": "正股代码", "type": "string", "description": "正股代码"},
            {"name": "正股名称", "type": "string", "description": "正股名称"},
            {"name": "正股最新价", "type": "float", "description": "正股最新价"},
            {"name": "正股涨跌幅", "type": "float", "description": "正股涨跌幅(%)"},
            {"name": "转股价", "type": "float", "description": "转股价"},
            {"name": "转股价值", "type": "float", "description": "转股价值"},
            {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
            {"name": "纯债溢价率", "type": "float", "description": "纯债溢价率(%)"},
            {"name": "回售触发价", "type": "float", "description": "回售触发价"},
            {"name": "强赎触发价", "type": "float", "description": "强赎触发价"},
            {"name": "到期赎回价", "type": "float", "description": "到期赎回价"},
            {"name": "纯债价值", "type": "float", "description": "纯债价值"},
            {"name": "开始转股日", "type": "string", "description": "开始转股日"},
            {"name": "上市日期", "type": "string", "description": "上市日期"},
            {"name": "申购日期", "type": "string", "description": "申购日期"},
        ]
