"""
债券数据服务注册与发现

负责扫描 bonds/services 目录，加载所有 Service 类
"""

from functools import lru_cache
from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from app.services.data_sources.base_service import BaseService

SERVICES_PACKAGE = "app.services.data_sources.bonds.services"
SERVICES_PATH = Path(__file__).resolve().parent / "services"


@lru_cache()
def get_registered_bond_services() -> List[Type[BaseService]]:
    """获取所有 Bond Service 类"""
    service_classes: List[Type[BaseService]] = []

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
                    service_classes.append(attr)
        except Exception as e:
            # 跳过加载失败的模块（可能是旧格式的Service）
            import logging
            logging.getLogger(__name__).warning(f"加载 Service 模块失败: {module_info.name}, 错误: {e}")
            continue

    return service_classes


def get_service_class(collection_name: str) -> Optional[Type[BaseService]]:
    """根据集合名称获取 Service 类"""
    for service_cls in get_registered_bond_services():
        if service_cls.collection_name == collection_name:
            return service_cls
    return None


def get_all_service_classes() -> Dict[str, Type[BaseService]]:
    """获取所有 Service 类的字典（collection_name -> Service类）"""
    return {
        service_cls.collection_name: service_cls
        for service_cls in get_registered_bond_services()
    }
