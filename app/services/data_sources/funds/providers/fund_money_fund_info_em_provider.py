"""
货币型基金历史行情-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundMoneyFundInfoEmProvider:
    """货币型基金历史行情-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_money_fund_info_em"
        self.display_name = "货币型基金历史行情-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取货币型基金历史行情数据
        
        Args:
            fund_code/fund: 基金代码（必填）
        
        Returns:
            DataFrame: 货币型基金历史行情-东财数据
        """
        try:
            # 处理参数名称映射
            fund = kwargs.get("fund_code") or kwargs.get("fund") or kwargs.get("code")
            
            if not fund:
                raise ValueError("缺少必须参数: fund_code/fund")
            
            logger.info(f"Fetching {self.collection_name} data for fund={fund}")
            df = ak.fund_money_fund_info_em(fund=str(fund))
            
            if df is None or df.empty:
                logger.warning(f"No data returned for fund={fund}")
                return pd.DataFrame()
            
            # 添加基金代码字段
            if '基金代码' not in df.columns:
                df['基金代码'] = fund
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for fund={fund}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "基金代码", "type": "string", "description": "基金代码"},
            {"name": "净值日期", "type": "string", "description": "净值日期"},
            {"name": "每万份收益", "type": "float", "description": "每万份收益"},
            {"name": "7日年化收益率", "type": "float", "description": "7日年化收益率"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
