"""货币报价最新数据提供者"""
import pandas as pd

from app.services.data_sources.base_provider import BaseProvider


class CurrencyLatestProvider(BaseProvider):
    """货币报价最新数据提供者

    为了与其他数据集合保持一致，这里将底层 akshare 返回的英文字段
    （currency、date、base、rates）统一转换为中文字段名：
    - 货币代码
    - 报价时间
    - 基准货币
    - 汇率
    """

    collection_name = "currency_latest"
    display_name = "货币报价最新数据"
    akshare_func = "currency_latest"

    # 唯一键使用中文字段名
    unique_keys = ["货币代码", "基准货币", "报价时间"]

    collection_description = "货币报价最新数据，返回指定货币的最新报价"
    collection_route = "/currencies/collections/currency_latest"
    collection_order = 1

    # 参数映射仍然使用英文参数传递给 akshare
    param_mapping = {"base": "base", "symbols": "symbols", "api_key": "api_key"}
    required_params = ["base", "api_key"]
    # 不再额外添加英文字段列，全部使用中文列
    add_param_columns = {}

    # 字段信息：name 使用中文字段名，description 也为中文说明
    field_info = [
        {"name": "货币代码", "type": "string", "description": "货币代码"},
        {"name": "报价时间", "type": "datetime", "description": "报价时间"},
        {"name": "基准货币", "type": "string", "description": "基准货币"},
        {"name": "汇率", "type": "float", "description": "汇率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:  # type: ignore[override]
        """获取并转换数据，使返回的字段全部为中文

        流程：
        1. 使用基类的参数映射和校验逻辑
        2. 调用 akshare.currency_latest 获取原始数据（英文列名）
        3. 将英文列重命名为中文列名
        4. 添加中文时间戳字段（"更新时间"）
        """

        # 1. 参数映射与校验（保留 BaseProvider 的逻辑）
        mapped_params = self._map_params(kwargs)
        self._validate_params(mapped_params)
        self.logger.info(
            f"Fetching {self.collection_name} data with params={mapped_params}"
        )

        # 2. 调用 akshare 获取原始数据
        df = self._call_akshare(self.akshare_func, **mapped_params)
        if df is None or df.empty:
            self.logger.warning(f"No data returned for {self.collection_name}")
            return pd.DataFrame()

        # 3. 将英文列名转换为中文列名
        rename_map = {
            "currency": "货币代码",
            "date": "报价时间",
            "base": "基准货币",
            "rates": "汇率",
        }
        exist_rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
        if exist_rename_map:
            df = df.rename(columns=exist_rename_map)

        # 4. 添加中文时间戳字段（使用基类的元数据逻辑）
        df = self._add_metadata(df)

        self.logger.info(
            f"Successfully fetched {len(df)} records for {self.collection_name} "
            "with Chinese field names"
        )
        return df
