"""
行业分类数据-巨潮资讯数据提供者

巨潮资讯-数据-行业分类数据
接口: stock_industry_category_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndustryCategoryCninfoProvider(BaseProvider):
    """行业分类数据-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_industry_category_cninfo"
    display_name = "行业分类数据-巨潮资讯"
    akshare_func = "stock_industry_category_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据-行业分类数据"
    collection_route = "/stocks/collections/stock_industry_category_cninfo"
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
        {"name": "类目编码", "type": "object", "description": "-"},
        {"name": "终止日期", "type": "datetime64", "description": "-"},
        {"name": "行业类型", "type": "object", "description": "-"},
        {"name": "行业类型编码", "type": "object", "description": "-"},
        {"name": "父类编码", "type": "object", "description": "-"},
        {"name": "分级", "type": "int32", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
