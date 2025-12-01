"""
新发基金-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundNewFoundEmProvider(SimpleProvider):
    """新发基金-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-基金数据-新发基金（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_new_found_em"
    collection_order = 52

    collection_name = "fund_new_found_em"
    display_name = "新发基金-东财"
    akshare_func = "fund_new_found_em"
    unique_keys = ["基金代码"]  # 以基金代码为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_new_found_em 接口不需要参数）
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
        {"name": "发行公司", "type": "string", "description": "发行公司"},
        {"name": "基金类型", "type": "string", "description": "基金类型"},
        {"name": "集中认购期", "type": "string", "description": "集中认购期"},
        {"name": "募集份额", "type": "float", "description": "募集份额（亿份）"},
        {"name": "成立日期", "type": "string", "description": "成立日期"},
        {"name": "成立来涨幅", "type": "float", "description": "成立来涨幅（%）"},
        {"name": "基金经理", "type": "string", "description": "基金经理"},
        {"name": "申购状态", "type": "string", "description": "申购状态"},
        {"name": "优惠费率", "type": "float", "description": "优惠费率（%）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_new_found_em"},
    ]
