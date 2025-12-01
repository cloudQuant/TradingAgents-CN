"""
基金模块缓存管理器
提供带过期时间的缓存机制
"""
from datetime import datetime, timedelta
from typing import Optional, Any, Dict
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class FundCollectionCache:
    """基金集合缓存管理器"""
    
    def __init__(self, default_ttl_seconds: int = 300):
        """
        初始化缓存管理器
        
        Args:
            default_ttl_seconds: 默认过期时间（秒）
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = timedelta(seconds=default_ttl_seconds)
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存键"""
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return f"{prefix}:{hashlib.md5(key_str.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在或已过期则返回 None
        """
        if key not in self.cache:
            self.stats["misses"] += 1
            return None
        
        entry = self.cache[key]
        if datetime.utcnow() > entry["expires_at"]:
            # 缓存已过期，删除
            del self.cache[key]
            self.stats["misses"] += 1
            self.stats["evictions"] += 1
            logger.debug(f"缓存键 {key} 已过期，已删除")
            return None
        
        self.stats["hits"] += 1
        return entry["data"]
    
    def set(
        self,
        key: str,
        data: Any,
        ttl_seconds: Optional[int] = None
    ):
        """
        设置缓存
        
        Args:
            key: 缓存键
            data: 要缓存的数据
            ttl_seconds: 过期时间（秒），如果为 None 则使用默认值
        """
        ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else self.default_ttl
        self.cache[key] = {
            "data": data,
            "expires_at": datetime.utcnow() + ttl,
            "created_at": datetime.utcnow()
        }
        logger.debug(f"设置缓存键 {key}，过期时间: {ttl}")
    
    def invalidate(self, pattern: Optional[str] = None):
        """
        失效缓存
        
        Args:
            pattern: 匹配模式，如果为 None 则清空所有缓存
        """
        if pattern:
            keys_to_delete = [k for k in self.cache.keys() if pattern in k]
            for k in keys_to_delete:
                del self.cache[k]
            logger.info(f"失效了 {len(keys_to_delete)} 个匹配 '{pattern}' 的缓存")
        else:
            count = len(self.cache)
            self.cache.clear()
            logger.info(f"清空了所有缓存（{count} 个）")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "evictions": self.stats["evictions"],
            "hit_rate": f"{hit_rate:.2f}%",
            "total_requests": total_requests
        }
    
    def cleanup_expired(self):
        """清理所有过期的缓存"""
        now = datetime.utcnow()
        expired_keys = [
            k for k, v in self.cache.items()
            if now > v["expires_at"]
        ]
        
        for k in expired_keys:
            del self.cache[k]
            self.stats["evictions"] += 1
        
        if expired_keys:
            logger.info(f"清理了 {len(expired_keys)} 个过期缓存")
        
        return len(expired_keys)


# 全局缓存实例
_fund_cache = FundCollectionCache(default_ttl_seconds=300)


def get_fund_cache() -> FundCollectionCache:
    """获取基金缓存实例"""
    return _fund_cache
