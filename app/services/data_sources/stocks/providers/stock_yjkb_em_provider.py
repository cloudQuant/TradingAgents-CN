"""
业绩快报数据提供者

东方财富-数据中心-年报季报-业绩快报
接口: stock_yjkb_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockYjkbEmProvider(BaseProvider):
    """业绩快报数据提供者"""
    
    # 必填属性
    collection_name = "stock_yjkb_em"
    display_name = "业绩快报"
    akshare_func = "stock_yjkb_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-年报季报-业绩快报"
    collection_route = "/stocks/collections/stock_yjkb_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "每股收益", "type": "object", "description": "-"},
        {"name": "营业收入-营业收入", "type": "object", "description": "-"},
        {"name": "营业收入-去年同期", "type": "object", "description": "-"},
        {"name": "营业收入-同比增长", "type": "str", "description": "-"},
        {"name": "营业收入-季度环比增长", "type": "object", "description": "-"},
        {"name": "净利润-净利润", "type": "object", "description": "-"},
        {"name": "净利润-去年同期", "type": "object", "description": "-"},
        {"name": "净利润-同比增长", "type": "str", "description": "-"},
        {"name": "净利润-季度环比增长", "type": "object", "description": "-"},
        {"name": "每股净资产", "type": "object", "description": "-"},
        {"name": "净资产收益率", "type": "object", "description": "-"},
        {"name": "所处行业", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "市场板块", "type": "object", "description": "-"},
        {"name": "证券类型", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
