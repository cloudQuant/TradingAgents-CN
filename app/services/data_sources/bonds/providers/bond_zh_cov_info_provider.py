"""
可转债详情-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondZhCovInfoProvider:
    """可转债详情-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_zh_cov_info"
        self.display_name = "可转债详情-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取可转债详情数据
        
        Args:
            symbol: 可转债代码，如"123121"
            indicator: 指标类型，可选 "基本信息", "中签号", "筹资用途", "重要日期"
                       默认"基本信息"，其中"可转债重要条款"在"基本信息"中
            
        Returns:
            DataFrame: 可转债详情数据
        """
        try:
            symbol = kwargs.get("symbol")
            indicator = kwargs.get("indicator", "基本信息")
            
            if not symbol:
                raise ValueError("缺少必须参数: symbol")
            
            logger.info(f"Fetching {self.collection_name} data for {symbol}, indicator={indicator}")
            
            df = ak.bond_zh_cov_info(symbol=symbol, indicator=indicator)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['可转债代码'] = symbol
            df['查询指标'] = indicator
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_zh_cov_info'
            df['更新时间'] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息（基本信息包含67个字段）"""
        return [
            {"name": "SECURITY_CODE", "type": "string", "description": "可转债代码"},
            {"name": "SECUCODE", "type": "string", "description": "证券代码"},
            {"name": "TRADE_MARKET", "type": "string", "description": "交易市场"},
            {"name": "SECURITY_NAME_ABBR", "type": "string", "description": "可转债简称"},
            {"name": "BOND_EXPIRE", "type": "string", "description": "债券期限"},
            {"name": "INTEREST_RATE_EXPLAIN", "type": "string", "description": "利率说明"},
            {"name": "CONVERT_STOCK_CODE", "type": "string", "description": "正股代码"},
            {"name": "CONVERT_STOCK_NAME", "type": "string", "description": "正股名称"},
            {"name": "CONVERT_STOCK_PRICE", "type": "float", "description": "正股价格"},
            {"name": "TRANSFER_PRICE", "type": "float", "description": "转股价"},
            {"name": "TRANSFER_VALUE", "type": "float", "description": "转股价值"},
            {"name": "IS_CONVERT_STOCK", "type": "string", "description": "是否可转股"},
            {"name": "IS_REDEEM", "type": "string", "description": "是否赎回"},
            {"name": "IS_SELLBACK", "type": "string", "description": "是否回售"},
        ]
