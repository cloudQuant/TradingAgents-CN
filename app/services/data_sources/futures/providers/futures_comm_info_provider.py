"""
期货手续费与保证金数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesCommInfoProvider:
    """期货手续费与保证金数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_comm_info"
        self.display_name = "期货手续费与保证金"
        self.akshare_func = "futures_comm_info"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取期货手续费与保证金数据
        
        Args:
            symbol: 交易所选择，默认"所有"
        """
        try:
            symbol = kwargs.get("symbol", "所有")
            logger.info(f"Fetching {self.collection_name} data, symbol={symbol}")
            
            df = ak.futures_comm_info(symbol=symbol)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for symbol={symbol}")
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            df['查询参数_symbol'] = symbol
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键字段"""
        return ["交易所名称", "合约代码"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版（21个字段）"""
        return [
            {"name": "交易所名称", "type": "string", "description": "交易所名称"},
            {"name": "合约名称", "type": "string", "description": "合约名称"},
            {"name": "合约代码", "type": "string", "description": "合约代码"},
            {"name": "现价", "type": "float", "description": "当前价格"},
            {"name": "涨停板", "type": "float", "description": "涨停板价格"},
            {"name": "跌停板", "type": "float", "description": "跌停板价格"},
            {"name": "保证金-买开", "type": "float", "description": "买开保证金(%)"},
            {"name": "保证金-卖开", "type": "float", "description": "卖开保证金(%)"},
            {"name": "保证金-每手", "type": "float", "description": "每手保证金(元)"},
            {"name": "手续费标准-开仓-万分之", "type": "float", "description": "开仓手续费率"},
            {"name": "手续费标准-开仓-元", "type": "string", "description": "开仓手续费"},
            {"name": "手续费标准-平昨-万分之", "type": "float", "description": "平昨手续费率"},
            {"name": "手续费标准-平昨-元", "type": "string", "description": "平昨手续费"},
            {"name": "手续费标准-平今-万分之", "type": "float", "description": "平今手续费率"},
            {"name": "手续费标准-平今-元", "type": "string", "description": "平今手续费"},
            {"name": "每跳毛利", "type": "int", "description": "每跳毛利(元)"},
            {"name": "手续费", "type": "float", "description": "手续费(开+平)"},
            {"name": "每跳净利", "type": "float", "description": "每跳净利(元)"},
            {"name": "备注", "type": "string", "description": "是否主力合约"},
            {"name": "手续费更新时间", "type": "string", "description": "手续费更新时间"},
            {"name": "价格更新时间", "type": "string", "description": "价格更新时间"},
        ]
