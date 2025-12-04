"""
质押机构分布统计-银行数据提供者

东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行
接口: stock_gpzy_distribute_statistics_bank_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockGpzyDistributeStatisticsBankEmProvider(SimpleProvider):
    """质押机构分布统计-银行数据提供者"""
    
    # 必填属性
    collection_name = "stock_gpzy_distribute_statistics_bank_em"
    display_name = "质押机构分布统计-银行"
    akshare_func = "stock_gpzy_distribute_statistics_bank_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股权质押-质押机构分布统计-银行"
    collection_route = "/stocks/collections/stock_gpzy_distribute_statistics_bank_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "质押机构", "type": "object", "description": "-"},
        {"name": "质押公司数量", "type": "int64", "description": "-"},
        {"name": "质押笔数", "type": "int64", "description": "-"},
        {"name": "质押数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "未达预警线比例", "type": "float64", "description": "注意单位: %"},
        {"name": "达到预警线未达平仓线比例", "type": "float64", "description": "注意单位: %"},
        {"name": "达到平仓线比例", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
