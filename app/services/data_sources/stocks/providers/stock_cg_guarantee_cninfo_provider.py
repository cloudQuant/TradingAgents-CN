"""
对外担保数据提供者

巨潮资讯-数据中心-专题统计-公司治理-对外担保
接口: stock_cg_guarantee_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCgGuaranteeCninfoProvider(BaseProvider):
    """对外担保数据提供者"""
    
    # 必填属性
    collection_name = "stock_cg_guarantee_cninfo"
    display_name = "对外担保"
    akshare_func = "stock_cg_guarantee_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-专题统计-公司治理-对外担保"
    collection_route = "/stocks/collections/stock_cg_guarantee_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "证劵代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "公告统计区间", "type": "object", "description": "-"},
        {"name": "担保笔数", "type": "int64", "description": "-"},
        {"name": "担保金额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "归属于母公司所有者权益", "type": "float64", "description": "注意单位: 万元"},
        {"name": "担保金融占净资产比例", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
