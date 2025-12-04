"""
重大合同数据提供者

东方财富网-数据中心-重大合同-重大合同明细
接口: stock_zdhtmx_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZdhtmxEmProvider(BaseProvider):
    """重大合同数据提供者"""
    
    # 必填属性
    collection_name = "stock_zdhtmx_em"
    display_name = "重大合同"
    akshare_func = "stock_zdhtmx_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-重大合同-重大合同明细"
    collection_route = "/stocks/collections/stock_zdhtmx_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "签署主体", "type": "object", "description": "-"},
        {"name": "签署主体-与上市公司关系", "type": "object", "description": "-"},
        {"name": "其他签署方", "type": "object", "description": "-"},
        {"name": "其他签署方-与上市公司关系", "type": "object", "description": "-"},
        {"name": "合同类型", "type": "object", "description": "-"},
        {"name": "合同金额", "type": "float64", "description": "-"},
        {"name": "上年度营业收入", "type": "float64", "description": "-"},
        {"name": "占上年度营业收入比例", "type": "float64", "description": "-"},
        {"name": "最新财务报表的营业收入", "type": "float64", "description": "-"},
        {"name": "签署日期", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
