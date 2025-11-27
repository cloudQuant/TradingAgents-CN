"""
基金持仓变动-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider
import pandas as pd


class FundPortfolioChangeEmProvider(BaseProvider):
    """基金持仓变动-东财数据提供者"""
    
    collection_name = "fund_portfolio_change_em"
    display_name = "基金持仓变动-东财"
    akshare_func = "fund_portfolio_change_em"
    unique_keys = ["基金代码", "股票代码", "季度"]
    
    # 参数映射：多个前端参数映射到akshare参数
    param_mapping = {
        "fund_code": "symbol",
        "symbol": "symbol",
        "code": "symbol",
        "year": "date",
        "date": "date",
    }
    required_params = ["symbol", "date"]
    
    # 自动添加基金代码字段
    add_param_columns = {
        "symbol": "基金代码",
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "股票代码", "type": "string", "description": "股票代码"},
        {"name": "股票名称", "type": "string", "description": "股票名称"},
        {"name": "持仓变动", "type": "string", "description": "持仓变动类型"},
        {"name": "变动数量", "type": "float", "description": "变动数量"},
        {"name": "变动市值", "type": "float", "description": "变动市值"},
        {"name": "季度", "type": "string", "description": "季度"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_portfolio_change_em"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取基金持仓变动数据
        
        重写以支持indicator默认值
        """
        # 设置indicator默认值
        if "indicator" not in kwargs:
            kwargs["indicator"] = "累计买入"
        
        return super().fetch_data(**kwargs)
