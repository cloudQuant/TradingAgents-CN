"""
场内交易基金实时数据-东财数据提供者（重构版：继承BaseProvider）

AKShare的fund_etf_fund_daily_em接口返回的列名包含具体日期，本provider将其重命名为通用名称：
- 当前交易日-单位净值、当前交易日-累计净值
- 前一个交易日-单位净值、前一个交易日-累计净值
"""
import pandas as pd
import re
from app.services.data_sources.base_provider import BaseProvider


class FundEtfFundDailyEmProvider(BaseProvider):
    
    """场内交易基金实时数据-东财数据提供者"""

    collection_description = "东方财富网-天天基金网-场内交易基金实时数据，每个交易日 16:00-23:00 更新"
    collection_route = "/funds/collections/fund_etf_fund_daily_em"
    collection_order = 23

    collection_name = "fund_etf_fund_daily_em"
    display_name = "场内交易基金实时行情-东方财富"
    akshare_func = "fund_etf_fund_daily_em"
    unique_keys = ["基金代码", "更新时间"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "类型", "type": "float", "description": ""},
        {"name": "当前交易日-单位净值", "type": "float", "description": "会返回具体的日期值作为字段"},
        {"name": "当前交易日-累计净值", "type": "float", "description": "会返回具体的日期值作为字段"},
        {"name": "前一个交易日-单位净值", "type": "float", "description": "会返回具体的日期值作为字段"},
        {"name": "前一个交易日-累计净值", "type": "float", "description": "会返回具体的日期值作为字段"},
        {"name": "增长值", "type": "float", "description": ""},
        {"name": "增长率", "type": "string", "description": ""},
        {"name": "市价", "type": "string", "description": ""},
        {"name": "折价率", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_fund_daily_em"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取场内交易基金实时数据，将日期列重命名为通用名称。"""
        try:
            self.logger.info(f"Fetching {self.collection_name} data")
            
            # 调用akshare获取数据
            df = self._call_akshare(self.akshare_func, **kwargs)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            df = df.copy()
            
            # 重命名日期相关列
            df = self._rename_date_columns(df)
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise

    def _rename_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """将日期格式的列名重命名为通用名称。"""
        # akshare 返回的列名格式可能是：
        # - "2024-11-29-单位净值" -> "当前交易日-单位净值"
        # - "2024-11-28-单位净值" -> "前一个交易日-单位净值"
        # - "2024-11-29-累计净值" -> "当前交易日-累计净值"
        # - "2024-11-28-累计净值" -> "前一个交易日-累计净值"
        
        rename_map = {}
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-(.+)$')
        
        # 找到所有包含日期的列
        date_columns = {}
        for col in df.columns:
            match = date_pattern.match(col)
            if match:
                field_name = match.group(1)
                date_str = col.split('-')[0:3]  # 提取日期部分
                date_key = '-'.join(date_str)
                
                if field_name not in date_columns:
                    date_columns[field_name] = []
                date_columns[field_name].append((date_key, col))
        
        # 对每个字段，找到最新的日期（当前交易日）和次新的日期（前一个交易日）
        for field_name, date_cols in date_columns.items():
            if len(date_cols) >= 2:
                # 按日期排序，最新的在前
                date_cols.sort(key=lambda x: x[0], reverse=True)
                # 当前交易日（最新的日期）
                rename_map[date_cols[0][1]] = f"当前交易日-{field_name}"
                # 前一个交易日（次新的日期）
                rename_map[date_cols[1][1]] = f"前一个交易日-{field_name}"
            elif len(date_cols) == 1:
                # 只有一个日期，假设是当前交易日
                rename_map[date_cols[0][1]] = f"当前交易日-{field_name}"
        
        # 执行重命名
        if rename_map:
            df.rename(columns=rename_map, inplace=True)
            self.logger.debug(f"Renamed columns: {rename_map}")
        
        return df
