"""
基金模块 Pydantic 模型定义
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
    tracking_target: Optional[str] = Field(None, description="跟踪标的筛选（仅指数型基金）")
    tracking_method: Optional[str] = Field(None, description="跟踪方式筛选（仅指数型基金）")
    fund_company: Optional[str] = Field(None, description="基金公司筛选（仅指数型基金）")
    
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
    purchase_status_stats: Optional[List[Dict[str, Any]]] = Field(None, description="申购状态统计")
    redeem_status_stats: Optional[List[Dict[str, Any]]] = Field(None, description="赎回状态统计")
    top_gainers: Optional[List[Dict[str, Any]]] = Field(None, description="涨幅TOP10")
    top_losers: Optional[List[Dict[str, Any]]] = Field(None, description="跌幅TOP10")
    top_volume: Optional[List[Dict[str, Any]]] = Field(None, description="成交额TOP10")
    market_cap_stats: Optional[List[Dict[str, Any]]] = Field(None, description="市值分布统计")


class CollectionInfo(BaseModel):
    """集合信息"""
    name: str = Field(..., description="集合名称")
    display_name: str = Field(..., description="显示名称")
    description: str = Field(default="", description="描述")
    route: str = Field(..., description="路由路径")
    fields: List[str] = Field(default_factory=list, description="字段列表")


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
    fund_code: Optional[str] = Field(None, description="基金代码（单条更新时必需）")
    symbol: Optional[str] = Field(None, description="代码/符号")
    year: Optional[int] = Field(None, ge=2000, le=2100, description="年份")
    date: Optional[str] = Field(None, description="日期（YYYY-MM-DD格式）")
    quarter_date: Optional[str] = Field(None, description="季度日期（YYYY-MM-DD格式）")
    period: Optional[str] = Field(None, description="周期")
    adjust: Optional[str] = Field(None, description="复权方式")
    concurrency: Optional[int] = Field(None, ge=1, le=10, description="并发数")
    limit: Optional[int] = Field(None, ge=1, description="限制数量")
    start_year: Optional[int] = Field(None, ge=2000, le=2100, description="起始年份")
    end_year: Optional[int] = Field(None, ge=2000, le=2100, description="结束年份")
    delay: Optional[float] = Field(None, ge=0, description="延迟时间（秒）")
    
    @validator('fund_code', 'symbol')
    def validate_code(cls, v):
        if v and not v.strip():
            raise ValueError('代码不能为空')
        return v.strip() if v else None
    
    @validator('year', 'start_year', 'end_year', pre=True)
    def validate_year(cls, v):
        """将字符串年份转换为整数"""
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return None
            try:
                return int(v)
            except ValueError:
                raise ValueError(f'年份必须是数字: {v}')
        if isinstance(v, int):
            return v
        raise ValueError(f'年份类型无效: {type(v)}')
    
    @validator('date', 'quarter_date')
    def validate_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('日期格式必须为 YYYY-MM-DD')
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
    tracking_target: Optional[str] = Field(None, description="跟踪标的")
    tracking_method: Optional[str] = Field(None, description="跟踪方式")
    fund_company: Optional[str] = Field(None, description="基金公司")


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
