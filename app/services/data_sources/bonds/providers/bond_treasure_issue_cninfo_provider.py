"""
国债发行数据提供者（重构版）

数据集合名称: bond_treasure_issue_cninfo
数据唯一标识: 债券代码
数据来源: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-国债发行
"""
from app.services.data_sources.base_provider import BaseProvider


class BondTreasureIssueCninfoProvider(BaseProvider):
    """国债发行数据提供者"""
    
    collection_name = "bond_treasure_issue_cninfo"
    display_name = "国债发行"
    akshare_func = "bond_treasure_issue_cninfo"
    unique_keys = ['债券代码', '公告日期']
    
    collection_description = "国债发行数据"
    collection_route = "/bonds/collections/bond_treasure_issue_cninfo"
    collection_order = 28
    
    field_info = [
        {"name": "债券代码", "type": "string", "description": "债券代码"},
        {"name": "债券简称", "type": "string", "description": "债券简称"},
        {"name": "发行起始日", "type": "date", "description": "发行起始日期"},
        {"name": "发行终止日", "type": "date", "description": "发行终止日期"},
        {"name": "计划发行总量", "type": "float", "description": "计划发行总量（亿元）"},
        {"name": "实际发行总量", "type": "float", "description": "实际发行总量（亿元）"},
        {"name": "发行价格", "type": "float", "description": "发行价格（元）"},
        {"name": "单位面值", "type": "integer", "description": "单位面值（元）"},
        {"name": "缴款日", "type": "date", "description": "缴款日期"},
        {"name": "增发次数", "type": "integer", "description": "增发次数"},
        {"name": "交易市场", "type": "string", "description": "交易市场"},
        {"name": "发行方式", "type": "string", "description": "发行方式"},
        {"name": "发行对象", "type": "string", "description": "发行对象"},
        {"name": "公告日期", "type": "date", "description": "公告日期"},
        {"name": "债券名称", "type": "string", "description": "债券名称"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
