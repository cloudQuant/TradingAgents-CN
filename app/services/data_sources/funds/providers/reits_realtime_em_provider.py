"""
REITs实时行情-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from datetime import datetime
from app.services.data_sources.base_provider import SimpleProvider


class ReitsRealtimeEmProvider(SimpleProvider):
    """REITs实时行情-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-行情中心-REITs-沪深 REITs-实时行情（无需参数，支持更新所有）"
    collection_route = "/funds/collections/reits_realtime_em"
    collection_order = 59

    collection_name = "reits_realtime_em"
    display_name = "REITs实时行情-东财"
    akshare_func = "reits_realtime_em"
    unique_keys = ["代码", "日期"]  # 以代码和日期为唯一标识
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare，并添加日期字段
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（reits_realtime_em 接口不需要参数）
            df = self._call_akshare(self.akshare_func)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 添加日期字段（当前日期，格式：YYYY-MM-DD）
            current_date = datetime.now().strftime("%Y-%m-%d")
            df["日期"] = current_date
            self.logger.debug(f"添加日期字段: {current_date}")
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise

    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "代码", "type": "string", "description": "REITs代码"},
        {"name": "名称", "type": "string", "description": "REITs名称"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌额", "type": "float", "description": "涨跌额"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅（%）"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "成交额", "type": "float", "description": "成交额"},
        {"name": "开盘价", "type": "float", "description": "开盘价"},
        {"name": "最高价", "type": "float", "description": "最高价"},
        {"name": "最低价", "type": "float", "description": "最低价"},
        {"name": "昨收", "type": "float", "description": "昨收价"},
        {"name": "日期", "type": "string", "description": "日期（YYYY-MM-DD格式）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: reits_realtime_em"},
    ]
