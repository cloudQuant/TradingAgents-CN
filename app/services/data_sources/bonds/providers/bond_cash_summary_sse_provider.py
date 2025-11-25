"""
债券现券市场概览数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCashSummarySseProvider:
    """债券现券市场概览数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cash_summary_sse"
        self.display_name = "债券现券市场概览"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取债券现券市场概览"""
        try:
            date = kwargs.get("date")
            if not date:
                date = datetime.now().strftime("%Y%m%d")
            else:
                date = str(date).replace("-", "")
            
            logger.info(f"Fetching {self.collection_name} data for {date}")
            
            df = ak.bond_cash_summary_sse(date=date)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {date}")
                return pd.DataFrame()
            
            df['查询日期'] = date
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cash_summary_sse'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for {date}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "债券现货", "type": "string", "description": "债券类型"},
            {"name": "交易笔数-本周", "type": "int", "description": "本周交易笔数"},
            {"name": "交易笔数-本月", "type": "int", "description": "本月交易笔数"},
            {"name": "交易笔数-本年", "type": "int", "description": "本年交易笔数"},
            {"name": "交易数量(万手)-本周", "type": "float", "description": "本周交易数量"},
            {"name": "交易数量(万手)-本月", "type": "float", "description": "本月交易数量"},
            {"name": "交易数量(万手)-本年", "type": "float", "description": "本年交易数量"},
            {"name": "交易金额(亿元)-本周", "type": "float", "description": "本周交易金额"},
            {"name": "交易金额(亿元)-本月", "type": "float", "description": "本月交易金额"},
            {"name": "交易金额(亿元)-本年", "type": "float", "description": "本年交易金额"},
        ]
