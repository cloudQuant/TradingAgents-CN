"""
赚钱效应分析服务

乐咕乐股网-赚钱效应分析数据
接口: stock_market_activity_legu
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_market_activity_legu_provider import StockMarketActivityLeguProvider


class StockMarketActivityLeguService(SimpleService):
    """赚钱效应分析服务"""
    
    collection_name = "stock_market_activity_legu"
    provider_class = StockMarketActivityLeguProvider
    
    # 时间字段名
    time_field = "更新时间"
