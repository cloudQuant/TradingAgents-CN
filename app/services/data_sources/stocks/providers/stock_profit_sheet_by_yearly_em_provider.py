"""
利润表-按年度数据提供者

东方财富-股票-财务分析-利润表-按年度
接口: stock_profit_sheet_by_yearly_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockProfitSheetByYearlyEmProvider(BaseProvider):
    """利润表-按年度数据提供者"""
    
    # 必填属性
    collection_name = "stock_profit_sheet_by_yearly_em"
    display_name = "利润表-按年度"
    akshare_func = "stock_profit_sheet_by_yearly_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-股票-财务分析-利润表-按年度"
    collection_route = "/stocks/collections/stock_profit_sheet_by_yearly_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "-", "type": "-", "description": "203 项，不逐一列出"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
