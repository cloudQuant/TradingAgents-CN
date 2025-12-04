"""
分析师指数排行数据提供者

东方财富网-数据中心-研究报告-东方财富分析师指数
接口: stock_analyst_rank_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockAnalystRankEmProvider(BaseProvider):
    """分析师指数排行数据提供者"""
    
    # 必填属性
    collection_name = "stock_analyst_rank_em"
    display_name = "分析师指数排行"
    akshare_func = "stock_analyst_rank_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-研究报告-东方财富分析师指数"
    collection_route = "/stocks/collections/stock_analyst_rank_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "year": "year"
    }
    
    # 必填参数
    required_params = ['year']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "分析师单位", "type": "object", "description": "-"},
        {"name": "年度指数", "type": "float64", "description": "-"},
        {"name": "xxxx年收益率", "type": "float64", "description": "其中 xxxx 表示指定的年份; 注意单位: %"},
        {"name": "3个月收益率", "type": "float64", "description": "注意单位: %"},
        {"name": "6个月收益率", "type": "float64", "description": "注意单位: %"},
        {"name": "12个月收益率", "type": "float64", "description": "注意单位: %"},
        {"name": "成分股个数", "type": "int64", "description": "-"},
        {"name": "xxxx最新个股评级-股票代码", "type": "object", "description": "其中 xxxx 表示指定的年份"},
        {"name": "分析师ID", "type": "object", "description": "-"},
        {"name": "行业代码", "type": "object", "description": "-"},
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "更新日期", "type": "object", "description": "数据更新日期"},
        {"name": "年度", "type": "object", "description": "数据更新年度"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
