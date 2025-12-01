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

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.fund_refresh_service import FundRefreshService
from app.services.fund_data_service import FundDataService
from app.config.fund_update_config import get_collection_update_config
from app.services.data_sources.funds.provider_registry import (
    get_collection_definitions,
    get_provider_class,
)
from app.schemas.funds import (
    CollectionDataQuery,
    CollectionListResponse,
    CollectionDataResponse,
    CollectionStatsResponse,
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
from app.utils.fund_cache import get_fund_cache


class FundCollectionExportRequest(BaseModel):
    """导出基金集合请求"""

    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"
    tracking_target: Optional[str] = None
    tracking_method: Optional[str] = None
    fund_company: Optional[str] = None

router = APIRouter(prefix="/api/funds", tags=["funds"])
logger = logging.getLogger("webapi")

# 使用改进的缓存管理器
fund_cache = get_fund_cache()


def _get_collection_fields_order(collection_name: str) -> list:
    """
    获取集合的字段顺序，直接从 provider 的 field_info 获取。
    
    优化说明：
    - 移除了硬编码的 COLLECTION_FIELDS 字典
    - 直接从 provider 的 field_info 属性动态获取字段
    - 字段顺序与 provider 中定义的 field_info 顺序一致
    """
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            # 直接从 field_info 提取字段名，保持顺序
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                # 排除系统字段（更新时间、更新人、创建时间、创建人、来源）
                system_fields = {"更新时间", "更新人", "创建时间", "创建人", "来源"}
                fields = [f.get("name") for f in field_info 
                         if f.get("name") and f.get("name") not in system_fields]
                if fields:
                    return fields
    except Exception as e:
        logger.warning(f"从 provider 获取字段信息失败 {collection_name}: {e}")
    
    return []


def _get_provider_field_info(collection_name: str) -> List[Dict[str, Any]]:
    """
    获取 provider 的完整字段信息（包括类型和描述），保持 field_info 的顺序
    
    Returns:
        字段信息列表，每个元素包含 name, type, description
    """
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            # 直接从 field_info 获取完整字段信息，保持顺序
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                return field_info
    except Exception as e:
        logger.warning(f"从 provider 获取字段信息失败 {collection_name}: {e}")
    
    return []


@router.get("/overview")
async def get_funds_overview(current_user: dict = Depends(get_current_user)):
    """获取基金概览数据"""
    try:
        db = get_mongo_db()
        
        # 统计数据
        stats = {
            "total_funds": 0,
            "categories": [],
            "recent_performance": {},
            "message": "基金概览功能正在开发中"
        }
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取基金概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get(
    "/collections",
    response_model=CollectionListResponse,
    summary="获取基金数据集合列表",
    description="获取所有可用的基金数据集合列表，包含集合名称、描述、字段等信息"
)
async def list_fund_collections(
    current_user: dict = Depends(get_current_user)
) -> CollectionListResponse:
    """获取基金数据集合列表"""
    try:
        cache_key = fund_cache._generate_key("fund_collections")
        cached = fund_cache.get(cache_key)
        if cached:
            return CollectionListResponse(success=True, data=cached)

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
                    "route": meta.get("route") or f"/funds/collections/{name}",
                    "fields": fields,
                }
            )

        fund_cache.set(cache_key, collection_items, ttl_seconds=300)
        return CollectionListResponse(success=True, data=collection_items)
    except Exception as e:
        logger.error(f"获取基金集合列表失败: {e}", exc_info=True)
        return CollectionListResponse(success=False, error=str(e))


