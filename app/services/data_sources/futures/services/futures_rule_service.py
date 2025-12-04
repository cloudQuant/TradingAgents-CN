"""期货规则-交易日历表数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesRuleService(SimpleService):
    """期货规则-交易日历表数据服务"""
    collection_name = "futures_rule"
