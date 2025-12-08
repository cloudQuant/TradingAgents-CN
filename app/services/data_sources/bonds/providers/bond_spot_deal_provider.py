"""
现券市场成交行情数据提供者（重构版）

数据集合名称: bond_spot_deal
数据唯一标识: 序号, 债券简称, 更新时间
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class BondSpotDealProvider(SimpleProvider):
    """现券市场成交行情数据提供者"""
    
    collection_name = "bond_spot_deal"
    display_name = "现券市场成交行情"
    akshare_func = "bond_spot_deal"
    unique_keys = ['序号', '债券简称', '更新时间']
    
    collection_description = "现券市场成交行情数据"
    collection_route = "/bonds/collections/bond_spot_deal"
    collection_order = 12
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "债券简称", "type": "string", "description": "债券简称"},
        {"name": "成交净价", "type": "number", "description": "成交净价，单位：元"},
        {"name": "最新收益率", "type": "number", "description": "最新收益率，单位：%"},
        {"name": "涨跌", "type": "number", "description": "收益率涨跌，单位：BP"},
        {"name": "加权收益率", "type": "number", "description": "加权收益率，单位：%"},
        {"name": "交易量", "type": "number", "description": "交易量，单位：亿"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取数据并添加递增序号列"""
        df = super().fetch_data(**kwargs)
        
        if df is not None and not df.empty:
            # 添加递增序号列（从1开始）
            df.insert(0, '序号', range(1, len(df) + 1))
        
        return df
