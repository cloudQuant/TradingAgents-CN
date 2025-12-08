"""
可转债比价表数据提供者（重构版）

数据集合名称: bond_cov_comparison
数据唯一标识: 转债代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCovComparisonProvider(SimpleProvider):
    """可转债比价表数据提供者"""
    
    collection_name = "bond_cov_comparison"
    display_name = "可转债比价表"
    akshare_func = "bond_cov_comparison"
    unique_keys = ['转债代码',"更新时间"]
    
    collection_description = "可转债比价表数据"
    collection_route = "/bonds/collections/bond_cov_comparison"
    collection_order = 17
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "转债代码", "type": "string", "description": "可转债代码"},
        {"name": "转债名称", "type": "string", "description": "可转债名称"},
        {"name": "转债最新价", "type": "float", "description": "转债最新价"},
        {"name": "转债涨跌幅", "type": "float", "description": "转债涨跌幅，单位：%"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股名称", "type": "string", "description": "正股名称"},
        {"name": "正股最新价", "type": "float", "description": "正股最新价"},
        {"name": "正股涨跌幅", "type": "float", "description": "正股涨跌幅，单位：%"},
        {"name": "转股价", "type": "float", "description": "转股价"},
        {"name": "转股价值", "type": "float", "description": "转股价值"},
        {"name": "转股溢价率", "type": "float", "description": "转股溢价率，单位：%"},
        {"name": "纯债溢价率", "type": "float", "description": "纯债溢价率，单位：%"},
        {"name": "回售触发价", "type": "float", "description": "回售触发价"},
        {"name": "强赎触发价", "type": "float", "description": "强赎触发价"},
        {"name": "到期赎回价", "type": "float", "description": "到期赎回价"},
        {"name": "纯债价值", "type": "float", "description": "纯债价值"},
        {"name": "开始转股日", "type": "string", "description": "开始转股日"},
        {"name": "上市日期", "type": "string", "description": "上市日期"},
        {"name": "申购日期", "type": "string", "description": "申购日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
