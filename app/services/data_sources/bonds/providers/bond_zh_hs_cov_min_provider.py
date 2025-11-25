"""
可转债分时行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhHsCovMinProvider:
    """可转债分时行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_hs_cov_min"
        self.display_name = "可转债分时行情"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取可转债分时行情数据
        
        Args:
            symbol: 可转债代码，如"sz123106"
            period: 周期，可选 '1', '5', '15', '30', '60'，默认'1'
            adjust: 复权类型，可选 '', 'qfq', 'hfq'，默认''不复权
            start_date: 开始日期时间，如"2021-09-01 09:32:00"
            end_date: 结束日期时间，如"2021-11-01 09:32:00"
            
        Returns:
            DataFrame: 可转债分时行情数据
        """
        try:
            symbol = kwargs.get("symbol")
            period = str(kwargs.get("period", "1"))
            adjust = kwargs.get("adjust", "")
            start_date = kwargs.get("start_date", "1979-09-01 09:32:00")
            end_date = kwargs.get("end_date", "2222-01-01 09:32:00")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data for {symbol}, period={period}, adjust={adjust}")
            
            df = ak.bond_zh_hs_cov_min(
                symbol=symbol, 
                period=period, 
                adjust=adjust,
                start_date=start_date,
                end_date=end_date
            )
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['可转债代码'] = symbol
            df['周期'] = period
            df['复权类型'] = adjust if adjust else '不复权'
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_hs_cov_min'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "时间", "type": "datetime", "description": "时间"},
            {"name": "开盘", "type": "float", "description": "开盘价"},
            {"name": "收盘", "type": "float", "description": "收盘价"},
            {"name": "最高", "type": "float", "description": "最高价"},
            {"name": "最低", "type": "float", "description": "最低价"},
            {"name": "成交量", "type": "float", "description": "成交量(手)"},
            {"name": "成交额", "type": "float", "description": "成交额"},
            {"name": "最新价", "type": "float", "description": "最新价"},
            {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)，非1分钟时有"},
            {"name": "涨跌额", "type": "float", "description": "涨跌额，非1分钟时有"},
            {"name": "振幅", "type": "float", "description": "振幅(%)，非1分钟时有"},
            {"name": "换手率", "type": "float", "description": "换手率(%)，非1分钟时有"},
        ]
