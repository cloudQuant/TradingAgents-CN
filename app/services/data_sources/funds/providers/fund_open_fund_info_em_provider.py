"""
开放式基金历史行情-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundOpenFundInfoEmProvider:
    """开放式基金历史行情-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_open_fund_info_em"
        self.display_name = "开放式基金历史行情-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取开放式基金历史行情数据
        
        Args:
            fund_code/fund: 基金代码（必填）
            indicator: 指标类型（可选，默认 "单位净值走势"）
                可选: "单位净值走势", "累计净值走势", "累计收益率走势", "同类排名走势", "同类排名百分比", "分红送配详情", "拆分详情"
        
        Returns:
            DataFrame: 开放式基金历史行情-东财数据
        """
        try:
            # 处理参数名称映射
            fund = kwargs.get("fund_code") or kwargs.get("fund") or kwargs.get("code")
            indicator = kwargs.get("indicator", "单位净值走势")
            
            if not fund:
                raise ValueError("缺少必须参数: fund_code/fund")
            
            logger.info(f"Fetching {self.collection_name} data for fund={fund}, indicator={indicator}")
            df = ak.fund_open_fund_info_em(fund=str(fund), indicator=indicator)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for fund={fund}")
                return pd.DataFrame()
            
            # 添加基金代码字段
            if '基金代码' not in df.columns:
                df['基金代码'] = fund
            
            # 添加指标类型字段
            df['指标类型'] = indicator
            
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
            {"name": "指标类型", "type": "string", "description": "指标类型"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
