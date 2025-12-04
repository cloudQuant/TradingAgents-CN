"""
债券模块 Pydantic 模型定义
提供类型安全和数据验证
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class SortDirection(str, Enum):
    """排序方向"""
    ASC = "asc"
    DESC = "desc"


class CollectionDataQuery(BaseModel):
    """集合数据查询参数"""
    page: int = Field(1, ge=1, description="页码，从1开始")
    page_size: int = Field(50, ge=1, le=500, description="每页数量，默认50，最大500")
    sort_by: Optional[str] = Field(None, description="排序字段")
    sort_dir: SortDirection = Field(SortDirection.DESC, description="排序方向")
    filter_field: Optional[str] = Field(None, description="过滤字段")
    filter_value: Optional[str] = Field(None, description="过滤值")
    bond_type: Optional[str] = Field(None, description="债券类型筛选")
    issuer: Optional[str] = Field(None, description="发行人筛选")
    rating: Optional[str] = Field(None, description="评级筛选")
    
    @validator('page_size')
    def validate_page_size(cls, v):
        if v > 500:
            raise ValueError('每页数量不能超过500')
        return v


class CollectionStatsResponse(BaseModel):
    """集合统计响应"""
    total_count: int = Field(..., description="总记录数")
    latest_date: Optional[str] = Field(None, description="最新日期")
    latest_time: Optional[str] = Field(None, description="最新时间")
    type_stats: List[Dict[str, Any]] = Field(default_factory=list, description="类型统计")
    rise_count: Optional[int] = Field(None, description="上涨数量")
    fall_count: Optional[int] = Field(None, description="下跌数量")
    flat_count: Optional[int] = Field(None, description="平盘数量")
    rating_stats: Optional[List[Dict[str, Any]]] = Field(None, description="评级统计")
    issuer_stats: Optional[List[Dict[str, Any]]] = Field(None, description="发行人统计")
    top_gainers: Optional[List[Dict[str, Any]]] = Field(None, description="涨幅TOP10")
    top_losers: Optional[List[Dict[str, Any]]] = Field(None, description="跌幅TOP10")
    top_volume: Optional[List[Dict[str, Any]]] = Field(None, description="成交额TOP10")


class CollectionInfo(BaseModel):
    """集合信息"""
    name: str = Field(..., description="集合名称")
    display_name: str = Field(..., description="显示名称")
    description: str = Field(default="", description="描述")
    route: str = Field(..., description="路由路径")
    fields: List[str] = Field(default_factory=list, description="字段列表")
    source: Optional[str] = Field(None, description="数据来源")
    category: Optional[str] = Field(None, description="分类")
    order: Optional[int] = Field(None, description="排序")


class CollectionListResponse(BaseModel):
    """集合列表响应"""
    success: bool = Field(True, description="是否成功")
    data: List[CollectionInfo] = Field(..., description="集合列表")
    error: Optional[str] = Field(None, description="错误信息")


class CollectionDataResponse(BaseModel):
    """集合数据响应"""
    success: bool = Field(True, description="是否成功")
    data: Dict[str, Any] = Field(..., description="数据")
    error: Optional[str] = Field(None, description="错误信息")


class UpdateType(str, Enum):
    """更新类型"""
    SINGLE = "single"
    BATCH = "batch"


class RefreshCollectionRequest(BaseModel):
    """刷新集合请求"""
    update_type: UpdateType = Field(..., description="更新类型：single 或 batch")
    update_mode: Optional[str] = Field("incremental", description="更新方式：incremental（增量更新）或 full（全量更新）")
    bond_code: Optional[str] = Field(None, description="债券代码（单条更新时必需）")
    symbol: Optional[str] = Field(None, description="代码/符号")
    indicator: Optional[str] = Field(None, description="指标类型")
    period: Optional[str] = Field(None, description="期限")
    date: Optional[str] = Field(None, description="日期（YYYY-MM-DD格式）")
    start_date: Optional[str] = Field(None, description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    concurrency: Optional[int] = Field(None, ge=1, le=10, description="并发数")
    cookie: Optional[str] = Field(None, description="Cookie（集思录数据）")
    
    @validator('bond_code', 'symbol')
    def validate_code(cls, v):
        if v and not v.strip():
            raise ValueError('代码不能为空')
        return v.strip() if v else None
    
    @validator('date', 'start_date', 'end_date')
    def validate_date(cls, v):
        if v:
            # 支持多种日期格式
            for fmt in ['%Y-%m-%d', '%Y%m%d']:
                try:
                    datetime.strptime(v, fmt)
                    return v
                except ValueError:
                    continue
            raise ValueError('日期格式必须为 YYYY-MM-DD 或 YYYYMMDD')
        return v


class RefreshTaskResponse(BaseModel):
    """刷新任务响应"""
    success: bool = Field(True, description="是否成功")
    data: Dict[str, Any] = Field(..., description="任务信息")
    error: Optional[str] = Field(None, description="错误信息")


class TaskStatus(BaseModel):
    """任务状态"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="状态：pending/running/success/failed")
    progress: Optional[int] = Field(None, description="进度")
    total: Optional[int] = Field(None, description="总数")
    message: Optional[str] = Field(None, description="消息")
    error: Optional[str] = Field(None, description="错误信息")
    result: Optional[Dict[str, Any]] = Field(None, description="结果")


class CollectionExportRequest(BaseModel):
    """导出集合请求"""
    file_format: str = Field("xlsx", pattern="^(csv|xlsx|json)$", description="文件格式")
    filter_field: Optional[str] = Field(None, description="过滤字段")
    filter_value: Optional[str] = Field(None, description="过滤值")
    sort_by: Optional[str] = Field(None, description="排序字段")
    sort_dir: SortDirection = Field(SortDirection.DESC, description="排序方向")
    bond_type: Optional[str] = Field(None, description="债券类型")
    issuer: Optional[str] = Field(None, description="发行人")
    rating: Optional[str] = Field(None, description="评级")


class ClearCollectionResponse(BaseModel):
    """清空集合响应"""
    success: bool = Field(True, description="是否成功")
    data: Dict[str, Any] = Field(..., description="结果")
    error: Optional[str] = Field(None, description="错误信息")


class ApiResponse(BaseModel):
    """通用API响应"""
    success: bool = Field(True, description="是否成功")
    data: Optional[Any] = Field(None, description="数据")
    error: Optional[str] = Field(None, description="错误信息")
    timestamp: Optional[str] = Field(None, description="时间戳")
