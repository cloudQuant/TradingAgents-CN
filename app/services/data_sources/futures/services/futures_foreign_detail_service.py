"""外盘-合约详情服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesForeignDetailService(SimpleService):
    """外盘-合约详情服务"""
    collection_name = "futures_foreign_detail"
