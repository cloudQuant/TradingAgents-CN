"""
ETF实时行情-同花顺数据提供者（重构版：继承SimpleProvider）
"""
from datetime import date, datetime
from typing import Any

from app.services.data_sources.base_provider import SimpleProvider


class FundEtfSpotThsProvider(SimpleProvider):
    """ETF实时行情-同花顺数据提供者"""
    
    collection_name = "fund_etf_spot_ths"
    display_name = "ETF基金实时行情-同花顺"
    akshare_func = "fund_etf_spot_ths"
    unique_keys = ["基金代码", "查询日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": ""},
        {"name": "当前-单位净值", "type": "float", "description": ""},
        {"name": "当前-累计净值", "type": "float", "description": ""},
        {"name": "前一日-单位净值", "type": "float", "description": ""},
        {"name": "前一日-累计净值", "type": "float", "description": ""},
        {"name": "增长值", "type": "float", "description": ""},
        {"name": "增长率", "type": "float", "description": "注意单位: %"},
        {"name": "赎回状态", "type": "string", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "最新-交易日", "type": "string", "description": ""},
        {"name": "最新-单位净值", "type": "float", "description": ""},
        {"name": "最新-累计净值", "type": "float", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "查询日期", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_spot_ths"},
    ]

    collection_description = "同花顺-ETF实时行情数据，包括净值、增长率、申赎状态等"
    collection_route = "/funds/collections/fund_etf_spot_ths"
    collection_order = 7

    def fetch_data(self, **kwargs: Any):
        """
        重写 SimpleProvider 的默认流程，补充日期字段格式化。

        ak.fund_etf_spot_ths 返回的“最新-交易日”和“查询日期”使用 datetime.date，
        直接写入 Mongo 会导致 `cannot encode object: datetime.date`。
        """
        df = super().fetch_data(**kwargs)
        if df is None or df.empty:
            return df

        df = df.copy()
        date_columns = ("最新-交易日", "查询日期")
        for column in date_columns:
            if column in df.columns:
                df[column] = df[column].apply(self._format_date_value)

        return df

    @staticmethod
    def _format_date_value(value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except Exception:
                pass

        text = str(value).strip()
        return text or None
