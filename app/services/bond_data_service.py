from typing import Optional, Iterable, Dict, Any
from datetime import datetime
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne


class BondDataService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.col_basic = db.get_collection("bond_basic_info")
        self.col_daily = db.get_collection("bond_daily")
        self.col_curve = db.get_collection("yield_curve_daily")
        self.col_events = db.get_collection("bond_events")
        self.col_spot = db.get_collection("bond_spot_quotes")
        self.col_indices = db.get_collection("bond_indices_daily")
        self.col_us_yield = db.get_collection("us_yield_daily")
        self.col_cb_profiles = db.get_collection("bond_cb_profiles")
        self.col_buybacks = db.get_collection("bond_buybacks")
        # 未覆盖端点的集合
        self.col_issues = db.get_collection("bond_issues")
        self.col_cb_adjustments = db.get_collection("bond_cb_adjustments")
        self.col_cb_redeems = db.get_collection("bond_cb_redeems")
        self.col_cb_summary = db.get_collection("bond_cb_summary")
        self.col_cb_valuation = db.get_collection("bond_cb_valuation_daily")
        self.col_cb_comparison = db.get_collection("bond_cb_comparison")
        self.col_spot_quote_detail = db.get_collection("bond_spot_quote_detail")
        self.col_spot_deals = db.get_collection("bond_spot_deals")
        self.col_deal_summary = db.get_collection("bond_deal_summary")
        self.col_cash_summary = db.get_collection("bond_cash_summary")
        self.col_nafmii = db.get_collection("bond_nafmii_debts")
        self.col_info_cm = db.get_collection("bond_info_cm")
        self.col_curve_map = db.get_collection("yield_curve_map")
        self.col_buybacks_hist = db.get_collection("bond_buybacks_hist")
        self.col_cb_list_jsl = db.get_collection("bond_cb_list_jsl")
        self.col_cov_list = db.get_collection("bond_cov_list")
        self.col_minute = db.get_collection("bond_minute_quotes")

    async def _safe_create_index(self, collection, index_spec, unique=False, sparse=False, name=None):
        """安全创建索引，如果索引已存在则跳过"""
        try:
            # 如果没有指定名称，尝试从索引规范生成
            if name is None:
                if isinstance(index_spec, list):
                    # 复合索引
                    name_parts = [f"{field}_{direction}" for field, direction in index_spec]
                    name = "_".join(name_parts)
                else:
                    # 单字段索引
                    name = f"{index_spec}_1"
            
            # 检查索引是否已存在
            existing_indexes = await collection.list_indexes().to_list(length=None)
            for idx in existing_indexes:
                if idx.get("name") == name:
                    # 检查索引定义是否匹配
                    idx_keys = list(idx.get("key", {}).keys())
                    if isinstance(index_spec, list):
                        expected_keys = [field for field, _ in index_spec]
                    else:
                        expected_keys = [index_spec]
                    
                    idx_unique = idx.get("unique", False)
                    idx_sparse = idx.get("sparse", False)
                    
                    # 如果键匹配且属性匹配，则跳过
                    if idx_keys == expected_keys and idx_unique == unique and idx_sparse == sparse:
                        return
                    # 如果键匹配但属性不匹配，需要删除旧索引
                    elif idx_keys == expected_keys:
                        try:
                            await collection.drop_index(name)
                        except Exception as drop_err:
                            pass  # 忽略删除失败
            
            # 创建索引
            if isinstance(index_spec, list):
                await collection.create_index(index_spec, unique=unique, sparse=sparse, name=name)
            else:
                await collection.create_index(index_spec, unique=unique, sparse=sparse, name=name)
        except Exception as e:
            # 忽略索引已存在的错误和索引冲突错误
            import logging
            logger = logging.getLogger("webapi")
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["already exists", "duplicate key", "indexkeyspecsconflict", "index key specs conflict"]):
                # 如果是索引冲突，尝试删除旧索引并重新创建
                try:
                    if name:
                        await collection.drop_index(name)
                        # 重新创建索引
                        if isinstance(index_spec, list):
                            await collection.create_index(index_spec, unique=unique, sparse=sparse, name=name)
                        else:
                            await collection.create_index(index_spec, unique=unique, sparse=sparse, name=name)
                except Exception as retry_err:
                    # 如果重试也失败，记录警告但继续
                    logger.warning(f"⚠️ 处理索引冲突后重试创建失败: {retry_err}")
            else:
                logger.warning(f"⚠️ 创建索引失败: {e}")

    async def ensure_indexes(self) -> None:
        await self.col_basic.create_index("code", unique=True)
        await self.col_basic.create_index("category")
        await self.col_basic.create_index("maturity_date")
        await self.col_basic.create_index("exchange")
        await self.col_basic.create_index("list_date")
        await self.col_basic.create_index("coupon_rate")
        await self.col_basic.create_index("name")
        await self.col_daily.create_index([("code", 1), ("date", 1)], unique=True)
        # 收益率曲线索引：使用 (date, tenor, curve_name, yield_type?) 作为唯一键
        # curve_name 为空字符串表示未分类的曲线
        # yield_type 可选，用于区分到期收益率、即期收益率等
        await self._safe_create_index(
            self.col_curve,
            [("date", 1), ("tenor", 1), ("curve_name", 1), ("yield_type", 1)],
            unique=True,
            sparse=True,
            name="date_1_tenor_1_curve_name_1_yield_type_1"
        )
        await self._safe_create_index(
            self.col_curve,
            [("date", 1), ("tenor", 1), ("curve_name", 1)],
            unique=True,
            name="date_1_tenor_1_curve_name_1"
        )
        await self.col_curve.create_index("date")
        await self.col_curve.create_index("curve_name")
        # 注意：这个非唯一索引可能与之前的唯一索引冲突，使用安全创建方法
        await self._safe_create_index(
            self.col_curve,
            [("date", 1), ("tenor", 1)],
            unique=False,
            name="date_1_tenor_1_query"
        )
        await self.col_events.create_index([("code", 1), ("date", 1), ("event_type", 1)], unique=True)
        await self.col_spot.create_index([("code", 1), ("timestamp", 1), ("category", 1)], unique=True)
        await self.col_indices.create_index([("index_id", 1), ("date", 1)], unique=True)
        # us_yield 集合的索引可能与其他集合冲突，使用安全创建
        await self._safe_create_index(
            self.col_us_yield,
            [("date", 1), ("tenor", 1)],
            unique=True,
            name="date_1_tenor_1"
        )
        await self.col_cb_profiles.create_index("code", unique=True)
        await self.col_buybacks.create_index([("exchange", 1), ("date", 1), ("code", 1)], unique=True)
        # 新增索引
        await self.col_issues.create_index([("issue_type", 1), ("code", 1), ("date", 1)], unique=True)
        await self.col_cb_adjustments.create_index([("code", 1), ("date", 1)], unique=True)
        await self.col_cb_redeems.create_index([("code", 1), ("date", 1)], unique=True)
        await self.col_cb_summary.create_index("code", unique=True)
        await self.col_cb_valuation.create_index([("code", 1), ("date", 1)], unique=True)
        await self.col_cb_comparison.create_index([("date", 1), ("code", 1)], unique=True)
        await self.col_spot_quote_detail.create_index([("code", 1), ("timestamp", 1), ("报价机构", 1)], unique=True)
        await self.col_spot_deals.create_index([("code", 1), ("timestamp", 1)], unique=True)
        await self.col_deal_summary.create_index([("date", 1), ("债券类型", 1)], unique=True)
        await self.col_cash_summary.create_index([("date", 1), ("债券现货", 1)], unique=True)
        # NAFMII 使用注册通知书文号作为唯一标识（部分记录无 reg_no 时仍可写入，但建议数据源尽量提供）
        await self._safe_create_index(self.col_nafmii, "reg_no", unique=True, sparse=True, name="reg_no_1")
        await self.col_info_cm.create_index("code")
        # 唯一索引：每个债券的每个接口只有一条记录
        await self.col_info_cm.create_index([("code", 1), ("endpoint", 1)], unique=True)
        await self.col_curve_map.create_index("date", unique=True)
        await self.col_buybacks_hist.create_index([("exchange", 1), ("date", 1)], unique=True)
        await self.col_cb_list_jsl.create_index("code", unique=True)
        await self.col_cov_list.create_index("code", unique=True)
        # 分钟数据索引：使用 (code, datetime, period) 作为唯一键
        await self.col_minute.create_index([("code", 1), ("datetime", 1), ("period", 1)], unique=True)
        await self.col_minute.create_index("code")
        await self.col_minute.create_index("datetime")
        # 分钟数据的查询索引，可能与唯一索引冲突，使用安全创建
        await self._safe_create_index(
            self.col_minute,
            [("code", 1), ("datetime", 1)],
            unique=False,
            name="code_1_datetime_1_query"
        )

    async def save_yield_curve(self, df: pd.DataFrame) -> int:
        """保存收益率曲线数据到数据库（过滤非数值数据）"""
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            logger.warning("⚠️ [收益率曲线保存] DataFrame为空")
            return 0
        
        ops = []
        valid_count = 0
        skipped_count = 0
        
        for _, r in df.iterrows():
            try:
                date_val = r.get("date")
                tenor_val = r.get("tenor")
                yield_val = r.get("yield")
                
                # 验证日期
                if pd.isna(date_val) or not date_val:
                    skipped_count += 1
                    continue
                
                # 验证期限（tenor）
                if pd.isna(tenor_val) or not tenor_val:
                    skipped_count += 1
                    continue
                
                # 验证收益率值（yield）- 必须是数值
                if pd.isna(yield_val):
                    skipped_count += 1
                    continue
                
                # 尝试转换为浮点数
                try:
                    # 如果已经是数值类型，直接转换
                    if isinstance(yield_val, (int, float)):
                        yield_float = float(yield_val)
                    elif isinstance(yield_val, str):
                        # 尝试转换为浮点数
                        # 如果包含非数字字符（比如中文），会抛出异常
                        yield_float = float(yield_val.strip())
                    else:
                        # 尝试强制转换
                        yield_float = float(yield_val)
                    
                    # 验证是否为有效数值（不是 NaN 或 Inf）
                    if pd.isna(yield_float) or not pd.isfinite(yield_float):
                        skipped_count += 1
                        continue
                        
                except (ValueError, TypeError) as e:
                    # 无法转换为数值，跳过这条记录
                    skipped_count += 1
                    logger.debug(f"⚠️ [收益率曲线保存] 跳过非数值数据: date={date_val}, tenor={tenor_val}, yield={yield_val}, error={e}")
                    continue
                
                # 构建文档（包含曲线名称，如果存在）
                doc = {
                    "date": str(date_val),
                    "tenor": str(tenor_val).strip(),
                    "yield": yield_float,
                    "source": "akshare",
                }
                
                # 如果存在曲线名称，也保存
                if "curve_name" in r:
                    curve_name = r.get("curve_name")
                    if curve_name and not pd.isna(curve_name):
                        doc["curve_name"] = str(curve_name).strip()
                
                # 如果存在收益率类型，也保存（用于区分到期收益率、即期收益率等）
                if "yield_type" in r:
                    yield_type = r.get("yield_type")
                    if yield_type and not pd.isna(yield_type):
                        doc["yield_type"] = str(yield_type).strip()
                
                # 使用 (date, tenor, curve_name, yield_type?) 作为唯一键
                # 如果没有 curve_name，使用空字符串作为默认值
                unique_key = {
                    "date": doc["date"],
                    "tenor": doc["tenor"],
                    "curve_name": doc.get("curve_name", "")
                }
                # 如果有 yield_type，也加入到唯一键中
                if "yield_type" in doc:
                    unique_key["yield_type"] = doc["yield_type"]
                
                ops.append(
                    UpdateOne(
                        unique_key,
                        {"$set": doc},
                        upsert=True
                    )
                )
                valid_count += 1
                
            except Exception as e:
                skipped_count += 1
                logger.warning(f"⚠️ [收益率曲线保存] 处理行数据失败: {e}, row={dict(r)}")
                continue
        
        if not ops:
            logger.warning(f"⚠️ [收益率曲线保存] 没有有效数据可保存（跳过 {skipped_count} 条无效数据，总计 {len(df)} 条）")
            return 0
        
        try:
            # 执行批量写入
            res = await self.col_curve.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            total_saved = upserted + modified
            
            logger.info(f"💾 [收益率曲线保存] 批量写入完成: 新增={upserted}, 更新={modified}, 总计={total_saved}, 有效数据={valid_count}, 跳过={skipped_count}, 总行数={len(df)}")
            
            return total_saved
        except Exception as e:
            logger.error(f"❌ [收益率曲线保存] 批量写入失败: {e}", exc_info=True)
            return 0

    async def save_bond_daily(self, code: str, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            doc = {k: r.get(k) for k in df.columns}
            doc["code"] = code
            doc["date"] = str(doc.get("date"))
            ops.append(
                UpdateOne({"code": doc["code"], "date": doc["date"]}, {"$set": doc}, upsert=True)
            )
        if ops:
            res = await self.col_daily.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_basic_list(self, items: Iterable[Dict[str, Any]]) -> int:
        """保存债券基础信息列表到数据库（使用code作为唯一键，存在则更新，不存在则插入）"""
        import logging
        logger = logging.getLogger("webapi")
        
        ops = []
        valid_count = 0
        skipped_count = 0
        
        for it in items:
            code = str(it.get("code") or "").strip()
            if not code:
                skipped_count += 1
                continue
            
            # 规范化code（确保格式一致）
            from tradingagents.utils.instrument_validator import normalize_bond_code
            norm = normalize_bond_code(code)
            code_std = norm.get("code_std") or code
            
            # 构建文档，移除None值
            doc = {
                "code": code_std,
                "name": it.get("name"),
                "exchange": it.get("exchange"),
                "category": (it.get("category") or "").lower() or None,
                "issuer": it.get("issuer"),
                "list_date": str(it.get("list_date")) if it.get("list_date") else None,
                "maturity_date": str(it.get("maturity_date")) if it.get("maturity_date") else None,
                "coupon_rate": it.get("coupon_rate"),
                "type": it.get("type"),
                "raw_code": it.get("raw_code"),
                "source": it.get("source", "akshare"),
                "updated_at": datetime.now().isoformat(),  # 添加更新时间
            }
            
            # 移除None值，避免覆盖已有字段为None
            doc = {k: v for k, v in doc.items() if v is not None}
            
            # 使用code作为唯一键，存在则更新，不存在则插入
            ops.append(UpdateOne(
                {"code": code_std},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now().isoformat()}},
                upsert=True
            ))
            valid_count += 1
        
        if not ops:
            logger.warning(f"⚠️ [债券数据保存] 没有有效数据可保存（跳过 {skipped_count} 条无效数据）")
            return 0
        
        try:
            # 执行批量写入
            res = await self.col_basic.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            matched = res.matched_count or 0
            
            # 统计处理的数据数量：
            # - upserted_count: 新插入的数据
            # - modified_count: 更新的数据
            # - matched_count: 匹配到的数据（即使没有修改也会被计数）
            # 如果 matched_count > (upserted + modified)，说明有些数据已存在且无需更新
            total_processed = upserted + modified
            # 如果 matched_count 大于 processed，说明有些数据已存在但没有变化
            if matched > total_processed:
                # 实际处理的数量应该包括已存在但未更新的数据
                total_processed = matched
            
            logger.info(f"💾 [债券数据保存] 批量写入完成: 新增={upserted}, 更新={modified}, 匹配={matched}, 总计={total_processed}, 有效数据={valid_count}, 跳过={skipped_count}")
            
            # 如果保存数量异常，记录警告
            if total_processed == 0 and valid_count > 0:
                logger.warning(f"⚠️ [债券数据保存] 警告：有 {valid_count} 条有效数据，但保存数量为0，可能存在数据格式问题")
            
            return total_processed if total_processed > 0 else (upserted + modified)
        except Exception as e:
            logger.error(f"❌ [债券数据保存] 批量写入失败: {e}", exc_info=True)
            return 0

    async def query_basic_list(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        exchange: Optional[str] = None,
        only_not_matured: bool = False,
        page: int = 1,
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_dir: str = "asc",
    ) -> Dict[str, Any]:
        filt: Dict[str, Any] = {}
        if q:
            q_regex = {"$regex": q, "$options": "i"}
            filt["$or"] = [{"code": q_regex}, {"name": q_regex}]
        if category:
            filt["category"] = str(category).lower()
        if exchange:
            filt["exchange"] = str(exchange).upper()
        # 仅对利率债启用未到期过滤
        if only_not_matured and (not category or str(category).lower() == "interest"):
            try:
                import datetime as _dt
                today = _dt.datetime.utcnow().strftime("%Y-%m-%d")
            except Exception:
                today = "1970-01-01"
            filt["maturity_date"] = {"$gte": today}

        total = await self.col_basic.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
        skip = max(0, (page - 1) * page_size)
        allowed = {"code", "name", "maturity_date", "list_date", "coupon_rate"}
        field = (sort_by or "code").lower()
        if field not in allowed:
            field = "code"
        direc = 1 if str(sort_dir).lower() != "desc" else -1
        cursor = self.col_basic.find(filt).sort([(field, direc)]).skip(skip).limit(page_size)
        items = []
        async for doc in cursor:
            # 移除 _id 字段，避免序列化问题
            if "_id" in doc:
                doc.pop("_id", None)
            items.append(doc)
        return {"total": total, "items": items}

    async def save_spot_quotes(self, df: pd.DataFrame, category: str) -> int:
        """保存债券现货报价数据（根据AKShare接口字段结构映射）"""
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            return 0
        
        ops = []
        valid_count = 0
        skipped_count = 0
        
        for _, r in df.iterrows():
            try:
                # 提取代码（支持多种字段名）
                code = str(r.get("code") or r.get("债券代码") or r.get("可转债代码") or r.get("代码") or r.get("symbol") or "").strip()
                if not code:
                    skipped_count += 1
                    continue
                
                # 规范化代码
                from tradingagents.utils.instrument_validator import normalize_bond_code
                norm = normalize_bond_code(code)
                code_std = norm.get("code_std") or code
                
                # 提取时间戳
                timestamp = (
                    r.get("timestamp") or r.get("ticktime") or 
                    r.get("time") or r.get("日期") or 
                    r.get("date") or datetime.now().strftime("%H:%M:%S")
                )
                timestamp = str(timestamp).strip()
                
                # 字段映射表：AKShare字段 -> 标准字段
                field_mapping = {
                    # 价格相关
                    "最新价": "latest_price",
                    "trade": "latest_price",
                    "price": "latest_price",
                    # 涨跌相关
                    "涨跌额": "change",
                    "pricechange": "change",
                    "涨跌幅": "change_percent",
                    "changepercent": "change_percent",
                    # 买卖价
                    "买入": "buy",
                    "卖出": "sell",
                    # 昨收和今开
                    "昨收": "prev_close",
                    "preclose": "prev_close",
                    "今开": "open",
                    "open": "open",
                    # 最高最低
                    "最高": "high",
                    "high": "high",
                    "最低": "low",
                    "low": "low",
                    # 成交相关
                    "成交量": "volume",
                    "volume": "volume",
                    "成交额": "amount",
                    "amount": "amount",
                    # 名称
                    "名称": "name",
                    "name": "name",
                }
                
                # 构建标准文档
                doc = {
                    "code": code_std,
                    "timestamp": timestamp,
                    "category": category,
                    "source": "akshare",
                }
                
                # 映射字段
                for ak_field, std_field in field_mapping.items():
                    if ak_field in r.index or ak_field in r:
                        value = r.get(ak_field)
                        if value is not None and not pd.isna(value):
                            doc[std_field] = value
                
                # 如果name字段还未设置，尝试从其他字段获取
                if "name" not in doc:
                    name = str(r.get("名称") or r.get("name") or "").strip()
                    if name:
                        doc["name"] = name
                
                # 移除None值
                doc = {k: v for k, v in doc.items() if v is not None}
                
                # 使用 (code, timestamp, category) 作为唯一键
                ops.append(
                    UpdateOne(
                        {"code": code_std, "timestamp": timestamp, "category": category},
                        {"$set": doc},
                        upsert=True
                    )
                )
                valid_count += 1
                
            except Exception as e:
                skipped_count += 1
                logger.warning(f"⚠️ [现货报价保存] 处理行数据失败: {e}")
                continue
        
        if not ops:
            logger.warning(f"⚠️ [现货报价保存] 没有有效数据可保存（跳过 {skipped_count} 条）")
            return 0
        
        try:
            res = await self.col_spot.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            total_saved = upserted + modified
            
            logger.info(f"💾 [现货报价保存] 批量写入完成: 新增={upserted}, 更新={modified}, 总计={total_saved}, 有效={valid_count}, 跳过={skipped_count}")
            
            return total_saved
        except Exception as e:
            logger.error(f"❌ [现货报价保存] 批量写入失败: {e}", exc_info=True)
            return 0

    async def save_indices(self, df: pd.DataFrame, index_id: str, value_column: str = "value") -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            date = str(r.get("date"))
            val = r.get(value_column)
            doc = {"index_id": index_id, "date": date, value_column: val, "source": "akshare"}
            ops.append(UpdateOne({"index_id": index_id, "date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_indices.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_us_yields(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            doc = {
                "date": str(r.get("date")),
                "tenor": r.get("tenor"),
                "yield": None if pd.isna(r.get("yield")) else float(r.get("yield")),
                "source": "akshare",
            }
            ops.append(UpdateOne({"date": doc["date"], "tenor": doc["tenor"]}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_us_yield.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cb_profiles(self, profiles: Iterable[Dict[str, Any]]) -> int:
        ops = []
        for p in profiles:
            code = p.get("code")
            if not code:
                continue
            ops.append(UpdateOne({"code": code}, {"$set": p}, upsert=True))
        if ops:
            res = await self.col_cb_profiles.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_buybacks(self, df: pd.DataFrame, exchange: str) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            doc = r.to_dict()
            doc["exchange"] = exchange
            date = str(doc.get("date") or doc.get("日期") or doc.get("公告日期") or "")
            code = str(doc.get("code") or doc.get("证券代码") or doc.get("债券代码") or "").strip()
            if date:
                doc["date"] = date
            if code:
                doc["code"] = code
            ops.append(
                UpdateOne({"exchange": exchange, "date": doc.get("date"), "code": doc.get("code")}, {"$set": doc}, upsert=True)
            )
        if ops:
            res = await self.col_buybacks.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    # ========== 通用辅助 ==========
    @staticmethod
    def _norm_code(row: dict) -> str:
        for k in (
            "code",
            "证券代码",
            "债券代码",
            "可转债代码",
            "查询代码",
            "bondCode",
            "symbol",
            "代码",
        ):
            v = row.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
        return ""

    @staticmethod
    def _norm_date(row: dict) -> str:
        for k in ("date", "日期", "数据日期", "公告日期", "list_date", "上市日期"):
            v = row.get(k)
            if v is not None and str(v).strip():
                try:
                    import pandas as pd  # local import
                    return pd.to_datetime(v).strftime("%Y-%m-%d")
                except Exception:
                    return str(v).strip()
        return ""

    # ========== CNINFO 发行 ==========
    async def save_cninfo_issues(self, df: pd.DataFrame, issue_type: str, endpoint: str) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            date = self._norm_date(row)
            doc = row
            doc.update({"issue_type": issue_type, "endpoint": endpoint, "code": code, "date": date, "source": "akshare"})
            filt = {"issue_type": issue_type, "endpoint": endpoint, "code": code, "date": date}
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_issues.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    # ========== 可转债事件/估值 ==========
    async def save_cb_adjustments(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            date = self._norm_date(row)
            filt = {"code": code, "date": date}
            doc = row
            doc.update({"code": code, "date": date, "source": "akshare"})
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cb_adjustments.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cb_redeems(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            date = self._norm_date(row)
            filt = {"code": code, "date": date}
            doc = row
            doc.update({"code": code, "date": date, "source": "akshare"})
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cb_redeems.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cb_summary(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            filt = {"code": code}
            doc = row
            doc.update({"code": code, "source": "akshare"})
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cb_summary.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cb_valuation(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            date = self._norm_date(row)
            filt = {"code": code, "date": date}
            doc = row
            doc.update({"code": code, "date": date, "source": "akshare"})
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cb_valuation.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cb_comparison(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            code = self._norm_code(row)
            if not code:
                code = str(row.get("债券简称") or row.get("名称") or "").strip()
            filt = {"date": date, "code": code}
            doc = row
            doc.update({"date": date, "code": code, "source": "akshare"})
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cb_comparison.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    # ========== 报价/成交/汇总 ==========
    async def save_spot_quote_detail(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            if not code:
                code = str(row.get("债券简称") or row.get("名称") or row.get("报价品种") or "").strip()
            ts = str(row.get("timestamp") or row.get("time") or row.get("时间") or row.get("日期") or "")
            doc = row
            dealer = str(row.get("报价机构") or "").strip()
            doc.update({"code": code, "timestamp": ts, "source": "akshare"})
            if dealer:
                ops.append(UpdateOne({"code": code, "timestamp": ts, "报价机构": dealer}, {"$set": doc}, upsert=True))
            else:
                ops.append(UpdateOne({"code": code, "timestamp": ts}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_spot_quote_detail.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_spot_deals(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            if not code:
                code = str(row.get("债券简称") or row.get("名称") or row.get("报价品种") or "").strip()
            ts = str(row.get("timestamp") or row.get("time") or row.get("时间") or row.get("日期") or "")
            doc = row
            doc.update({"code": code, "timestamp": ts, "source": "akshare"})
            ops.append(UpdateOne({"code": code, "timestamp": ts}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_spot_deals.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_deal_summary(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            doc = row
            doc.update({"date": date, "source": "akshare"})
            bt = row.get("债券类型")
            if bt is not None:
                ops.append(UpdateOne({"date": date, "债券类型": bt}, {"$set": doc}, upsert=True))
            else:
                ops.append(UpdateOne({"date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_deal_summary.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cash_summary(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            doc = row
            doc.update({"date": date, "source": "akshare"})
            ops.append(UpdateOne({"date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cash_summary.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    # ========== NAFMII / 中债信息 ==========
    async def save_nafmii(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            date = self._norm_date(row)
            doc = row
            reg_no = str(row.get("注册通知书文号") or row.get("reg_no") or "").strip()
            doc.update({"code": code, "date": date, "source": "akshare"})
            if reg_no:
                doc["reg_no"] = reg_no
                filt = {"reg_no": reg_no}
            else:
                # 回退到名称+日期+code 的组合
                filt = {"code": code, "date": date, "债券名称": row.get("债券名称")}
            ops.append(UpdateOne(filt, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_nafmii.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_info_cm(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            doc = row
            doc.update({"code": code, "source": "akshare", "endpoint": "bond_info_cm"})
            ops.append(UpdateOne({"code": code, "endpoint": "bond_info_cm"}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_info_cm.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_yield_curve_map(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            doc = row
            doc.update({"date": date, "source": "akshare"})
            ops.append(UpdateOne({"date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_curve_map.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_buybacks_history(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            exch = str(row.get("exchange") or row.get("交易所") or "").strip()
            doc = row
            doc.update({"date": date, "exchange": exch, "source": "akshare"})
            ops.append(UpdateOne({"exchange": exch, "date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_buybacks_hist.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cb_list_jsl(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            doc = row
            doc.update({"code": code, "source": "akshare"})
            ops.append(UpdateOne({"code": code}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cb_list_jsl.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_cov_list(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            doc = row
            doc.update({"code": code, "source": "akshare"})
            ops.append(UpdateOne({"code": code}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cov_list.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_info_cm_query(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            doc = row
            doc.update({"code": code, "source": "akshare", "endpoint": "bond_info_cm_query"})
            ops.append(UpdateOne({"code": code, "endpoint": "bond_info_cm_query"}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_info_cm.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0

    async def save_info_cm_detail(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        # 若为 name/value 形式，合并为单文档
        try:
            cols = [c.lower() for c in df.columns]
        except Exception:
            cols = []
        if ("name" in cols) and ("value" in cols):
            mapping = {}
            for _, r in df.iterrows():
                name_key = r.get("name") if "name" in df.columns else r.get(df.columns[0])
                value_val = r.get("value") if "value" in df.columns else r.get(df.columns[1])
                if name_key is not None and str(name_key).strip():
                    mapping[str(name_key).strip()] = value_val
            # 提取code（优先使用明确定义的编码字段）
            code = (
                str(mapping.get("bondCode") or mapping.get("债券代码") or mapping.get("bondDefinedCode") or mapping.get("查询代码") or "").strip()
            )
            if not code:
                # 回退：尝试从映射中找常见键
                for k in ("code", "证券代码", "可转债代码"):
                    if mapping.get(k):
                        code = str(mapping.get(k)).strip()
                        break
            doc = mapping
            doc.update({"code": code, "source": "akshare", "endpoint": "bond_info_detail_cm"})
            res = await self.col_info_cm.update_one(
                {"code": code, "endpoint": "bond_info_detail_cm"},
                {"$set": doc},
                upsert=True,
            )
            return 1 if (res.upserted_id or res.modified_count) else 0
        else:
            # 回退：逐行写入（同一个code会被后续行覆盖，仍保持单文档）
            ops = []
            for _, r in df.iterrows():
                row = r.to_dict()
                code = self._norm_code(row)
                if not code:
                    code = str(row.get("bondCode") or row.get("债券代码") or row.get("bondDefinedCode") or row.get("查询代码") or "").strip()
                doc = row
                doc.update({"code": code, "source": "akshare", "endpoint": "bond_info_detail_cm"})
                ops.append(UpdateOne({"code": code, "endpoint": "bond_info_detail_cm"}, {"$set": doc}, upsert=True))
            if ops:
                res = await self.col_info_cm.bulk_write(ops, ordered=False)
                return (res.upserted_count or 0) + (res.modified_count or 0)
            return 0

    async def query_bond_daily(self, code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """查询债券历史数据"""
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        # 构建查询条件
        query = {
            "code": code_std,
            "date": {"$gte": start_date, "$lte": end_date}
        }
        
        # 查询数据
        cursor = self.col_daily.find(query).sort("date", 1)
        docs = [doc async for doc in cursor]
        
        if not docs:
            return None
        
        # 转换为DataFrame
        for doc in docs:
            doc.pop("_id", None)
        
        df = pd.DataFrame(docs)
        return df if not df.empty else None

    async def query_yield_curve(self, start_date: Optional[str] = None, end_date: Optional[str] = None, curve_name: Optional[str] = None) -> Optional[pd.DataFrame]:
        """查询收益率曲线数据
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            curve_name: 曲线名称（可选），如"中债国债收益率曲线"
        
        Returns:
            DataFrame: 包含 date, curve_name, tenor, yield 列的 DataFrame
        """
        query = {}
        if start_date:
            query["date"] = {"$gte": start_date}
        if end_date:
            if "date" in query:
                query["date"]["$lte"] = end_date
            else:
                query["date"] = {"$lte": end_date}
        if curve_name:
            query["curve_name"] = str(curve_name).strip()
        
        cursor = self.col_curve.find(query).sort("date", 1).sort("tenor", 1)
        docs = [doc async for doc in cursor]
        
        if not docs:
            return None
        
        # 转换为DataFrame
        for doc in docs:
            doc.pop("_id", None)
            # 确保所有必需的字段都存在
            if "curve_name" not in doc:
                doc["curve_name"] = ""
        
        df = pd.DataFrame(docs)
        return df if not df.empty else None

    async def save_bond_info_from_api(self, code: str, info_dict: Dict[str, Any]) -> int:
        """将从接口获取的债券详情信息保存到数据库"""
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        # 更新基础信息表
        basic_doc = {
            "code": code_std,
            "name": info_dict.get("name"),
            "exchange": info_dict.get("exchange"),
            "category": info_dict.get("category"),
            "issuer": info_dict.get("issuer"),
            "list_date": info_dict.get("list_date"),
            "maturity_date": info_dict.get("maturity_date"),
            "coupon_rate": info_dict.get("coupon_rate"),
            "source": info_dict.get("source", "akshare"),
        }
        
        # 移除None值
        basic_doc = {k: v for k, v in basic_doc.items() if v is not None}
        
        await self.col_basic.update_one(
            {"code": code_std},
            {"$set": basic_doc},
            upsert=True
        )
        
        # 如果有详细信息，保存到详细信息表
        # 将info_dict转换为DataFrame格式以便保存
        if info_dict and len(info_dict) > 1:  # 不止code字段
            detail_df = pd.DataFrame([info_dict])
            saved = await self.save_info_cm_detail(detail_df)
            return saved
        
        return 1

    async def query_bond_info(self, code: str) -> Optional[Dict[str, Any]]:
        """查询债券详情信息，合并基础信息和详细信息"""
        # 标准化代码
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        # 先查询基础信息
        basic_info = await self.col_basic.find_one({"code": code_std})
        
        # 查询详细信息（bond_info_detail_cm）- 支持多种代码格式查询
        detail_info = await self.col_info_cm.find_one({
            "code": code_std,
            "endpoint": "bond_info_detail_cm"
        })
        # 如果没找到，尝试用原始代码查询
        if not detail_info:
            detail_info = await self.col_info_cm.find_one({
                "$or": [
                    {"code": code},
                    {"code": norm.get("digits")},
                    {"债券代码": code},
                    {"债券代码": code_std},
                    {"债券代码": norm.get("digits")},
                ],
                "endpoint": "bond_info_detail_cm"
            })
        
        # 合并信息
        result = {}
        
        # 如果有基础信息，合并到结果中
        if basic_info:
            basic_info.pop("_id", None)
            result.update(basic_info)
        
        # 如果有详细信息，合并到结果中（详细信息字段优先）
        if detail_info:
            detail_info.pop("_id", None)
            detail_info.pop("endpoint", None)  # 移除内部字段
            detail_info.pop("source", None)  # 先移除，后面统一设置
            
            # 定义字段映射表：详细信息字段 -> 标准字段
            field_mapping = {
                # 名称相关
                "债券名称": "name",
                "名称": "name",
                "债券全称": "name",
                # 发行人相关
                "发行人": "issuer",
                "发行主体": "issuer",
                "发行人全称": "issuer",
                # 息票率相关
                "票面利率": "coupon_rate",
                "息票率": "coupon_rate",
                "利率": "coupon_rate",
                "票息": "coupon_rate",
                # 上市日期相关
                "上市日期": "list_date",
                "上市日": "list_date",
                "上市时间": "list_date",
                # 到期日相关
                "到期日": "maturity_date",
                "到期日期": "maturity_date",
                "债券到期日": "maturity_date",
                "到期时间": "maturity_date",
                # 交易所相关
                "交易所": "exchange",
                "上市交易所": "exchange",
                "交易市场": "exchange",
            }
            
            # 将详细信息中的字段合并
            for key, value in detail_info.items():
                if value is not None and value != "" and str(value).strip() != "nan":
                    # 检查是否需要映射字段名
                    mapped_key = field_mapping.get(key, key)
                    
                    # 如果目标字段已经有值，跳过
                    if mapped_key in result and result[mapped_key]:
                        continue
                    
                    # 根据字段类型进行转换
                    if mapped_key == "name":
                        result["name"] = str(value).strip()
                    elif mapped_key == "issuer":
                        result["issuer"] = str(value).strip()
                    elif mapped_key == "coupon_rate":
                        try:
                            if isinstance(value, str):
                                value_str = value.strip().strip('%')
                                result["coupon_rate"] = float(value_str)
                            else:
                                result["coupon_rate"] = float(value)
                        except (ValueError, TypeError):
                            pass
                    elif mapped_key == "list_date":
                        try:
                            if hasattr(value, 'strftime'):  # pandas Timestamp 或 datetime
                                result["list_date"] = value.strftime("%Y-%m-%d")
                            elif isinstance(value, str) and len(value) >= 10:
                                # 尝试格式化日期字符串
                                result["list_date"] = value[:10].replace("/", "-")
                            else:
                                result["list_date"] = str(value)
                        except Exception:
                            result["list_date"] = str(value) if value else None
                    elif mapped_key == "maturity_date":
                        try:
                            if hasattr(value, 'strftime'):  # pandas Timestamp 或 datetime
                                result["maturity_date"] = value.strftime("%Y-%m-%d")
                            elif isinstance(value, str) and len(value) >= 10:
                                # 尝试格式化日期字符串
                                result["maturity_date"] = value[:10].replace("/", "-")
                            else:
                                result["maturity_date"] = str(value)
                        except Exception:
                            result["maturity_date"] = str(value) if value else None
                    elif mapped_key == "exchange":
                        # 标准化交易所代码
                        exchange_val = str(value).strip().upper()
                        if "上海" in exchange_val or "上交所" in exchange_val or exchange_val in ["SH", "SHANGHAI"]:
                            result["exchange"] = "SH"
                        elif "深圳" in exchange_val or "深交所" in exchange_val or exchange_val in ["SZ", "SHENZHEN"]:
                            result["exchange"] = "SZ"
                        else:
                            result["exchange"] = exchange_val
                    else:
                        # 其他字段直接添加，但不覆盖已有字段
                        if mapped_key not in result:
                            result[mapped_key] = value
        
        # 确保code字段存在
        if "code" not in result:
            result["code"] = code_std
        
        # 确保source字段存在
        if "source" not in result:
            result["source"] = "database"
        
        # 如果有任何字段，返回结果
        return result if result else None

    async def save_bond_minute_quotes(self, code: str, df: pd.DataFrame, period: str = "1") -> int:
        """保存债券分钟数据
        
        Args:
            code: 债券代码（标准化后）
            df: 包含分钟数据的DataFrame，必须包含datetime或时间列
            period: 数据周期（"1", "5", "15", "30", "60"）
        
        Returns:
            保存的记录数
        """
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            return 0
        
        ops = []
        valid_count = 0
        skipped_count = 0
        
        # 规范化代码
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        # 字段映射表：AKShare字段 -> 标准字段
        field_mapping = {
            # 时间相关
            "时间": "datetime",
            "date": "datetime",
            "datetime": "datetime",
            # 价格相关
            "开盘": "open",
            "open": "open",
            "最高": "high",
            "high": "high",
            "最低": "low",
            "low": "low",
            "收盘": "close",
            "close": "close",
            "最新价": "close",
            # 成交相关
            "成交量": "volume",
            "volume": "volume",
            "成交额": "amount",
            "amount": "amount",
            # 其他
            "涨跌幅": "change_percent",
            "涨跌额": "change",
            "振幅": "amplitude",
            "换手率": "turnover_rate",
        }
        
        for _, r in df.iterrows():
            try:
                # 提取datetime
                datetime_val = None
                for dt_col in ["时间", "datetime", "date"]:
                    if dt_col in r.index or dt_col in r:
                        dt_val = r.get(dt_col)
                        if dt_val is not None and not pd.isna(dt_val):
                            try:
                                if isinstance(dt_val, pd.Timestamp):
                                    datetime_val = dt_val.strftime("%Y-%m-%d %H:%M:%S")
                                elif isinstance(dt_val, str):
                                    # 尝试解析日期时间字符串
                                    datetime_val = pd.to_datetime(dt_val).strftime("%Y-%m-%d %H:%M:%S")
                                else:
                                    datetime_val = str(dt_val)
                                break
                            except Exception:
                                continue
                
                if not datetime_val:
                    skipped_count += 1
                    continue
                
                # 构建文档
                doc = {
                    "code": code_std,
                    "datetime": datetime_val,
                    "period": str(period),
                    "source": "akshare",
                }
                
                # 映射字段
                for ak_field, std_field in field_mapping.items():
                    if ak_field in r.index or ak_field in r:
                        value = r.get(ak_field)
                        if value is not None and not pd.isna(value):
                            try:
                                # 数值类型转换
                                if std_field in ["open", "high", "low", "close", "volume", "amount", 
                                                "change_percent", "change", "amplitude", "turnover_rate"]:
                                    doc[std_field] = float(value)
                                else:
                                    doc[std_field] = value
                            except (ValueError, TypeError):
                                pass
                
                # 移除None值
                doc = {k: v for k, v in doc.items() if v is not None}
                
                # 使用 (code, datetime, period) 作为唯一键
                ops.append(
                    UpdateOne(
                        {"code": code_std, "datetime": datetime_val, "period": period},
                        {"$set": doc},
                        upsert=True
                    )
                )
                valid_count += 1
                
            except Exception as e:
                skipped_count += 1
                logger.warning(f"⚠️ [分钟数据保存] 处理行数据失败: {e}")
                continue
        
        if not ops:
            logger.warning(f"⚠️ [分钟数据保存] 没有有效数据可保存（跳过 {skipped_count} 条）")
            return 0
        
        try:
            res = await self.col_minute.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            total_saved = upserted + modified
            
            logger.info(f"💾 [分钟数据保存] 批量写入完成: 新增={upserted}, 更新={modified}, 总计={total_saved}, 有效={valid_count}, 跳过={skipped_count}")
            
            return total_saved
        except Exception as e:
            logger.error(f"❌ [分钟数据保存] 批量写入失败: {e}", exc_info=True)
            return 0
