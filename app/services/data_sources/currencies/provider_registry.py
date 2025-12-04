"""
货币数据Provider注册表
动态发现和注册所有货币数据Provider
"""
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, List, Type, Any

from app.services.data_sources.base_provider import BaseProvider, SimpleProvider
from app.services.data_sources.currencies.collection_metadata import CURRENCY_COLLECTION_METADATA

# Provider模块路径
PROVIDERS_PATH = Path(__file__).parent / "providers"
PROVIDERS_PACKAGE = "app.services.data_sources.currencies.providers"


def _apply_metadata(provider_class: Type[BaseProvider]) -> None:
    """应用元信息配置到Provider类"""
    collection_name = getattr(provider_class, "collection_name", "")
    if collection_name in CURRENCY_COLLECTION_METADATA:
        meta = CURRENCY_COLLECTION_METADATA[collection_name]
        # 如果Provider没有设置这些属性，则使用元信息配置
        if not getattr(provider_class, "collection_description", ""):
            provider_class.collection_description = meta.get("description", "")
        if not getattr(provider_class, "collection_route", ""):
            provider_class.collection_route = meta.get("route", "")
        if not getattr(provider_class, "collection_order", 0):
            provider_class.collection_order = meta.get("order", 0)


@lru_cache()
def get_registered_currency_providers() -> List[Type[BaseProvider]]:
    """
    获取所有已注册的货币数据Provider
    自动扫描providers目录下的所有Provider类
    """
    provider_classes: List[Type[BaseProvider]] = []
    
    if not PROVIDERS_PATH.exists():
        return provider_classes
    
    for module_info in iter_modules([str(PROVIDERS_PATH)]):
        if module_info.name.startswith("_"):
            continue
        
        try:
            module = import_module(f"{PROVIDERS_PACKAGE}.{module_info.name}")
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and (issubclass(attr, BaseProvider) or issubclass(attr, SimpleProvider))
                    and attr is not BaseProvider
                    and attr is not SimpleProvider
                    and getattr(attr, "collection_name", "")
                ):
                    _apply_metadata(attr)
                    provider_classes.append(attr)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(
                f"加载Provider模块 {module_info.name} 失败: {e}"
            )
    
    return provider_classes


def get_currency_provider_by_name(collection_name: str) -> Type[BaseProvider] | None:
    """根据集合名称获取Provider类"""
    for provider_class in get_registered_currency_providers():
        if provider_class.collection_name == collection_name:
            return provider_class
    return None


def get_currency_collection_definitions() -> List[Dict[str, Any]]:
    """获取所有货币集合的定义信息"""
    definitions = []
    
    for provider_class in get_registered_currency_providers():
        collection_name = provider_class.collection_name
        meta = CURRENCY_COLLECTION_METADATA.get(collection_name, {})
        
        definitions.append({
            "name": collection_name,
            "display_name": getattr(provider_class, "display_name", "") or meta.get("display_name", collection_name),
            "description": getattr(provider_class, "collection_description", "") or meta.get("description", ""),
            "route": getattr(provider_class, "collection_route", "") or meta.get("route", ""),
            "order": getattr(provider_class, "collection_order", 0) or meta.get("order", 0),
            "field_info": getattr(provider_class, "field_info", []),
            "unique_keys": getattr(provider_class, "unique_keys", []),
            "required_params": getattr(provider_class, "required_params", []),
        })
    
    # 按order排序
    definitions.sort(key=lambda x: x.get("order", 0))
    
    return definitions
