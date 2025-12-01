"""
基金报告资产配置-巨潮数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundReportAssetAllocationCninfoProvider(SimpleProvider):
    """基金报告资产配置-巨潮数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "巨潮资讯-数据中心-专题统计-基金报表-基金资产配置（无需参数，支持更新所有）"
    collection_route = "/funds/collections/fund_report_asset_allocation_cninfo"
    collection_order = 63

    collection_name = "fund_report_asset_allocation_cninfo"
    display_name = "基金资产配置-巨潮"
    akshare_func = "fund_report_asset_allocation_cninfo"
    unique_keys = ["报告期"]  # 以报告期为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_report_asset_allocation_cninfo 接口不需要参数）
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
        {"name": "报告期", "type": "string", "description": "报告期"},
        {"name": "基金覆盖家数", "type": "string", "description": "基金覆盖家数（只）"},
        {"name": "股票权益类占净资产比例", "type": "string", "description": "股票权益类占净资产比例（%）"},
        {"name": "债券固定收益类占净资产比例", "type": "string", "description": "债券固定收益类占净资产比例（%）"},
        {"name": "现金货币类占净资产比例", "type": "string", "description": "现金货币类占净资产比例（%）"},
        {"name": "基金市场净资产规模", "type": "string", "description": "基金市场净资产规模（亿元）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_report_asset_allocation_cninfo"},
    ]
