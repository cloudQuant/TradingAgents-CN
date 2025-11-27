"""
基金持仓债券-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundPortfolioBondHoldEmProvider(BaseProvider):
    """基金持仓债券-东财数据提供者"""
    
    collection_name = "fund_portfolio_bond_hold_em"
    display_name = "基金持仓债券-东财"
    akshare_func = "fund_portfolio_bond_hold_em"
    unique_keys = ["基金代码", "债券代码", "季度"]
    
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
        {"name": "更新时间", "type": "datetime", "description": "更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_portfolio_bond_hold_em"},
    ]
