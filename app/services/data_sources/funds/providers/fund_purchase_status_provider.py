"""
基金申购状态-东财数据提供者（重构版：继承SimpleProvider）
"""
from datetime import date, datetime
from typing import Any

from app.services.data_sources.base_provider import SimpleProvider


class FundPurchaseStatusProvider(SimpleProvider):
    """基金申购状态-东财数据提供者"""
    
    collection_name = "fund_purchase_status"
    display_name = "基金申购状态"
    akshare_func = "fund_purchase_em"
    unique_keys = ["基金代码", "最新净值/万份收益-报告时间"]

    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "最新净值/万份收益", "type": "float", "description": ""},
        {"name": "最新净值/万份收益-报告时间", "type": "string", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "赎回状态", "type": "string", "description": ""},
        {"name": "下一开放日", "type": "string", "description": ""},
        {"name": "购买起点", "type": "float", "description": ""},
        {"name": "日累计限定金额", "type": "float", "description": ""},
        {"name": "手续费", "type": "float", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_purchase_em"},
    ]

  
    collection_description = "东方财富网-天天基金网-基金数据-基金申购状态，包括申购赎回状态、手续费、购买起点等"
    collection_route = "/funds/collections/fund_purchase_status"
    collection_order = 5
    def fetch_data(self, **kwargs: Any):
        """
        复用 SimpleProvider 的默认实现，并补充日期字段格式化。

        ak.fund_purchase_em 中的“下一开放日”字段会以 datetime.date 返回，
        直接写入 Mongo 会触发 `cannot encode object: datetime.date`。
        这里统一转成 ISO 字符串，便于前端展示/筛选。
        """
        df = super().fetch_data(**kwargs)
        if df is None or df.empty:
            return df

        df = df.copy()
        date_columns = ("下一开放日", "最新净值/万份收益-报告时间")
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

        # pandas Timestamp / numpy datetime64 也有 isoformat 方法
        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except Exception:
                pass

        text = str(value).strip()
        return text or None
