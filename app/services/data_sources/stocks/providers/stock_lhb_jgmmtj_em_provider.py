"""
机构买卖每日统计数据提供者

东方财富网-数据中心-龙虎榜单-机构买卖每日统计
接口: stock_lhb_jgmmtj_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbJgmmtjEmProvider(BaseProvider):
    """机构买卖每日统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_jgmmtj_em"
    display_name = "机构买卖每日统计"
    akshare_func = "stock_lhb_jgmmtj_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-机构买卖每日统计"
    collection_route = "/stocks/collections/stock_lhb_jgmmtj_em"
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
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "买方机构数", "type": "float64", "description": "-"},
        {"name": "卖方机构数", "type": "float64", "description": "-"},
        {"name": "机构买入总额", "type": "float64", "description": "注意单位: 元"},
        {"name": "机构卖出总额", "type": "float64", "description": "注意单位: 元"},
        {"name": "机构买入净额", "type": "float64", "description": "注意单位: 元"},
        {"name": "市场总成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "机构净买额占总成交额比", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "-"},
        {"name": "流通市值", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "上榜原因", "type": "object", "description": "-"},
        {"name": "上榜日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
