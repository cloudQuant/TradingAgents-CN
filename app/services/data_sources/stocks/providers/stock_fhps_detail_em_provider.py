"""
分红配送详情-东财数据提供者

东方财富网-数据中心-分红送配-分红送配详情
接口: stock_fhps_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFhpsDetailEmProvider(BaseProvider):
    """分红配送详情-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_fhps_detail_em"
    display_name = "分红配送详情-东财"
    akshare_func = "stock_fhps_detail_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-分红送配-分红送配详情"
    collection_route = "/stocks/collections/stock_fhps_detail_em"
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
        {"name": "报告期", "type": "object", "description": "-"},
        {"name": "业绩披露日期", "type": "object", "description": "-"},
        {"name": "送转股份-送转总比例", "type": "float64", "description": "-"},
        {"name": "送转股份-送股比例", "type": "float64", "description": "-"},
        {"name": "送转股份-转股比例", "type": "float64", "description": "-"},
        {"name": "现金分红-现金分红比例", "type": "float64", "description": "-"},
        {"name": "现金分红-现金分红比例描述", "type": "object", "description": "-"},
        {"name": "现金分红-股息率", "type": "float64", "description": "-"},
        {"name": "每股收益", "type": "float64", "description": "-"},
        {"name": "每股净资产", "type": "float64", "description": "-"},
        {"name": "每股公积金", "type": "float64", "description": "-"},
        {"name": "每股未分配利润", "type": "float64", "description": "-"},
        {"name": "净利润同比增长", "type": "float64", "description": "-"},
        {"name": "总股本", "type": "int64", "description": "-"},
        {"name": "预案公告日", "type": "object", "description": "-"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "除权除息日", "type": "object", "description": "-"},
        {"name": "方案进度", "type": "object", "description": "-"},
        {"name": "最新公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
