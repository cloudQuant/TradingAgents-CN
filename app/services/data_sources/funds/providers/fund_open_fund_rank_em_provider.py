"""
开放式基金排行-东财数据提供者（重构版：继承SimpleProvider，无参数接口）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundOpenFundRankEmProvider(SimpleProvider):
    """开放式基金排行-东财数据提供者（无参数接口，直接获取所有数据）"""

    collection_description = "东方财富网-数据中心-开放式基金排行，支持按类型筛选(全部/股票型/混合型/债券型/指数型/QDII/FOF)"
    collection_route = "/funds/collections/fund_open_fund_rank_em"
    collection_order = 30

    collection_name = "fund_open_fund_rank_em"
    display_name = "开放式基金排行-东方财富"
    akshare_func = "fund_open_fund_rank_em"
    unique_keys = ["基金代码", "日期"]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据（无参数接口）
        
        重写基类方法，确保不传递任何参数给 akshare
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data (无参数接口)")
            
            # 不传递任何参数给 akshare（fund_open_fund_rank_em 接口不需要参数）
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
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "累计净值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "近1周", "type": "float", "description": "注意单位: %"},
        {"name": "近1月", "type": "float", "description": "注意单位: %"},
        {"name": "近3月", "type": "float", "description": "注意单位: %"},
        {"name": "近6月", "type": "float", "description": "注意单位: %"},
        {"name": "近1年", "type": "float", "description": "注意单位: %"},
        {"name": "近2年", "type": "float", "description": "注意单位: %"},
        {"name": "近3年", "type": "float", "description": "注意单位: %"},
        {"name": "今年来", "type": "float", "description": "注意单位: %"},
        {"name": "成立来", "type": "float", "description": "注意单位: %"},
        {"name": "自定义", "type": "float", "description": "注意单位: %"},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_open_fund_rank_em"},
    ]
