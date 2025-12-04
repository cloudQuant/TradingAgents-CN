"""
申万个股行业分类变动历史数据提供者

申万宏源研究-行业分类-全部行业分类
接口: stock_industry_clf_hist_sw
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockIndustryClfHistSwProvider(SimpleProvider):
    """申万个股行业分类变动历史数据提供者"""
    
    # 必填属性
    collection_name = "stock_industry_clf_hist_sw"
    display_name = "申万个股行业分类变动历史"
    akshare_func = "stock_industry_clf_hist_sw"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "申万宏源研究-行业分类-全部行业分类"
    collection_route = "/stocks/collections/stock_industry_clf_hist_sw"
    collection_category = "历史行情"

    # 字段信息
    field_info = [
        {"name": "symbol", "type": "object", "description": "股票代码"},
        {"name": "start_date", "type": "object", "description": "计入日期"},
        {"name": "industry_code", "type": "object", "description": "申万行业代码"},
        {"name": "update_time", "type": "object", "description": "更新日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
