"""
股票数据集合API路由

使用动态注册机制管理362个股票数据集合
参考funds模块的架构设计
"""
from datetime import datetime
import asyncio
import logging
import os
import tempfile
import uuid
from typing import Optional, Dict, Any, List

from fastapi import (
    APIRouter,
    Depends,
    Query,
    BackgroundTasks,
    HTTPException,
    status,
    Body,
    UploadFile,
    File,
)
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.core.response import ok
from app.utils.task_manager import get_task_manager
from app.services.data_sources.stocks.provider_registry import (
    get_collection_definitions,
    get_provider_class,
)
from app.services.data_sources.stocks.service_registry import get_service_class
from app.config.stock_update_config import get_collection_update_config
from app.schemas.stocks import (
    StockCollectionDataQuery,
    StockRefreshRequest,
    StockExportRequest,
    StockRemoteSyncRequest,
    TaskStatus,
)


router = APIRouter(prefix="/api/stocks", tags=["stock_collections"])
logger = logging.getLogger("webapi")

# 简单的内存缓存
_cache: Dict[str, Any] = {}
_cache_times: Dict[str, datetime] = {}
CACHE_TTL = 300  # 5分钟


def _get_cache(key: str) -> Optional[Any]:
    """获取缓存"""
    if key in _cache:
        if (datetime.now() - _cache_times.get(key, datetime.min)).seconds < CACHE_TTL:
            return _cache[key]
    return None


def _set_cache(key: str, value: Any):
    """设置缓存"""
    _cache[key] = value
    _cache_times[key] = datetime.now()


def _get_collection_fields_order(collection_name: str) -> list:
    """获取集合的字段顺序"""
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                system_fields = {"更新时间", "更新人", "创建时间", "创建人", "来源", "scraped_at"}
                fields = [f.get("name") for f in field_info 
                         if f.get("name") and f.get("name") not in system_fields]
                if fields:
                    return fields
    except Exception as e:
        logger.warning(f"获取字段信息失败 {collection_name}: {e}")
    return []


def _get_provider_field_info(collection_name: str) -> List[Dict[str, Any]]:
    """获取 provider 的完整字段信息"""
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                return field_info
    except Exception as e:
        logger.warning(f"获取字段信息失败 {collection_name}: {e}")
    return []


# ==================== 集合列表API ====================

