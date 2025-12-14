"""
指数数据 API 路由
"""
from datetime import datetime
import logging
import os
import tempfile
from typing import Optional, Dict, Any, List

from fastapi import (
    APIRouter,
    Depends,
    Query,
    BackgroundTasks,
    HTTPException,
    Body,
    UploadFile,
    File,
)
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.index_refresh_service import IndexRefreshService
from app.services.index_data_service import IndexDataService
from app.config.index_update_config import get_collection_update_config
from app.services.data_sources.indexs.provider_registry import (
    get_collection_definitions,
    get_provider_class,
)
from app.schemas.funds import (
    CollectionDataQuery,
    CollectionListResponse,
    CollectionDataResponse,
    RefreshCollectionRequest,
    RefreshTaskResponse,
    CollectionExportRequest,
    ClearCollectionResponse,
    ApiResponse,
)
from app.exceptions.funds import (
    FundCollectionNotFound,
    FundDataUpdateError,
    FundTaskNotFound,
)


router = APIRouter(prefix="/api/indexs", tags=["indexs"])
logger = logging.getLogger("webapi")


def _get_collection_fields_order(collection_name: str) -> list:
    """获取集合的字段顺序，直接从 provider 的 field_info 获取"""
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


@router.get("/overview")
async def get_indexs_overview(current_user: dict = Depends(get_current_user)):
    """获取指数概览数据"""
    try:
        db = get_mongo_db()
        
        stats = {
            "total_indexs": 0,
            "categories": [],
            "message": "指数概览功能正在开发中"
        }
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取指数概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get(
    "/collections",
    response_model=CollectionListResponse,
    summary="获取指数数据集合列表",
    description="获取所有可用的指数数据集合列表"
)
async def list_index_collections(
    current_user: dict = Depends(get_current_user)
) -> CollectionListResponse:
    """获取指数数据集合列表"""
    try:
        collection_items = []
        for meta in get_collection_definitions():
            name = meta.get("name")
            if not name:
                continue

            fields = meta.get("fields") or _get_collection_fields_order(name)
            collection_items.append(
                {
                    "name": name,
                    "display_name": meta.get("display_name") or name,
                    "description": meta.get("description") or "",
                    "route": meta.get("route") or f"/indexs/collections/{name}",
                    "fields": fields,
                }
            )

        return CollectionListResponse(success=True, data=collection_items)
    except Exception as e:
        logger.error(f"获取指数集合列表失败: {e}", exc_info=True)
        return CollectionListResponse(success=False, error=str(e))


