"""货币对价格转换提供者"""
import pandas as pd
from datetime import datetime

from app.services.data_sources.base_provider import BaseProvider


class CurrencyConvertProvider(BaseProvider):
    """货币对价格转换提供者"""
    
    collection_name = "currency_convert"
    display_name = "货币对价格转换"
    akshare_func = "currency_convert"
    unique_keys = ["转换时间"]
    
    collection_description = "指定货币对指定货币数量的转换后价格"
    collection_route = "/currencies/collections/currency_convert"
    collection_order = 5
    
    param_mapping = {"base": "base", "to": "to", "amount": "amount", "api_key": "api_key"}
    required_params = ["base", "to", "amount", "api_key"]
    add_param_columns = {}
    
    field_info = [
        {"name": "源货币", "type": "string", "description": "源货币代码（from）"},
        {"name": "目标货币", "type": "string", "description": "目标货币代码（to）"},
        {"name": "转换金额", "type": "string", "description": "转换金额（amount）"},
        {"name": "转换结果", "type": "string", "description": "转换结果值（value）"},
        {"name": "转换时间", "type": "datetime", "description": "转换时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:  # type: ignore[override]
        """
        获取货币对价格转换数据。
        
        currency_convert 返回的数据格式为键值对，需要转换为标准表格格式。
        """
        mapped_params = self._map_params(kwargs)
        self._validate_params(mapped_params)
        self.logger.info(
            f"Fetching {self.collection_name} data with params={mapped_params}"
        )

        import akshare as ak
        try:
            # 直接调用 akshare
            call_params = {k: str(v) if v is not None else v for k, v in mapped_params.items()}
            df = ak.currency_convert(**call_params)
        except Exception as e:
            self.logger.error(f"调用 akshare.{self.akshare_func} 失败: {e}")
            raise
        
        if df is None or df.empty:
            self.logger.warning(f"No data returned for {self.collection_name}")
            return pd.DataFrame()

        # 确保 timestamp 字段存在（akshare 可能返回或不返回此字段）
        if "timestamp" not in df.columns:
            df["timestamp"] = datetime.now().strftime("%Y-%m-%d")

        # currency_convert 返回的是键值对格式，需要转换为单行记录
        # item 列的值作为字段名，value 列的值作为字段值
        if "item" in df.columns and "value" in df.columns:
            # 定义英文字段到中文字段的映射
            field_name_mapping = {
                "from": "源货币",
                "to": "目标货币",
                "amount": "转换金额",
                "value": "转换结果",
            }
            
            # 将键值对转换为单行记录
            row_data = {}
            for _, row in df.iterrows():
                item_name = row["item"]
                item_value = row["value"]
                if item_name:
                    # 使用映射表转换字段名，如果没有映射则保持原名
                    chinese_name = field_name_mapping.get(item_name, item_name)
                    row_data[chinese_name] = item_value
            
            # 添加时间戳字段
            if "timestamp" in df.columns:
                row_data["转换时间"] = df.iloc[0]["timestamp"] if len(df) > 0 else datetime.now()
            
            # 创建新的 DataFrame，只有一行
            df = pd.DataFrame([row_data])
        else:
            # 如果没有 item 和 value 列，直接重命名 timestamp
            if "timestamp" in df.columns:
                df = df.rename(columns={"timestamp": "转换时间"})

        # 如果没有转换时间字段，使用当前时间
        if "转换时间" not in df.columns:
            df["转换时间"] = datetime.now()

        # 添加更新时间元数据
        df[self.timestamp_field] = datetime.now()

        self.logger.info(
            f"Successfully fetched {len(df)} records for {self.collection_name}"
        )
        return df
