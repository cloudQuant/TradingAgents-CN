"""
股东持股明细-十大流通股东数据提供者

东方财富网-数据中心-股东分析-股东持股明细-十大流通股东
接口: stock_gdfx_free_holding_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGdfxFreeHoldingDetailEmProvider(BaseProvider):
    """股东持股明细-十大流通股东数据提供者"""
    
    # 必填属性
    collection_name = "stock_gdfx_free_holding_detail_em"
    display_name = "股东持股明细-十大流通股东"
    akshare_func = "stock_gdfx_free_holding_detail_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股东分析-股东持股明细-十大流通股东"
    collection_route = "/stocks/collections/stock_gdfx_free_holding_detail_em"
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
        {"name": "股东类型", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "报告期", "type": "object", "description": "-"},
        {"name": "期末持股-数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "期末持股-数量变化", "type": "float64", "description": "注意单位: 股"},
        {"name": "期末持股-数量变化比例", "type": "float64", "description": "注意单位: %"},
        {"name": "期末持股-持股变动", "type": "float64", "description": "-"},
        {"name": "期末持股-流通市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "公告日", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
