"""
赚钱效应分析数据提供者

乐咕乐股网-赚钱效应分析数据
接口: stock_market_activity_legu
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockMarketActivityLeguProvider(SimpleProvider):
    """赚钱效应分析数据提供者"""
    
    # 必填属性
    collection_name = "stock_market_activity_legu"
    display_name = "赚钱效应分析"
    akshare_func = "stock_market_activity_legu"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股网-赚钱效应分析数据"
    collection_route = "/stocks/collections/stock_market_activity_legu"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "item", "type": "object", "description": "-"},
        {"name": "value", "type": "object", "description": "-"},
        {"name": "标题", "type": "object", "description": "-"},
        {"name": "摘要", "type": "object", "description": "-"},
        {"name": "发布时间", "type": "object", "description": "-"},
        {"name": "链接", "type": "object", "description": "-"},
        {"name": "标题", "type": "object", "description": "-"},
        {"name": "摘要", "type": "object", "description": "-"},
        {"name": "发布时间", "type": "object", "description": "-"},
        {"name": "链接", "type": "object", "description": "-"},
        {"name": "时间", "type": "object", "description": "-"},
        {"name": "内容", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
