"""
上证质押式回购数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondShBuyBackEmProvider:
    """上证质押式回购数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_sh_buy_back_em"
        self.display_name = "上证质押式回购"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取上证质押式回购"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_sh_buy_back_em()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_sh_buy_back_em'
            df['更新时间'] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "序号", "type": "int", "description": "序号"},
            {"name": "代码", "type": "string", "description": "回购代码"},
            {"name": "名称", "type": "string", "description": "回购名称"},
            {"name": "最新价", "type": "float", "description": "最新价"},
            {"name": "涨跌额", "type": "float", "description": "涨跌额"},
            {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
            {"name": "今开", "type": "float", "description": "今日开盘价"},
            {"name": "最高", "type": "float", "description": "最高价"},
            {"name": "最低", "type": "float", "description": "最低价"},
            {"name": "昨收", "type": "float", "description": "昨日收盘价"},
            {"name": "成交量", "type": "float", "description": "成交量"},
            {"name": "成交额", "type": "float", "description": "成交额"},
        ]
