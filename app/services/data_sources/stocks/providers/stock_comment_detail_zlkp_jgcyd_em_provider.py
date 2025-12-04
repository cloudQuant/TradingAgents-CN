"""
机构参与度数据提供者

东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度
接口: stock_comment_detail_zlkp_jgcyd_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCommentDetailZlkpJgcydEmProvider(BaseProvider):
    """机构参与度数据提供者"""
    
    # 必填属性
    collection_name = "stock_comment_detail_zlkp_jgcyd_em"
    display_name = "机构参与度"
    akshare_func = "stock_comment_detail_zlkp_jgcyd_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度"
    collection_route = "/stocks/collections/stock_comment_detail_zlkp_jgcyd_em"
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
        {"name": "交易日", "type": "object", "description": "-"},
        {"name": "机构参与度", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
