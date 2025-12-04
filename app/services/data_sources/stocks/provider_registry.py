"""
股票数据提供者注册与发现

负责扫描 stocks/providers 目录，加载所有 Provider 类，
并为其附加必要的元信息。

支持两种Provider类型：
1. 新式Provider（继承BaseProvider/SimpleProvider）
2. 旧式Provider（独立类，不继承基类）
"""

from functools import lru_cache
from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path
from typing import Any, Dict, List, Optional, Type
import logging

from app.services.data_sources.base_provider import BaseProvider, SimpleProvider
from app.services.data_sources.stocks.collection_metadata import (
    STOCK_COLLECTION_METADATA,
    get_collection_metadata,
)
from app.config.stock_update_config import STOCK_UPDATE_CONFIGS, get_collection_update_config

logger = logging.getLogger(__name__)

PROVIDERS_PACKAGE = "app.services.data_sources.stocks.providers"
PROVIDERS_PATH = Path(__file__).resolve().parent / "providers"


def _apply_metadata(provider_cls: Type):
    """将配置中的元信息应用到 Provider 类上（仅当类中未定义时）"""
    collection_name = getattr(provider_cls, "collection_name", "")
    if not collection_name:
        return
    
    config = STOCK_UPDATE_CONFIGS.get(collection_name, {})
    meta = STOCK_COLLECTION_METADATA.get(collection_name, {})
    
    # 优先使用类中已定义的属性，否则从配置中读取
    if not getattr(provider_cls, "display_name", None):
        display_name = meta.get("display_name") or config.get("display_name")
        if display_name:
            provider_cls.display_name = display_name
    
    if not getattr(provider_cls, "collection_description", None):
        description = meta.get("description") or config.get("update_description")
        if description:
            provider_cls.collection_description = description
    
    if not getattr(provider_cls, "collection_route", None):
        route = meta.get("route")
        if route:
            provider_cls.collection_route = route
    
    if not getattr(provider_cls, "collection_order", None) or getattr(provider_cls, "collection_order", 100) == 100:
        order = meta.get("order")
        if order is not None:
            provider_cls.collection_order = order


def _is_valid_provider(attr) -> bool:
    """判断是否是有效的Provider类"""
    if not isinstance(attr, type):
        return False
    
    # 新式Provider：继承BaseProvider或SimpleProvider
    if issubclass(attr, (BaseProvider, SimpleProvider)) and attr not in (BaseProvider, SimpleProvider):
        return bool(getattr(attr, "collection_name", ""))
    
    # 旧式Provider：类名以Provider结尾，有collection_name属性
    if attr.__name__.endswith("Provider") and attr.__name__ not in ("BaseProvider", "SimpleProvider"):
        return bool(getattr(attr, "collection_name", None) or hasattr(attr, "fetch_data"))
    
    return False


@lru_cache()
def get_registered_stock_providers() -> List[Type]:
    """获取所有 Stock Provider 类"""
    provider_classes: List[Type] = []
    seen_collections = set()
    
    if not PROVIDERS_PATH.exists():
        logger.warning(f"Provider目录不存在: {PROVIDERS_PATH}")
        return provider_classes
    
    for module_info in iter_modules([str(PROVIDERS_PATH)]):
        if module_info.name.startswith("_"):
            continue
        
        try:
            module = import_module(f"{PROVIDERS_PACKAGE}.{module_info.name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if _is_valid_provider(attr):
                    collection_name = getattr(attr, "collection_name", "")
                    
                    # 如果没有collection_name，尝试从文件名推断
                    if not collection_name:
                        # stock_zh_a_spot_em_provider.py -> stock_zh_a_spot_em
                        collection_name = module_info.name.replace("_provider", "")
                        attr.collection_name = collection_name
                    
                    # 避免重复注册
                    if collection_name in seen_collections:
                        continue
                    
                    seen_collections.add(collection_name)
                    _apply_metadata(attr)
                    provider_classes.append(attr)
        except Exception as e:
            logger.debug(f"加载Provider模块 {module_info.name} 失败: {e}")
    
    logger.info(f"已注册 {len(provider_classes)} 个股票数据Provider")
    return provider_classes


def get_provider_class(collection_name: str) -> Optional[Type]:
    """根据集合名称获取 Provider 类"""
    for provider_cls in get_registered_stock_providers():
        if getattr(provider_cls, "collection_name", "") == collection_name:
            return provider_cls
    return None


def get_collection_definitions() -> List[Dict[str, Any]]:
    """返回所有集合的定义信息"""
    collections = []
    
    for provider_cls in get_registered_stock_providers():
        # 跳过标记为不可见的集合
        if not getattr(provider_cls, "collection_visible", True):
            continue
        
        collection_name = getattr(provider_cls, "collection_name", "")
        meta = get_collection_metadata(collection_name)
        
        # 获取字段信息
        field_info = []
        if hasattr(provider_cls, "get_field_info"):
            try:
                provider = provider_cls()
                field_info = provider.get_field_info()
            except:
                pass
        elif hasattr(provider_cls, "field_info"):
            field_info = getattr(provider_cls, "field_info", [])
        
        collections.append({
            "name": collection_name,
            "display_name": getattr(provider_cls, "display_name", meta.get("display_name", collection_name)),
            "description": getattr(provider_cls, "collection_description", meta.get("description", "")),
            "route": getattr(provider_cls, "collection_route", meta.get("route", f"/stocks/collections/{collection_name}")),
            "order": getattr(provider_cls, "collection_order", meta.get("order", 100)),
            "fields": [f.get("name", "") for f in field_info] if field_info else [],
        })
    
    collections.sort(key=lambda item: (item.get("order", 100), item.get("display_name", "")))
    return collections


def clear_provider_registry_cache():
    """清除Provider注册表缓存（用于热重载）"""
    get_registered_stock_providers.cache_clear()
