from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException, BackgroundTasks, Body
from fastapi.responses import JSONResponse
import logging
import pandas as pd
import io
import os
import akshare as ak
from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.services.currency_data_service import CurrencyDataService
from app.services.currency_refresh_service import CurrencyRefreshService
from app.config.currency_update_config import get_collection_update_config, get_all_collection_update_configs
from app.utils.task_manager import get_task_manager

router = APIRouter(prefix="/api/currencies", tags=["currencies"])
logger = logging.getLogger("webapi")

@router.get("/config")
async def get_currency_config(current_user: dict = Depends(get_current_user)):
    """Get currency configuration including default API key"""
    return {
        "success": True,
        "data": {
            "default_api_key": os.getenv("CURRENCYSCOOP_API_KEY", "")
        }
    }

@router.get("/collections")
async def list_currencies_collections(current_user: dict = Depends(get_current_user)):
    """Get list of currency collections"""
    collections = [
        {
            "name": "currency_latest",
            "display_name": "货币报价最新数据",
            "description": "货币报价最新数据，包含货币代码、日期、基础货币、比率等",
            "route": "/currencies/collections/currency_latest",
            "fields": ["currency", "date", "base", "rates"],
        },
        {
            "name": "currency_history",
            "display_name": "货币报价历史数据",
            "description": "货币报价历史数据，包含货币代码、日期、基础货币、比率等",
            "route": "/currencies/collections/currency_history",
            "fields": ["currency", "date", "base", "rates"],
        },
        {
            "name": "currency_time_series",
            "display_name": "货币报价时间序列数据",
            "description": "货币报价时间序列数据",
            "route": "/currencies/collections/currency_time_series",
            "fields": [],  # Dynamic columns based on actual data
            "dynamic_columns": True,
        },
        {
            "name": "currency_currencies",
            "display_name": "货币基础信息查询",
            "description": "所有货币的基础信息",
            "route": "/currencies/collections/currency_currencies",
            "fields": ["id", "name", "short_code", "code", "precision", "subunit", "symbol", "symbol_first", "decimal_mark", "thousands_separator"],
        },
        {
            "name": "currency_convert",
            "display_name": "货币转换",
            "description": "实时货币转换数据",
            "route": "/currencies/collections/currency_convert",
            "fields": ["date", "base", "to", "amount", "value"],
        },
    ]
    return {"success": True, "data": collections}

