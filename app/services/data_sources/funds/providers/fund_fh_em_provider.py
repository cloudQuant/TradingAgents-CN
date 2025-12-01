"""
基金分红-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundFhEmProvider(SimpleProvider):
    
    """基金分红-东财数据提供者"""

    collection_description = "东方财富网-天天基金网-基金数据-分红送配-基金分红，包含权益登记日、除息日期、分红金额等"
    collection_route = "/funds/collections/fund_fh_em"
    collection_order = 27

    collection_name = "fund_fh_em"
    display_name = "基金分红-东财"
    akshare_func = "fund_fh_em"
    unique_keys = ["基金代码", "权益登记日"]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_fh_em 接口不需要参数）
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
        {"name": "序号", "type": "int64", "description": "序号"},
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "权益登记日", "type": "string", "description": "权益登记日"},
        {"name": "除息日期", "type": "string", "description": "除息日期"},
        {"name": "分红", "type": "float64", "description": "分红（单位：元/份）"},
        {"name": "分红发放日", "type": "string", "description": "分红发放日"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_fh_em"},
    ]
