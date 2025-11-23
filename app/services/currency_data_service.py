from typing import Optional, Iterable, Dict, Any, List
from datetime import datetime
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from pymongo import UpdateOne
from loguru import logger

class CurrencyDataService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.col_latest = db.get_collection("currency_latest")
        self.col_history = db.get_collection("currency_history")
        self.col_time_series = db.get_collection("currency_time_series")
        self.col_currencies = db.get_collection("currency_currencies")
        self.col_convert = db.get_collection("currency_convert")
        # Further collections will be added here as requirements are implemented

    async def ensure_indexes(self) -> None:
        """Ensure indexes for all currency collections"""
        # currency_latest index
        await self.col_latest.create_index(
            [("currency", 1), ("base", 1), ("date", 1)], 
            unique=True,
            name="currency_base_date_unique"
        )
        await self.col_latest.create_index("currency")
        
        # currency_history index
        await self.col_history.create_index(
            [("currency", 1), ("base", 1), ("date", 1)], 
            unique=True,
            name="history_currency_base_date_unique"
        )
        await self.col_history.create_index("currency")
        await self.col_history.create_index("date")
        
        # currency_time_series index
        await self.col_time_series.create_index("date", unique=True)
        
        # currency_currencies index
        await self.col_currencies.create_index("id", unique=True)
        await self.col_currencies.create_index("code")
        await self.col_currencies.create_index("short_code")
        
        # currency_convert index
        await self.col_convert.create_index(
            [("date", 1), ("base", 1), ("to", 1), ("amount", 1)], 
            unique=True,
            name="convert_unique"
        )

    async def save_currency_convert(self, items: Iterable[Dict[str, Any]]) -> int:
        """Save currency convert data to database"""
        # The API returns a list of dicts like [{"item": "...", "value": ...}, ...]
        # We need to pivot this to a single document for storage
        
        if isinstance(items, pd.DataFrame):
            items = items.to_dict(orient="records")
            
        # If items is a list of key-value pairs, convert to a single dict
        if items and "item" in items[0]:
            doc = {}
            for it in items:
                key = it.get("item")
                val = it.get("value")
                if key == "from": key = "base" # Rename 'from' to 'base' to avoid keyword issues
                if key:
                    doc[key] = val
            
            # Ensure we have necessary fields
            if not doc.get("date") or not doc.get("base") or not doc.get("to"):
                return 0
                
            doc["updated_at"] = datetime.now().isoformat()
            doc["source"] = "akshare"
            
            try:
                res = await self.col_convert.update_one(
                    {
                        "date": doc["date"], 
                        "base": doc["base"], 
                        "to": doc["to"], 
                        "amount": doc.get("amount")
                    },
                    {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                    upsert=True
                )
                return 1 if (res.upserted_count or res.modified_count) else 0
            except Exception as e:
                logger.error(f"❌ [Currency Convert] Write failed: {e}", exc_info=True)
                return 0
        
        # If items is a list of full documents (e.g. from file import)
        ops = []
        for doc in items:
            if not doc.get("date") or not doc.get("base") or not doc.get("to"):
                continue
                
            doc["updated_at"] = datetime.now().isoformat()
            doc["source"] = "akshare"
            
            ops.append(UpdateOne(
                {
                    "date": doc["date"], 
                    "base": doc["base"], 
                    "to": doc["to"], 
                    "amount": doc.get("amount")
                },
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                upsert=True
            ))
            
        if not ops:
            return 0
            
        try:
            res = await self.col_convert.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
        except Exception as e:
            logger.error(f"❌ [Currency Convert] Bulk write failed: {e}", exc_info=True)
            return 0

    async def query_currency_convert(
        self, 
        q: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> Dict[str, Any]:
        """Query currency convert data"""
        filt = {}
        if q:
            # Filter by base or to currency
            filt["$or"] = [
                {"base": {"$regex": q, "$options": "i"}},
                {"to": {"$regex": q, "$options": "i"}}
            ]
            
        total = await self.col_convert.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
            
        skip = max(0, (page - 1) * page_size)
        sort_field = sort_by if sort_by in ["date", "base", "to", "amount", "value"] else "date"
        sort_direction = 1 if sort_dir.lower() == "asc" else -1
        
        cursor = self.col_convert.find(filt).sort(sort_field, sort_direction).skip(skip).limit(page_size)
        items = [doc for doc in await cursor.to_list(length=page_size)]
        for item in items:
            item.pop("_id", None)
            
        return {"total": total, "items": items}

    async def save_currency_currencies(self, items: Iterable[Dict[str, Any]]) -> int:
        """Save currency currencies data to database"""
        ops = []
        
        if isinstance(items, pd.DataFrame):
            items = items.to_dict(orient="records")
            
        for it in items:
            id_val = it.get("id")
            
            if not id_val:
                continue
                
            doc = dict(it)
            doc["updated_at"] = datetime.now().isoformat()
            doc["source"] = "akshare"
            
            # Remove None values
            doc = {k: v for k, v in doc.items() if v is not None}
            
            ops.append(UpdateOne(
                {"id": id_val},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                upsert=True
            ))
            
        if not ops:
            return 0
            
        try:
            res = await self.col_currencies.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
        except Exception as e:
            logger.error(f"❌ [Currency Currencies] Bulk write failed: {e}", exc_info=True)
            return 0

    async def query_currency_currencies(
        self, 
        q: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> Dict[str, Any]:
        """Query currency currencies data"""
        filt = {}
        if q:
            # Filter by name, code or short_code
            filt["$or"] = [
                {"name": {"$regex": q, "$options": "i"}},
                {"code": {"$regex": q, "$options": "i"}},
                {"short_code": {"$regex": q, "$options": "i"}}
            ]
            
        total = await self.col_currencies.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
            
        skip = max(0, (page - 1) * page_size)
        # Default sort by id
        sort_field = sort_by if sort_by in ["id", "name", "code", "short_code"] else "id"
        sort_direction = 1 if sort_dir.lower() == "asc" else -1
        
        cursor = self.col_currencies.find(filt).sort(sort_field, sort_direction).skip(skip).limit(page_size)
        items = [doc for doc in await cursor.to_list(length=page_size)]
        for item in items:
            item.pop("_id", None)
            
        return {"total": total, "items": items}

    async def save_currency_time_series(self, items: Iterable[Dict[str, Any]]) -> int:
        """Save currency time series data to database"""
        import math
        
        ops = []
        
        if isinstance(items, pd.DataFrame):
            logger.info(f"📊 [Currency Time Series] DataFrame shape: {items.shape}, columns: {list(items.columns)[:5]}...")
            
            # Convert DataFrame to records, handling NaN values properly
            # Replace NaN/NA with None first
            items_df = items.copy()
            items_df = items_df.replace({pd.NA: None, pd.NaT: None})
            
            # Convert to dict, fillna will be handled per value
            items = items_df.to_dict(orient="records")
            logger.info(f"📊 [Currency Time Series] Converted to {len(items)} records")
            
        saved_count = 0
        skipped_count = 0
        
        for idx, it in enumerate(items):
            date_val = it.get("date")
            
            if not date_val:
                logger.warning(f"⚠️ [Currency Time Series] Record {idx}: missing date, skipping")
                skipped_count += 1
                continue
            
            # Convert date to string format
            if hasattr(date_val, 'isoformat'):
                date_str = date_val.isoformat()
            elif hasattr(date_val, 'strftime'):
                date_str = date_val.strftime('%Y-%m-%d')
            else:
                date_str = str(date_val)
            
            # Build document with all currency columns
            doc = {}
            for key, value in it.items():
                if key == "date":
                    continue
                    
                # Skip None values
                if value is None:
                    continue
                
                # Skip pandas/numpy NaN values
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        continue
                
                # Convert numpy/pandas types to Python native types
                if hasattr(value, 'item'):
                    try:
                        value = value.item()
                    except (ValueError, AttributeError):
                        pass
                
                # Store numeric values as float
                try:
                    doc[key] = float(value)
                except (ValueError, TypeError):
                    doc[key] = str(value)
                        
            doc["date"] = date_str
            doc["updated_at"] = datetime.now().isoformat()
            doc["source"] = "akshare"
            
            if len(doc) <= 3:  # Only date, updated_at, source - no actual data
                logger.warning(f"⚠️ [Currency Time Series] Record {idx} (date={date_str}): no currency data, skipping")
                skipped_count += 1
                continue
            
            ops.append(UpdateOne(
                {"date": date_str},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                upsert=True
            ))
            
            if idx == 0:
                logger.info(f"📝 [Currency Time Series] Sample record: date={date_str}, currencies={len(doc)-3}")
            
        if not ops:
            logger.warning(f"⚠️ [Currency Time Series] No valid data to save (skipped {skipped_count} records)")
            return 0
            
        try:
            res = await self.col_time_series.bulk_write(ops, ordered=False)
            saved_count = (res.upserted_count or 0) + (res.modified_count or 0)
            logger.info(f"✅ [Currency Time Series] Saved {saved_count} records, skipped {skipped_count}")
            return saved_count
        except Exception as e:
            logger.error(f"❌ [Currency Time Series] Bulk write failed: {e}", exc_info=True)
            # Try to log first failed operation for debugging
            if ops:
                logger.error(f"❌ [Currency Time Series] First operation sample: {ops[0]}")
            return 0

    async def query_currency_time_series(
        self, 
        q: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> Dict[str, Any]:
        """Query currency time series data"""
        import math
        
        filt = {}
        if q:
            # For time series, q usually means filtering by date range or just a specific date
            # But here simple string match on date might suffice for now
            filt["date"] = {"$regex": q, "$options": "i"}
            
        total = await self.col_time_series.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
            
        skip = max(0, (page - 1) * page_size)
        sort_field = sort_by if sort_by == "date" else "date"
        sort_direction = 1 if sort_dir.lower() == "asc" else -1
        
        cursor = self.col_time_series.find(filt).sort(sort_field, sort_direction).skip(skip).limit(page_size)
        items = []
        
        async for doc in cursor:
            doc.pop("_id", None)
            
            # Clean up any NaN or Infinity values that might cause JSON serialization issues
            cleaned_doc = {}
            for key, value in doc.items():
                if value is None:
                    continue
                    
                # Check for NaN or Infinity in float values
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        continue  # Skip invalid float values
                    cleaned_doc[key] = value
                else:
                    cleaned_doc[key] = value
            
            items.append(cleaned_doc)
            
        return {"total": total, "items": items}

    async def save_currency_history(self, items: Iterable[Dict[str, Any]]) -> int:
        """Save currency history data to database"""
        ops = []
        valid_count = 0
        
        if isinstance(items, pd.DataFrame):
            items = items.to_dict(orient="records")
            
        for it in items:
            currency = str(it.get("currency") or "").strip()
            base = str(it.get("base") or "").strip()
            date_val = it.get("date")
            
            if not currency or not base or not date_val:
                continue
            
            date_str = date_val.isoformat() if hasattr(date_val, 'isoformat') else str(date_val)

            doc = {
                "currency": currency,
                "base": base,
                "date": date_str,
                "rates": it.get("rates"),
                "updated_at": datetime.now().isoformat(),
                "source": it.get("source", "akshare")
            }
            doc = {k: v for k, v in doc.items() if v is not None}
            
            ops.append(UpdateOne(
                {"currency": currency, "base": base, "date": date_str},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                upsert=True
            ))
            valid_count += 1
            
        if not ops:
            return 0
            
        try:
            res = await self.col_history.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
        except Exception as e:
            logger.error(f"❌ [Currency History] Bulk write failed: {e}", exc_info=True)
            return 0

    async def query_currency_history(
        self, 
        q: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> Dict[str, Any]:
        """Query currency history data"""
        filt = {}
        if q:
            filt["currency"] = {"$regex": q, "$options": "i"}
            
        total = await self.col_history.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
            
        skip = max(0, (page - 1) * page_size)
        sort_field = sort_by if sort_by in ["currency", "date", "rates"] else "date"
        sort_direction = 1 if sort_dir.lower() == "asc" else -1
        
        cursor = self.col_history.find(filt).sort(sort_field, sort_direction).skip(skip).limit(page_size)
        items = [doc for doc in await cursor.to_list(length=page_size)]
        for item in items:
            item.pop("_id", None)
            
        return {"total": total, "items": items}

    async def save_currency_latest(self, items: Iterable[Dict[str, Any]]) -> int:
        """Save currency latest data to database"""
        ops = []
        valid_count = 0
        skipped_count = 0
        
        # Convert DataFrame to dict records if input is DataFrame
        if isinstance(items, pd.DataFrame):
            items = items.to_dict(orient="records")
            
        for it in items:
            currency = str(it.get("currency") or "").strip()
            base = str(it.get("base") or "").strip()
            date_val = it.get("date")
            
            if not currency or not base or not date_val:
                skipped_count += 1
                continue
            
            # Standardize date to string format if it's datetime
            if hasattr(date_val, 'isoformat'):
                date_str = date_val.isoformat()
            else:
                date_str = str(date_val)

            doc = {
                "currency": currency,
                "base": base,
                "date": date_str,
                "rates": it.get("rates"),
                "updated_at": datetime.now().isoformat(),
                "source": it.get("source", "akshare")
            }
            
            # Remove None values
            doc = {k: v for k, v in doc.items() if v is not None}
            
            # Upsert based on unique key
            ops.append(UpdateOne(
                {"currency": currency, "base": base, "date": date_str},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                upsert=True
            ))
            valid_count += 1
            
        if not ops:
            logger.warning(f"⚠️ [Currency Latest] No valid data to save (skipped {skipped_count} items)")
            return 0
            
        try:
            res = await self.col_latest.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            matched = res.matched_count or 0
            total = upserted + modified + matched
            
            logger.info(f"💾 [Currency Latest] Saved: {total} (New={upserted}, Updated={modified}, Matched={matched})")
            return total
        except Exception as e:
            logger.error(f"❌ [Currency Latest] Bulk write failed: {e}", exc_info=True)
            return 0

    async def query_currency_latest(
        self, 
        q: Optional[str] = None, 
        page: int = 1, 
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc"
    ) -> Dict[str, Any]:
        """Query currency latest data"""
        filt = {}
        if q:
            # Case-insensitive search for currency code
            filt["currency"] = {"$regex": q, "$options": "i"}
            
        total = await self.col_latest.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
            
        skip = max(0, (page - 1) * page_size)
        
        # Sorting
        sort_field = sort_by if sort_by in ["currency", "date", "rates"] else "date"
        sort_direction = 1 if sort_dir.lower() == "asc" else -1
        
        cursor = self.col_latest.find(filt).sort(sort_field, sort_direction).skip(skip).limit(page_size)
        
        items = []
        async for doc in cursor:
            doc.pop("_id", None)
            items.append(doc)
            
        return {"total": total, "items": items}

    async def sync_from_remote_mongodb(
        self,
        collection_name: str,
        remote_host: str,
        remote_collection: str,
        remote_username: Optional[str] = None,
        remote_password: Optional[str] = None,
        remote_auth_source: str = "admin",
        batch_size: int = 1000
    ) -> Dict[str, int]:
        """
        从远程 MongoDB 同步数据到本地集合
        
        Args:
            collection_name: 本地集合名称
            remote_host: 远程MongoDB地址
            remote_collection: 远程集合名称
            remote_username: 远程用户名
            remote_password: 远程密码
            remote_auth_source: 认证库
            batch_size: 批次大小
            
        Returns:
            {"remote_total": int, "synced": int}
        """
        remote_client = None
        try:
            # 构建远程 MongoDB 连接字符串
            if remote_username and remote_password:
                if remote_host.startswith("mongodb://"):
                    # 已经是完整URI，使用原样
                    remote_uri = remote_host
                else:
                    # 构建带认证的URI
                    remote_uri = f"mongodb://{remote_username}:{remote_password}@{remote_host}/?authSource={remote_auth_source}"
            else:
                if remote_host.startswith("mongodb://"):
                    remote_uri = remote_host
                else:
                    remote_uri = f"mongodb://{remote_host}"
            
            logger.info(f"🔄 [Remote Sync] Connecting to remote MongoDB...")
            remote_client = AsyncIOMotorClient(remote_uri, serverSelectionTimeoutMS=5000)
            
            # 尝试连接
            await remote_client.admin.command('ping')
            logger.info(f"✅ [Remote Sync] Connected to remote MongoDB")
            
            # 获取远程数据库和集合（从URI中提取数据库名，或使用默认）
            if "mongodb://" in remote_uri and "/" in remote_uri.split("@")[-1]:
                remote_db_name = remote_uri.split("@")[-1].split("/")[1].split("?")[0]
                if not remote_db_name:
                    remote_db_name = "tradingagents"
            else:
                remote_db_name = "tradingagents"
            
            remote_db = remote_client[remote_db_name]
            remote_col = remote_db[remote_collection]
            
            # 获取本地集合
            local_col = self.db.get_collection(collection_name)
            
            # 统计远程数据量
            remote_total = await remote_col.count_documents({})
            logger.info(f"📊 [Remote Sync] Remote collection has {remote_total} documents")
            
            if remote_total == 0:
                return {"remote_total": 0, "synced": 0}
            
            # 分批同步
            synced_count = 0
            cursor = remote_col.find({}).batch_size(batch_size)
            
            batch = []
            async for doc in cursor:
                doc.pop("_id", None)  # 移除_id字段
                doc["synced_at"] = datetime.now().isoformat()
                batch.append(doc)
                
                if len(batch) >= batch_size:
                    # 批量插入
                    ops = []
                    for item in batch:
                        # 根据集合类型选择唯一键
                        if collection_name in ["currency_latest", "currency_history"]:
                            filter_key = {"currency": item.get("currency"), "base": item.get("base"), "date": item.get("date")}
                        elif collection_name == "currency_time_series":
                            filter_key = {"date": item.get("date")}
                        elif collection_name == "currency_currencies":
                            filter_key = {"id": item.get("id")}
                        elif collection_name == "currency_convert":
                            filter_key = {"date": item.get("date"), "base": item.get("base"), "to": item.get("to")}
                        else:
                            filter_key = item  # 使用全部字段作为唯一键（不推荐）
                        
                        ops.append(UpdateOne(filter_key, {"$set": item}, upsert=True))
                    
                    if ops:
                        result = await local_col.bulk_write(ops, ordered=False)
                        synced_count += (result.upserted_count or 0) + (result.modified_count or 0)
                    
                    batch = []
                    logger.info(f"🔄 [Remote Sync] Synced {synced_count}/{remote_total} documents...")
            
            # 处理剩余批次
            if batch:
                ops = []
                for item in batch:
                    if collection_name in ["currency_latest", "currency_history"]:
                        filter_key = {"currency": item.get("currency"), "base": item.get("base"), "date": item.get("date")}
                    elif collection_name == "currency_time_series":
                        filter_key = {"date": item.get("date")}
                    elif collection_name == "currency_currencies":
                        filter_key = {"id": item.get("id")}
                    elif collection_name == "currency_convert":
                        filter_key = {"date": item.get("date"), "base": item.get("base"), "to": item.get("to")}
                    else:
                        filter_key = item
                    
                    ops.append(UpdateOne(filter_key, {"$set": item}, upsert=True))
                
                if ops:
                    result = await local_col.bulk_write(ops, ordered=False)
                    synced_count += (result.upserted_count or 0) + (result.modified_count or 0)
            
            logger.info(f"✅ [Remote Sync] Completed: {synced_count}/{remote_total} documents synced")
            return {"remote_total": remote_total, "synced": synced_count}
            
        except Exception as e:
            logger.error(f"❌ [Remote Sync] Failed: {e}", exc_info=True)
            raise
        finally:
            if remote_client:
                remote_client.close()
