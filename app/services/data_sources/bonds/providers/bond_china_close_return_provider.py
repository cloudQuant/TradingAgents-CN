"""
收益率曲线历史数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class BondChinaCloseReturnProvider:
    """收益率曲线历史数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_china_close_return"
        self.display_name = "收益率曲线历史数据"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取收盘收益率曲线历史数据
        
        注意: 该接口只能获取近3个月的数据，且每次获取的数据不超过1个月
        
        Args:
            symbol: 债券类型，如"国债"、"政策性金融债(进出口行)"等
                    可通过 ak.bond_china_close_return_map() 获取完整列表
            period: 期限间隔，可选 '0.1', '0.5', '1'，默认 '1'
            start_date: 开始日期，如"20231101"
            end_date: 结束日期，如"20231130"，与start_date间隔不超过1个月
            
        Returns:
            DataFrame: 收益率曲线历史数据
        """
        try:
            symbol = kwargs.get("symbol", "国债")
            period = kwargs.get("period", "1")
            end_date = kwargs.get("end_date")
            start_date = kwargs.get("start_date")
            
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                # 默认获取最近一个月的数据
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
            
            logger.info(f"Fetching {self.collection_name} data: symbol={symbol}, period={period}, {start_date} to {end_date}")
            
            df = ak.bond_china_close_return(
                symbol=symbol, 
                period=period, 
                start_date=start_date, 
                end_date=end_date
            )
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['债券类型'] = symbol
            df['期限间隔'] = period
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_china_close_return'
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
            {"name": "期限", "type": "float", "description": "期限（年）"},
            {"name": "到期收益率", "type": "float", "description": "到期收益率(%)"},
            {"name": "即期收益率", "type": "float", "description": "即期收益率(%)"},
            {"name": "远期收益率", "type": "float", "description": "远期收益率(%)"},
        ]
