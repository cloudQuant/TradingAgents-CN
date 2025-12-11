"""货币报价历史数据提供者"""
import pandas as pd

from app.services.data_sources.base_provider import BaseProvider


class CurrencyHistoryProvider(BaseProvider):
    """货币报价历史数据提供者"""

    collection_name = "currency_history"
    display_name = "货币报价历史数据"
    akshare_func = "currency_history"
    # 唯一键与字段全部使用中文，保持与集合展示一致
    unique_keys = ["货币代码", "基准货币", "报价日期"]

    collection_description = "货币报价历史数据，返回指定货币在指定交易日的报价"
    collection_route = "/currencies/collections/currency_history"
    collection_order = 2

    param_mapping = {
        "base": "base",
        "date": "date",
        "symbols": "symbols",
        "api_key": "api_key",
    }
    required_params = ["base", "date", "api_key"]
    add_param_columns = {
        "base": "基准货币",
        "date": "查询日期",
    }

    field_info = [
        {"name": "货币代码", "type": "string", "description": "货币代码"},
        {"name": "报价日期", "type": "string", "description": "该笔汇率对应的日期"},
        {"name": "基准货币", "type": "string", "description": "汇率基准货币"},
        {"name": "汇率", "type": "float", "description": "货币对基准货币的汇率"},
        {"name": "查询日期", "type": "string", "description": "请求参数中的查询日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:  # type: ignore[override]
        """
        获取并转换历史汇率数据，输出的列名全部为中文。

        流程：
        1. 映射并校验参数
        2. 调用 akshare.currency_history 获取原始数据
        3. 将英文列统一重命名为中文
        4. 写入查询参数对应的中文列，并补充更新时间
        """

        mapped_params = self._map_params(kwargs)
        self._validate_params(mapped_params)
        self.logger.info(
            f"Fetching {self.collection_name} data with params={mapped_params}"
        )

        df = self._call_akshare(self.akshare_func, **mapped_params)
        if df is None or df.empty:
            self.logger.warning(f"No data returned for {self.collection_name}")
            return pd.DataFrame()

        rename_map = {
            "currency": "货币代码",
            "date": "报价日期",
            "base": "基准货币",
            "rates": "汇率",
        }
        exist_rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
        if exist_rename_map:
            df = df.rename(columns=exist_rename_map)

        df = self._add_param_columns(df, mapped_params)
        df = self._add_metadata(df)

        self.logger.info(
            f"Successfully fetched {len(df)} records for {self.collection_name} "
            "with Chinese field names"
        )
        return df
