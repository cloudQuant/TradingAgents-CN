"""
期货数据集合路由
重构版：参考 bonds.py 和 funds.py 实现
"""
from datetime import datetime, timedelta
import asyncio
import hashlib
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
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel

from app.routers.auth_db import get_current_user, get_current_user_optional
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.futures_refresh_service import FuturesRefreshService
from app.services.futures_data_service import FuturesDataService
from app.config.futures_update_config import (
    get_futures_collection_update_config,
    FUTURES_UPDATE_CONFIGS,
)
from app.services.data_sources.futures.provider_registry import (
    get_collection_definitions,
    get_provider_class,
)
from app.schemas.futures import (
    CollectionDataQuery,
    CollectionListResponse,
    CollectionDataResponse,
    CollectionStatsResponse,
    RefreshCollectionRequest,
    RefreshTaskResponse,
    CollectionExportRequest,
    ClearCollectionResponse,
    ApiResponse,
    RemoteSyncConfig,
)
from app.exceptions.futures import (
    FuturesCollectionNotFound,
    FuturesDataUpdateError,
    FuturesTaskNotFound,
)


class FuturesCollectionExportRequest(BaseModel):
    """导出期货集合请求"""
    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"


router = APIRouter(prefix="/api/futures", tags=["futures"])
logger = logging.getLogger("webapi")


def _get_collection_fields_order(collection_name: str) -> list:
    """获取集合的字段顺序，从 provider 的 field_info 获取"""
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                system_fields = {"更新时间", "更新人", "创建时间", "创建人", "来源"}
                fields = [f.get("name") for f in field_info 
                         if f.get("name") and f.get("name") not in system_fields]
                if fields:
                    return fields
    except Exception as e:
        logger.warning(f"从 provider 获取字段信息失败 {collection_name}: {e}")
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
        logger.warning(f"从 provider 获取字段信息失败 {collection_name}: {e}")
    return []


# ==================== 概览接口 ====================

