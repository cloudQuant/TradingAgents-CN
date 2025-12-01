"""
开放式基金实时行情-东财数据提供者（重构版：继承SimpleProvider）

AKShare的fund_open_fund_daily_em接口返回的列名包含具体日期，本provider将其重命名为通用名称：
- 单位净值、累计净值（今日）
- 前一日单位净值、前一日累计净值（昨日）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundOpenFundDailyEmProvider(SimpleProvider):
    
    """开放式基金实时行情-东财数据提供者"""

    collection_description = "东方财富网-天天基金网-基金数据，每个交易日 16:00-23:00 更新当日最新开放式基金净值数据"
    collection_route = "/funds/collections/fund_open_fund_daily_em"
    collection_order = 15

    collection_name = "fund_open_fund_daily_em"
    display_name = "开放式基金实时行情-东方财富"
    akshare_func = "fund_open_fund_daily_em"
    unique_keys = ["基金代码", "更新时间"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": "今日单位净值"},
        {"name": "累计净值", "type": "float", "description": "今日累计净值"},
        {"name": "前一日单位净值", "type": "float", "description": "前一日单位净值"},
        {"name": "前一日累计净值", "type": "float", "description": "前一日累计净值"},
        {"name": "日增长值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "赎回状态", "type": "string", "description": ""},
        {"name": "手续费", "type": "string", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_open_fund_daily_em"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取开放式基金实时行情数据，将日期列重命名为通用名称。"""
        try:
            self.logger.info(f"Fetching {self.collection_name} data")
            
            # 调用akshare获取数据
            df = self._call_akshare(self.akshare_func, **kwargs)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df = df.copy()
            
            # 重命名日期相关列
            df = self._rename_date_columns(df)
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise

    def _rename_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """将日期格式的列名重命名为通用名称。"""
        columns = ["基金代码", "基金简称", "单位净值", "累计净值", "前一日单位净值","前一日累计净值",
                   "日增长值", "日增长率", "申购状态", "赎回状态", "手续费"]

        df.columns = columns
        return df
