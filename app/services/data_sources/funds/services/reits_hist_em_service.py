"""
REITs历史行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.reits_hist_em_provider import ReitsHistEmProvider


class ReitsHistEmService(SimpleService):
    """REITs历史行情-东财服务"""
    
    collection_name = "reits_hist_em"
    provider_class = ReitsHistEmProvider
