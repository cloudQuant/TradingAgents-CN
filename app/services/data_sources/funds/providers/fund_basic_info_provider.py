"""
基金基本信息-雪球数据提供者（重构版：继承BaseProvider）
"""
import pandas as pd
from app.services.data_sources.base_provider import BaseProvider


class FundBasicInfoProvider(BaseProvider):
    """基金基本信息-雪球数据提供者"""
    
    collection_name = "fund_basic_info"
    display_name = "雪球基金基本信息"
    akshare_func = "fund_individual_basic_info_xq"
    unique_keys = ["基金代码"]
    
    # 参数映射：将前端参数名映射到 akshare 参数名
    param_mapping = {
        "基金代码": "symbol",
        "fund_code": "symbol",
        "code": "symbol",
        "symbol": "symbol",
    }
    
    # 必填参数
    required_params = ["symbol"]
    
    # 将 symbol 参数值写入"基金代码"列
    add_param_columns = {
        "symbol": "基金代码",
    }


    collection_description = "雪球基金-基金详情，包括成立时间、最新规模、基金经理、评级等"
    collection_route = "/funds/collections/fund_basic_info"
    collection_order = 1

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法

        1. 映射参数名称
        2. 验证必填参数
        3. 调用 akshare 接口
        4. 添加参数列（如基金代码）
        5. 添加元数据字段

        子类可以重写此方法以实现自定义逻辑
        """
        try:
            # 1. 参数映射
            mapped_params = self._map_params(kwargs)

            # 2. 验证必填参数
            self._validate_params(mapped_params)

            # 3. 记录调用日志
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")

            # 4. 调用 akshare
            df = self._call_akshare(self.akshare_func, **mapped_params)

            # fund_individual_basic_info_xq 返回两列的长表（item/value）
            # 之前使用 pivot，当存在重复 item 时会触发 ValueError，导致 API 更新失败。
            # 这里改为手动转换为单行宽表，以首个出现的值为准，并避免 pivot 的限制。
            if df is not None and not df.empty and {"item", "value"}.issubset(df.columns):
                kv_pairs = (
                    df.dropna(subset=["item"])
                    .assign(item=lambda d: d["item"].astype(str).str.strip())
                    .loc[lambda d: d["item"] != ""]
                )
                pivot_dict = (
                    kv_pairs.drop_duplicates(subset=["item"])
                    .set_index("item")["value"]
                    .to_dict()
                )
                df = pd.DataFrame([pivot_dict])

            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()

            # 5. 添加参数列（如基金代码）
            df = self._add_param_columns(df, mapped_params)

            # 6. 添加元数据
            df = self._add_metadata(df)

            self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
            return df

        except ValueError as e:
            # 参数验证错误，直接抛出
            raise
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise


    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": ""},
        {"name": "基金全称", "type": "string", "description": ""},
        {"name": "成立时间", "type": "string", "description": ""},
        {"name": "最新规模", "type": "string", "description": ""},
        {"name": "基金公司", "type": "string", "description": ""},
        {"name": "基金经理", "type": "string", "description": ""},
        {"name": "托管银行", "type": "string", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "评级机构", "type": "string", "description": ""},
        {"name": "基金评级", "type": "string", "description": ""},
        {"name": "投资策略", "type": "string", "description": ""},
        {"name": "投资目标", "type": "string", "description": ""},
        {"name": "业绩比较基准", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_basic_info_xq"},
    ]


