"""
REITs实时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.reits_realtime_em_provider import ReitsRealtimeEmProvider


class ReitsRealtimeEmService(SimpleService):
    """REITs实时行情-东财服务"""
    
    collection_name = "reits_realtime_em"
    provider_class = ReitsRealtimeEmProvider
