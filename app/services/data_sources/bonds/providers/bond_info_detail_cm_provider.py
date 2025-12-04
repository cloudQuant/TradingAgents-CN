"""
债券基础信息-中国外汇交易中心数据提供者（重构版：继承BaseProvider）

需求文档: tests/bonds/requirements/02_债券基础信息-中国外汇交易中心.md
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_provider import BaseProvider


class BondInfoDetailCmProvider(BaseProvider):
    """债券基础信息-中国外汇交易中心数据提供者"""
    
    # 基本属性
    collection_name = "bond_info_detail_cm"
    display_name = "债券基础信息-中国外汇交易中心"
    akshare_func = "bond_info_detail_cm"
    unique_keys = ["债券代码"]  # 以债券代码作为唯一标识
    
    # 参数映射
    param_mapping = {
        "bond_code": "symbol",
        "symbol": "symbol",
        "code": "symbol",
    }
    required_params = ["symbol"]
    add_param_columns = {"symbol": "债券代码"}
    
    # 元信息
    collection_description = "债券详细信息，包括发行条款、评级等详细数据"
    collection_route = "/bonds/collections/bond_info_detail_cm"
    collection_order = 2
    
    # 字段信息
    field_info = [
        {"name": "债券代码", "type": "string", "description": "债券代码（查询参数）"},
        {"name": "item", "type": "string", "description": "信息项"},
        {"name": "value", "type": "string", "description": "信息值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
