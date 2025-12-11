"""货币基础信息查询提供者"""
import pandas as pd

from app.services.data_sources.base_provider import BaseProvider


class CurrencyCurrenciesProvider(BaseProvider):
    """货币基础信息查询提供者"""
    
    collection_name = "currency_currencies"
    display_name = "货币基础信息查询"
    akshare_func = "currency_currencies"
    unique_keys = ["货币代码"]
    
    collection_description = "所有货币的基础信息，包含名称、代码、符号等"
    collection_route = "/currencies/collections/currency_currencies"
    collection_order = 4
    
    param_mapping = {"c_type": "c_type", "api_key": "api_key"}
    required_params = ["c_type", "api_key"]
    add_param_columns = {"c_type": "货币类型"}
    
    field_info = [
        {"name": "货币ID", "type": "int", "description": "货币ID"},
        {"name": "货币名称", "type": "string", "description": "货币名称"},
        {"name": "简码", "type": "string", "description": "货币简码"},
        {"name": "货币代码", "type": "string", "description": "货币代码"},
        {"name": "精度", "type": "int", "description": "小数精度"},
        {"name": "子单位", "type": "int", "description": "子单位"},
        {"name": "符号", "type": "string", "description": "货币符号"},
        {"name": "符号位置", "type": "bool", "description": "符号在前为True"},
        {"name": "小数点", "type": "string", "description": "小数点标记"},
        {"name": "千分位", "type": "string", "description": "千分位分隔符"},
        {"name": "货币类型", "type": "string", "description": "货币类型(fiat/crypto)"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:  # type: ignore[override]
        """
        获取并转换货币基础信息数据，输出的列名全部为中文。

        流程：
        1. 映射并校验参数
        2. 调用 akshare.currency_currencies 获取原始数据
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
            "id": "货币ID",
            "name": "货币名称",
            "short_code": "简码",
            "code": "货币代码",
            "precision": "精度",
            "subunit": "子单位",
            "symbol": "符号",
            "symbol_first": "符号位置",
            "decimal_mark": "小数点",
            "thousands_separator": "千分位",
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
