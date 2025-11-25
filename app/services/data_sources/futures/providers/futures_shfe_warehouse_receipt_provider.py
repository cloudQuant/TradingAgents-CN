"""
上海期货交易所仓单日报数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesShfeWarehouseReceiptProvider:
    """上海期货交易所仓单日报数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_shfe_warehouse_receipt"
        self.display_name = "仓单日报-上海期货交易所"
        self.akshare_func = "futures_shfe_warehouse_receipt"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取上海期货交易所仓单日报数据
        
        Args:
            date: 交易日期（必需），格式YYYYMMDD
        """
        try:
            date = kwargs.get("date")
            
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}")
            
            # API返回字典：{品种代码: DataFrame}
            data_dict = ak.futures_shfe_warehouse_receipt(date=date)
            
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
        return ["查询参数_date", "symbol", "REGNAME", "ROWORDER"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版（11个字段）"""
        return [
            {"name": "symbol", "type": "string", "description": "品种名称"},
            {"name": "VARNAME", "type": "string", "description": "品种名称"},
            {"name": "VARSORT", "type": "int", "description": "品种排序"},
            {"name": "REGNAME", "type": "string", "description": "地区名称"},
            {"name": "REGSORT", "type": "int", "description": "地区排序"},
            {"name": "WHABBRNAME", "type": "string", "description": "仓库简称"},
            {"name": "WRTNUM", "type": "int", "description": "仓单数量"},
            {"name": "WRTWGHTS", "type": "int", "description": "仓单重量"},
            {"name": "WRTCHANGE", "type": "int", "description": "仓单变化"},
            {"name": "ROWORDER", "type": "int", "description": "行序号"},
            {"name": "ROWSTATUS", "type": "int", "description": "行状态"},
        ]
