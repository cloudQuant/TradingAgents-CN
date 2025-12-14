"""剩余到期时间数据提供者"""
import pandas as pd
import akshare as ak
from datetime import datetime
from app.services.data_sources.base_provider import BaseProvider


class OptionSseExpireDaySinaProvider(BaseProvider):
    """剩余到期时间数据提供者"""
    
    collection_name = "option_sse_expire_day_sina"
    display_name = "剩余到期时间"
    akshare_func = "option_sse_expire_day_sina"
    unique_keys = ["到期月份", "品种"]
    
    collection_description = "获取指定到期月份指定品种的剩余到期时间"
    collection_route = "/options/collections/option_sse_expire_day_sina"
    collection_order = 18
    
    param_mapping = {"trade_date": "trade_date", "symbol": "symbol", "exchange": "exchange"}
    required_params = ["trade_date", "symbol"]
    add_param_columns = {"trade_date": "到期月份", "symbol": "品种"}
    
    field_info = [
        {"name": "到期月份", "type": "string", "description": "到期月份"},
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "到期日期", "type": "string", "description": "到期日期"},
        {"name": "剩余天数", "type": "int", "description": "剩余到期天数"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取数据 - 处理元组返回值"""
        try:
            # 参数映射
            mapped_params = self._map_params(kwargs)
            self._validate_params(mapped_params)
            
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")
            
            # 调用akshare接口
            result = ak.option_sse_expire_day_sina(**mapped_params)
            
            if result is None:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 处理元组返回值 (到期日期, 剩余天数)
            if isinstance(result, tuple):
                expire_date, days_left = result
                df = pd.DataFrame([{
                    "到期日期": expire_date,
                    "剩余天数": days_left
                }])
            else:
                df = result
            
            if df.empty:
                return pd.DataFrame()
            
            # 添加参数列
            df = self._add_param_columns(df, mapped_params)
            
            # 添加更新时间
            df["更新时间"] = datetime.now()
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            return pd.DataFrame()
