"""
期货模块Pydantic模型定义
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class UpdateType(str, Enum):
    """更新类型枚举"""
    single = "single"
    batch = "batch"


class UpdateMode(str, Enum):
    """更新模式枚举"""
    incremental = "incremental"
    full = "full"


class TaskStatus(str, Enum):
    """任务状态枚举"""
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"
    completed = "completed"


class CollectionDataQuery(BaseModel):
    """集合数据查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=100, ge=1, le=10000, description="每页大小")
    sort_by: Optional[str] = Field(default=None, description="排序字段")
    sort_dir: Optional[str] = Field(default="desc", description="排序方向: asc/desc")
    filter_field: Optional[str] = Field(default=None, description="过滤字段")
    filter_value: Optional[str] = Field(default=None, description="过滤值")


class CollectionStatsResponse(BaseModel):
    """集合统计信息响应"""
    total: int = Field(..., description="数据总数")
    last_update: Optional[datetime] = Field(default=None, description="最后更新时间")
    field_count: int = Field(default=0, description="字段数量")
    collection_name: str = Field(..., description="集合名称")


class CollectionInfo(BaseModel):
    """集合信息"""
    name: str = Field(..., description="集合名称")
    display_name: str = Field(..., description="显示名称")
    description: str = Field(default="", description="集合描述")
    route: str = Field(..., description="前端路由")
    order: int = Field(default=100, description="排序顺序")
    fields: List[Dict[str, Any]] = Field(default_factory=list, description="字段列表")


class CollectionListResponse(BaseModel):
    """集合列表响应"""
    collections: List[CollectionInfo] = Field(..., description="集合列表")


class CollectionDataResponse(BaseModel):
    """集合数据响应"""
    total: int = Field(..., description="数据总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    items: List[Dict[str, Any]] = Field(..., description="数据列表")


class RefreshCollectionRequest(BaseModel):
    """刷新集合请求"""
    update_type: UpdateType = Field(..., description="更新类型")
    update_mode: Optional[UpdateMode] = Field(default=UpdateMode.incremental, description="更新模式")
    # 通用参数
    symbol: Optional[str] = Field(default=None, description="品种/合约代码")
    date: Optional[str] = Field(default=None, description="日期参数")
    market: Optional[str] = Field(default=None, description="市场/交易所")
    period: Optional[str] = Field(default=None, description="周期")
    indicator: Optional[str] = Field(default=None, description="指标")
    start_date: Optional[str] = Field(default=None, description="开始日期")
    end_date: Optional[str] = Field(default=None, description="结束日期")
    concurrency: int = Field(default=3, ge=1, le=20, description="并发数")


class RefreshTaskResponse(BaseModel):
    """刷新任务响应"""
    task_id: str = Field(..., description="任务ID")
    status: TaskStatus = Field(..., description="任务状态")
    progress: int = Field(default=0, description="进度(0-100)")
    total: int = Field(default=0, description="总数")
    message: str = Field(default="", description="状态消息")
    error: Optional[str] = Field(default=None, description="错误信息")
    result: Optional[Dict[str, Any]] = Field(default=None, description="结果数据")


class CollectionExportRequest(BaseModel):
    """集合数据导出请求"""
    format: str = Field(default="csv", description="导出格式: csv/excel/json")
    filter_field: Optional[str] = Field(default=None, description="过滤字段")
    filter_value: Optional[str] = Field(default=None, description="过滤值")


class ClearCollectionResponse(BaseModel):
    """清空集合响应"""
    deleted: int = Field(..., description="删除的记录数")
    collection_name: str = Field(..., description="集合名称")


class ApiResponse(BaseModel):
    """通用API响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(default="", description="消息")
    data: Optional[Any] = Field(default=None, description="数据")


class RemoteSyncConfig(BaseModel):
    """远程同步配置"""
    remote_host: str = Field(..., description="远程数据库地址")
    remote_collection: Optional[str] = Field(default=None, description="远程集合名称")
    remote_username: Optional[str] = Field(default=None, description="用户名")
    remote_password: Optional[str] = Field(default=None, description="密码")
    remote_auth_source: str = Field(default="admin", description="认证数据库")
    batch_size: int = Field(default=5000, ge=100, le=50000, description="批量大小")
