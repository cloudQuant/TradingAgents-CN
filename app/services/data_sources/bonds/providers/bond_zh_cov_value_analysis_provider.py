"""
可转债价值分析数据提供者（重构版）

数据集合名称: bond_zh_cov_value_analysis
数据唯一标识: 代码, 日期
数据来源: 东方财富网-行情中心-新股数据-可转债数据-可转债价值分析
"""
import pandas as pd
import akshare as ak
from app.services.data_sources.base_provider import BaseProvider


class BondZhCovValueAnalysisProvider(BaseProvider):
    """可转债价值分析数据提供者"""
    
    collection_name = "bond_zh_cov_value_analysis"
    display_name = "可转债价值分析"
    akshare_func = "bond_zh_cov_value_analysis"
    unique_keys = ['代码', '日期']
    
    collection_description = "可转债价值分析数据"
    collection_route = "/bonds/collections/bond_zh_cov_value_analysis"
    collection_order = 18
    
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "日期", "type": "object", "description": "日期"},
        {"name": "收盘价", "type": "float", "description": "收盘价，单位：元"},
        {"name": "纯债价值", "type": "float", "description": "纯债价值，单位：元"},
        {"name": "转股价值", "type": "float", "description": "转股价值，单位：元"},
        {"name": "纯债溢价率", "type": "float", "description": "纯债溢价率，单位：%"},
        {"name": "转股溢价率", "type": "float", "description": "转股溢价率，单位：%"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
    
    def fetch_data(self, symbol: str = None, **kwargs) -> pd.DataFrame:
        """
        获取可转债价值分析数据
        
        Args:
            symbol: 可转债代码，如 "113527"
        """
        if not symbol:
            return pd.DataFrame()
        
        try:
            df = ak.bond_zh_cov_value_analysis(symbol=symbol)
            
            if df is not None and not df.empty:
                # 添加代码列（插入到第一列）
                df.insert(0, '代码', symbol)
            
            return df
        except Exception as e:
            self.logger.warning(f"获取可转债价值分析数据失败 {symbol}: {e}")
            return pd.DataFrame()
