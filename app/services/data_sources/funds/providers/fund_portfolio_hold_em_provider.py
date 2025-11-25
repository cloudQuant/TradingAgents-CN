"""
基金持仓股票-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundPortfolioHoldEmProvider:
    """基金持仓股票-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_portfolio_hold_em"
        self.display_name = "基金持仓股票-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取基金持仓股票数据
        
        Returns:
            DataFrame: 基金持仓股票-东财数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data, kwargs={kwargs}")

            # 前端会传入 fund_code/year，AkShare 接口需要 symbol/date
            symbol = kwargs.get("fund_code") or kwargs.get("symbol") or kwargs.get("code")
            date = kwargs.get("year") or kwargs.get("date")

            if not symbol:
                raise ValueError("缺少必须参数: fund_code/symbol")
            if not date:
                raise ValueError("缺少必须参数: year/date")

            df = ak.fund_portfolio_hold_em(symbol=str(symbol), date=str(date))

            if df is None or df.empty:
                logger.warning(f"No data returned for symbol={symbol}, date={date}")
                return pd.DataFrame()

            # 保留基金代码，方便后续统计
            if '基金代码' not in df.columns:
                df['基金代码'] = symbol

            # 添加元数据
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for symbol={symbol}, date={date}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "基金代码", "type": "string", "description": "基金代码"},
            {"name": "股票代码", "type": "string", "description": "股票代码"},
            {"name": "股票名称", "type": "string", "description": "股票名称"},
            {"name": "占净值比例", "type": "float", "description": "持仓占比"},
            {"name": "持仓数", "type": "int", "description": "持仓数量"},
            {"name": "持仓市值", "type": "float", "description": "持仓市值"},
            {"name": "季度", "type": "string", "description": "季度"},
            {"name": "更新时间", "type": "datetime", "description": "更新时间"},
        ]
