"""
期货数据源模块

包含期货相关的数据提供者(Provider)和数据服务(Service)
包含52个期货数据集合的Provider和Service
"""

from .collection_metadata import FUTURES_COLLECTION_METADATA
from .provider_registry import (
    get_registered_futures_providers,
    get_provider_class,
    get_collection_definitions,
    clear_provider_registry_cache,
)
from .service_registry import (
    get_registered_futures_services,
    get_service_class,
    clear_service_registry_cache,
)

__all__ = [
    "FUTURES_COLLECTION_METADATA",
    "get_registered_futures_providers",
    "get_provider_class",
    "get_collection_definitions",
    "clear_provider_registry_cache",
    "get_registered_futures_services",
    "get_service_class",
    "clear_service_registry_cache",
]
