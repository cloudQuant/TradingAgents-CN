"""
龙虎榜详情数据提供者

东方财富网-数据中心-龙虎榜单-龙虎榜详情
接口: stock_lhb_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbDetailEmProvider(BaseProvider):
    """龙虎榜详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_detail_em"
    display_name = "龙虎榜详情"
    akshare_func = "stock_lhb_detail_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-龙虎榜详情"
    collection_route = "/stocks/collections/stock_lhb_detail_em"
    collection_category = "龙虎榜"

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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "上榜日", "type": "object", "description": "-"},
        {"name": "解读", "type": "object", "description": "-"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "龙虎榜净买额", "type": "float64", "description": "注意单位: 元"},
        {"name": "龙虎榜买入额", "type": "float64", "description": "注意单位: 元"},
        {"name": "龙虎榜卖出额", "type": "float64", "description": "注意单位: 元"},
        {"name": "龙虎榜成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "市场总成交额", "type": "int64", "description": "注意单位: 元"},
        {"name": "净买额占总成交比", "type": "float64", "description": "注意单位: %"},
        {"name": "成交额占总成交比", "type": "float64", "description": "注意单位: %"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "流通市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "上榜原因", "type": "object", "description": "-"},
        {"name": "上榜后1日", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后2日", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后5日", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后10日", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
