"""中金所上证50指数合约列表数据提供者"""
import pandas as pd
import akshare as ak
from datetime import datetime
from app.services.data_sources.base_provider import SimpleProvider


class OptionCffexSz50ListSinaProvider(SimpleProvider):
    """中金所上证50指数合约列表数据提供者"""
    
    collection_name = "option_cffex_sz50_list_sina"
    display_name = "中金所上证50指数合约列表"
    akshare_func = "option_cffex_sz50_list_sina"
    unique_keys = ["合约代码"]
    
    collection_description = "中金所上证50指数所有合约，返回的第一个合约为主力合约"
    collection_route = "/options/collections/option_cffex_sz50_list_sina"
    collection_order = 8
    
    field_info = [
        {"name": "指数名称", "type": "string", "description": "指数名称"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取数据 - 处理字典返回值"""
        try:
            self.logger.info(f"Fetching {self.collection_name} data")
            
            # 调用akshare接口
            result = getattr(ak, self.akshare_func)()
            
            if result is None:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 处理字典返回值
            if isinstance(result, dict):
                # 将字典转换为DataFrame
                rows = []
                for index_name, contracts in result.items():
                    for contract in contracts:
                        rows.append({"指数名称": index_name, "合约代码": contract})
                df = pd.DataFrame(rows)
            else:
                df = result
            
            if df.empty:
                return pd.DataFrame()
            
            # 添加更新时间
            df["更新时间"] = datetime.now()
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            return pd.DataFrame()
