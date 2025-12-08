"""
可转债转股数据提供者（重构版）

数据集合名称: bond_cov_stock_issue_cninfo
数据唯一标识: 债券代码
数据来源: 巨潮资讯-数据中心-专题统计-债券报表-可转债转股
说明: 无参数接口，一次性获取所有可转债转股数据
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCovStockIssueCninfoProvider(SimpleProvider):
    """可转债转股数据提供者"""
    
    collection_name = "bond_cov_stock_issue_cninfo"
    display_name = "可转债转股"
    akshare_func = "bond_cov_stock_issue_cninfo"
    unique_keys = ['债券代码',"公告日期"]
    
    collection_description = "可转债转股数据"
    collection_route = "/bonds/collections/bond_cov_stock_issue_cninfo"
    collection_order = 32
    
    field_info = [
        {"name": "债券代码", "type": "string", "description": "债券代码"},
        {"name": "债券简称", "type": "string", "description": "债券简称"},
        {"name": "转股起始日", "type": "date", "description": "转股起始日期"},
        {"name": "转股终止日", "type": "date", "description": "转股终止日期"},
        {"name": "转股代码", "type": "string", "description": "转股代码"},
        {"name": "转股简称", "type": "string", "description": "转股简称"},
        {"name": "转股价", "type": "float", "description": "转股价格（元）"},
        {"name": "累计转股数量", "type": "float", "description": "累计转股数量（万股）"},
        {"name": "累计转股金额", "type": "float", "description": "累计转股金额（万元）"},
        {"name": "未转股数量", "type": "float", "description": "未转股数量（万张）"},
        {"name": "未转股金额", "type": "float", "description": "未转股金额（万元）"},
        {"name": "转股比例", "type": "float", "description": "转股比例（%）"},
        {"name": "当年转股数量", "type": "float", "description": "当年转股数量（万股）"},
        {"name": "当年转股金额", "type": "float", "description": "当年转股金额（万元）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
