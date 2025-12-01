"""
封闭式基金规模-新浪数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundScaleCloseSinaProvider(SimpleProvider):
    """封闭式基金规模-新浪数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "新浪财经-基金数据-封闭式基金规模（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_scale_close_sina"
    collection_order = 54

    collection_name = "fund_scale_close_sina"
    display_name = "封闭式基金规模-新浪"
    akshare_func = "fund_scale_close_sina"
    unique_keys = ["基金代码", "更新日期"]  # 以基金代码和更新日期为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_scale_close_sina 接口不需要参数）
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
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "单位净值", "type": "float", "description": "单位净值（元）"},
        {"name": "总募集规模", "type": "float", "description": "总募集规模（万份）"},
        {"name": "最近总份额", "type": "float", "description": "最近总份额（份）"},
        {"name": "成立日期", "type": "string", "description": "成立日期"},
        {"name": "基金经理", "type": "string", "description": "基金经理"},
        {"name": "更新日期", "type": "string", "description": "更新日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_scale_close_sina"},
    ]
