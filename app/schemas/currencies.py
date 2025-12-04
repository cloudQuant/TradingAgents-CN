"""
货币模块Pydantic模型定义
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class UpdateType(str, Enum):
    """更新类型枚举"""
    FULL = "full"  # 全量更新
    INCREMENTAL = "incremental"  # 增量更新
    SINGLE = "single"  # 单条更新
    BATCH = "batch"  # 批量更新


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CollectionDataQuery(BaseModel):
    """集合数据查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=1000, description="每页数量")
    sort_field: Optional[str] = Field(default=None, description="排序字段")
    sort_order: Optional[str] = Field(default="desc", description="排序方向")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="过滤条件")


class CollectionStatsResponse(BaseModel):
    """集合统计信息响应"""
    collection_name: str
    total_count: int
    last_updated: Optional[datetime] = None
    index_info: Optional[Dict[str, Any]] = None


class CollectionInfo(BaseModel):
    """集合信息"""
    name: str
    display_name: str
    description: str = ""
    route: str = ""
    order: int = 0
    field_info: List[Dict[str, Any]] = []
    unique_keys: List[str] = []
    required_params: List[str] = []


class CollectionListResponse(BaseModel):
    """集合列表响应"""
    collections: List[CollectionInfo]
    total: int


class CollectionDataResponse(BaseModel):
    """集合数据响应"""
    data: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    has_more: bool


class RefreshCollectionRequest(BaseModel):
    """刷新集合请求"""
    update_type: UpdateType = UpdateType.FULL
    params: Optional[Dict[str, Any]] = None
    batch_size: Optional[int] = Field(default=100, ge=1, le=1000)
    concurrency: Optional[int] = Field(default=3, ge=1, le=10)
    delay: Optional[float] = Field(default=0.5, ge=0)


class RefreshTaskResponse(BaseModel):
    """刷新任务响应"""
    task_id: str
    status: TaskStatus
    message: str = ""
    progress: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CollectionExportRequest(BaseModel):
    """导出请求"""
    format: str = Field(default="csv", description="导出格式: csv, excel, json")
    filters: Optional[Dict[str, Any]] = None
    fields: Optional[List[str]] = None


class ClearCollectionResponse(BaseModel):
    """清空集合响应"""
    success: bool
    message: str
    deleted_count: int = 0


class ApiResponse(BaseModel):
    """通用API响应"""
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None


class RemoteSyncConfig(BaseModel):
    """远程同步配置"""
    host: str
    port: int = 27017
    database: str
    collection: str
    username: Optional[str] = None
    password: Optional[str] = None
    query: Optional[Dict[str, Any]] = None
