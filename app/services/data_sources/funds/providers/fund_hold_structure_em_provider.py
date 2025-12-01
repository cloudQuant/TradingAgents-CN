"""
基金持有结构-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundHoldStructureEmProvider(SimpleProvider):
    """基金持有结构-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "天天基金网-基金数据-规模份额-持有人结构（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_hold_structure_em"
    collection_order = 65

    collection_name = "fund_hold_structure_em"
    display_name = "持有人结构-东财"
    akshare_func = "fund_hold_structure_em"
    unique_keys = ["截止日期"]  # 以截止日期为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_hold_structure_em 接口不需要参数）
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
        {"name": "截止日期", "type": "string", "description": "截止日期"},
        {"name": "基金家数", "type": "int", "description": "基金家数"},
        {"name": "机构持有比列", "type": "float", "description": "机构持有比列（%）"},
        {"name": "个人持有比列", "type": "float", "description": "个人持有比列（%）"},
        {"name": "内部持有比列", "type": "float", "description": "内部持有比列（%）"},
        {"name": "总份额", "type": "float", "description": "总份额（亿份）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_hold_structure_em"},
    ]
