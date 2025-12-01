"""
基金拆分-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundCfEmProvider(SimpleProvider):
    """基金拆分-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-天天基金网-基金数据-分红送配-基金拆分，包含拆分折算日、拆分类型、拆分折算比例等"
    collection_route = "/funds/collections/fund_cf_em"
    collection_order = 28

    collection_name = "fund_cf_em"
    display_name = "基金拆分-东方财富"
    akshare_func = "fund_cf_em"
    unique_keys = ["基金代码", "拆分折算日", "拆分类型"]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_cf_em 接口不需要参数）
            df = self._call_akshare(self.akshare_func)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "拆分折算日", "type": "string", "description": "拆分折算日"},
        {"name": "拆分类型", "type": "string", "description": "拆分类型"},
        {"name": "拆分折算比例", "type": "float", "description": "拆分折算比例"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_cf_em"},
    ]
