"""
场内交易基金历史行情-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider
import pandas as pd


class FundEtfFundInfoEmProvider(BaseProvider):
    """场内交易基金历史行情-东财数据提供者"""
    
    collection_name = "fund_etf_fund_info_em"
    display_name = "场内交易基金-历史行情"
    akshare_func = "fund_etf_fund_info_em"
    unique_keys = ["基金代码", "净值日期"]
    
    # 参数映射：多个前端参数映射到fund
    param_mapping = {
        "fund_code": "fund",
        "fund": "fund",
        "code": "fund",
    }
    required_params = ["fund"]
    
    # 自动添加基金代码字段
    add_param_columns = {
        "fund": "基金代码",
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "净值日期", "type": "string", "description": "净值日期"},
        {"name": "单位净值", "type": "float", "description": "单位净值"},
        {"name": "累计净值", "type": "float", "description": "累计净值"},
        {"name": "日增长率", "type": "float", "description": "日增长率"},
        {"name": "申购状态", "type": "string", "description": "申购状态"},
        {"name": "赎回状态", "type": "string", "description": "赎回状态"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_fund_info_em"},
    ]
    
 
    collection_description = "东方财富网-天天基金网-场内交易基金-历史净值数据"
    collection_route = "/funds/collections/fund_etf_fund_info_em"
    collection_order = 25

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取场内交易基金历史行情数据
        
        重写以支持start_date和end_date默认值
        """
        # 设置默认值
        if "start_date" not in kwargs:
            kwargs["start_date"] = "2000-01-01"
        if "end_date" not in kwargs:
            kwargs["end_date"] = "2050-01-01"
        
        return super().fetch_data(**kwargs)
