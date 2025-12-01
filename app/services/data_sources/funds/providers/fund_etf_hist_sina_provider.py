"""
ETF基金历史行情-新浪数据提供者
"""
from typing import Any

import pandas as pd

from app.services.data_sources.base_provider import BaseProvider


class FundEtfHistSinaProvider(BaseProvider):
    """基金历史行情-新浪（ETF）"""

    collection_description = "新浪财经-ETF历史行情，按基金代码返回全部历史K线数据"
    collection_route = "/funds/collections/fund_etf_hist_sina"
    collection_order = 14

    collection_name = "fund_etf_hist_sina"
    display_name = "ETF基金历史行情-新浪"
    akshare_func = "fund_etf_hist_sina"
    unique_keys = ["代码", "日期"]

    # 参数映射：支持 fund_code/code/symbol
    param_mapping = {
        "fund_code": "symbol",
        "code": "symbol",
        "symbol": "symbol",
    }
    required_params = ["symbol"]
    add_param_columns = {
        "symbol": "代码",
    }

    field_info = [
        {"name": "代码", "type": "string", "description": "基金代码（如 sh510050）"},
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "开盘价", "type": "float", "description": "开盘价"},
        {"name": "最高价", "type": "float", "description": "最高价"},
        {"name": "最低价", "type": "float", "description": "最低价"},
        {"name": "收盘价", "type": "float", "description": "收盘价"},
        {"name": "成交量", "type": "int", "description": "成交量（手）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_hist_sina"},
    ]

    def fetch_data(self, **kwargs: Any) -> pd.DataFrame:
        """
        调用 akshare 接口并做基础清洗：
          - 确保存在 "代码" 列
          - date 转字符串
          - 价格列转 float
          - volume 转 int
        """
        df = super().fetch_data(**kwargs)

        if df is None or df.empty:
            self.logger.warning("[fund_etf_hist_sina] no data returned")
            return pd.DataFrame()

        df = df.copy()
        df["date"] = df["date"].astype(str)
        if "代码" not in df.columns:
            symbol = kwargs.get("symbol")
            df["代码"] = symbol

        for col in ("open", "high", "low", "close"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if "volume" in df.columns:
            df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int)
        
        df.rename(
            columns={
                "date": "日期",
                "open": "开盘价",
                "high": "最高价",
                "low": "最低价",
                "close": "收盘价",
                "volume": "成交量",
            },
            inplace=True,
        )

        ordered_columns = [field["name"] for field in self.field_info if field["name"] in df.columns]
        df = df[ordered_columns]

        return df

