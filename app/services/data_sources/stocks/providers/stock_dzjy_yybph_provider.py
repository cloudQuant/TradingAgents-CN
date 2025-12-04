"""
营业部排行数据提供者

东方财富网-数据中心-大宗交易-营业部排行
接口: stock_dzjy_yybph
"""
from app.services.data_sources.base_provider import BaseProvider


class StockDzjyYybphProvider(BaseProvider):
    """营业部排行数据提供者"""
    
    # 必填属性
    collection_name = "stock_dzjy_yybph"
    display_name = "营业部排行"
    akshare_func = "stock_dzjy_yybph"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-大宗交易-营业部排行"
    collection_route = "/stocks/collections/stock_dzjy_yybph"
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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "上榜后1天-买入次数", "type": "float64", "description": "-"},
        {"name": "上榜后1天-平均涨幅", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后1天-上涨概率", "type": "float64", "description": "-"},
        {"name": "上榜后5天-买入次数", "type": "float64", "description": "-"},
        {"name": "上榜后5天-平均涨幅", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后5天-上涨概率", "type": "float64", "description": "-"},
        {"name": "上榜后10天-买入次数", "type": "float64", "description": "-"},
        {"name": "上榜后10天-平均涨幅", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后10天-上涨概率", "type": "float64", "description": "-"},
        {"name": "上榜后20天-买入次数", "type": "float64", "description": "-"},
        {"name": "上榜后20天-平均涨幅", "type": "float64", "description": "注意单位: %"},
        {"name": "上榜后20天-上涨概率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
