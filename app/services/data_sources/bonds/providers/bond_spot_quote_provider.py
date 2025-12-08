"""
现券市场做市报价数据提供者（重构版）

数据集合名称: bond_spot_quote
数据唯一标识: 序号, 报价机构, 债券简称
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class BondSpotQuoteProvider(SimpleProvider):
    """现券市场做市报价数据提供者"""
    
    collection_name = "bond_spot_quote"
    display_name = "现券市场做市报价"
    akshare_func = "bond_spot_quote"
    unique_keys = ["序号", '报价机构', '债券简称']
    
    collection_description = "现券市场做市报价数据"
    collection_route = "/bonds/collections/bond_spot_quote"
    collection_order = 11
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "报价机构", "type": "string", "description": "报价机构"},
        {"name": "债券简称", "type": "string", "description": "债券简称"},
        {"name": "买入净价", "type": "number", "description": "买入净价，单位：元"},
        {"name": "卖出净价", "type": "number", "description": "卖出净价，单位：元"},
        {"name": "买入收益率", "type": "number", "description": "买入收益率，单位：%"},
        {"name": "卖出收益率", "type": "number", "description": "卖出收益率，单位：%"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取数据并添加递增序号列"""
        df = super().fetch_data(**kwargs)
        
        if df is not None and not df.empty:
            # 添加递增序号列（从1开始）
            # df.insert(0, '序号', range(1, len(df) + 1))
            df["序号"] = range(len(df))
        
        return df
