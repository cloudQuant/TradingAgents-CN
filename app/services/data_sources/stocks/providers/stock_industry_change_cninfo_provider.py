"""
上市公司行业归属的变动情况-巨潮资讯数据提供者

巨潮资讯-数据-上市公司行业归属的变动情况
接口: stock_industry_change_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndustryChangeCninfoProvider(BaseProvider):
    """上市公司行业归属的变动情况-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_industry_change_cninfo"
    display_name = "上市公司行业归属的变动情况-巨潮资讯"
    akshare_func = "stock_industry_change_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据-上市公司行业归属的变动情况"
    collection_route = "/stocks/collections/stock_industry_change_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "新证券简称", "type": "object", "description": "-"},
        {"name": "行业中类", "type": "object", "description": "-"},
        {"name": "行业大类", "type": "object", "description": "-"},
        {"name": "行业次类", "type": "object", "description": "-"},
        {"name": "行业门类", "type": "object", "description": "-"},
        {"name": "行业编码", "type": "object", "description": "-"},
        {"name": "分类标准", "type": "object", "description": "-"},
        {"name": "分类标准编码", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "变更日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
