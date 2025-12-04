"""
货币数据源模块
提供货币数据的Provider和Service注册、发现功能
"""
from app.services.data_sources.currencies.collection_metadata import CURRENCY_COLLECTION_METADATA
from app.services.data_sources.currencies.provider_registry import (
    get_registered_currency_providers,
    get_currency_provider_by_name,
    get_currency_collection_definitions,
)
from app.services.data_sources.currencies.service_registry import (
    get_registered_currency_services,
    get_currency_service_by_name,
)

__all__ = [
    "CURRENCY_COLLECTION_METADATA",
    "get_registered_currency_providers",
    "get_currency_provider_by_name",
    "get_currency_collection_definitions",
    "get_registered_currency_services",
    "get_currency_service_by_name",
]
