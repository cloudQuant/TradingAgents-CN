"""
股票模块 Pydantic 数据模型

定义股票数据集合的请求和响应模型
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field


# ==================== 枚举类型 ====================

class StockUpdateType(str, Enum):
    """更新类型"""
    SINGLE = "single"
    BATCH = "batch"


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    COMPLETED = "completed"


class FileFormat(str, Enum):
    """文件格式"""
    CSV = "csv"
    XLSX = "xlsx"
    JSON = "json"


class SortDirection(str, Enum):
    """排序方向"""
    ASC = "asc"
    DESC = "desc"


# ==================== 请求模型 ====================

class StockCollectionDataQuery(BaseModel):
    """集合数据查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=50, ge=1, le=1000, description="每页数量")
    sort_by: Optional[str] = Field(default=None, description="排序字段")
    sort_dir: Optional[SortDirection] = Field(default=SortDirection.DESC, description="排序方向")
    filter_field: Optional[str] = Field(default=None, description="筛选字段")
    filter_value: Optional[str] = Field(default=None, description="筛选值")


class StockRefreshRequest(BaseModel):
    """刷新数据请求"""
    update_type: StockUpdateType = Field(default=StockUpdateType.BATCH, description="更新类型")
    update_mode: Optional[str] = Field(default="incremental", description="更新模式: incremental/full")
    symbol: Optional[str] = Field(default=None, description="股票代码")
    date: Optional[str] = Field(default=None, description="日期，格式YYYYMMDD")
    start_date: Optional[str] = Field(default=None, description="开始日期")
    end_date: Optional[str] = Field(default=None, description="结束日期")
    period: Optional[str] = Field(default=None, description="周期: daily/weekly/monthly")
    adjust: Optional[str] = Field(default=None, description="复权类型: qfq/hfq/none")
    concurrency: int = Field(default=3, ge=1, le=20, description="并发数")
    limit: Optional[int] = Field(default=None, description="限制数量")
    
    class Config:
        extra = "allow"  # 允许额外字段


class StockExportRequest(BaseModel):
    """导出数据请求"""
    file_format: FileFormat = Field(default=FileFormat.CSV, description="导出格式")
    filter_field: Optional[str] = Field(default=None, description="筛选字段")
    filter_value: Optional[str] = Field(default=None, description="筛选值")
    sort_by: Optional[str] = Field(default=None, description="排序字段")
    sort_dir: Optional[SortDirection] = Field(default=None, description="排序方向")


class StockRemoteSyncRequest(BaseModel):
    """远程同步请求"""
    host: str = Field(..., description="远程主机地址")
    username: Optional[str] = Field(default=None, description="用户名")
    password: Optional[str] = Field(default=None, description="密码")
    auth_source: Optional[str] = Field(default="admin", description="认证数据库")
    collection: Optional[str] = Field(default=None, description="远程集合名")
    batch_size: int = Field(default=5000, ge=100, le=50000, description="批量大小")


# ==================== 响应模型 ====================

class FieldDefinition(BaseModel):
    """字段定义"""
    name: str
    type: str
    description: Optional[str] = None
    example: Optional[Any] = None


class StockCollection(BaseModel):
    """集合信息"""
    name: str
    display_name: str
    description: str
    route: str
    fields: List[str] = []
    order: int = 100


class StockCollectionData(BaseModel):
    """集合数据响应"""
    items: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    fields: List[FieldDefinition]


class StockCollectionStats(BaseModel):
    """集合统计信息"""
    total_count: int
    collection_name: Optional[str] = None
    latest_date: Optional[str] = None
    latest_time: Optional[str] = None
    earliest_date: Optional[str] = None
    rise_count: Optional[int] = None
    fall_count: Optional[int] = None
    flat_count: Optional[int] = None


class TaskResult(BaseModel):
    """任务结果"""
    saved: Optional[int] = None
    inserted: Optional[int] = None
    updated: Optional[int] = None
    deleted: Optional[int] = None
    fetched_rows: Optional[int] = None
    processed: Optional[int] = None
    success: Optional[int] = None
    failed: Optional[int] = None


class RefreshTask(BaseModel):
    """刷新任务状态"""
    task_id: str
    status: TaskStatus
    progress: Optional[int] = None
    total: Optional[int] = None
    message: Optional[str] = None
    error: Optional[str] = None
    result: Optional[TaskResult] = None


class SyncResult(BaseModel):
    """同步结果"""
    inserted: int = 0
    updated: int = 0
    failed: int = 0
    message: str


# ==================== 更新配置模型 ====================

class UpdateParam(BaseModel):
    """更新参数定义"""
    name: str
    label: str
    type: str  # text, number, select, date
    placeholder: Optional[str] = None
    required: bool = False
    default: Optional[Any] = None
    options: Optional[List[Dict[str, Any]]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None


class UpdateConfig(BaseModel):
    """更新配置"""
    enabled: bool = False
    description: str = ""
    params: List[UpdateParam] = []


class CollectionUpdateConfig(BaseModel):
    """集合更新配置"""
    collection_name: str
    display_name: str
    update_description: Optional[str] = None
    single_update: UpdateConfig
    batch_update: UpdateConfig
