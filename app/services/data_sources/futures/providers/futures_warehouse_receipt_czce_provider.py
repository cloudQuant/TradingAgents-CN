"""
郑州商品交易所仓单日报数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesWarehouseReceiptCzceProvider:
    """郑州商品交易所仓单日报数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_warehouse_receipt_czce"
        self.display_name = "仓单日报-郑州商品交易所"
        self.akshare_func = "futures_warehouse_receipt_czce"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取郑州商品交易所仓单日报数据
        
        Args:
            date: 交易日期（必需），格式YYYYMMDD
        """
        try:
            date = kwargs.get("date")
            
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            
            # API返回字典：{品种代码: DataFrame}
            data_dict = ak.futures_warehouse_receipt_czce(date=date)
            
            if not data_dict:
                logger.warning(f"No data returned for date={date}")
                return pd.DataFrame()
            
            all_dfs = []
            for symbol, df in data_dict.items():
                if df is not None and not df.empty:
                    df['symbol'] = symbol
                    all_dfs.append(df)
            
            if not all_dfs:
                return pd.DataFrame()
            
            result_df = pd.concat(all_dfs, ignore_index=True)
            result_df['更新时间'] = datetime.now()
            result_df['数据源'] = 'akshare'
            result_df['接口名称'] = self.akshare_func
            result_df['查询参数_date'] = date
            
            logger.info(f"Successfully fetched {len(result_df)} records")
            return result_df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键字段"""
        return ["查询参数_date", "symbol", "仓库编号"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版"""
        return [
            {"name": "symbol", "type": "string", "description": "品种代码"},
            {"name": "仓库编号", "type": "string", "description": "仓库编号"},
            {"name": "仓库简称", "type": "string", "description": "仓库简称"},
            {"name": "年度", "type": "string", "description": "年度"},
            {"name": "等级", "type": "string", "description": "等级"},
            {"name": "品牌", "type": "string", "description": "品牌"},
            {"name": "仓单数量", "type": "int", "description": "仓单数量"},
            {"name": "当日增减", "type": "int", "description": "当日增减"},
            {"name": "有效预报", "type": "string", "description": "有效预报"},
            {"name": "升贴水", "type": "int", "description": "升贴水"},
        ]
