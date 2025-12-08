"""
收益率曲线历史数据数据提供者（重构版）

数据集合名称: bond_china_close_return
数据唯一标识: 曲线名称, 日期, 期限
"""
from app.services.data_sources.base_provider import BaseProvider


class BondChinaCloseReturnProvider(BaseProvider):
    """收益率曲线历史数据数据提供者"""
    
    collection_name = "bond_china_close_return"
    display_name = "收益率曲线历史数据"
    akshare_func = "bond_china_close_return"
    unique_keys = ["曲线名称", "日期", "期限"]
    
    collection_description = "收益率曲线历史数据数据"
    collection_route = "/bonds/collections/bond_china_close_return"
    collection_order = 26

    # 前端参数到 AkShare 参数的映射
    # - symbol 直接透传
    # - start_date / end_date 直接透传（date 在 fetch_data 中特殊处理）
    param_mapping = {
        "symbol": "symbol",
        "start_date": "start_date",
        "end_date": "end_date",
    }

    # AkShare 必须参数
    required_params = ["symbol", "start_date", "end_date"]

    # 将关键参数写回到结果中
    add_param_columns = {
        "symbol": "曲线名称",
        "period": "期限间隔",
    }
    
    field_info = [
        {"name": "曲线名称", "type": "string", "description": "收益率曲线名称（AkShare symbol 参数）"},
        {"name": "日期", "type": "date", "description": "收益率曲线日期"},
        {"name": "期限", "type": "float", "description": "期限（年）"},
        {"name": "到期收益率", "type": "float", "description": "到期收益率(%)"},
        {"name": "即期收益率", "type": "float", "description": "即期收益率(%)"},
        {"name": "远期收益率", "type": "float", "description": "远期收益率(%)"},
        {"name": "期限间隔", "type": "string", "description": "期限间隔设置，例如 1 或 0.5"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]

    def fetch_data(self, **kwargs):
        raw_kwargs = dict(kwargs)
        self.logger.info(f"[{self.collection_name}] fetch_data 收到原始参数: {raw_kwargs}")
        self.logger.info(f"[{self.collection_name}] param_mapping: {self.param_mapping}")

        # 如果只传入 date，则同时作为 start_date 和 end_date
        date_value = raw_kwargs.pop("date", None)  # 弹出 date 避免后续 _map_params 再处理
        if date_value:
            self.logger.info(f"[{self.collection_name}] 处理 date 参数: {date_value}")
            if not raw_kwargs.get("start_date") and not raw_kwargs.get("end_date"):
                s = str(date_value).strip().replace("-", "").replace("/", "")
                if len(s) == 8 and s.isdigit():
                    raw_kwargs["start_date"] = s
                    raw_kwargs["end_date"] = s
                    self.logger.info(f"[{self.collection_name}] date 转换为 start_date={s}, end_date={s}")
                else:
                    self.logger.warning(f"日期格式不正确: {date_value}，期望 YYYYMMDD 或 YYYY-MM-DD")

        self.logger.info(f"[{self.collection_name}] 调用 _map_params 前的参数: {raw_kwargs}")
        mapped_params = self._map_params(raw_kwargs)
        self.logger.info(f"[{self.collection_name}] 映射后的参数: {mapped_params}")

        if "period" not in mapped_params or mapped_params["period"] is None:
            mapped_params["period"] = "1"

        self._validate_params(mapped_params)

        self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")
        df = self._call_akshare(self.akshare_func, **mapped_params)

        if df is None or df.empty:
            self.logger.warning(f"No data returned for {self.collection_name}")
            return df

        df = self._add_param_columns(df, mapped_params)
        df = self._add_metadata(df)

        self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
        return df
