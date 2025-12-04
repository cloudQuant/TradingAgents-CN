"""
期权数据Service注册表
动态发现和注册所有期权数据Service
"""
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, Type

from app.services.data_sources.base_service import BaseService, SimpleService

# Service模块路径
SERVICES_PATH = Path(__file__).parent / "services"
SERVICES_PACKAGE = "app.services.data_sources.options.services"


@lru_cache()
def get_registered_option_services() -> Dict[str, Type[BaseService]]:
    """
    获取所有已注册的期权数据Service
    自动扫描services目录下的所有Service类
    返回: {collection_name: ServiceClass}
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
                    and (issubclass(attr, BaseService) or issubclass(attr, SimpleService))
                    and attr is not BaseService
                    and attr is not SimpleService
                    and getattr(attr, "collection_name", "")
                ):
                    collection_name = attr.collection_name
                    service_classes[collection_name] = attr
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(
                f"加载Service模块 {module_info.name} 失败: {e}"
            )
    
    return service_classes


def get_option_service_by_name(collection_name: str) -> Type[BaseService] | None:
    """根据集合名称获取Service类"""
    services = get_registered_option_services()
    return services.get(collection_name)
