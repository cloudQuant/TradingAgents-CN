"""
债券查询-中国外汇交易中心数据提供者（重构版：继承SimpleProvider）

需求文档: tests/bonds/requirements/01_债券查询-中国外汇交易中心.md
数据唯一标识: 查询代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondInfoCmProvider(SimpleProvider):
    """债券查询-中国外汇交易中心数据提供者"""
    
    # 基本属性
    collection_name = "bond_info_cm"
    display_name = "债券查询-中国外汇交易中心"
    akshare_func = "bond_info_cm"
    unique_keys = ["查询代码"]  # 以查询代码作为唯一标识
    
    # 元信息
    collection_description = "中国外汇交易中心债券信息查询，支持按债券名称、代码、发行人、债券类型、付息方式、发行年份、承销商、评级等条件查询"
    collection_route = "/bonds/collections/bond_info_cm"
    collection_order = 1
    
    # 字段信息
    field_info = [
        {"name": "债券简称", "type": "string", "description": "债券简称"},
        {"name": "债券代码", "type": "string", "description": "债券代码"},
        {"name": "发行人/受托机构", "type": "string", "description": "发行人"},
        {"name": "债券类型", "type": "string", "description": "债券类型"},
        {"name": "发行日期", "type": "string", "description": "发行日期"},
        {"name": "最新债项评级", "type": "string", "description": "最新债项评级"},
        {"name": "查询代码", "type": "string", "description": "查询代码（唯一标识）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
