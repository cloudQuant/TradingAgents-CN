"""
基金评级汇总-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundRatingAllEmProvider(SimpleProvider):
    """基金评级汇总-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-基金评级-基金评级总汇（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_rating_all_em"
    collection_order = 47

    collection_name = "fund_rating_all_em"
    display_name = "基金评级总汇-东财"
    akshare_func = "fund_rating_all"
    unique_keys = ["代码"]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_rating_all_em 接口不需要参数）
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
        {"name": "代码", "type": "string", "description": "基金代码"},
        {"name": "简称", "type": "string", "description": "基金简称"},
        {"name": "基金经理", "type": "string", "description": "基金经理"},
        {"name": "基金公司", "type": "string", "description": "基金公司"},
        {"name": "5星评级家数", "type": "int", "description": "5星评级家数"},
        {"name": "上海证券", "type": "float", "description": "上海证券评级"},
        {"name": "招商证券", "type": "float", "description": "招商证券评级"},
        {"name": "济安金信", "type": "float", "description": "济安金信评级"},
        {"name": "手续费", "type": "float", "description": "手续费"},
        {"name": "类型", "type": "string", "description": "基金类型"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_rating_all_em"},
    ]
