"""
公司股本变动-巨潮资讯数据提供者

巨潮资讯-数据-公司股本变动
接口: stock_share_change_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockShareChangeCninfoProvider(BaseProvider):
    """公司股本变动-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_share_change_cninfo"
    display_name = "公司股本变动-巨潮资讯"
    akshare_func = "stock_share_change_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据-公司股本变动"
    collection_route = "/stocks/collections/stock_share_change_cninfo"
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
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "境外法人持股", "type": "float64", "description": "-"},
        {"name": "证券投资基金持股", "type": "float64", "description": "-"},
        {"name": "国家持股-受限", "type": "float64", "description": "-"},
        {"name": "国有法人持股", "type": "float64", "description": "-"},
        {"name": "配售法人股", "type": "float64", "description": "-"},
        {"name": "发起人股份", "type": "float64", "description": "-"},
        {"name": "未流通股份", "type": "float64", "description": "-"},
        {"name": "其中：境外自然人持股", "type": "float64", "description": "-"},
        {"name": "其他流通受限股份", "type": "float64", "description": "-"},
        {"name": "其他流通股", "type": "float64", "description": "-"},
        {"name": "外资持股-受限", "type": "float64", "description": "-"},
        {"name": "内部职工股", "type": "float64", "description": "-"},
        {"name": "境外上市外资股-H股", "type": "float64", "description": "-"},
        {"name": "其中：境内法人持股", "type": "float64", "description": "-"},
        {"name": "自然人持股", "type": "float64", "description": "-"},
        {"name": "人民币普通股", "type": "float64", "description": "-"},
        {"name": "国有法人持股-受限", "type": "float64", "description": "-"},
        {"name": "一般法人持股", "type": "float64", "description": "-"},
        {"name": "控股股东、实际控制人", "type": "float64", "description": "-"},
        {"name": "其中：限售H股", "type": "float64", "description": "-"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "境内法人持股", "type": "float64", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "战略投资者持股", "type": "float64", "description": "-"},
        {"name": "国家持股", "type": "float64", "description": "-"},
        {"name": "其中：限售B股", "type": "float64", "description": "-"},
        {"name": "其他未流通股", "type": "float64", "description": "-"},
        {"name": "流通受限股份", "type": "float64", "description": "-"},
        {"name": "优先股", "type": "float64", "description": "-"},
        {"name": "高管股", "type": "float64", "description": "-"},
        {"name": "总股本", "type": "float64", "description": "-"},
        {"name": "其中：限售高管股", "type": "float64", "description": "-"},
        {"name": "转配股", "type": "float64", "description": "-"},
        {"name": "境内上市外资股-B股", "type": "float64", "description": "-"},
        {"name": "其中：境外法人持股", "type": "float64", "description": "-"},
        {"name": "募集法人股", "type": "float64", "description": "-"},
        {"name": "已流通股份", "type": "float64", "description": "-"},
        {"name": "其中：境内自然人持股", "type": "float64", "description": "-"},
        {"name": "其他内资持股-受限", "type": "float64", "description": "-"},
        {"name": "变动原因编码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
