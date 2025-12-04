"""
A 股等权重与中位数市净率数据提供者

乐咕乐股-A 股等权重与中位数市净率
接口: stock_a_all_pb
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockAAllPbProvider(SimpleProvider):
    """A 股等权重与中位数市净率数据提供者"""
    
    # 必填属性
    collection_name = "stock_a_all_pb"
    display_name = "A 股等权重与中位数市净率"
    akshare_func = "stock_a_all_pb"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-A 股等权重与中位数市净率"
    collection_route = "/stocks/collections/stock_a_all_pb"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "middlePB", "type": "float64", "description": "全部A股市净率中位数"},
        {"name": "equalWeightAveragePB", "type": "float64", "description": "全部A股市净率等权平均"},
        {"name": "close", "type": "float64", "description": "上证指数"},
        {"name": "quantileInAllHistoryMiddlePB", "type": "float64", "description": "当前市净率中位数在历史数据上的分位数"},
        {"name": "quantileInRecent10YearsMiddlePB", "type": "float64", "description": "当前市净率中位数在最近10年数据上的分位数"},
        {"name": "quantileInAllHistoryEqualWeightAveragePB", "type": "float64", "description": "当前市净率等权平均在历史数据上的分位数"},
        {"name": "quantileInRecent10YearsEqualWeightAveragePB", "type": "float64", "description": "当前市净率等权平均在最近10年数据上的分位数"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
