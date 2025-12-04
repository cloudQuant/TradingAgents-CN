"""
期货模块自定义异常类
"""
from typing import Optional, Dict, Any


class FuturesException(Exception):
    """期货模块基础异常类"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "FUTURES_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class FuturesCollectionNotFound(FuturesException):
    """期货集合不存在异常"""
    
    def __init__(self, collection_name: str):
        super().__init__(
            message=f"期货数据集合 '{collection_name}' 不存在",
            error_code="FUTURES_COLLECTION_NOT_FOUND",
            details={"collection_name": collection_name}
        )


class FuturesDataUpdateError(FuturesException):
    """期货数据更新错误"""
    
    def __init__(self, collection_name: str, reason: str):
        super().__init__(
            message=f"更新期货集合 '{collection_name}' 失败: {reason}",
            error_code="FUTURES_DATA_UPDATE_ERROR",
            details={"collection_name": collection_name, "reason": reason}
        )


class FuturesDataValidationError(FuturesException):
    """期货数据验证错误"""
    
    def __init__(self, field: str, reason: str):
        super().__init__(
            message=f"数据验证失败 - 字段 '{field}': {reason}",
            error_code="FUTURES_DATA_VALIDATION_ERROR",
            details={"field": field, "reason": reason}
        )


class FuturesProviderError(FuturesException):
    """期货数据提供者错误"""
    
    def __init__(self, provider_name: str, reason: str):
        super().__init__(
            message=f"数据提供者 '{provider_name}' 错误: {reason}",
            error_code="FUTURES_PROVIDER_ERROR",
            details={"provider_name": provider_name, "reason": reason}
        )


class FuturesTaskNotFound(FuturesException):
    """期货任务不存在异常"""
    
    def __init__(self, task_id: str):
        super().__init__(
            message=f"任务 '{task_id}' 不存在或已过期",
            error_code="FUTURES_TASK_NOT_FOUND",
            details={"task_id": task_id}
        )


class FuturesDataFetchError(FuturesException):
    """期货数据获取错误"""
    
    def __init__(self, source: str, reason: str):
        super().__init__(
            message=f"从 '{source}' 获取数据失败: {reason}",
            error_code="FUTURES_DATA_FETCH_ERROR",
            details={"source": source, "reason": reason}
        )