@router.get("/latest/list")
async def list_currency_latest(
    q: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    sort_by: Optional[str] = Query(None),
    sort_dir: str = Query("asc"),
    current_user: dict = Depends(get_current_user),
):
    """Get currency latest data list"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        result = await svc.query_currency_latest(
            q=q, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir
        )
        
        return {
            "success": True, 
            "data": {
                "total": result["total"], 
                "items": result["items"],
                "page": page,
                "page_size": page_size
            }
        }
    except Exception as e:
        logger.error(f"❌ [Currency Latest] List failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/latest/upload")
async def upload_currency_latest(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Import currency latest data from file (CSV/Excel)"""
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return {"success": False, "message": "Unsupported file format"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_latest(df)
        return {"success": True, "message": f"Successfully imported {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency Latest] Upload failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.delete("/latest/clear")
async def clear_currency_latest(
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        collection = db.get_collection("currency_latest")
        res = await collection.delete_many({})
        return {"success": True, "message": f"Cleared {res.deleted_count} records"}
    except Exception as e:
        logger.error(f"❌ [Currency Latest] Clear failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/latest/remote-sync")
async def remote_sync_currency_latest(
    data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
):
    """Sync currency latest data from remote MongoDB"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        
        result = await svc.sync_from_remote_mongodb(
            collection_name="currency_latest",
            remote_host=data.get("remote_host"),
            remote_collection=data.get("remote_collection", "currency_latest"),
            remote_username=data.get("remote_username"),
            remote_password=data.get("remote_password"),
            remote_auth_source=data.get("remote_auth_source", "admin"),
            batch_size=data.get("batch_size", 1000)
        )
        
        return {
            "success": True,
            "message": f"Successfully synced {result['synced']} records from remote",
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ [Currency Latest] Remote sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/latest/sync")
async def sync_currency_latest(
    base: str = Query("USD", description="Base currency"),
    symbols: str = Query("", description="Currency symbols"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    current_user: dict = Depends(get_current_user),
):
    """Sync currency latest data from AKShare (Remote)"""
    try:
        logger.info(f"🔄 [Currency Latest] Syncing data from AKShare (base={base})")
        
        # Call AKShare API
        try:
            # ak.currency_latest returns a DataFrame
            df = ak.currency_latest(base=base, symbols=symbols, api_key=api_key)
        except Exception as api_err:
             return {"success": False, "message": f"API call failed: {str(api_err)}"}
        
        if df is None or df.empty:
            return {"success": False, "message": "No data fetched from API"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_latest(df)
        return {"success": True, "message": f"Successfully synced {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency Latest] Sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/latest/batch-sync")
async def batch_sync_currency_latest(
    api_key: str = Query(..., description="API Key for currencyscoop"),
    current_user: dict = Depends(get_current_user),
):
    """Batch sync currency latest data for USD and CNY only"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()

        # Fixed: Only sync USD and CNY
        bases = ["USD", "CNY"]
        total_saved = 0
        
        for base in bases:
            try:
                logger.info(f"🔄 [Currency Latest] Batch syncing base={base}")
                # Get all currencies with this base
                df = ak.currency_latest(base=base, symbols="", api_key=api_key)
                if df is not None and not df.empty:
                    count = await svc.save_currency_latest(df)
                    total_saved += count
                    logger.info(f"✅ [Currency Latest] Saved {count} records for base={base}")
            except Exception as api_err:
                logger.error(f"❌ [Currency Latest] API call failed for base={base}: {api_err}", exc_info=True)
                continue

        return {
            "success": True,
            "message": f"Batch synced latest quotes for USD and CNY, saved {total_saved} records",
            "data": {"bases": bases, "saved": total_saved},
        }
    except Exception as e:
        logger.error(f"❌ [Currency Latest] Batch sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/latest/update")
async def update_single_currency(
    code: str,
    current_user: dict = Depends(get_current_user),
):
    """Update single currency data (Placeholder - API might not support single without API key)"""
    # Implementing as a placeholder or leveraging sync with symbols=code
    return {"success": False, "message": "Single update requires API Key, please use Sync function"}

@router.get("/history/list")
async def list_currency_history(
    q: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    sort_by: Optional[str] = Query(None),
    sort_dir: str = Query("asc"),
    current_user: dict = Depends(get_current_user),
):
    """Get currency history data list"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        result = await svc.query_currency_history(
            q=q, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir
        )
        
        return {
            "success": True, 
            "data": {
                "total": result["total"], 
                "items": result["items"],
                "page": page,
                "page_size": page_size
            }
        }
    except Exception as e:
        logger.error(f"❌ [Currency History] List failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history/upload")
async def upload_currency_history(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Import currency history data from file"""
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return {"success": False, "message": "Unsupported file format"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_history(df)
        return {"success": True, "message": f"Successfully imported {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency History] Upload failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.delete("/history/clear")
async def clear_currency_history(
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        collection = db.get_collection("currency_history")
        res = await collection.delete_many({})
        return {"success": True, "message": f"Cleared {res.deleted_count} records"}
    except Exception as e:
        logger.error(f"❌ [Currency History] Clear failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/history/remote-sync")
async def remote_sync_currency_history(
    data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
):
    """Sync currency history data from remote MongoDB"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        
        result = await svc.sync_from_remote_mongodb(
            collection_name="currency_history",
            remote_host=data.get("remote_host"),
            remote_collection=data.get("remote_collection", "currency_history"),
            remote_username=data.get("remote_username"),
            remote_password=data.get("remote_password"),
            remote_auth_source=data.get("remote_auth_source", "admin"),
            batch_size=data.get("batch_size", 1000)
        )
        
        return {
            "success": True,
            "message": f"Successfully synced {result['synced']} records from remote",
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ [Currency History] Remote sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/history/sync")
async def sync_currency_history(
    base: str = Query("USD", description="Base currency"),
    date: str = Query(..., description="Date YYYY-MM-DD"),
    symbols: str = Query("", description="Currency symbols"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    current_user: dict = Depends(get_current_user),
):
    """Sync currency history data from AKShare (Remote)"""
    try:
        logger.info(f"🔄 [Currency History] Syncing data from AKShare (base={base}, date={date})")
        
        try:
            df = ak.currency_history(base=base, date=date, symbols=symbols, api_key=api_key)
        except Exception as api_err:
             return {"success": False, "message": f"API call failed: {str(api_err)}"}
        
        if df is None or df.empty:
            return {"success": False, "message": "No data fetched from API"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_history(df)
        return {"success": True, "message": f"Successfully synced {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency History] Sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/history/batch-sync")
async def batch_sync_currency_history(
    base: str = Query("USD", description="Base currency"),
    date: str = Query(..., description="Date YYYY-MM-DD"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    max_codes: int = Query(100, ge=1, le=500),
    batch_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()

        codes_collection = db.get_collection("currency_currencies")
        cursor = codes_collection.find({}, {"code": 1})
        codes = []
        async for doc in cursor:
            code_val = doc.get("code")
            if code_val:
                codes.append(str(code_val).strip())
            if len(codes) >= max_codes:
                break

        if not codes:
            return {"success": False, "message": "No currency codes found in currency_currencies collection"}

        total_saved = 0
        total_batches = 0

        for i in range(0, len(codes), batch_size):
            batch_codes = sorted(set(codes[i:i + batch_size]))
            symbols = ",".join(batch_codes)
            try:
                df = ak.currency_history(base=base, date=date, symbols=symbols, api_key=api_key)
            except Exception as api_err:
                logger.error(f"❌ [Currency History] Batch API call failed: {api_err}", exc_info=True)
                continue
            if df is None or df.empty:
                continue
            count = await svc.save_currency_history(df)
            total_saved += count
            total_batches += 1

        return {
            "success": True,
            "message": f"Batch synced history quotes for {len(codes)} codes, saved {total_saved} records in {total_batches} batches",
            "data": {"codes": len(codes), "saved": total_saved, "batches": total_batches},
        }
    except Exception as e:
        logger.error(f"❌ [Currency History] Batch sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.get("/timeseries/list")
async def list_currency_time_series(
    q: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    sort_by: Optional[str] = Query(None),
    sort_dir: str = Query("asc"),
    current_user: dict = Depends(get_current_user),
):
    """Get currency time series data list"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        result = await svc.query_currency_time_series(
            q=q, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir
        )
        
        return {
            "success": True, 
            "data": {
                "total": result["total"], 
                "items": result["items"],
                "page": page,
                "page_size": page_size
            }
        }
    except Exception as e:
        logger.error(f"❌ [Currency Time Series] List failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/timeseries/upload")
async def upload_currency_time_series(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Import currency time series data from file"""
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return {"success": False, "message": "Unsupported file format"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_time_series(df)
        return {"success": True, "message": f"Successfully imported {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency Time Series] Upload failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.delete("/timeseries/clear")
async def clear_currency_time_series(
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        collection = db.get_collection("currency_time_series")
        res = await collection.delete_many({})
        return {"success": True, "message": f"Cleared {res.deleted_count} records"}
    except Exception as e:
        logger.error(f"❌ [Currency Time Series] Clear failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/timeseries/remote-sync")
async def remote_sync_currency_time_series(
    data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
):
    """Sync currency time series data from remote MongoDB"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        
        result = await svc.sync_from_remote_mongodb(
            collection_name="currency_time_series",
            remote_host=data.get("remote_host"),
            remote_collection=data.get("remote_collection", "currency_time_series"),
            remote_username=data.get("remote_username"),
            remote_password=data.get("remote_password"),
            remote_auth_source=data.get("remote_auth_source", "admin"),
            batch_size=data.get("batch_size", 1000)
        )
        
        return {
            "success": True,
            "message": f"Successfully synced {result['synced']} records from remote",
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ [Currency Time Series] Remote sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/timeseries/sync")
async def sync_currency_time_series(
    base: str = Query("USD", description="Base currency"),
    start_date: str = Query(..., description="Start Date YYYY-MM-DD"),
    end_date: str = Query(..., description="End Date YYYY-MM-DD"),
    symbols: str = Query("", description="Currency symbols"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    current_user: dict = Depends(get_current_user),
):
    """Sync currency time series data from AKShare (Remote)"""
    try:
        logger.info(f"🔄 [Currency Time Series] Syncing data from AKShare (base={base}, start={start_date}, end={end_date})")
        
        try:
            df = ak.currency_time_series(base=base, start_date=start_date, end_date=end_date, symbols=symbols, api_key=api_key)
        except Exception as api_err:
             return {"success": False, "message": f"API call failed: {str(api_err)}"}
        
        if df is None or df.empty:
            return {"success": False, "message": "No data fetched from API"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_time_series(df)
        return {"success": True, "message": f"Successfully synced {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency Time Series] Sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/timeseries/batch-sync")
async def batch_sync_currency_time_series(
    base: str = Query("USD", description="Base currency"),
    start_date: str = Query(..., description="Start Date YYYY-MM-DD"),
    end_date: str = Query(..., description="End Date YYYY-MM-DD"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    max_codes: int = Query(100, ge=1, le=500),
    batch_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()

        codes_collection = db.get_collection("currency_currencies")
        cursor = codes_collection.find({}, {"code": 1})
        codes = []
        async for doc in cursor:
            code_val = doc.get("code")
            if code_val:
                codes.append(str(code_val).strip())
            if len(codes) >= max_codes:
                break

        if not codes:
            return {"success": False, "message": "No currency codes found in currency_currencies collection"}

        total_saved = 0
        total_batches = 0

        for i in range(0, len(codes), batch_size):
            batch_codes = sorted(set(codes[i:i + batch_size]))
            symbols = ",".join(batch_codes)
            try:
                df = ak.currency_time_series(base=base, start_date=start_date, end_date=end_date, symbols=symbols, api_key=api_key)
            except Exception as api_err:
                logger.error(f"❌ [Currency Time Series] Batch API call failed: {api_err}", exc_info=True)
                continue
            if df is None or df.empty:
                continue
            count = await svc.save_currency_time_series(df)
            total_saved += count
            total_batches += 1

        return {
            "success": True,
            "message": f"Batch synced time series quotes for {len(codes)} codes, saved {total_saved} records in {total_batches} batches",
            "data": {"codes": len(codes), "saved": total_saved, "batches": total_batches},
        }
    except Exception as e:
        logger.error(f"❌ [Currency Time Series] Batch sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.get("/currencies/list")
async def list_currency_currencies(
    q: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    sort_by: Optional[str] = Query(None),
    sort_dir: str = Query("asc"),
    current_user: dict = Depends(get_current_user),
):
    """Get currency currencies data list"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        result = await svc.query_currency_currencies(
            q=q, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir
        )
        
        return {
            "success": True, 
            "data": {
                "total": result["total"], 
                "items": result["items"],
                "page": page,
                "page_size": page_size
            }
        }
    except Exception as e:
        logger.error(f"❌ [Currency Currencies] List failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/currencies/upload")
async def upload_currency_currencies(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Import currency currencies data from file"""
    try:
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            return {"success": False, "message": "Unsupported file format"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_currencies(df)
        return {"success": True, "message": f"Successfully imported {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency Currencies] Upload failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.delete("/currencies/clear")
async def clear_currency_currencies(
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        collection = db.get_collection("currency_currencies")
        res = await collection.delete_many({})
        return {"success": True, "message": f"Cleared {res.deleted_count} records"}
    except Exception as e:
        logger.error(f"❌ [Currency Currencies] Clear failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/currencies/remote-sync")
async def remote_sync_currency_currencies(
    data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
):
    """Sync currency currencies data from remote MongoDB"""
    try:
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        
        result = await svc.sync_from_remote_mongodb(
            collection_name="currency_currencies",
            remote_host=data.get("remote_host"),
            remote_collection=data.get("remote_collection", "currency_currencies"),
            remote_username=data.get("remote_username"),
            remote_password=data.get("remote_password"),
            remote_auth_source=data.get("remote_auth_source", "admin"),
            batch_size=data.get("batch_size", 1000)
        )
        
        return {
            "success": True,
            "message": f"Successfully synced {result['synced']} records from remote",
            "data": result
        }
    except Exception as e:
        logger.error(f"❌ [Currency Currencies] Remote sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}

@router.post("/currencies/sync")
async def sync_currency_currencies(
    c_type: str = Query("fiat", description="Currency type"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    code: Optional[str] = Query(None, description="Filter by currency code"),
    current_user: dict = Depends(get_current_user),
):
    """Sync currency currencies data from AKShare (Remote)"""
    try:
        logger.info(f"🔄 [Currency Currencies] Syncing data from AKShare (c_type={c_type})")
        
        try:
            df = ak.currency_currencies(c_type=c_type, api_key=api_key)
        except Exception as api_err:
             return {"success": False, "message": f"API call failed: {str(api_err)}"}
        
        if code:
            try:
                df = df[df["code"].astype(str).str.upper() == code.upper()]
            except Exception as filter_err:
                logger.error(f"❌ [Currency Currencies] Filter by code failed: {filter_err}", exc_info=True)
                return {"success": False, "message": f"Filter by code failed: {filter_err}"}
        
        if df is None or df.empty:
            return {"success": False, "message": "No data fetched from API"}
            
        db = get_mongo_db()
        svc = CurrencyDataService(db)
        await svc.ensure_indexes()
        
        count = await svc.save_currency_currencies(df)
        return {"success": True, "message": f"Successfully synced {count} records"}
        
    except Exception as e:
        logger.error(f"❌ [Currency Currencies] Sync failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}







@router.get("/tool/convert")
async def tool_currency_convert(
    base: str = Query("USD", description="Base currency"),
    to: str = Query("CNY", description="Target currency"),
    amount: str = Query("10000", description="Amount"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    current_user: dict = Depends(get_current_user),
):
    """Real-time currency conversion tool"""
    try:
        import akshare as ak
        import asyncio
        logger.info(f"🔄 [Currency Tool] Converting: {amount} {base} -> {to}")
        
        try:
            # Run blocking AKShare call in thread pool
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                None, 
                lambda: ak.currency_convert(base=base, to=to, amount=amount, api_key=api_key)
            )
        except Exception as api_err:
             return {"success": False, "message": f"API call failed: {str(api_err)}"}
        
        if df is None or df.empty:
            return {"success": False, "message": "No data fetched from API"}
            
        # The result usually contains 'date', 'base', 'to', 'amount', 'value'
        data = df.to_dict(orient="records")[0]
        return {"success": True, "data": data}
        
    except Exception as e:
        logger.error(f"❌ [Currency Tool] Conversion failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


# ============== 统一刷新 API ==============

@router.get("/collections/{collection_name}/update-config")
async def get_currency_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合的更新配置"""
    config = get_collection_update_config(collection_name)
    return {"success": True, "data": config}


@router.post("/collections/{collection_name}/refresh")
async def refresh_currency_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新指定的外汇数据集合
    
    Args:
        collection_name: 集合名称
        params: 更新参数，包含 update_type ('single' 或 'batch') 和其他参数
    """
    try:
        task_manager = get_task_manager()
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"更新外汇集合: {collection_name}"
        )
        
        async def do_refresh():
            db = get_mongo_db()
            refresh_service = CurrencyRefreshService(db)
            await refresh_service.refresh_collection(collection_name, task_id, params)
        
        background_tasks.add_task(do_refresh)
        
        return {"success": True, "data": {"task_id": task_id}}
        
    except Exception as e:
        logger.error(f"❌ [Currency Refresh] Failed to start refresh: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


@router.get("/collections/{collection_name}/refresh/status/{task_id}")
async def get_currency_refresh_task_status(
    collection_name: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取刷新任务状态"""
    try:
        task_manager = get_task_manager()
        task = task_manager.get_task(task_id)
        
        if task is None:
            return {"success": False, "message": f"Task {task_id} not found"}
        
        return {"success": True, "data": task}
        
    except Exception as e:
        logger.error(f"❌ [Currency Refresh] Failed to get task status: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


@router.get("/collections/{collection_name}/data")
async def get_currency_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    current_user: dict = Depends(get_current_user),
):
    """获取集合数据"""
    try:
        db = get_mongo_db()
        refresh_service = CurrencyRefreshService(db)
        
        skip = (page - 1) * page_size
        result = await refresh_service.get_collection_data(
            collection_name, skip=skip, limit=page_size
        )
        
        return {
            "success": True,
            "data": {
                "items": result.get("data", []),
                "total": result.get("total", 0),
                "page": page,
                "page_size": page_size
            }
        }
        
    except Exception as e:
        logger.error(f"❌ [Currency Collection] Failed to get data: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


@router.get("/collections/{collection_name}/overview")
async def get_currency_collection_overview(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合数据概览"""
    try:
        db = get_mongo_db()
        refresh_service = CurrencyRefreshService(db)
        
        result = await refresh_service.get_collection_overview(collection_name)
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [Currency Collection] Failed to get overview: {e}", exc_info=True)
        return {"success": False, "message": str(e)}
