"""
大连商品交易所仓单日报数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesWarehouseReceiptDceProvider:
    """大连商品交易所仓单日报数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_warehouse_receipt_dce"
        self.display_name = "仓单日报-大连商品交易所"
        self.akshare_func = "futures_warehouse_receipt_dce"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取大连商品交易所仓单日报数据
        
        Args:
            date: 交易日期（必需），格式YYYYMMDD
        """
        try:
            date = kwargs.get("date")
            
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            
            df = ak.futures_warehouse_receipt_dce(date=date)
            
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
        return ["查询参数_date", "品种代码", "仓库/分库"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版（7个字段）"""
        return [
            {"name": "品种代码", "type": "string", "description": "品种代码"},
            {"name": "品种名称", "type": "string", "description": "品种名称"},
            {"name": "仓库/分库", "type": "string", "description": "仓库/分库名称"},
            {"name": "可选提货地点/分库-数量", "type": "string", "description": "可选提货地点"},
            {"name": "昨日仓单量（手）", "type": "int", "description": "昨日仓单量(手)"},
            {"name": "今日仓单量（手）", "type": "int", "description": "今日仓单量(手)"},
            {"name": "增减（手）", "type": "int", "description": "仓单增减(手)"},
        ]
