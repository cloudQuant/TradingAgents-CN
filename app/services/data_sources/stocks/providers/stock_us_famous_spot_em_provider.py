"""
知名美股数据提供者

美股-知名美股的实时行情数据
接口: stock_us_famous_spot_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockUsFamousSpotEmProvider(BaseProvider):
    """知名美股数据提供者"""
    
    # 必填属性
    collection_name = "stock_us_famous_spot_em"
    display_name = "知名美股"
    akshare_func = "stock_us_famous_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "美股-知名美股的实时行情数据"
    collection_route = "/stocks/collections/stock_us_famous_spot_em"
    collection_category = "实时行情"

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 美元"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "开盘价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最高价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最低价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "昨收价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "总市值", "type": "float64", "description": "注意单位: 美元"},
        {"name": "市盈率", "type": "float64", "description": "-"},
        {"name": "代码", "type": "object", "description": "注意: 用来获取历史数据的代码"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
