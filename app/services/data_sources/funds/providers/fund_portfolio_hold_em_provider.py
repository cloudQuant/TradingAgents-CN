"""
基金持仓股票-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundPortfolioHoldEmProvider(BaseProvider):
    """基金持仓股票-东财数据提供者"""
    
    collection_name = "fund_portfolio_hold_em"
    display_name = "基金持仓股票-东财"
    akshare_func = "fund_portfolio_hold_em"
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
    
    # 自定义时间戳字段名
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
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_portfolio_hold_em"},
    ]
