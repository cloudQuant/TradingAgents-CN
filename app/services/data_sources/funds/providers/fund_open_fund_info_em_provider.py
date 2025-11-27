"""
开放式基金历史行情-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider
import pandas as pd


class FundOpenFundInfoEmProvider(BaseProvider):
    """开放式基金历史行情-东财数据提供者"""
    
    collection_name = "fund_open_fund_info_em"
    display_name = "开放式基金历史行情-东财"
    akshare_func = "fund_open_fund_info_em"
    unique_keys = ["基金代码", "净值日期", "指标类型"]
    
    # 参数映射：多个前端参数映射到fund
    param_mapping = {
        "fund_code": "fund",
        "fund": "fund",
        "code": "fund",
    }
    required_params = ["fund"]
    
    # 自动添加基金代码和指标类型字段
    add_param_columns = {
        "fund": "基金代码",
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "净值日期", "type": "string", "description": "净值日期"},
        {"name": "单位净值", "type": "float", "description": "单位净值"},
        {"name": "累计净值", "type": "float", "description": "累计净值"},
        {"name": "日增长率", "type": "float", "description": "日增长率"},
        {"name": "指标类型", "type": "string", "description": "指标类型"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_open_fund_info_em"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取开放式基金历史行情数据
        
        重写以支持indicator默认值并添加指标类型字段
        """
        # 设置indicator默认值
        if "indicator" not in kwargs:
            kwargs["indicator"] = "单位净值走势"
        
        # 调用父类方法获取数据
        df = super().fetch_data(**kwargs)
        
        # 添加指标类型字段
        if not df.empty and "指标类型" not in df.columns:
            df["指标类型"] = kwargs.get("indicator", "单位净值走势")
        
        return df
