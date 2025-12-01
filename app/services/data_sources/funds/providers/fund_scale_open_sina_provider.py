"""
开放式基金规模-新浪数据提供者（重构版：继承BaseProvider，需要symbol参数）
"""
import pandas as pd
from app.services.data_sources.base_provider import BaseProvider


class FundScaleOpenSinaProvider(BaseProvider):
    """开放式基金规模-新浪数据提供者（需要symbol参数：基金类型）"""

    collection_description = "新浪财经-基金数据-开放式基金规模（需要基金类型参数）"
    collection_route = "/funds/collections/fund_scale_open_sina"
    collection_order = 53

    collection_name = "fund_scale_open_sina"
    display_name = "开放式基金规模-新浪"
    akshare_func = "fund_scale_open_sina"
    unique_keys = ["基金代码", "更新日期"]
    
    # 参数映射：支持多种参数名
    param_mapping = {
        "symbol": "symbol",
        "fund_type": "symbol",
        "type": "symbol",
    }
    required_params = ["symbol"]
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "单位净值", "type": "float", "description": "单位净值（元）"},
        {"name": "总募集规模", "type": "float", "description": "总募集规模（万份）"},
        {"name": "最近总份额", "type": "float", "description": "最近总份额（份）"},
        {"name": "成立日期", "type": "string", "description": "成立日期"},
        {"name": "基金经理", "type": "string", "description": "基金经理"},
        {"name": "更新日期", "type": "string", "description": "更新日期"},
        {"name": "基金类型", "type": "string", "description": "基金类型（从symbol参数中获取）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_scale_open_sina"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        重写以添加"基金类型"字段（从symbol参数中获取）
        """
        try:
            # 1. 参数映射
            mapped_params = self._map_params(kwargs)
            
            # 2. 验证必填参数
            self._validate_params(mapped_params)
            
            # 3. 记录调用日志
            symbol_param = mapped_params.get("symbol")
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")
            
            # 4. 调用 akshare
            df = self._call_akshare(self.akshare_func, **mapped_params)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 5. 添加基金类型字段（从symbol参数中获取）
            if symbol_param:
                df["基金类型"] = symbol_param
                self.logger.debug(f"添加基金类型字段: {symbol_param}")
            else:
                df["基金类型"] = ""
            
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
