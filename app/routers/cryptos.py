from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel
import logging
import tempfile
import os
from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db

router = APIRouter(prefix="/api/cryptos", tags=["cryptos"])
logger = logging.getLogger("webapi")


@router.get("/overview")
async def get_cryptos_overview(current_user: dict = Depends(get_current_user)):
    """获取数字货币概览数据"""
    return {"success": True, "data": {"total_cryptos": 0, "message": "数字货币概览功能正在开发中"}}


@router.get("/collections")
async def list_cryptos_collections(current_user: dict = Depends(get_current_user)):
    """获取数字货币数据集合列表"""
    collections = [
        {
            "name": "crypto_prices",
            "display_name": "数字货币价格",
            "description": "主要数字货币的价格数据",
            "route": "/cryptos/collections/crypto_prices",
            "fields": ["symbol", "date", "price", "volume", "market_cap", "change_24h"],
        },
    ]
    return {"success": True, "data": collections}


@router.get("/collections/{collection_name}")
async def get_crypto_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    current_user: dict = Depends(get_current_user),
):
    """获取指定数字货币集合的数据"""
    db = get_mongo_db()
    collection_map = {"crypto_prices": db.get_collection("crypto_prices")}
    collection = collection_map.get(collection_name)
    if collection is None:
        return {"success": False, "error": f"集合 {collection_name} 不存在"}
    return {
        "success": True,
        "data": {"items": [], "total": 0, "page": page, "page_size": page_size, "fields": []},
    }


@router.get("/search")
async def search_cryptos(keyword: str = Query(...), current_user: dict = Depends(get_current_user)):
    """搜索数字货币"""
    return {"success": True, "data": []}


@router.get("/analysis/{crypto_symbol}")
async def get_crypto_analysis(crypto_symbol: str, current_user: dict = Depends(get_current_user)):
    """获取数字货币分析数据"""
    return {"success": True, "data": {"message": "数字货币分析功能正在开发中"}}


# ============ 集合导出功能 ============

class CryptoCollectionExportRequest(BaseModel):
    """导出数字货币集合请求"""
    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"


@router.post("/collections/{collection_name}/export")
async def export_crypto_collection_data(
    collection_name: str,
    request: CryptoCollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出指定数字货币集合的全部数据到文件"""
    from app.services.collection_export_service import CollectionExportService

    db = get_mongo_db()
    service = CollectionExportService(db)

    try:
        filters: Dict[str, Any] = {}
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

        file_bytes = await service.export_to_file(
            collection_name=collection_name,
            file_format=export_format,
            filters=filters,
        )

        suffix_map = {"csv": "csv", "xlsx": "xlsx", "json": "json"}
        suffix = suffix_map.get(export_format, "xlsx")
        filename = f"{collection_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{suffix}"

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{suffix}", prefix="crypto-export-"
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
        logger.error(f"导出数字货币集合 {collection_name} 数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")
