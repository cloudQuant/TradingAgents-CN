"""
机构排行数据提供者

东方财富网-数据中心-沪深港通-沪深港通持股-机构排行
接口: stock_hsgt_institution_statistics_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtInstitutionStatisticsEmProvider(BaseProvider):
    """机构排行数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_institution_statistics_em"
    display_name = "机构排行"
    akshare_func = "stock_hsgt_institution_statistics_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-沪深港通-沪深港通持股-机构排行"
    collection_route = "/stocks/collections/stock_hsgt_institution_statistics_em"
    collection_category = "沪深港通"

    # 参数映射
    param_mapping = {
        "market": "market",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['market', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "持股日期", "type": "object", "description": "-"},
        {"name": "持股只数", "type": "float64", "description": "注意单位: 只"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 元; 南向持股单位为: 港元"},
        {"name": "持股市值变化-1日", "type": "float64", "description": "注意单位: 元; 南向持股单位为: 港元"},
        {"name": "持股市值变化-5日", "type": "float64", "description": "注意单位: 元; 南向持股单位为: 港元"},
        {"name": "持股市值变化-10日", "type": "float64", "description": "注意单位: 元; 南向持股单位为: 港元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
