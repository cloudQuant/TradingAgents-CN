"""
基金数据服务注册与发现

负责扫描 funds/services 目录，加载所有 Service 类，
并提供按集合名称查找服务类的功能。
"""

from functools import lru_cache
from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path
from typing import Dict, List, Optional, Type

from app.services.data_sources.base_service import BaseService

SERVICES_PACKAGE = "app.services.data_sources.funds.services"
SERVICES_PATH = Path(__file__).resolve().parent / "services"


@lru_cache()
def get_registered_fund_services() -> Dict[str, Type[BaseService]]:
    """
    获取所有已注册的 Fund Service 类
    
    Returns:
        字典：{collection_name: ServiceClass}
    """
    service_classes: Dict[str, Type[BaseService]] = {}

    if not SERVICES_PATH.exists():
        return service_classes

    for module_info in iter_modules([str(SERVICES_PATH)]):
        if module_info.name.startswith("_"):
            continue

        try:
            module = import_module(f"{SERVICES_PACKAGE}.{module_info.name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseService)
                    and attr is not BaseService
                    and getattr(attr, "collection_name", "")
                ):
                    collection_name = attr.collection_name
                    service_classes[collection_name] = attr
        except Exception as e:
            # 跳过加载失败的模块，记录但不中断
            import logging
            logging.getLogger(__name__).warning(
                f"加载服务模块 {module_info.name} 失败: {e}"
            )

    return service_classes


def get_service_class(collection_name: str) -> Optional[Type[BaseService]]:
    """
    根据集合名称获取 Service 类
    
    Args:
        collection_name: 集合名称
        
    Returns:
        服务类，如果没有专门定义的服务类则返回 None
    """
    return get_registered_fund_services().get(collection_name)


def clear_service_registry_cache():
    """清除服务注册表缓存（用于热重载）"""
    get_registered_fund_services.cache_clear()