@router.get("/collections/{collection_name}/update-config")
async def get_fund_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定基金集合的更新配置"""
    try:
        config = get_collection_update_config(collection_name)
        return {
            "success": True,
            "data": config
        }
    except Exception as e:
        logger.error(f"获取基金集合更新配置失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get(
    "/collections/{collection_name}",
    response_model=CollectionDataResponse,
    summary="获取基金集合数据",
    description="分页获取指定基金集合的数据，支持排序和过滤"
)
async def get_fund_collection_data(
    collection_name: str,
    query: CollectionDataQuery = Depends(),
    current_user: dict = Depends(get_current_user),
) -> CollectionDataResponse:
    """获取指定基金集合的数据（分页）"""
    db = get_mongo_db()
    
    # 验证集合是否存在
    supported_collections = [c["name"] for c in get_collection_definitions()]
    if collection_name not in supported_collections:
        raise FundCollectionNotFound(collection_name)
    
    # 动态获取集合（避免硬编码）
    collection = db.get_collection(collection_name)
    
    try:
        # 构建查询条件
        mongo_query = {}
        if query.filter_field and query.filter_value:
            filter_field_stripped = query.filter_field.strip()
            filter_value_stripped = query.filter_value.strip()
            if filter_field_stripped and filter_value_stripped:
                if filter_field_stripped in ["code", "name"]:
                    mongo_query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
                else:
                    mongo_query[filter_field_stripped] = filter_value_stripped
        
        # 添加指数型基金特定筛选
        if collection_name == "fund_info_index_em":
            if query.tracking_target and query.tracking_target != "全部":
                mongo_query["跟踪标的"] = query.tracking_target
            if query.tracking_method and query.tracking_method != "全部":
                mongo_query["跟踪方式"] = query.tracking_method
                
            # 基金公司筛选 (关联查询)
            if query.fund_company and query.fund_company != "全部":
                basic_info_col = db.get_collection("fund_basic_info")
                company_funds = await basic_info_col.find(
                    {"基金公司": query.fund_company}, 
                    {"code": 1, "基金代码": 1}
                ).to_list(None)
                
                codes = []
                for doc in company_funds:
                    if "code" in doc:
                        codes.append(doc["code"])
                    elif "基金代码" in doc:
                        codes.append(doc["基金代码"])
                
                if codes:
                    mongo_query["code"] = {"$in": codes}
                else:
                    mongo_query["code"] = "IMPOSSIBLE_CODE"
        
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
            
            # 首先从 provider 获取完整的字段信息（包括类型和描述）
            provider_field_info = _get_provider_field_info(collection_name)
            
            # 构建实际数据中的字段字典
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
            
            # 按 provider 的 field_info 顺序排列字段
            if provider_field_info:
                # 使用 provider 定义的字段顺序和类型信息
                for field_def in provider_field_info:
                    field_name = field_def.get("name")
                    if field_name and field_name in fields_dict:
                        # 使用 provider 定义的类型和描述，但保留实际数据的示例值
                        field_info = {
                            "name": field_name,
                            "type": field_def.get("type", fields_dict[field_name]["type"]),
                            "description": field_def.get("description", ""),
                            "example": fields_dict[field_name].get("example"),
                        }
                        fields_info.append(field_info)
                        del fields_dict[field_name]
                
                # 添加 provider 中未定义但实际数据中存在的字段（通常是系统字段）
                for field_info in fields_dict.values():
                    fields_info.append(field_info)
            else:
                # 如果没有 provider 定义，使用实际数据的字段顺序
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
        logger.error(f"获取基金集合 {collection_name} 数据失败: {e}", exc_info=True)
        return CollectionDataResponse(success=False, error=str(e))


@router.post(
    "/collections/{collection_name}/export",
    summary="导出基金集合数据",
    description="导出指定基金集合的全部数据到文件（CSV/Excel/JSON）"
)
async def export_fund_collection_data(
    collection_name: str,
    request: CollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出指定基金集合的全部数据到文件"""

    db = get_mongo_db()
    service = FundDataService(db)

    try:
        # 复用列表接口中的过滤构建逻辑
        filters: Dict[str, Any] = {}
        if request.filter_field and request.filter_value:
            field = request.filter_field.strip()
            value = request.filter_value.strip()
            if field and value:
                if field in ["code", "name"]:
                    filters[field] = {"$regex": value, "$options": "i"}
                else:
                    filters[field] = value

        if collection_name == "fund_info_index_em":
            if request.tracking_target and request.tracking_target != "全部":
                filters["跟踪标的"] = request.tracking_target
            if request.tracking_method and request.tracking_method != "全部":
                filters["跟踪方式"] = request.tracking_method

            if request.fund_company and request.fund_company != "全部":
                basic_info_col = db.get_collection("fund_basic_info")
                company_docs = await basic_info_col.find(
                    {"基金公司": request.fund_company}, {"code": 1, "基金代码": 1}
                ).to_list(None)

                codes: List[str] = []
                for doc in company_docs:
                    if "code" in doc:
                        codes.append(doc["code"])
                    elif "基金代码" in doc:
                        codes.append(doc["基金代码"])

                if codes:
                    filters["code"] = {"$in": codes}
                else:
                    filters["code"] = "__NO_MATCH__"

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
            delete=False, suffix=f".{suffix}", prefix="fund-export-"
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
        logger.error(f"导出基金集合 {collection_name} 数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")
