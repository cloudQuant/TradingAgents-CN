"""
沪深债券实时行情数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhHsSpotProvider:
    """沪深债券实时行情数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_hs_spot"
        self.display_name = "沪深债券实时行情"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取沪深债券实时行情数据
        
        Args:
            start_page: 开始获取的页面，默认"1"，每页80条数据
            end_page: 结束获取的页面，默认"10"
            
        Returns:
            DataFrame: 沪深债券实时行情数据
        """
        try:
            start_page = kwargs.get("start_page", "1")
            end_page = kwargs.get("end_page", "10")
            
            logger.info(f"Fetching {self.collection_name} data, pages {start_page}-{end_page}")
            
            df = ak.bond_zh_hs_spot(start_page=start_page, end_page=end_page)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_hs_spot'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "代码", "type": "string", "description": "债券代码，如sh010107"},
            {"name": "名称", "type": "string", "description": "债券名称"},
            {"name": "最新价", "type": "float", "description": "最新成交价"},
            {"name": "涨跌额", "type": "float", "description": "涨跌额"},
            {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
            {"name": "买入", "type": "float", "description": "买一价"},
            {"name": "卖出", "type": "float", "description": "卖一价"},
            {"name": "昨收", "type": "float", "description": "昨日收盘价"},
            {"name": "今开", "type": "float", "description": "今日开盘价"},
            {"name": "最高", "type": "float", "description": "今日最高价"},
            {"name": "最低", "type": "float", "description": "今日最低价"},
            {"name": "成交量", "type": "int", "description": "成交量(手)"},
            {"name": "成交额", "type": "int", "description": "成交额(万)"},
        ]
