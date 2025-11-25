"""
股票数据服务工厂
动态加载 data_sources/stocks/services 目录中的所有服务类
支持约 290 个股票数据集合
"""
import logging
import importlib
import os
from typing import Dict, Any, List, Type, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config.stock_update_config import get_collection_update_config

logger = logging.getLogger(__name__)


def _snake_to_pascal(name: str) -> str:
    """将下划线命名转换为帕斯卡命名（大驼峰）"""
    return ''.join(word.capitalize() for word in name.split('_'))


def _load_service_classes() -> Dict[str, Type]:
    """
    动态加载所有股票数据服务类
    
    Returns:
        集合名称到服务类的映射
    """
    service_classes = {}
    
    # 获取当前文件目录，然后定位到 services 子目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    services_dir = os.path.join(current_dir, 'services')
    
    if not os.path.exists(services_dir):
        logger.warning(f"服务目录不存在: {services_dir}")
        return service_classes
    
    for filename in os.listdir(services_dir):
        if not filename.endswith('_service.py'):
            continue
        if filename.startswith('__') or filename == 'base_service.py':
            continue
        
        # 提取集合名称：stock_zh_a_spot_em_service.py -> stock_zh_a_spot_em
        collection_name = filename[:-11]  # 移除 _service.py
        
        # 构建类名：stock_zh_a_spot_em -> StockZhASpotEmService
        class_name = _snake_to_pascal(collection_name) + 'Service'
        
        # 动态导入模块
        module_name = f"app.services.data_sources.stocks.services.{filename[:-3]}"
        try:
            module = importlib.import_module(module_name)
            service_class = getattr(module, class_name, None)
            if service_class:
                service_classes[collection_name] = service_class
        except Exception as e:
            logger.debug(f"加载服务 {collection_name} 失败: {e}")
    
    logger.info(f"已加载 {len(service_classes)} 个股票数据服务")
    return service_classes


# 服务类缓存
_SERVICE_CLASSES: Dict[str, Type] = {}


def _ensure_service_classes():
    """确保服务类已加载"""
    global _SERVICE_CLASSES
    if not _SERVICE_CLASSES:
        _SERVICE_CLASSES = _load_service_classes()


class StockServiceFactory:
    """
    股票数据服务工厂
    根据集合名称动态获取对应的 Service 实例
    """
    
    # 服务实例缓存（按 db 实例分组）
    _instance_cache: Dict[int, Dict[str, Any]] = {}
    
    @classmethod
    def get_service(cls, collection_name: str, db: AsyncIOMotorDatabase):
        """
        获取指定集合的服务实例
        
        Args:
            collection_name: 集合名称
            db: 数据库连接
            
        Returns:
            服务实例，如果不存在则返回 None
        """
        _ensure_service_classes()
        
        # 使用 db 的 id 作为缓存键
        db_id = id(db)
        if db_id not in cls._instance_cache:
            cls._instance_cache[db_id] = {}
        
        cache = cls._instance_cache[db_id]
        
        if collection_name not in cache:
            service_class = _SERVICE_CLASSES.get(collection_name)
            if service_class:
                cache[collection_name] = service_class(db)
            else:
                return None
        
        return cache[collection_name]
    
    @classmethod
    def get_all_services(cls, db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        获取所有集合的服务实例
        
        Args:
            db: 数据库连接
            
        Returns:
            集合名称到服务实例的映射
        """
        _ensure_service_classes()
        
        services = {}
        for collection_name in _SERVICE_CLASSES.keys():
            service = cls.get_service(collection_name, db)
            if service:
                services[collection_name] = service
        
        return services
    
    @classmethod
    def get_supported_collections(cls) -> List[str]:
        """
        获取支持的所有集合名称
        
        Returns:
            集合名称列表
        """
        _ensure_service_classes()
        return list(_SERVICE_CLASSES.keys())
    
    @classmethod
    def get_collection_count(cls) -> int:
        """
        获取支持的数据集合数量
        
        Returns:
            集合数量
        """
        _ensure_service_classes()
        return len(_SERVICE_CLASSES)
    
    @classmethod
    def has_service(cls, collection_name: str) -> bool:
        """
        检查是否存在指定集合的服务
        
        Args:
            collection_name: 集合名称
            
        Returns:
            是否存在
        """
        _ensure_service_classes()
        return collection_name in _SERVICE_CLASSES


# 导出便捷函数
def get_stock_service(collection_name: str, db: AsyncIOMotorDatabase):
    """获取股票数据服务"""
    return StockServiceFactory.get_service(collection_name, db)


def get_all_stock_services(db: AsyncIOMotorDatabase) -> Dict[str, Any]:
    """获取所有股票数据服务"""
    return StockServiceFactory.get_all_services(db)


def get_supported_stock_collections() -> List[str]:
    """获取支持的股票集合列表"""
    return StockServiceFactory.get_supported_collections()
