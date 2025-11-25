"""
可转债等权指数-集思录数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCbIndexJslProvider:
    """可转债等权指数-集思录数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cb_index_jsl"
        self.display_name = "可转债等权指数-集思录"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取可转债等权指数"""
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.bond_cb_index_jsl()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cb_index_jsl'
            df['更新时间'] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "price_dt", "type": "string", "description": "日期"},
            {"name": "price", "type": "float", "description": "指数"},
            {"name": "amount", "type": "float", "description": "剩余规模(亿元)"},
            {"name": "volume", "type": "float", "description": "成交额(亿元)"},
            {"name": "count", "type": "int", "description": "数量"},
            {"name": "increase_val", "type": "float", "description": "涨跌"},
            {"name": "increase_rt", "type": "float", "description": "涨幅"},
            {"name": "avg_price", "type": "float", "description": "平均价格(元)"},
            {"name": "mid_price", "type": "float", "description": "中位数价格(元)"},
            {"name": "mid_convert_value", "type": "float", "description": "中位数转股价值"},
            {"name": "avg_dblow", "type": "float", "description": "平均双底"},
            {"name": "avg_premium_rt", "type": "float", "description": "平均溢价率"},
            {"name": "mid_premium_rt", "type": "float", "description": "中位数溢价率"},
            {"name": "avg_ytm_rt", "type": "float", "description": "平均收益率"},
            {"name": "turnover_rt", "type": "float", "description": "换手率"},
            {"name": "price_90", "type": "int", "description": ">90数量"},
            {"name": "price_90_100", "type": "int", "description": "90~100数量"},
            {"name": "price_100_110", "type": "int", "description": "100~110数量"},
            {"name": "price_110_120", "type": "int", "description": "110~120数量"},
            {"name": "price_120_130", "type": "int", "description": "120~130数量"},
            {"name": "price_130", "type": "int", "description": ">130数量"},
            {"name": "idx_price", "type": "float", "description": "沪深300指数"},
            {"name": "idx_increase_rt", "type": "float", "description": "沪深300指数涨幅"},
        ]
