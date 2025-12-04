"""
板块排行数据提供者

东方财富网-数据中心-沪深港通持股-板块排行
接口: stock_hsgt_board_rank_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHsgtBoardRankEmProvider(BaseProvider):
    """板块排行数据提供者"""
    
    # 必填属性
    collection_name = "stock_hsgt_board_rank_em"
    display_name = "板块排行"
    akshare_func = "stock_hsgt_board_rank_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-沪深港通持股-板块排行"
    collection_route = "/stocks/collections/stock_hsgt_board_rank_em"
    collection_category = "板块数据"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "最新涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "北向资金今日持股-股票只数", "type": "float64", "description": "-"},
        {"name": "北向资金今日持股-市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "北向资金今日持股-占板块比", "type": "float64", "description": "-"},
        {"name": "北向资金今日持股-占北向资金比", "type": "float64", "description": "-"},
        {"name": "北向资金今日增持估计-股票只数", "type": "float64", "description": "-"},
        {"name": "北向资金今日增持估计-市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "北向资金今日增持估计-市值增幅", "type": "float64", "description": "-"},
        {"name": "北向资金今日增持估计-占板块比", "type": "float64", "description": "-"},
        {"name": "北向资金今日增持估计-占北向资金比", "type": "float64", "description": "-"},
        {"name": "今日增持最大股-市值", "type": "float64", "description": "-"},
        {"name": "今日增持最大股-占股本比", "type": "float64", "description": "-"},
        {"name": "今日减持最大股-占股本比", "type": "float64", "description": "-"},
        {"name": "今日减持最大股-市值", "type": "float64", "description": "-"},
        {"name": "报告时间", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
