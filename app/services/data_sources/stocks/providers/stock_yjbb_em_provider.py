"""
业绩报表数据提供者

东方财富-数据中心-年报季报-业绩报表
接口: stock_yjbb_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockYjbbEmProvider(BaseProvider):
    """业绩报表数据提供者"""
    
    # 必填属性
    collection_name = "stock_yjbb_em"
    display_name = "业绩报表"
    akshare_func = "stock_yjbb_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-年报季报-业绩报表"
    collection_route = "/stocks/collections/stock_yjbb_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "每股收益", "type": "float64", "description": "注意单位: 元"},
        {"name": "营业总收入-营业总收入", "type": "float64", "description": "注意单位: 元"},
        {"name": "营业总收入-同比增长", "type": "float64", "description": "注意单位: %"},
        {"name": "营业总收入-季度环比增长", "type": "float64", "description": "注意单位: %"},
        {"name": "净利润-净利润", "type": "float64", "description": "注意单位: 元"},
        {"name": "净利润-同比增长", "type": "float64", "description": "注意单位: %"},
        {"name": "净利润-季度环比增长", "type": "float64", "description": "注意单位: %"},
        {"name": "每股净资产", "type": "float64", "description": "注意单位: 元"},
        {"name": "净资产收益率", "type": "float64", "description": "注意单位: %"},
        {"name": "每股经营现金流量", "type": "float64", "description": "注意单位: 元"},
        {"name": "销售毛利率", "type": "float64", "description": "注意单位: %"},
        {"name": "所处行业", "type": "object", "description": "-"},
        {"name": "最新公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