@router.get(
    "/collections/{collection_name}/stats",
    response_model=ApiResponse,
    summary="获取基金集合统计信息",
    description="获取指定基金集合的统计信息，包括总数、最新日期、类型分布等"
)
async def get_fund_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
) -> ApiResponse:
    """获取基金集合统计信息"""
    try:
        db = get_mongo_db()
        refresh_service = FundRefreshService(db)
        
        # 检查集合是否支持
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            raise FundCollectionNotFound(collection_name)
        
        # 获取集合统计信息
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
        logger.error(f"获取基金集合统计失败: {e}", exc_info=True)
        return ApiResponse(
            success=False,
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


@router.get("/companies")
async def get_fund_companies(current_user: dict = Depends(get_current_user)):
    """获取所有基金公司列表"""
    try:
        db = get_mongo_db()
        collection = db.get_collection("fund_basic_info")
        companies = await collection.distinct("基金公司")
        # 过滤掉空值
        companies = [c for c in companies if c]
        companies.sort()
        return {"success": True, "data": companies}
    except Exception as e:
        logger.error(f"获取基金公司列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/search")
async def search_funds(
    keyword: str = Query(..., description="搜索关键词"),
    current_user: dict = Depends(get_current_user),
):
    """搜索基金"""
    try:
        db = get_mongo_db()
        collection = db.get_collection("fund_basic_info")
        
        # 按代码或名称搜索
        query = {
            "$or": [
                {"code": {"$regex": keyword, "$options": "i"}},
                {"name": {"$regex": keyword, "$options": "i"}},
            ]
        }
        
        cursor = collection.find(query).limit(20)
        results = []
        
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            results.append(doc)
        
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        logger.error(f"搜索基金失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/analysis/{fund_code}")
async def get_fund_analysis(
    fund_code: str,
    current_user: dict = Depends(get_current_user),
):
    """获取基金分析数据"""
    try:
        db = get_mongo_db()
        
        # 获取基金基础信息
        basic_info = await db.get_collection("fund_basic_info").find_one({"code": fund_code})
        
        if not basic_info:
            return {"success": False, "error": f"未找到基金 {fund_code}"}
        
        if "_id" in basic_info:
            basic_info["_id"] = str(basic_info["_id"])
        
        # 获取净值数据（从 fund_open_fund_daily_em 获取）
        net_value_cursor = db.get_collection("fund_open_fund_daily_em").find(
            {"基金代码": fund_code}
        ).sort("更新时间", -1).limit(100)
        
        net_values = []
        async for doc in net_value_cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            net_values.append(doc)
        
        return {
            "success": True,
            "data": {
                "basic_info": basic_info,
                "net_values": net_values,
                "message": "基金分析功能正在开发中"
            }
        }
    except Exception as e:
        logger.error(f"获取基金分析失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post(
    "/collections/{collection_name}/refresh",
    response_model=RefreshTaskResponse,
    summary="刷新基金数据集合",
    description="创建后台任务刷新指定基金集合的数据"
)
async def refresh_fund_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: RefreshCollectionRequest,
    current_user: dict = Depends(get_current_user),
) -> RefreshTaskResponse:
    """刷新基金数据集合"""
    try:
        logger.info(f"[API refresh] 接收到刷新请求: collection={collection_name}, params={params.dict()}")
        db = get_mongo_db()
        task_manager = get_task_manager()
        
        # 验证集合是否存在
        refresh_service = FundRefreshService(db, current_user)
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            raise FundCollectionNotFound(collection_name)
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"更新基金集合: {collection_name}"
        )
        
        # 在后台异步执行刷新任务
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
        logger.error(f"刷新基金集合失败: {e}", exc_info=True)
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
async def upload_fund_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传基金数据文件"""
    try:
        if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
             return {"success": False, "error": "只支持CSV或Excel文件"}
             
        db = get_mongo_db()
        service = FundDataService(db)
        
        # Read file content
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
async def sync_fund_data(
    collection_name: str,
    sync_config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """远程同步基金数据"""
    try:
        db = get_mongo_db()
        service = FundDataService(db)
        
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
    summary="清空基金数据集合",
    description="清空指定基金集合的所有数据（危险操作，需谨慎使用）"
)
async def clear_fund_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
) -> ClearCollectionResponse:
    """清空基金数据集合（统一使用通用清空方法）"""
    try:
        # 验证集合是否存在
        refresh_service = FundRefreshService(get_mongo_db(), current_user)
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            raise FundCollectionNotFound(collection_name)
        
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        # 统一调用通用清空方法
        deleted_count = await data_service.clear_fund_data(collection_name)
        
        # 清除相关缓存
        fund_cache.invalidate(f"fund_{collection_name}")
        
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
        logger.error(f"清空基金集合失败: {e}", exc_info=True)
        return ClearCollectionResponse(success=False, error=str(e))


@router.post("/collections/fund_etf_dividend_sina/upload")
async def upload_fund_etf_dividend_sina(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传基金累计分红数据文件"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        content = await file.read()
        result = await data_service.import_fund_etf_dividend_sina_from_file(content, file.filename)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"上传基金累计分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_etf_dividend_sina/sync")
async def sync_fund_etf_dividend_sina(
    remote_host: str = Body(..., embed=True),
    batch_size: int = Body(5000, embed=True),
    remote_collection: str = Body(None, embed=True),
    remote_username: str = Body(None, embed=True),
    remote_password: str = Body(None, embed=True),
    remote_auth_source: str = Body(None, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """从远程MongoDB同步基金累计分红数据"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        result = await data_service.sync_fund_etf_dividend_sina_from_remote(
            remote_host=remote_host,
            batch_size=batch_size,
            remote_collection=remote_collection,
            remote_username=remote_username,
            remote_password=remote_password,
            remote_auth_source=remote_auth_source,
        )
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"同步基金累计分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_fh_em/upload")
async def upload_fund_fh_em(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传基金分红数据文件"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        content = await file.read()
        result = await data_service.import_fund_fh_em_from_file(content, file.filename)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"上传基金分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_fh_em/sync")
