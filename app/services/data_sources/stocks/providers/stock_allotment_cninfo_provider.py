"""
配股实施方案-巨潮资讯数据提供者

巨潮资讯-个股-配股实施方案
接口: stock_allotment_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockAllotmentCninfoProvider(BaseProvider):
    """配股实施方案-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_allotment_cninfo"
    display_name = "配股实施方案-巨潮资讯"
    akshare_func = "stock_allotment_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-个股-配股实施方案"
    collection_route = "/stocks/collections/stock_allotment_cninfo"
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
        {"name": "记录标识", "type": "int64", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "停牌起始日", "type": "object", "description": "-"},
        {"name": "上市公告日期", "type": "object", "description": "-"},
        {"name": "配股缴款起始日", "type": "object", "description": "-"},
        {"name": "可转配股数量", "type": "float64", "description": "-"},
        {"name": "停牌截止日", "type": "object", "description": "-"},
        {"name": "实际配股数量", "type": "float64", "description": "-"},
        {"name": "配股价格", "type": "float64", "description": "-"},
        {"name": "配股比例", "type": "float64", "description": "-"},
        {"name": "配股前总股本", "type": "float64", "description": "-"},
        {"name": "每股配权转让费(元)", "type": "float64", "description": "-"},
        {"name": "法人股实配数量", "type": "float64", "description": "-"},
        {"name": "实际募资净额", "type": "float64", "description": "-"},
        {"name": "大股东认购方式", "type": "object", "description": "-"},
        {"name": "其他配售简称", "type": "object", "description": "-"},
        {"name": "发行方式", "type": "object", "description": "-"},
        {"name": "配股失败，退还申购款日期", "type": "object", "description": "-"},
        {"name": "除权基准日", "type": "object", "description": "-"},
        {"name": "预计发行费用", "type": "float64", "description": "-"},
        {"name": "配股发行结果公告日", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "配股权证交易截止日", "type": "datetime64", "description": "-"},
        {"name": "其他股份实配数量", "type": "float64", "description": "-"},
        {"name": "国家股实配数量", "type": "float64", "description": "-"},
        {"name": "委托单位", "type": "object", "description": "-"},
        {"name": "公众获转配数量", "type": "float64", "description": "-"},
        {"name": "其他配售代码", "type": "object", "description": "-"},
        {"name": "配售对象", "type": "object", "description": "-"},
        {"name": "配股权证交易起始日", "type": "datetime64", "description": "-"},
        {"name": "资金到账日", "type": "datetime64", "description": "-"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "实际募资总额", "type": "float64", "description": "-"},
        {"name": "预计募集资金", "type": "float64", "description": "-"},
        {"name": "大股东认购数量", "type": "float64", "description": "-"},
        {"name": "公众股实配数量", "type": "float64", "description": "-"},
        {"name": "转配股实配数量", "type": "float64", "description": "-"},
        {"name": "承销费用", "type": "float64", "description": "-"},
        {"name": "法人获转配数量", "type": "float64", "description": "-"},
        {"name": "配股后流通股本", "type": "float64", "description": "-"},
        {"name": "股票类别", "type": "object", "description": "-"},
        {"name": "公众配售简称", "type": "object", "description": "-"},
        {"name": "发行方式编码", "type": "object", "description": "-"},
        {"name": "承销方式", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "配股上市日", "type": "object", "description": "-"},
        {"name": "配股缴款截止日", "type": "object", "description": "-"},
        {"name": "承销余额(股)", "type": "float64", "description": "-"},
        {"name": "预计配股数量", "type": "float64", "description": "-"},
        {"name": "配股后总股本", "type": "float64", "description": "-"},
        {"name": "职工股实配数量", "type": "float64", "description": "-"},
        {"name": "承销方式编码", "type": "object", "description": "-"},
        {"name": "发行费用总额", "type": "float64", "description": "-"},
        {"name": "配股前流通股本", "type": "float64", "description": "-"},
        {"name": "股票类别编码", "type": "object", "description": "-"},
        {"name": "公众配售代码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
