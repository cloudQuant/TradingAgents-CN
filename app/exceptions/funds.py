"""
基金模块自定义异常
提供统一的错误处理
"""
from fastapi import HTTPException, status
from typing import Optional


class FundException(HTTPException):
    """基金模块基础异常"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "FUND_ERROR",
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


class FundCollectionNotFound(FundException):
    """集合不存在异常"""
    def __init__(self, collection_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"基金集合 '{collection_name}' 不存在",
            error_code="FUND_COLLECTION_NOT_FOUND"
        )
        self.collection_name = collection_name


class FundDataUpdateError(FundException):
    """数据更新错误"""
    def __init__(self, message: str, collection_name: Optional[str] = None):
        detail = f"更新基金数据失败: {message}"
        if collection_name:
            detail = f"更新集合 '{collection_name}' 失败: {message}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="FUND_DATA_UPDATE_ERROR"
        )
        self.collection_name = collection_name
        self.message = message


class FundDataValidationError(FundException):
    """数据验证错误"""
    def __init__(self, message: str, field: Optional[str] = None):
        detail = f"数据验证失败: {message}"
        if field:
            detail = f"字段 '{field}' 验证失败: {message}"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="FUND_DATA_VALIDATION_ERROR"
        )
        self.field = field
        self.message = message


class FundProviderError(FundException):
    """数据提供者错误"""
    def __init__(self, message: str, provider_name: Optional[str] = None):
        detail = f"数据提供者错误: {message}"
        if provider_name:
            detail = f"数据提供者 '{provider_name}' 错误: {message}"
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
            error_code="FUND_PROVIDER_ERROR"
        )
        self.provider_name = provider_name
        self.message = message


class FundTaskNotFound(FundException):
    """任务不存在异常"""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务 '{task_id}' 不存在",
            error_code="FUND_TASK_NOT_FOUND"
        )
        self.task_id = task_id
