"""
期货规则-交易日历表数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FuturesRuleProvider:
    """期货规则-交易日历表数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_rule"
        self.display_name = "期货规则-交易日历表"
        self.akshare_func = "futures_rule"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取期货规则-交易日历表数据
        
        Args:
            date: 交易日期，格式YYYYMMDD，需要是近期交易日
        """
        try:
            date = kwargs.get("date")
            
            # 如果未提供日期，使用今天或最近的工作日
            if not date:
                today = datetime.now()
                if today.weekday() == 5:  # 周六
                    today = today - timedelta(days=1)
                elif today.weekday() == 6:  # 周日
                    today = today - timedelta(days=2)
                date = today.strftime("%Y%m%d")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            
            df = ak.futures_rule(date=date)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for date={date}")
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_date'] = date
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键字段"""
        return ["交易所", "代码", "查询参数_date"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版（10个字段）"""
        return [
            {"name": "交易所", "type": "string", "description": "交易所名称"},
            {"name": "品种", "type": "string", "description": "品种名称"},
            {"name": "代码", "type": "string", "description": "合约代码"},
            {"name": "交易保证金比例", "type": "float", "description": "交易保证金比例(%)"},
            {"name": "涨跌停板幅度", "type": "float", "description": "涨跌停板幅度(%)"},
            {"name": "合约乘数", "type": "int", "description": "合约乘数"},
            {"name": "最小变动价位", "type": "float", "description": "最小变动价位"},
            {"name": "限价单每笔最大下单手数", "type": "int", "description": "限价单每笔最大下单手数"},
            {"name": "特殊合约参数调整", "type": "string", "description": "特殊合约参数调整说明"},
            {"name": "调整备注", "type": "string", "description": "调整备注"},
        ]
