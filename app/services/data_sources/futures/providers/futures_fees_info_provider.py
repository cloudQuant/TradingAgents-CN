"""
期货交易费用参照表数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesFeesInfoProvider:
    """期货交易费用参照表数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_fees_info"
        self.display_name = "期货交易费用参照表"
        self.akshare_func = "futures_fees_info"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取期货交易费用参照表数据
        无需参数
        """
        try:
            logger.info(f"Fetching {self.collection_name} data")
            
            df = ak.futures_fees_info()
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df['更新时间'] = datetime.now()
            df['数据源'] = 'akshare'
            df['接口名称'] = self.akshare_func
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键字段"""
        return ["交易所", "合约代码"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版（36个字段）"""
        return [
            {"name": "交易所", "type": "string", "description": "交易所名称"},
            {"name": "合约代码", "type": "string", "description": "合约代码"},
            {"name": "合约名称", "type": "string", "description": "合约名称"},
            {"name": "品种代码", "type": "string", "description": "品种代码"},
            {"name": "品种名称", "type": "string", "description": "品种名称"},
            {"name": "合约乘数", "type": "int", "description": "合约乘数"},
            {"name": "最小跳动", "type": "float", "description": "最小变动价位"},
            {"name": "开仓费率（按金额）", "type": "float", "description": "开仓费率"},
            {"name": "开仓费用（按手）", "type": "float", "description": "开仓费用"},
            {"name": "平仓费率（按金额）", "type": "float", "description": "平仓费率"},
            {"name": "平仓费用（按手）", "type": "float", "description": "平仓费用"},
            {"name": "平今费率（按金额）", "type": "float", "description": "平今费率"},
            {"name": "平今费用（按手）", "type": "float", "description": "平今费用"},
            {"name": "做多保证金率（按金额）", "type": "float", "description": "做多保证金率"},
            {"name": "做多保证金（按手）", "type": "int", "description": "做多保证金"},
            {"name": "做空保证金率（按金额）", "type": "float", "description": "做空保证金率"},
            {"name": "做空保证金（按手）", "type": "int", "description": "做空保证金"},
            {"name": "上日结算价", "type": "float", "description": "上日结算价"},
            {"name": "上日收盘价", "type": "float", "description": "上日收盘价"},
            {"name": "最新价", "type": "float", "description": "最新价格"},
            {"name": "成交量", "type": "int", "description": "成交量"},
            {"name": "持仓量", "type": "int", "description": "持仓量"},
            {"name": "1手开仓费用", "type": "float", "description": "1手开仓费用"},
            {"name": "1手平仓费用", "type": "float", "description": "1手平仓费用"},
            {"name": "1手平今费用", "type": "float", "description": "1手平今费用"},
            {"name": "做多1手保证金", "type": "float", "description": "做多1手保证金"},
            {"name": "做空1手保证金", "type": "float", "description": "做空1手保证金"},
        ]
