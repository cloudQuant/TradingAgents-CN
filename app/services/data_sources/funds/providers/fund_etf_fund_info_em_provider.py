"""
场内交易基金历史行情-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundEtfFundInfoEmProvider:
    """场内交易基金历史行情-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_etf_fund_info_em"
        self.display_name = "场内交易基金历史行情-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取场内交易基金历史行情数据
        
        Args:
            fund_code/fund: 基金代码（必填）
            start_date: 开始日期（可选，格式 YYYYMMDD）
            end_date: 结束日期（可选，格式 YYYYMMDD）
        
        Returns:
            DataFrame: 场内交易基金历史行情-东财数据
        """
        try:
            # 处理参数名称映射
            fund = kwargs.get("fund_code") or kwargs.get("fund") or kwargs.get("code")
            start_date = kwargs.get("start_date", "")
            end_date = kwargs.get("end_date", "")
            
            if not fund:
                raise ValueError("缺少必须参数: fund_code/fund")
            
            logger.info(f"Fetching {self.collection_name} data for fund={fund}")
            df = ak.fund_etf_fund_info_em(fund=str(fund), start_date=start_date, end_date=end_date)
            
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
            {"name": "单位净值", "type": "float", "description": "单位净值"},
            {"name": "累计净值", "type": "float", "description": "累计净值"},
            {"name": "日增长率", "type": "float", "description": "日增长率"},
            {"name": "申购状态", "type": "string", "description": "申购状态"},
            {"name": "赎回状态", "type": "string", "description": "赎回状态"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