@router.get("/overview")
async def get_futures_overview(current_user: Optional[dict] = Depends(get_current_user_optional)):
    """获取期货概览数据"""
    try:
        db = get_mongo_db()
        data_service = FuturesDataService(db)
        
        # 获取主要集合的统计
        stats = {
            "total_collections": len(FUTURES_UPDATE_CONFIGS),
            "main_stats": {},
            "categories": [
                {"name": "交易费用", "count": 2},
                {"name": "持仓排名", "count": 2},
                {"name": "仓单日报", "count": 4},
                {"name": "历史行情", "count": 5},
                {"name": "实时行情", "count": 4},
                {"name": "合约信息", "count": 6},
            ]
        }
        
        # 获取一些关键集合的数量
        key_collections = ["futures_fees_info", "futures_dce_position_rank", "get_futures_daily"]
        for col_name in key_collections:
            try:
                collection = db.get_collection(col_name)
                count = await collection.count_documents({})
                stats["main_stats"][col_name] = count
            except Exception:
                stats["main_stats"][col_name] = 0
        
        return {"success": True, "data": stats}
    except Exception as e:
        logger.error(f"获取期货概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 集合列表接口 ====================

@router.get("/collections")
async def list_futures_collections(current_user: Optional[dict] = Depends(get_current_user_optional)):
    """获取期货数据集合列表"""
    try:
        collections = get_collection_definitions()
        return {
            "success": True,
            "data": collections,
            "total": len(collections),
        }
    except Exception as e:
        logger.error(f"获取集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 更新配置接口 ====================

@router.get("/collections/{collection_name}/update-config")
async def get_collection_update_config_endpoint(
    collection_name: str,
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """获取集合的更新配置"""
    try:
        config = get_futures_collection_update_config(collection_name)
        return {"success": True, "data": config}
    except Exception as e:
        logger.error(f"获取更新配置失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 集合数据接口 ====================

@router.get("/collections/{collection_name}")
async def get_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """获取集合数据（分页）"""
    db = get_mongo_db()
    
    # 验证集合是否存在
    supported_collections = [c["name"] for c in get_collection_definitions()]
    if collection_name not in supported_collections:
        raise FuturesCollectionNotFound(collection_name)
    
    collection = db.get_collection(collection_name)
    
    try:
        # 构建查询条件
        mongo_query = {}
        if filter_field and filter_value:
            filter_field_stripped = filter_field.strip()
            filter_value_stripped = filter_value.strip()
            if filter_field_stripped and filter_value_stripped:
                if filter_field_stripped in ["code", "name", "symbol", "品种", "合约代码", "品种代码"]:
                    mongo_query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
                else:
                    mongo_query[filter_field_stripped] = filter_value_stripped
        
        # 获取总数
        total = await collection.count_documents(mongo_query)
        
        # 构建排序
        sort_key = sort_by if sort_by else "_id"
        sort_direction = -1 if sort_dir == "desc" else 1
        
        # 分页查询
        skip = (page - 1) * page_size
        cursor = collection.find(mongo_query).sort(sort_key, sort_direction).skip(skip).limit(page_size)
        items = []
        
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            items.append(doc)
        
        # 获取字段信息
        fields_info = []
        if items:
            sample = items[0]
            provider_field_info = _get_provider_field_info(collection_name)
            
            fields_dict = {}
            for key, value in sample.items():
                if key != "_id":
                    field_type = type(value).__name__
                    if field_type == "int":
                        field_type = "整数"
                    elif field_type == "float":
                        field_type = "浮点数"
                    elif field_type == "bool":
                        field_type = "布尔值"
                    else:
                        field_type = "字符串"
                    fields_dict[key] = {
                        "name": key,
                        "type": field_type,
                        "example": str(value)[:50] if value is not None else None,
                    }
            
            if provider_field_info:
                for field_def in provider_field_info:
                    field_name = field_def.get("name")
                    if field_name and field_name in fields_dict:
                        field_info = {
                            "name": field_name,
                            "type": field_def.get("type", fields_dict[field_name]["type"]),
                            "description": field_def.get("description", ""),
                            "example": fields_dict[field_name].get("example"),
                        }
                        fields_info.append(field_info)
                        del fields_dict[field_name]
                
                for field_info in fields_dict.values():
                    fields_info.append(field_info)
            else:
                fields_info = list(fields_dict.values())
        
        return {
            "success": True,
            "data": {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "fields": fields_info,
            }
        }
    except FuturesCollectionNotFound:
        raise
    except Exception as e:
        logger.error(f"获取集合数据失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 统计接口 ====================

@router.get("/collections/{collection_name}/stats")
async def get_collection_stats(
    collection_name: str,
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """获取集合统计信息"""
    try:
        db = get_mongo_db()
        data_service = FuturesDataService(db)
        stats = await data_service.get_futures_stats(collection_name)
        return {"success": True, "data": stats}
    except Exception as e:
        logger.error(f"获取统计信息失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 刷新接口 ====================

@router.post("/collections/{collection_name}/refresh")
async def refresh_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    request: Optional[RefreshCollectionRequest] = Body(default=None),
    current_user: dict = Depends(get_current_user),
):
    """刷新期货数据集合（统一入口）"""
    try:
        # 处理请求参数，如果没有传入则使用默认值
        if request:
            params = request.model_dump(exclude_none=True)
        else:
            # 默认参数：单条更新，增量模式
            params = {"update_type": "single", "update_mode": "incremental"}
        
        logger.info(f"[API refresh] 接收到刷新请求: collection={collection_name}, params={params}")
        db = get_mongo_db()
        task_manager = get_task_manager()
        refresh_service = FuturesRefreshService(db)
        
        # 检查集合是否支持
        supported = refresh_service.get_supported_collections()
        if collection_name not in supported:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"集合 {collection_name} 不支持刷新操作"
            )
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"刷新期货集合: {collection_name}"
        )
        
        # 在后台执行刷新（与 funds 模块一致的调用方式）
        async def do_refresh():
            try:
                await refresh_service.refresh_collection(
                    collection_name=collection_name,
                    task_id=task_id,
                    params=params
                )
            except Exception as e:
                logger.error(f"后台刷新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_refresh)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"已启动 {collection_name} 刷新任务"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"启动刷新任务失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/refresh/task/{task_id}")
async def get_refresh_task_status(
    task_id: str,
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """获取刷新任务状态"""
    task_manager = get_task_manager()
    task_status = task_manager.get_task(task_id)
    
    if not task_status:
        raise HTTPException(status_code=404, detail=f"任务 {task_id} 不存在或已过期")
    
    return {"success": True, "data": task_status}


@router.get("/refresh/supported-collections")
async def get_supported_refresh_collections(
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """获取支持刷新的集合列表"""
    try:
        db = get_mongo_db()
        refresh_service = FuturesRefreshService(db)
        supported = refresh_service.get_supported_collections()
        return {"success": True, "data": supported}
    except Exception as e:
        logger.error(f"获取支持的集合失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 清空接口 ====================

@router.delete("/collections/{collection_name}")
async def clear_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空集合数据"""
    try:
        db = get_mongo_db()
        data_service = FuturesDataService(db)
        deleted_count = await data_service.clear_futures_data(collection_name)
        
        return {
            "success": True,
            "data": {
                "deleted": deleted_count,
                "collection_name": collection_name,
                "message": f"成功清空 {deleted_count} 条记录"
            }
        }
    except Exception as e:
        logger.error(f"清空集合失败 {collection_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== 导入导出接口 ====================

@router.post("/collections/{collection_name}/upload")
async def upload_collection_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传文件导入期货数据"""
    try:
        db = get_mongo_db()
        data_service = FuturesDataService(db)
        
        contents = await file.read()
        result = await data_service.import_data_from_file(
            collection_name=collection_name,
            content=contents,
            filename=file.filename
        )
        
        return {"success": result["success"], "data": result}
    except Exception as e:
        logger.error(f"上传文件失败 {collection_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/collections/{collection_name}/export")
async def export_collection_data(
    collection_name: str,
    request: FuturesCollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出集合数据到文件"""
    try:
        db = get_mongo_db()
        data_service = FuturesDataService(db)
        
        # 构建过滤条件
        filters = {}
        if request.filter_field and request.filter_value:
            field = request.filter_field.strip()
            value = request.filter_value.strip()
            if field and value:
                if field in ["code", "name", "symbol"]:
                    filters[field] = {"$regex": value, "$options": "i"}
                else:
                    filters[field] = value
        
        export_format = request.file_format.lower()
        if export_format == "excel":
            export_format = "xlsx"
        
        file_bytes = await data_service.export_data_to_file(
            collection_name=collection_name,
            file_format=export_format,
            filters=filters
        )
        
        suffix_map = {"csv": "csv", "xlsx": "xlsx", "json": "json"}
        suffix = suffix_map.get(export_format, "xlsx")
        filename = f"{collection_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{suffix}"
        
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{suffix}", prefix="futures-export-"
        ) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name
        
        def _cleanup(path: str) -> None:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
        
        return FileResponse(
            path=tmp_path,
            filename=filename,
            media_type="application/octet-stream",
            background=BackgroundTask(_cleanup, tmp_path),
        )
    except Exception as e:
        logger.error(f"导出集合数据失败 {collection_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/collections/{collection_name}/sync")
async def sync_collection_from_remote(
    collection_name: str,
    config: RemoteSyncConfig,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
):
    """从远程数据库同步数据"""
    try:
        db = get_mongo_db()
        data_service = FuturesDataService(db)
        
        # 构建远程配置
        remote_config = {
            "host": config.remote_host,
            "collection": config.remote_collection or collection_name,
            "username": config.remote_username,
            "password": config.remote_password,
            "database": "trading_agents",  # 默认数据库
        }
        
        # 创建任务
        task_manager = get_task_manager()
        task_id = task_manager.create_task(
            task_type=f"sync_{collection_name}",
            description=f"从远程同步期货集合: {collection_name}"
        )
        
        async def run_sync():
            try:
                task_manager.start_task(task_id)
                result = await data_service.sync_data_from_remote(collection_name, remote_config)
                if result["success"]:
                    task_manager.complete_task(task_id, result=result, message=result["message"])
                else:
                    task_manager.fail_task(task_id, result["message"])
            except Exception as e:
                task_manager.fail_task(task_id, str(e))
        
        background_tasks.add_task(lambda: asyncio.create_task(run_sync()))
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"已启动远程同步任务"
            }
        }
    except Exception as e:
        logger.error(f"启动远程同步失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== 搜索接口 ====================

@router.get("/search")
async def search_futures(
    keyword: str = Query(..., description="搜索关键词"),
    current_user: dict = Depends(get_current_user),
):
    """搜索期货（在主要集合中搜索）"""
    try:
        db = get_mongo_db()
        results = []
        
        # 在费用信息表中搜索
        fees_collection = db.get_collection("futures_fees_info")
        cursor = fees_collection.find({
            "$or": [
                {"合约代码": {"$regex": keyword, "$options": "i"}},
                {"合约名称": {"$regex": keyword, "$options": "i"}},
                {"品种名称": {"$regex": keyword, "$options": "i"}},
            ]
        }).limit(20)
        
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            doc["_source"] = "futures_fees_info"
            results.append(doc)
        
        return {
            "success": True,
            "data": {
                "items": results,
                "total": len(results),
                "keyword": keyword
            }
        }
    except Exception as e:
        logger.error(f"搜索期货失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
