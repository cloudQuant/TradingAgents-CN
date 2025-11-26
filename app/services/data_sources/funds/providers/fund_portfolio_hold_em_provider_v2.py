"""
基金持仓股票-东财数据提供者 (使用基类重构版本)

对比原版本 fund_portfolio_hold_em_provider.py（71行），新版本只需要约30行代码。
"""
from app.services.data_sources.base_provider import BaseProvider


class FundPortfolioHoldEmProviderV2(BaseProvider):
    """基金持仓股票-东财数据提供者"""
    
    collection_name = "fund_portfolio_hold_em"
    display_name = "基金持仓股票-东财"
    akshare_func = "fund_portfolio_hold_em"
    unique_keys = ["基金代码", "股票代码", "季度"]
    
    # 参数映射：前端参数名 -> akshare参数名
    param_mapping = {
        "fund_code": "symbol",
        "code": "symbol",
        "year": "date",
    }
    
    # 必填参数
    required_params = ["symbol", "date"]
    
    # 将参数值添加到数据列
    add_param_columns = {"symbol": "基金代码"}
    
    # 时间戳字段名
    timestamp_field = "更新时间"
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "股票代码", "type": "string", "description": "股票代码"},
        {"name": "股票名称", "type": "string", "description": "股票名称"},
        {"name": "占净值比例", "type": "float", "description": "持仓占比"},
        {"name": "持仓数", "type": "int", "description": "持仓数量"},
        {"name": "持仓市值", "type": "float", "description": "持仓市值"},
        {"name": "季度", "type": "string", "description": "季度"},
        {"name": "更新时间", "type": "datetime", "description": "更新时间"},
    ]