async def sync_fund_fh_em(
    remote_host: str = Body(..., embed=True),
    batch_size: int = Body(5000, embed=True),
    remote_collection: str = Body(None, embed=True),
    remote_username: str = Body(None, embed=True),
    remote_password: str = Body(None, embed=True),
    remote_auth_source: str = Body(None, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """从远程MongoDB同步基金分红数据"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        result = await data_service.sync_fund_fh_em_from_remote(
            remote_host=remote_host,
            batch_size=batch_size,
            remote_collection=remote_collection,
            remote_username=remote_username,
            remote_password=remote_password,
            remote_auth_source=remote_auth_source,
        )
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"同步基金分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 基金公告人事调整批量更新 API ====================

@router.post("/collections/fund_announcement_personnel_em/update/single")
async def update_single_fund_personnel(
    background_tasks: BackgroundTasks,
    fund_code: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user),
):
    """更新单个基金的公告人事调整数据"""
    try:
        from app.services.fund_announcement_personnel_batch_service import FundAnnouncementPersonnelBatchService
        
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type="update_single_fund_personnel",
            description=f"更新基金 {fund_code} 公告人事调整数据"
        )
        
        # 在后台异步执行
        async def do_update():
            try:
                service = FundAnnouncementPersonnelBatchService(task_manager)
                await service.update_single_fund(task_id, fund_code)
            except Exception as e:
                logger.error(f"后台更新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_update)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"更新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"创建更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_announcement_personnel_em/update/batch")
async def update_batch_fund_personnel(
    background_tasks: BackgroundTasks,
    fund_codes: List[str] = Body(..., embed=True),
    batch_size: int = Body(100, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """批量更新多个基金的公告人事调整数据"""
    try:
        from app.services.fund_announcement_personnel_batch_service import FundAnnouncementPersonnelBatchService
        
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type="update_batch_fund_personnel",
            description=f"批量更新 {len(fund_codes)} 个基金的公告人事调整数据"
        )
        
        # 在后台异步执行
        async def do_update():
            try:
                service = FundAnnouncementPersonnelBatchService(task_manager)
                await service.update_batch_funds(task_id, fund_codes, batch_size)
            except Exception as e:
                logger.error(f"后台更新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_update)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"批量更新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"创建批量更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_announcement_personnel_em/update/incremental")
async def update_incremental_fund_personnel(
    background_tasks: BackgroundTasks,
    limit: int = Body(None, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """增量更新：从fund_name_em获取基金代码并批量更新"""
    try:
        from app.services.fund_announcement_personnel_batch_service import FundAnnouncementPersonnelBatchService
        
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type="update_incremental_fund_personnel",
            description="增量更新基金公告人事调整数据"
        )
        
        # 在后台异步执行
        async def do_update():
            try:
                service = FundAnnouncementPersonnelBatchService(task_manager)
                await service.update_incremental(task_id, limit)
            except Exception as e:
                logger.error(f"后台更新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_update)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"增量更新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"创建增量更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