@router.get("/collections/{collection_name}/update-config")
async def get_index_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定指数集合的更新配置"""
    try:
        config = get_collection_update_config(collection_name)
        return {
            "success": True,
            "data": config
        }
    except Exception as e:
        logger.error(f"获取指数集合更新配置失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get(
    "/collections/{collection_name}",
    response_model=CollectionDataResponse,
    summary="获取指数集合数据",
    description="分页获取指定指数集合的数据"
)
async def get_index_collection_data(
    collection_name: str,
    query: CollectionDataQuery = Depends(),
    current_user: dict = Depends(get_current_user),
) -> CollectionDataResponse:
    """获取指定指数集合的数据（分页）"""
    db = get_mongo_db()
    
    # 验证集合是否存在
    supported_collections = [c["name"] for c in get_collection_definitions()]
    if collection_name not in supported_collections:
        raise FundCollectionNotFound(collection_name)
    
    collection = db.get_collection(collection_name)
    
    try:
        # 构建查询条件
        mongo_query = {}
        if query.filter_field and query.filter_value:
            filter_field_stripped = query.filter_field.strip()
            filter_value_stripped = query.filter_value.strip()
            if filter_field_stripped and filter_value_stripped:
                mongo_query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
        
        # 获取总数
        total = await collection.count_documents(mongo_query)
        
        # 构建排序
        sort_key = query.sort_by if query.sort_by else "_id"
        sort_direction = -1 if query.sort_dir == "desc" else 1
        
        # 分页查询
        skip = (query.page - 1) * query.page_size
        cursor = collection.find(mongo_query).sort(sort_key, sort_direction).skip(skip).limit(query.page_size)
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
                    elif field_type == "list":
                        field_type = "列表"
                    elif field_type == "dict":
                        field_type = "对象"
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
        
        return CollectionDataResponse(
            success=True,
            data={
                "items": items,
                "total": total,
                "page": query.page,
                "page_size": query.page_size,
                "fields": fields_info,
            }
        )
    except FundCollectionNotFound:
        raise
    except Exception as e:
        logger.error(f"获取指数集合 {collection_name} 数据失败: {e}", exc_info=True)
        return CollectionDataResponse(success=False, error=str(e))


@router.post(
    "/collections/{collection_name}/export",
    summary="导出指数集合数据",
    description="导出指定指数集合的全部数据到文件"
)
async def export_index_collection_data(
    collection_name: str,
    request: CollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出指定指数集合的全部数据到文件"""
    db = get_mongo_db()
    service = IndexDataService(db)

    try:
        filters: Dict[str, Any] = {}
        if request.filter_field and request.filter_value:
            field = request.filter_field.strip()
            value = request.filter_value.strip()
            if field and value:
                filters[field] = {"$regex": value, "$options": "i"}

        export_format = request.file_format.lower()
        if export_format == "excel":
            export_format = "xlsx"

        file_bytes = await service.export_data_to_file(
            collection_name=collection_name,
            file_format=export_format,
            filters=filters,
        )

        suffix_map = {"csv": "csv", "xlsx": "xlsx", "json": "json"}
        suffix = suffix_map.get(export_format, "xlsx")
        filename = f"{collection_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{suffix}"

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{suffix}", prefix="index-export-"
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
        logger.error(f"导出指数集合 {collection_name} 数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@router.get(
    "/collections/{collection_name}/stats",
    response_model=ApiResponse,
    summary="获取指数集合统计信息",
    description="获取指定指数集合的统计信息"
)
async def get_index_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
) -> ApiResponse:
    """获取指数集合统计信息"""
    try:
        db = get_mongo_db()
        refresh_service = IndexRefreshService(db)
        
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            raise FundCollectionNotFound(collection_name)
        
        stats = await refresh_service.get_collection_overview(collection_name)
        stats["collection_name"] = collection_name
        
        return ApiResponse(
            success=True,
            data=stats,
            timestamp=datetime.utcnow().isoformat()
        )
    except FundCollectionNotFound:
        raise
    except Exception as e:
        logger.error(f"获取指数集合统计失败: {e}", exc_info=True)
        return ApiResponse(
            success=False,
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


@router.post(
    "/collections/{collection_name}/refresh",
    response_model=RefreshTaskResponse,
    summary="刷新指数数据集合",
    description="创建后台任务刷新指定指数集合的数据"
)
async def refresh_index_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: RefreshCollectionRequest,
    current_user: dict = Depends(get_current_user),
) -> RefreshTaskResponse:
    """刷新指数数据集合"""
    try:
        logger.info(f"[API refresh] 接收到刷新请求: collection={collection_name}, params={params.dict()}")
        db = get_mongo_db()
        task_manager = get_task_manager()
        
        refresh_service = IndexRefreshService(db, current_user)
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            raise FundCollectionNotFound(collection_name)
        
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"更新指数集合: {collection_name}"
        )
        
        async def do_refresh():
            try:
                await refresh_service.refresh_collection(collection_name, task_id, params.dict())
            except Exception as e:
                logger.error(f"后台刷新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_refresh)
        
        return RefreshTaskResponse(
            success=True,
            data={
                "task_id": task_id,
                "message": f"刷新任务已创建"
            }
        )
    except FundCollectionNotFound:
        raise
    except Exception as e:
        logger.error(f"刷新指数集合失败: {e}", exc_info=True)
        raise FundDataUpdateError(str(e), collection_name)


@router.get(
    "/collections/{collection_name}/refresh/status/{task_id}",
    response_model=ApiResponse,
    summary="获取刷新任务状态",
    description="查询指定刷新任务的执行状态和进度"
)
async def get_refresh_task_status(
    collection_name: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
) -> ApiResponse:
    """获取刷新任务状态"""
    try:
        task_manager = get_task_manager()
        task = task_manager.get_task(task_id)
        
        if not task:
            raise FundTaskNotFound(task_id)
        
        return ApiResponse(
            success=True,
            data=task,
            timestamp=datetime.utcnow().isoformat()
        )
    except FundTaskNotFound:
        raise
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}", exc_info=True)
        return ApiResponse(
            success=False,
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


@router.post("/collections/{collection_name}/upload")
async def upload_index_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传指数数据文件"""
    try:
        if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
             return {"success": False, "error": "只支持CSV或Excel文件"}
             
        db = get_mongo_db()
        service = IndexDataService(db)
        
        content = await file.read()
        filename = file.filename
        
        result = await service.import_data_from_file(collection_name, content, filename)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"上传文件失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/sync")
async def sync_index_data(
    collection_name: str,
    sync_config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """远程同步指数数据"""
    try:
        db = get_mongo_db()
        service = IndexDataService(db)
        
        result = await service.sync_data_from_remote(collection_name, sync_config)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"远程同步失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.delete(
    "/collections/{collection_name}/clear",
    response_model=ClearCollectionResponse,
    summary="清空指数数据集合",
    description="清空指定指数集合的所有数据"
)
async def clear_index_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
) -> ClearCollectionResponse:
    """清空指数数据集合"""
    try:
        refresh_service = IndexRefreshService(get_mongo_db(), current_user)
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            raise FundCollectionNotFound(collection_name)
        
        db = get_mongo_db()
        data_service = IndexDataService(db)
        
        deleted_count = await data_service.clear_index_data(collection_name)
        
        return ClearCollectionResponse(
            success=True,
            data={
                "deleted_count": deleted_count,
                "message": f"成功清空 {deleted_count} 条数据"
            }
        )
    except FundCollectionNotFound:
        raise
    except Exception as e:
        logger.error(f"清空指数集合失败: {e}", exc_info=True)
        return ClearCollectionResponse(success=False, error=str(e))
