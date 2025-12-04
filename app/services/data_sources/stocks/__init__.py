"""
股票数据集合模块

提供股票数据的Provider和Service注册与发现功能
"""

from app.services.data_sources.stocks.collection_metadata import (
    STOCK_COLLECTION_METADATA,
    get_collection_metadata,
    get_all_collection_metadata,
)
from app.services.data_sources.stocks.provider_registry import (
    get_registered_stock_providers,
    get_provider_class,
    get_collection_definitions,
    clear_provider_registry_cache,
)
from app.services.data_sources.stocks.service_registry import (
    get_registered_stock_services,
    get_service_class,
    clear_service_registry_cache,
)

__all__ = [
    # 元信息
    "STOCK_COLLECTION_METADATA",
    "get_collection_metadata",
    "get_all_collection_metadata",
    # Provider注册
    "get_registered_stock_providers",
    "get_provider_class",
    "get_collection_definitions",
    "clear_provider_registry_cache",
    # Service注册
    "get_registered_stock_services",
    "get_service_class",
    "clear_service_registry_cache",
]
