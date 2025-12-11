"""货币报价时间序列数据提供者"""
import pandas as pd

from app.services.data_sources.base_provider import BaseProvider


class CurrencyTimeSeriesProvider(BaseProvider):
    """货币报价时间序列数据提供者
    
    返回指定货币在指定日期范围内的历史汇率时间序列数据。
    """

    collection_name = "currency_time_series"
    display_name = "货币报价时间序列数据"
    akshare_func = "currency_time_series"
    # 唯一键使用中文字段名
    unique_keys = ["报价日期", "基准货币"]

    collection_description = "货币报价时间序列数据，返回指定货币在指定日期范围的报价"
    collection_route = "/currencies/collections/currency_time_series"
    collection_order = 3

    param_mapping = {
        "base": "base",
        "start_date": "start_date",
        "end_date": "end_date",
        "symbols": "symbols",
        "api_key": "api_key",
    }
    required_params = ["base", "start_date", "end_date", "api_key"]
    add_param_columns = {
        "base": "基准货币",
    }

    # field_info 包含基础字段，实际列会动态检测并补充
    field_info = [
        {"name": "报价日期", "type": "string", "description": "该笔汇率对应的日期"},
        {"name": "基准货币", "type": "string", "description": "汇率基准货币"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:  # type: ignore[override]
        """
        获取并转换时间序列汇率数据，输出的列名全部为中文。

        流程：
        1. 映射并校验参数
        2. 调用 akshare.currency_time_series 获取原始数据
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

        # 将英文列名转换为中文列名
        rename_map = {
            "date": "报价日期",
            "base": "基准货币",
        }
        exist_rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
        if exist_rename_map:
            df = df.rename(columns=exist_rename_map)

        # 对于可能存在的其他货币列（如 symbols 中的货币），保持原名或转换
        # 例如 USD, EUR, GBP 等列保持不变
        for col in df.columns:
            if col not in ["报价日期", "基准货币", "更新时间"] and col.isupper():
                # 这些是货币代码列，保持不变
                pass

        df = self._add_param_columns(df, mapped_params)
        df = self._add_metadata(df)

        self.logger.info(
            f"Successfully fetched {len(df)} records for {self.collection_name} "
            "with Chinese field names"
        )
        return df
