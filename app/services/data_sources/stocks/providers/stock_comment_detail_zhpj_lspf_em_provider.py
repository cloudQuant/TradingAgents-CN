"""
历史评分数据提供者

东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分
接口: stock_comment_detail_zhpj_lspf_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCommentDetailZhpjLspfEmProvider(BaseProvider):
    """历史评分数据提供者"""
    
    # 必填属性
    collection_name = "stock_comment_detail_zhpj_lspf_em"
    display_name = "历史评分"
    akshare_func = "stock_comment_detail_zhpj_lspf_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分"
    collection_route = "/stocks/collections/stock_comment_detail_zhpj_lspf_em"
    collection_category = "历史行情"

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
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "评分", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