@router.get("/collections")
async def list_stock_collections(
    current_user: dict = Depends(get_current_user),
):
    """
    获取所有股票数据集合列表
    
    返回362个股票数据集合的基本信息
    """
    try:
        cache_key = "stock_collections_list"
        cached = _get_cache(cache_key)
        if cached:
            return {"success": True, "data": cached}

        collection_items = []
        for meta in get_collection_definitions():
            name = meta.get("name")
            if not name:
                continue

            fields = meta.get("fields") or _get_collection_fields_order(name)
            collection_items.append({
                "name": name,
                "display_name": meta.get("display_name") or name,
                "description": meta.get("description") or "",
                "route": meta.get("route") or f"/stocks/collections/{name}",
                "fields": fields,
                "category": meta.get("category", "默认"),
                "order": meta.get("order", 100),
            })

        _set_cache(cache_key, collection_items)
        return {"success": True, "data": collection_items}
    except Exception as e:
        logger.error(f"获取股票集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 集合更新配置API ====================

@router.get("/collections/{collection_name}/update-config")
async def get_stock_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定股票集合的更新配置"""
    try:
        config = get_collection_update_config(collection_name)
        return {"success": True, "data": config}
    except Exception as e:
        logger.error(f"获取股票集合更新配置失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 集合数据查询API ====================

@router.get("/collections/{collection_name}")
async def get_stock_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=1000, description="每页数量"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: Optional[str] = Query("desc", description="排序方向"),
    filter_field: Optional[str] = Query(None, description="筛选字段"),
    filter_value: Optional[str] = Query(None, description="筛选值"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取指定股票集合的数据
    
    支持分页、排序、筛选
    """
    try:
        db = get_mongo_db()
        
        # 验证集合是否存在
        provider_cls = get_provider_class(collection_name)
        if not provider_cls:
            return {"success": False, "error": f"集合不存在: {collection_name}"}
        
        # 获取Service类
        service_cls = get_service_class(collection_name)
        if service_cls:
            service = service_cls(db, current_user)
            
            # 构建过滤条件
            filters = {}
            if filter_field and filter_value:
                filters[filter_field] = {"$regex": filter_value, "$options": "i"}
            
            skip = (page - 1) * page_size
            result = await service.get_data(skip=skip, limit=page_size, filters=filters)
            
            # 获取字段信息
            field_info = _get_provider_field_info(collection_name)
            
            return {
                "success": True,
                "data": {
                    "items": result.get("data", []),
                    "total": result.get("total", 0),
                    "page": page,
                    "page_size": page_size,
                    "fields": field_info,
                }
            }
        else:
            # 直接从数据库查询
            collection = db[collection_name]
            
            query = {}
            if filter_field and filter_value:
                query[filter_field] = {"$regex": filter_value, "$options": "i"}
            
            # 排序
            sort_field = sort_by or "更新时间"
            sort_direction = -1 if sort_dir == "desc" else 1
            
            skip = (page - 1) * page_size
            cursor = collection.find(query).sort(sort_field, sort_direction).skip(skip).limit(page_size)
            items = await cursor.to_list(length=page_size)
            
            # 转换ObjectId
            for item in items:
                item["_id"] = str(item["_id"])
                for key, value in item.items():
                    if isinstance(value, datetime):
                        item[key] = value.isoformat()
            
            total = await collection.count_documents(query)
            field_info = _get_provider_field_info(collection_name)
            
            return {
                "success": True,
                "data": {
                    "items": items,
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "fields": field_info,
                }
            }
    except Exception as e:
        logger.error(f"获取股票集合数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 集合统计API ====================

@router.get("/collections/{collection_name}/stats")
async def get_stock_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取股票集合的统计信息"""
    try:
        db = get_mongo_db()
        
        provider_cls = get_provider_class(collection_name)
        if not provider_cls:
            return {"success": False, "error": f"集合不存在: {collection_name}"}
        
        service_cls = get_service_class(collection_name)
        if service_cls:
            service = service_cls(db, current_user)
            overview = await service.get_overview()
            return {"success": True, "data": overview}
        else:
            # 直接统计
            collection = db[collection_name]
            total_count = await collection.count_documents({})
            
            latest = await collection.find_one(sort=[("更新时间", -1)])
            oldest = await collection.find_one(sort=[("更新时间", 1)])
            
            return {
                "success": True,
                "data": {
                    "total_count": total_count,
                    "collection_name": collection_name,
                    "latest_time": latest.get("更新时间") if latest else None,
                    "earliest_time": oldest.get("更新时间") if oldest else None,
                }
            }
    except Exception as e:
        logger.error(f"获取股票集合统计失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 数据刷新API ====================

@router.post("/collections/{collection_name}/refresh")
async def refresh_stock_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    request: StockRefreshRequest = Body(default=StockRefreshRequest()),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新股票集合数据
    
    支持单条更新和批量更新
    """
    try:
        db = get_mongo_db()
        task_manager = get_task_manager()
        
        provider_cls = get_provider_class(collection_name)
        if not provider_cls:
            return {"success": False, "error": f"集合不存在: {collection_name}"}
        
        service_cls = get_service_class(collection_name)
        if not service_cls:
            return {"success": False, "error": f"服务不存在: {collection_name}"}
        
        # 创建任务
        task_id = str(uuid.uuid4())
        task_manager.create_task(
            task_id,
            task_type="refresh_stock_collection",
            description=f"刷新股票集合: {collection_name}",
        )
        
        # 后台执行刷新
        async def do_refresh():
            try:
                service = service_cls(db, current_user)
                
                # 转换请求参数
                params = request.model_dump(exclude_none=True)
                
                if request.update_type.value == "batch":
                    result = await service.update_batch_data(task_id=task_id, **params)
                else:
                    result = await service.update_single_data(**params)
                    task_manager.complete_task(task_id, result=result)
                
                return result
            except Exception as e:
                logger.error(f"刷新股票集合失败: {e}", exc_info=True)
                task_manager.fail_task(task_id, str(e))
                raise
        
        background_tasks.add_task(do_refresh)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "status": "pending",
                "message": f"刷新任务已创建: {collection_name}",
            }
        }
    except Exception as e:
        logger.error(f"创建刷新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 任务状态API ====================

@router.get("/tasks/{task_id}")
async def get_stock_refresh_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取刷新任务状态"""
    try:
        task_manager = get_task_manager()
        task = task_manager.get_task(task_id)
        
        if not task:
            return {"success": False, "error": "任务不存在"}
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "status": task.get("status", "unknown"),
                "progress": task.get("progress", 0),
                "total": task.get("total", 100),
                "message": task.get("message", ""),
                "result": task.get("result"),
                "error": task.get("error"),
            }
        }
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 清空数据API ====================

@router.delete("/collections/{collection_name}")
async def clear_stock_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空股票集合数据"""
    try:
        db = get_mongo_db()
        
        provider_cls = get_provider_class(collection_name)
        if not provider_cls:
            return {"success": False, "error": f"集合不存在: {collection_name}"}
        
        service_cls = get_service_class(collection_name)
        if service_cls:
            service = service_cls(db, current_user)
            result = await service.clear_data()
            return {"success": True, "data": result}
        else:
            collection = db[collection_name]
            result = await collection.delete_many({})
            return {
                "success": True,
                "data": {
                    "deleted_count": result.deleted_count,
                    "message": f"已删除 {result.deleted_count} 条数据",
                }
            }
    except Exception as e:
        logger.error(f"清空股票集合失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 导出数据API ====================

@router.post("/collections/{collection_name}/export")
async def export_stock_collection(
    collection_name: str,
    request: StockExportRequest = Body(default=StockExportRequest()),
    current_user: dict = Depends(get_current_user),
):
    """导出股票集合数据"""
    try:
        db = get_mongo_db()
        
        provider_cls = get_provider_class(collection_name)
        if not provider_cls:
            return {"success": False, "error": f"集合不存在: {collection_name}"}
        
        collection = db[collection_name]
        
        # 构建查询
        query = {}
        if request.filter_field and request.filter_value:
            query[request.filter_field] = {"$regex": request.filter_value, "$options": "i"}
        
        # 查询数据
        cursor = collection.find(query)
        if request.sort_by:
            sort_dir = -1 if request.sort_dir and request.sort_dir.value == "desc" else 1
            cursor = cursor.sort(request.sort_by, sort_dir)
        
        items = await cursor.to_list(length=100000)  # 最多导出10万条
        
        if not items:
            return {"success": False, "error": "没有数据可导出"}
        
        # 转换ObjectId
        for item in items:
            item["_id"] = str(item["_id"])
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = value.isoformat()
        
        # 生成导出文件
        import pandas as pd
        df = pd.DataFrame(items)
        
        # 创建临时文件
        file_format = request.file_format.value
        suffix = f".{file_format}"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            if file_format == "csv":
                df.to_csv(f.name, index=False, encoding="utf-8-sig")
            elif file_format == "xlsx":
                df.to_excel(f.name, index=False)
            elif file_format == "json":
                df.to_json(f.name, orient="records", force_ascii=False, indent=2)
            
            filename = f"{collection_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"
            
            return FileResponse(
                f.name,
                filename=filename,
                media_type="application/octet-stream",
                background=BackgroundTask(lambda: os.unlink(f.name)),
            )
    except Exception as e:
        logger.error(f"导出股票集合失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 概览API ====================

@router.get("/overview")
async def get_stocks_overview(current_user: dict = Depends(get_current_user)):
    """获取股票模块概览"""
    try:
        collections = get_collection_definitions()
        
        # 按类别分组
        categories = {}
        for col in collections:
            category = col.get("category", "默认")
            if category not in categories:
                categories[category] = []
            categories[category].append(col.get("name"))
        
        return {
            "success": True,
            "data": {
                "total_collections": len(collections),
                "categories": {k: len(v) for k, v in categories.items()},
                "message": "股票数据集合模块",
            }
        }
    except Exception as e:
        logger.error(f"获取股票概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
