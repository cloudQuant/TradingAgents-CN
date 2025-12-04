"""上交所期权风险指标数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionRiskIndicatorSseProvider(BaseProvider):
    """上交所期权风险指标数据提供者"""
    
    collection_name = "option_risk_indicator_sse"
    display_name = "上交所期权风险指标"
    akshare_func = "option_risk_indicator_sse"
    unique_keys = ["TRADE_DATE", "CONTRACT_ID"]
    
    collection_description = "上海证券交易所-产品-股票期权-期权风险指标数据"
    collection_route = "/options/collections/option_risk_indicator_sse"
    collection_order = 3
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {}
    
    field_info = [
        {"name": "TRADE_DATE", "type": "string", "description": "交易日期"},
        {"name": "SECURITY_ID", "type": "string", "description": "证券ID"},
        {"name": "CONTRACT_ID", "type": "string", "description": "合约ID"},
        {"name": "CONTRACT_SYMBOL", "type": "string", "description": "合约代码"},
        {"name": "DELTA_VALUE", "type": "float", "description": "Delta值"},
        {"name": "THETA_VALUE", "type": "float", "description": "Theta值"},
        {"name": "GAMMA_VALUE", "type": "float", "description": "Gamma值"},
        {"name": "VEGA_VALUE", "type": "float", "description": "Vega值"},
        {"name": "RHO_VALUE", "type": "float", "description": "Rho值"},
        {"name": "IMPLC_VOLATLTY", "type": "float", "description": "隐含波动率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
