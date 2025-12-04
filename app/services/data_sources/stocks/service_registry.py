"""
股票数据服务注册与发现

负责扫描 stocks/services 目录，加载所有 Service 类，
并提供按集合名称查找服务类的功能。

支持两种Service类型：
1. 新式Service（继承BaseService/SimpleService）
2. 旧式Service（独立类，不继承基类）
"""

from functools import lru_cache
from importlib import import_module
from pkgutil import iter_modules
from pathlib import Path
from typing import Dict, List, Optional, Type
import logging

from app.services.data_sources.base_service import BaseService, SimpleService

logger = logging.getLogger(__name__)

SERVICES_PACKAGE = "app.services.data_sources.stocks.services"
SERVICES_PATH = Path(__file__).resolve().parent / "services"


def _is_valid_service(attr) -> bool:
    """判断是否是有效的Service类"""
    if not isinstance(attr, type):
        return False
    
    # 新式Service：继承BaseService或SimpleService
    if issubclass(attr, (BaseService, SimpleService)) and attr not in (BaseService, SimpleService):
        return bool(getattr(attr, "collection_name", ""))
    
    # 旧式Service：类名以Service结尾
    if attr.__name__.endswith("Service") and attr.__name__ not in ("BaseService", "SimpleService"):
        return bool(getattr(attr, "collection_name", None) or hasattr(attr, "get_data"))
    
    return False


@lru_cache()
def get_registered_stock_services() -> Dict[str, Type]:
    """
    获取所有已注册的 Stock Service 类
    
    Returns:
        字典：{collection_name: ServiceClass}
    """
    service_classes: Dict[str, Type] = {}
    
    if not SERVICES_PATH.exists():
        logger.warning(f"Service目录不存在: {SERVICES_PATH}")
        return service_classes
    
    for module_info in iter_modules([str(SERVICES_PATH)]):
        if module_info.name.startswith("_"):
            continue
        
        try:
            module = import_module(f"{SERVICES_PACKAGE}.{module_info.name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if _is_valid_service(attr):
                    collection_name = getattr(attr, "collection_name", "")
                    
                    # 如果没有collection_name，尝试从文件名推断
                    if not collection_name:
                        # stock_zh_a_spot_em_service.py -> stock_zh_a_spot_em
                        collection_name = module_info.name.replace("_service", "")
                        attr.collection_name = collection_name
                    
                    if collection_name and collection_name not in service_classes:
                        service_classes[collection_name] = attr
        except Exception as e:
            # 跳过加载失败的模块，记录但不中断
            logger.debug(f"加载Service模块 {module_info.name} 失败: {e}")
    
    logger.info(f"已注册 {len(service_classes)} 个股票数据Service")
    return service_classes


def get_service_class(collection_name: str) -> Optional[Type]:
    """
    根据集合名称获取 Service 类
    
    Args:
        collection_name: 集合名称
        
    Returns:
        服务类，如果没有专门定义的服务类则返回 None
    """
    return get_registered_stock_services().get(collection_name)


def clear_service_registry_cache():
    """清除服务注册表缓存（用于热重载）"""
    get_registered_stock_services.cache_clear()
