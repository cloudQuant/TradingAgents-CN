"""
基金实时行情-新浪数据提供者（重构版：继承BaseProvider）
"""
from typing import Any, Dict

import pandas as pd

from app.services.data_sources.base_provider import BaseProvider


class FundSpotSinaProvider(BaseProvider):
    """基金实时行情-新浪数据提供者"""
    
    collection_name = "fund_spot_sina"
    display_name = "基金实时行情-新浪"
    akshare_func = "fund_etf_category_sina"
    unique_keys = ["代码"]
    # 前端传 fund_type，akshare 需要 symbol 参数
    param_mapping = {
        "fund_type": "symbol",
        "symbol": "symbol",
    }
    required_params = []
    add_param_columns = {
        "symbol": "基金类型",
    }
    collection_description = "新浪财经-基金实时行情数据，支持封闭式基金、ETF基金、LOF基金三种类型"
    collection_route = "/funds/collections/fund_spot_sina"
    collection_order = 9

    
    SUPPORTED_TYPES = ("封闭式基金", "ETF基金", "LOF基金")

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "名称", "type": "string", "description": ""},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "买入", "type": "float", "description": ""},
        {"name": "卖出", "type": "float", "description": ""},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "今开", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "成交量", "type": "int", "description": "注意单位: 股"},
        {"name": "成交额", "type": "int", "description": "注意单位: 元"},
        {"name": "基金类型", "type": "string", "description": "基金类型: 封闭式基金/ETF基金/LOF基金"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_spot_em"},
    ]

    def fetch_data(self, **kwargs: Any):
        """
        fund_etf_category_sina(symbol=...) 仅接受 '封闭式基金'/'ETF基金'/'LOF基金'。
        对于 '全部' 或未传参时，需要依次抓取三种类型并合并结果。
        """
        fund_type = kwargs.get("fund_type") or kwargs.get("symbol")

        if not fund_type or fund_type == "全部":
            frames = []
            for symbol in self.SUPPORTED_TYPES:
                df = self._fetch_single_type(symbol, kwargs)
                if df is not None and not df.empty:
                    df = df.copy()
                    df["基金类型"] = symbol
                    frames.append(df)

            if not frames:
                return pd.DataFrame()

            return pd.concat(frames, ignore_index=True)

        df = super().fetch_data(**kwargs)
        if df is not None and not df.empty:
            df = df.copy()
            df["基金类型"] = fund_type
        return df

    def _fetch_single_type(self, symbol: str, base_kwargs: Dict[str, Any]):
        params = dict(base_kwargs)
        params["fund_type"] = symbol
        params["symbol"] = symbol
        return super().fetch_data(**params)
