"""
龙虎榜-每日详情数据提供者

新浪财经-龙虎榜-每日详情
接口: stock_lhb_detail_daily_sina
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbDetailDailySinaProvider(BaseProvider):
    """龙虎榜-每日详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_detail_daily_sina"
    display_name = "龙虎榜-每日详情"
    akshare_func = "stock_lhb_detail_daily_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-龙虎榜-每日详情"
    collection_route = "/stocks/collections/stock_lhb_detail_daily_sina"
    collection_category = "龙虎榜"

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
        {"name": "收盘价", "type": "float64", "description": "注意单位: 元"},
        {"name": "对应值", "type": "float64", "description": "注意单位: %"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "指标", "type": "object", "description": "注意单位: 万元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
