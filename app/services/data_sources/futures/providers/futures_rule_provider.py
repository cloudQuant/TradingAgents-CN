"""期货规则-交易日历表数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesRuleProvider(BaseProvider):
    """期货规则-交易日历表数据提供者"""
    
    collection_name = "futures_rule"
    display_name = "期货规则-交易日历表"
    akshare_func = "futures_rule"
    unique_keys = ["交易所", "代码"]
    
    collection_description = "国泰君安期货交易日历数据表"
    collection_route = "/futures/collections/futures_rule"
    collection_order = 3
    
    param_mapping = {
        "date": "date",
    }
    required_params = ["date"]
    add_param_columns = {"date": "查询日期"}
    
    field_info = [
        {"name": "交易所", "type": "string", "description": ""},
        {"name": "品种", "type": "string", "description": ""},
        {"name": "代码", "type": "string", "description": ""},
        {"name": "交易保证金比例", "type": "float", "description": "单位: %"},
        {"name": "涨跌停板幅度", "type": "float", "description": "单位: %"},
        {"name": "合约乘数", "type": "int", "description": ""},
        {"name": "最小变动价位", "type": "float", "description": ""},
        {"name": "限价单每笔最大下单手数", "type": "int", "description": ""},
        {"name": "特殊合约参数调整", "type": "string", "description": ""},
        {"name": "调整备注", "type": "string", "description": ""},
        {"name": "查询日期", "type": "string", "description": "查询的交易日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
