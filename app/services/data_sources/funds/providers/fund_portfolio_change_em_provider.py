"""
基金持仓变动-东财数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FundPortfolioChangeEmProvider:
    """基金持仓变动-东财数据提供者"""
    
    def __init__(self):
        self.collection_name = "fund_portfolio_change_em"
        self.display_name = "基金持仓变动-东财"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取基金持仓变动数据
        
        Returns:
            DataFrame: 基金持仓变动-东财数据
        """
        try:
            logger.info(f"Fetching {self.collection_name} data, kwargs={kwargs}")

            # 前端会传入 fund_code/date，AkShare 接口需要 symbol/indicator/date
            symbol = kwargs.get("fund_code") or kwargs.get("symbol") or kwargs.get("code")
            date = kwargs.get("year") or kwargs.get("date")
            # indicator 前端暂未传入，默认使用累计买入，与文档示例保持一致
            indicator = kwargs.get("indicator") or "累计买入"

            if not symbol:
                raise ValueError("缺少必须参数: fund_code/symbol")
            if not date:
                raise ValueError("缺少必须参数: year/date")

            df = ak.fund_portfolio_change_em(symbol=str(symbol), indicator=str(indicator), date=str(date))

            if df is None or df.empty:
                logger.warning(f"No data returned for symbol={symbol}, indicator={indicator}, date={date}")
                return pd.DataFrame()

            # 保留基金代码，方便后续统计
            if '基金代码' not in df.columns:
                df['基金代码'] = symbol

            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records for symbol={symbol}, indicator={indicator}, date={date}")
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
            {"name": "持仓变动", "type": "string", "description": "持仓变动类型"},
            {"name": "变动数量", "type": "float", "description": "变动数量"},
            {"name": "变动市值", "type": "float", "description": "变动市值"},
            {"name": "季度", "type": "string", "description": "季度"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
