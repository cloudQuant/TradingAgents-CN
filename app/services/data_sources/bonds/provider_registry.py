"""
债券数据提供者注册与发现

负责扫描 bonds/providers 目录，加载所有 Provider 类，
并为其附加必要的元信息。
"""

from functools import lru_cache
from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from app.services.data_sources.base_provider import BaseProvider
from app.services.data_sources.bonds.collection_metadata import BOND_COLLECTION_METADATA
from app.config.bond_update_config import BOND_UPDATE_CONFIGS

PROVIDERS_PACKAGE = "app.services.data_sources.bonds.providers"
PROVIDERS_PATH = Path(__file__).resolve().parent / "providers"


def _apply_metadata(provider_cls: Type[BaseProvider]):
    """将配置中的元信息应用到 Provider 类上（仅当类中未定义时）"""
    config = BOND_UPDATE_CONFIGS.get(provider_cls.collection_name, {})
    meta = BOND_COLLECTION_METADATA.get(provider_cls.collection_name, {})

    # 优先使用类中已定义的属性，否则从配置中读取
    if not hasattr(provider_cls, "display_name") or not provider_cls.display_name:
        display_name = meta.get("display_name") or config.get("display_name")
        if display_name:
            provider_cls.display_name = display_name

    if not hasattr(provider_cls, "collection_description") or not provider_cls.collection_description:
        description = meta.get("description") or config.get("update_description")
        if description:
            provider_cls.collection_description = description

    if not hasattr(provider_cls, "collection_route") or not provider_cls.collection_route:
        route = meta.get("route")
        if route:
            provider_cls.collection_route = route

    if not hasattr(provider_cls, "collection_order") or provider_cls.collection_order == 100:
        order = meta.get("order")
        if order is not None:
            provider_cls.collection_order = order


@lru_cache()
def get_registered_bond_providers() -> List[Type[BaseProvider]]:
    """获取所有 Bond Provider 类"""
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
                    and issubclass(attr, BaseProvider)
                    and attr is not BaseProvider
                    and getattr(attr, "collection_name", "")
                ):
                    _apply_metadata(attr)
                    provider_classes.append(attr)
        except Exception as e:
            # 跳过加载失败的模块（可能是旧格式的Provider）
            import logging
            logging.getLogger(__name__).warning(f"加载 Provider 模块失败: {module_info.name}, 错误: {e}")
            continue

    return provider_classes


def get_provider_class(collection_name: str) -> Optional[Type[BaseProvider]]:
    """根据集合名称获取 Provider 类"""
    for provider_cls in get_registered_bond_providers():
        if provider_cls.collection_name == collection_name:
            return provider_cls
    return None


def get_collection_definitions() -> List[Dict[str, Any]]:
    """返回所有集合的定义信息"""
    collections = []
    for provider_cls in get_registered_bond_providers():
        # 跳过标记为不可见的集合
        if not getattr(provider_cls, "collection_visible", True):
            continue

        provider = provider_cls()
        meta = provider.get_collection_meta()
        collections.append(meta)

    collections.sort(key=lambda item: (item.get("order", 100), item.get("display_name")))
    return collections
