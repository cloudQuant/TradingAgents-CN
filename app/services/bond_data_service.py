from typing import Optional, Iterable, Dict, Any
from datetime import datetime
import datetime as dt
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from loguru import logger


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
            
            # 标准化索引键格式用于比较
            if isinstance(index_spec, str):
                target_key = [(index_spec, 1)]
            elif isinstance(index_spec, list):
                target_key = index_spec
            else:
                target_key = list(index_spec)
            
            # 检查索引是否已存在
            indexes = await collection.list_indexes().to_list(length=None)
            
            # 查找相同名称的索引
            existing_by_name = next((idx for idx in indexes if idx.get('name') == name), None)
            
            # 查找相同键的索引（不论名称）
            existing_by_key = None
            for idx in indexes:
                if idx.get('name') == '_id_':  # 跳过默认_id索引
                    continue
                idx_key = list(idx.get('key', {}).items())
                if idx_key == target_key:
                    existing_by_key = idx
                    break
            
            if existing_by_name:
                # 有相同名称的索引，检查规格是否一致
                existing_unique = existing_by_name.get('unique', False)
                existing_sparse = existing_by_name.get('sparse', False)
                
                if existing_unique == unique and existing_sparse == sparse:
                    # 索引已存在且规格一致，无需重建
                    logger.debug(f"✓ 索引 {name} 已存在且规格一致")
                    return
                else:
                    # 索引规格不一致，需要删除重建
                    logger.info(f"🔄 索引 {name} 规格不一致，删除旧索引并重建")
                    try:
                        await collection.drop_index(name)
                    except Exception as drop_err:
                        logger.warning(f"⚠️ 删除索引 {name} 失败: {drop_err}")
            
            elif existing_by_key:
                # 相同键但不同名称的索引已存在
                old_name = existing_by_key.get('name')
                existing_unique = existing_by_key.get('unique', False)
                existing_sparse = existing_by_key.get('sparse', False)
                
                if existing_unique == unique and existing_sparse == sparse:
                    # 键和规格都一致，只是名称不同，保留旧索引即可
                    logger.debug(f"✓ 索引键已存在 (旧名称: {old_name})，规格一致，跳过创建")
                    return
                else:
                    # 需要替换旧索引
                    logger.info(f"🔄 索引键已存在但规格不同 (旧名称: {old_name})，删除并重建")
                    try:
                        await collection.drop_index(old_name)
                    except Exception as drop_err:
                        logger.warning(f"⚠️ 删除旧索引 {old_name} 失败: {drop_err}")
            
            # 创建索引
            if isinstance(index_spec, str):
                await collection.create_index(index_spec, unique=unique, sparse=sparse, name=name)
            else:
                await collection.create_index(index_spec, unique=unique, sparse=sparse, name=name)
            
            logger.debug(f"✓ 成功创建索引 {name}")
            
        except Exception as e:
            error_msg = str(e)
            # 处理各种索引错误
            if 'IndexOptionsConflict' in error_msg or 'Index already exists with a different name' in error_msg:
                logger.debug(f"⚠️ 索引已存在（不同名称），跳过: {error_msg}")
                # 索引实际上已经存在，只是名称不同，可以忽略
                return
            elif 'IndexKeySpecsConflict' in error_msg:
                logger.warning(f"⚠️ 索引键冲突: {error_msg}")
            else:
                logger.warning(f"⚠️ 创建索引 {name} 失败: {e}")

    async def ensure_indexes(self) -> None:
        await self._safe_create_index(
            self.col_basic,
            "code",
            unique=True,
            name="basic_code_1"
        )
        await self.col_basic.create_index("category")
        await self.col_basic.create_index("maturity_date")
        await self.col_basic.create_index("exchange")
        await self.col_basic.create_index("list_date")
        await self.col_basic.create_index("coupon_rate")
        await self.col_basic.create_index("name")
        await self._safe_create_index(
            self.col_daily,
            [("code", 1), ("date", 1)],
            unique=True,
            name="daily_code_1_date_1"
        )
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
        await self._safe_create_index(
            self.col_events,
            [("code", 1), ("date", 1), ("event_type", 1)],
            unique=True,
            name="code_1_date_1_event_type_1"
        )
        await self._safe_create_index(
            self.col_spot,
            [("code", 1), ("timestamp", 1), ("category", 1)],
            unique=True,
            name="code_1_timestamp_1_category_1"
        )
        await self._safe_create_index(
            self.col_indices,
            [("index_id", 1), ("date", 1)],
            unique=True,
            name="index_id_1_date_1"
        )
        # us_yield 集合的索引可能与其他集合冲突，使用安全创建
        await self._safe_create_index(
            self.col_us_yield,
            [("date", 1), ("tenor", 1)],
            unique=True,
            name="date_1_tenor_1"
        )
        await self._safe_create_index(
            self.col_cb_profiles,
            "code",
            unique=True,
            name="code_1"
        )
        await self._safe_create_index(
            self.col_buybacks,
            [("exchange", 1), ("date", 1), ("code", 1)],
            unique=True,
            name="exchange_1_date_1_code_1"
        )
        # 新增索引
        await self._safe_create_index(
            self.col_issues,
            [("issue_type", 1), ("code", 1), ("date", 1)],
            unique=True,
            name="issue_type_1_code_1_date_1"
        )
        await self._safe_create_index(
            self.col_cb_adjustments,
            [("code", 1), ("date", 1)],
            unique=True,
            name="cb_adj_code_1_date_1"
        )
        await self._safe_create_index(
            self.col_cb_redeems,
            [("code", 1), ("date", 1)],
            unique=True,
            name="cb_redeem_code_1_date_1"
        )
        await self._safe_create_index(
            self.col_cb_summary,
            "code",
            unique=True,
            name="cb_summary_code_1"
        )
        await self._safe_create_index(
            self.col_cb_valuation,
            [("code", 1), ("date", 1)],
            unique=True,
            name="cb_val_code_1_date_1"
        )
        await self._safe_create_index(
            self.col_cb_comparison,
            [("date", 1), ("code", 1)],
            unique=True,
            name="cb_comp_date_1_code_1"
        )
        await self._safe_create_index(
            self.col_spot_quote_detail,
            [("code", 1), ("timestamp", 1), ("报价机构", 1)],
            unique=True,
            name="spot_quote_detail_unique"
        )
        await self._safe_create_index(
            self.col_spot_deals,
            [("code", 1), ("timestamp", 1)],
            unique=True,
            name="spot_deals_code_1_ts_1"
        )
        await self._safe_create_index(
            self.col_deal_summary,
            [("date", 1), ("债券类型", 1)],
            unique=True,
            name="deal_summary_date_1_type_1"
        )
        await self._safe_create_index(
            self.col_cash_summary,
            [("date", 1), ("债券现货", 1)],
            unique=True,
            name="cash_summary_date_1_type_1"
        )
        # NAFMII 使用注册通知书文号作为唯一标识（部分记录无 reg_no 时仍可写入，但建议数据源尽量提供）
        await self._safe_create_index(self.col_nafmii, "reg_no", unique=True, sparse=True, name="reg_no_1")
        await self.col_info_cm.create_index("code")
        # 唯一索引：每个债券的每个接口只有一条记录
        await self._safe_create_index(
            self.col_info_cm,
            [("code", 1), ("endpoint", 1)],
            unique=True,
            name="info_cm_code_1_endpoint_1"
        )
        await self._safe_create_index(
            self.col_curve_map,
            "date",
            unique=True,
            name="curve_map_date_1"
        )
        await self._safe_create_index(
            self.col_buybacks_hist,
            [("exchange", 1), ("date", 1)],
            unique=True,
            name="buybacks_hist_exch_1_date_1"
        )
        await self._safe_create_index(
            self.col_cb_list_jsl,
            "code",
            unique=True,
            name="cb_list_jsl_code_1"
        )
        await self._safe_create_index(
            self.col_cov_list,
            "code",
            unique=True,
            name="cov_list_code_1"
        )
        # 分钟数据索引：使用 (code, datetime, period) 作为唯一键
        await self._safe_create_index(
            self.col_minute,
            [("code", 1), ("datetime", 1), ("period", 1)],
            unique=True,
            name="minute_code_1_dt_1_period_1"
        )
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
        import numpy as np
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            logger.warning("[收益率曲线保存] DataFrame为空")
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
                    if pd.isna(yield_float) or not np.isfinite(yield_float):
                        skipped_count += 1
                        continue
                        
                except (ValueError, TypeError) as e:
                    # 无法转换为数值，跳过这条记录
                    skipped_count += 1
                    logger.debug(f"[收益率曲线保存] 跳过非数值数据: date={date_val}, tenor={tenor_val}, yield={yield_val}, error={e}")
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
                logger.warning(f"[收益率曲线保存] 处理行数据失败: {e}, row={dict(r)}")
                continue
        
        logger.info(f"[收益率曲线保存] 处理完成: ops数量={len(ops)}, valid_count={valid_count}, skipped_count={skipped_count}")
        
        if not ops:
            logger.warning(f"[收益率曲线保存] 没有有效数据可保存（跳过 {skipped_count} 条无效数据，总计 {len(df)} 条）")
            return 0
        
        try:
            # 执行批量写入
            res = await self.col_curve.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            matched = res.matched_count or 0
            total_saved = upserted + modified + matched
            
            logger.info(f"[收益率曲线保存] 批量写入完成: 新增={upserted}, 更新={modified}, 匹配={matched}, 总计={total_saved}, 有效数据={valid_count}, 跳过={skipped_count}, 总行数={len(df)}")
            logger.info(f"[收益率曲线保存] 详细结果: upserted_count={res.upserted_count}, modified_count={res.modified_count}, matched_count={res.matched_count}")
            
            return total_saved
        except Exception as e:
            # 处理BulkWriteError - 部分成功也可以提取结果
            from pymongo.errors import BulkWriteError
            if isinstance(e, BulkWriteError):
                # BulkWriteError也包含部分成功的结果
                result = e.details
                upserted = result.get('nUpserted', 0)
                modified = result.get('nModified', 0)
                matched = result.get('nMatched', 0)
                total_saved = upserted + modified + matched
                
                write_errors = result.get('writeErrors', [])
                logger.warning(f"[收益率曲线保存] 批量写入部分成功: 新增={upserted}, 更新={modified}, 匹配={matched}, 总计={total_saved}, 错误数={len(write_errors)}")
                
                # 记录前几个错误示例
                if write_errors:
                    for i, err in enumerate(write_errors[:3]):
                        logger.warning(f"[收益率曲线保存] 错误示例 {i+1}: {err.get('errmsg', 'Unknown error')}")
                
                # 即使有错误，也返回成功保存的数量
                if total_saved > 0:
                    return total_saved
            
            logger.error(f"[收益率曲线保存] 批量写入失败: {e}", exc_info=True)
            return 0

    async def save_bond_daily(self, code: str, df: pd.DataFrame) -> int:
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            logger.warning(f"⚠️ [日线数据] 数据为空，code={code}")
            return 0
        
        # 规范化债券代码
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        logger.info(f"📊 [日线数据] 开始保存 {len(df)} 条数据, code={code}, code_std={code_std}")
        ops = []
        for _, r in df.iterrows():
            doc = {k: r.get(k) for k in df.columns}
            doc["code"] = code_std  # 使用规范化的代码
            doc["date"] = str(doc.get("date"))
            ops.append(
                UpdateOne({"code": doc["code"], "date": doc["date"]}, {"$set": doc}, upsert=True)
            )
        if ops:
            res = await self.col_daily.bulk_write(ops, ordered=False)
            # upserted_count: 新插入的文档数
            # modified_count: 实际修改的文档数  
            # matched_count: 匹配到的文档数（包括内容相同未修改的）
            # 返回：新增 + 更新 + 匹配（内容相同的也算成功处理）
            saved = (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
            logger.info(f"💾 [日线数据] 保存完成: 新增={res.upserted_count}, 更新={res.modified_count}, 匹配={res.matched_count}, 总计={saved}")
            return saved
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
            
            # 获取并规范化category字段
            category_val = it.get("category")
            if category_val and str(category_val).strip():
                category_normalized = str(category_val).strip().lower()
            else:
                category_normalized = "other"  # 默认值，不再使用None
            
            # 调试日志：记录前几条数据的category值
            if valid_count < 3:
                logger.debug(f"🔍 [债券数据保存] 样本数据 {valid_count+1}: code={code_std}, raw_category={category_val}, normalized_category={category_normalized}")
            
            # 构建文档
            doc = {
                "code": code_std,
                "name": it.get("name"),
                "exchange": it.get("exchange"),
                "category": category_normalized,  # 确保category字段总是有值
                "issuer": it.get("issuer"),
                "list_date": str(it.get("list_date")) if it.get("list_date") else None,
                "maturity_date": str(it.get("maturity_date")) if it.get("maturity_date") else None,
                "coupon_rate": it.get("coupon_rate"),
                "type": it.get("type"),
                "raw_code": it.get("raw_code"),
                "source": it.get("source", "akshare"),
                "updated_at": datetime.now().isoformat(),  # 添加更新时间
            }
            
            # 移除None值（但保留category字段，因为它总是有值）
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
            
            # 添加调试：查询数据库中的category分布
            try:
                pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}}]
                category_stats = []
                async for doc in self.col_basic.aggregate(pipeline):
                    category_stats.append(f"{doc.get('_id', 'null')}: {doc.get('count', 0)}")
                logger.info(f"📊 [债券数据保存] 数据库category分布: {', '.join(category_stats)}")
            except Exception as stats_err:
                logger.warning(f"⚠️ [债券数据保存] 无法获取category统计: {stats_err}")
            
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
        import logging
        logger = logging.getLogger("webapi")
        
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

        # 调试日志：记录查询条件
        logger.debug(f"🔍 [债券查询] 查询条件: {filt}")
        
        total = await self.col_basic.count_documents(filt)
        logger.debug(f"📊 [债券查询] 查询结果总数: {total}")
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
                
                # 提取时间戳和日期
                timestamp = (
                    r.get("timestamp") or r.get("ticktime") or 
                    r.get("time") or datetime.now().strftime("%H:%M:%S")
                )
                timestamp = str(timestamp).strip()
                
                # 提取日期
                date = r.get("date") or r.get("日期") or datetime.now().strftime("%Y-%m-%d")
                date = str(date).strip()[:10]  # 只保留日期部分
                
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
                    "date": date,
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
                
                # 保存所有原始字段（用于调试）
                doc["_raw"] = dict(r)
                
                # 移除None值
                doc = {k: v for k, v in doc.items() if v is not None}
                
                # 使用 (code, date, category) 作为唯一键（同一天同一债券同一类别只保留最新数据）
                ops.append(
                    UpdateOne(
                        {"code": code_std, "date": date, "category": category},
                        {"$set": doc},
                        upsert=True
                    )
                )
                valid_count += 1
                
            except Exception as e:
                skipped_count += 1
                logger.warning(f"[现货报价保存] 处理行数据失败: {e}")
                continue
        
        if not ops:
            logger.warning(f"[现货报价保存] 没有有效数据可保存（跳过 {skipped_count} 条）")
            return 0
        
        try:
            res = await self.col_spot.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            matched = res.matched_count or 0
            total_saved = upserted + modified + matched
            
            logger.info(f"[现货报价保存] 批量写入完成: 新增={upserted}, 更新={modified}, 匹配={matched}, 总计={total_saved}, 有效={valid_count}, 跳过={skipped_count}")
            
            return total_saved
        except Exception as e:
            logger.error(f"[现货报价保存] 批量写入失败: {e}", exc_info=True)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
        return 0


    async def save_deal_summary(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            # 转换所有日期类型为字符串，避免MongoDB编码错误
            doc = {}
            for k, v in row.items():
                if isinstance(v, (pd.Timestamp, dt.date, dt.datetime)):
                    doc[k] = pd.to_datetime(v).strftime("%Y-%m-%d")
                else:
                    doc[k] = v
            doc.update({"date": date, "source": "akshare"})
            bt = row.get("债券类型")
            if bt is not None:
                ops.append(UpdateOne({"date": date, "债券类型": bt}, {"$set": doc}, upsert=True))
            else:
                ops.append(UpdateOne({"date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_deal_summary.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
        return 0

    async def save_cash_summary(self, df: pd.DataFrame) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            date = self._norm_date(row)
            # 转换所有日期类型为字符串，避免MongoDB编码错误
            doc = {}
            for k, v in row.items():
                if isinstance(v, (pd.Timestamp, dt.date, dt.datetime)):
                    doc[k] = pd.to_datetime(v).strftime("%Y-%m-%d")
                else:
                    doc[k] = v
            doc.update({"date": date, "source": "akshare"})
            ops.append(UpdateOne({"date": date}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_cash_summary.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
            return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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
                return (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
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

    async def query_yield_curve(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None, 
        curve_name: Optional[str] = None,
        tenor: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """查询收益率曲线数据
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            curve_name: 曲线名称（可选），如"中债国债收益率曲线"
            tenor: 期限（可选），如"10年"
            limit: 返回数量限制
        
        Returns:
            Dict: {"total": int, "items": list}
        """
        import logging
        logger = logging.getLogger("webapi")
        
        try:
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
            if tenor:
                query["tenor"] = str(tenor).strip()
            
            total = await self.col_curve.count_documents(query)
            
            if total == 0:
                return {"total": 0, "items": []}
            
            cursor = self.col_curve.find(query).sort("date", -1).sort("tenor", 1).limit(limit)
            items = []
            async for doc in cursor:
                if "_id" in doc:
                    doc.pop("_id", None)
                # 确保所有必需的字段都存在
                if "curve_name" not in doc:
                    doc["curve_name"] = ""
                items.append(doc)
            
            logger.debug(f"📊 [收益率曲线] 查询成功: {len(items)}/{total}")
            return {"total": total, "items": items}
        except Exception as e:
            logger.error(f"❌ [收益率曲线] 查询失败: {e}", exc_info=True)
            return {"total": 0, "items": []}

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

    async def save_cov_comparison(self, df: pd.DataFrame) -> int:
        """保存可转债比价表数据
        
        Args:
            df: 可转债比价表DataFrame（来自bond_cov_comparison）
            
        Returns:
            保存的记录数
        """
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            return 0
        
        ops = []
        timestamp = datetime.now().isoformat()
        
        for _, r in df.iterrows():
            code = str(r.get("转债代码") or r.get("债券代码") or "").strip()
            if not code:
                continue
            
            from tradingagents.utils.instrument_validator import normalize_bond_code
            norm = normalize_bond_code(code)
            code_std = norm.get("code_std") or code
            
            # 辅助函数：安全转换为float
            def safe_float(value):
                """安全转换为float，处理NaN和None"""
                if value is None or (isinstance(value, float) and pd.isna(value)):
                    return None
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None
            
            doc = {
                "code": code_std,
                "name": str(r.get("转债名称") or r.get("债券名称") or ""),
                "price": safe_float(r.get("转债最新价")),
                "change_pct": safe_float(r.get("转债涨跌幅")),
                "stock_code": str(r.get("正股代码") or ""),
                "stock_name": str(r.get("正股名称") or ""),
                "stock_price": safe_float(r.get("正股最新价")),
                "stock_change_pct": safe_float(r.get("正股涨跌幅")),
                "convert_price": safe_float(r.get("转股价")),
                "convert_value": safe_float(r.get("转股价值")),
                "convert_premium_rate": safe_float(r.get("转股溢价率")),
                "pure_debt_premium_rate": safe_float(r.get("纯债溢价率")),
                "put_trigger_price": safe_float(r.get("回售触发价")),
                "redeem_trigger_price": safe_float(r.get("强赎触发价")),
                "maturity_redeem_price": safe_float(r.get("到期赎回价")),
                "pure_debt_value": safe_float(r.get("纯债价值")),
                "start_convert_date": str(r.get("开始转股日") or ""),
                "list_date": str(r.get("上市日期") or ""),
                "apply_date": str(r.get("申购日期") or ""),
                "timestamp": timestamp,
                "source": "akshare",
            }
            
            # 移除None值，但保留0值
            doc = {k: v for k, v in doc.items() if v is not None and v != ""}
            
            ops.append(UpdateOne(
                {"code": code_std},
                {"$set": doc},
                upsert=True
            ))
        
        if not ops:
            return 0
        
        try:
            res = await self.col_cb_comparison.bulk_write(ops, ordered=False)
            saved = (res.upserted_count or 0) + (res.modified_count or 0)
            logger.info(f"💾 [可转债比价] 保存 {saved} 条数据")
            return saved
        except Exception as e:
            logger.error(f"❌ [可转债比价] 保存失败: {e}", exc_info=True)
            return 0

    async def save_cov_value_analysis(self, code: str, df: pd.DataFrame) -> int:
        """保存可转债价值分析历史数据
        
        Args:
            code: 债券代码
            df: 价值分析DataFrame（来自bond_zh_cov_value_analysis）
            
        Returns:
            保存的记录数
        """
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            return 0
        
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        # 辅助函数：安全转换为float
        def safe_float(value):
            """安全转换为float，处理NaN和None"""
            if value is None or (isinstance(value, float) and pd.isna(value)):
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        ops = []
        for _, r in df.iterrows():
            date = str(r.get("日期") or "").strip()
            if not date:
                continue
            
            doc = {
                "code": code_std,
                "date": date,
                "close_price": safe_float(r.get("收盘价")),
                "pure_debt_value": safe_float(r.get("纯债价值")),
                "convert_value": safe_float(r.get("转股价值")),
                "pure_debt_premium_rate": safe_float(r.get("纯债溢价率")),
                "convert_premium_rate": safe_float(r.get("转股溢价率")),
                "source": "akshare",
            }
            
            # 移除None值，但保留0值
            doc = {k: v for k, v in doc.items() if v is not None and v != ""}
            
            ops.append(UpdateOne(
                {"code": code_std, "date": date},
                {"$set": doc},
                upsert=True
            ))
        
        if not ops:
            return 0
        
        try:
            res = await self.col_cb_valuation.bulk_write(ops, ordered=False)
            saved = (res.upserted_count or 0) + (res.modified_count or 0) + (res.matched_count or 0)
            logger.info(f"💾 [可转债价值] {code_std} 保存 {saved} 条数据 (新增={res.upserted_count}, 更新={res.modified_count}, 匹配={res.matched_count})")
            return saved
        except Exception as e:
            logger.error(f"❌ [可转债价值] 保存失败: {e}", exc_info=True)
            return 0

    async def save_spot_deals(self, df: pd.DataFrame) -> int:
        """保存现券市场成交行情
        
        Args:
            df: 成交行情DataFrame（来自bond_spot_deal）
            
        Returns:
            保存的记录数
        """
        import logging
        logger = logging.getLogger("webapi")
        
        if df is None or df.empty:
            return 0
        
        # 辅助函数：安全转换为float
        def safe_float(value):
            """安全转换为float，处理NaN和None"""
            if value is None or (isinstance(value, float) and pd.isna(value)):
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        
        ops = []
        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().isoformat()
        
        logger.info(f"[现券成交] 开始处理 {len(df)} 条数据")
        logger.debug(f"[现券成交] DataFrame列: {df.columns.tolist()}")
        
        skipped = 0
        for idx, r in df.iterrows():
            name = str(r.get("债券简称") or "").strip()
            if not name:
                skipped += 1
                logger.debug(f"[现券成交] 行{idx}: 债券简称为空，跳过")
                continue
            
            doc = {
                "bond_name": name,
                "deal_price": safe_float(r.get("成交净价")),
                "latest_yield": safe_float(r.get("最新收益率")),
                "change": safe_float(r.get("涨跌")),
                "weighted_yield": safe_float(r.get("加权收益率")),
                "volume": safe_float(r.get("交易量")),
                "date": today,
                "timestamp": timestamp,
                "source": "akshare",
            }
            
            # 移除None值，但保留0值
            doc = {k: v for k, v in doc.items() if v is not None and v != ""}
            
            # 使用bond_name和date作为唯一键（同一天同一债券只保留最新数据）
            ops.append(UpdateOne(
                {"bond_name": name, "date": today},
                {"$set": doc},
                upsert=True
            ))
        
        if not ops:
            return 0
        
        try:
            res = await self.col_spot_deals.bulk_write(ops, ordered=False)
            upserted = res.upserted_count or 0
            modified = res.modified_count or 0
            matched = res.matched_count or 0
            saved = upserted + modified + matched
            logger.info(f"[现券成交] 保存完成: 新增={upserted}, 更新={modified}, 匹配={matched}, 总计={saved}, 跳过={skipped}")
            return saved
        except Exception as e:
            # 处理BulkWriteError - 部分成功也可以提取结果
            from pymongo.errors import BulkWriteError
            if isinstance(e, BulkWriteError):
                result = e.details
                upserted = result.get('nUpserted', 0)
                modified = result.get('nModified', 0)
                matched = result.get('nMatched', 0)
                saved = upserted + modified + matched
                
                write_errors = result.get('writeErrors', [])
                logger.warning(f"[现券成交] 批量写入部分成功: 新增={upserted}, 更新={modified}, 匹配={matched}, 总计={saved}, 错误数={len(write_errors)}")
                
                if write_errors:
                    for i, err in enumerate(write_errors[:3]):
                        logger.warning(f"[现券成交] 错误示例 {i+1}: {err.get('errmsg', 'Unknown error')}")
                
                if saved > 0:
                    return saved
            
            logger.error(f"[现券成交] 保存失败: {e}", exc_info=True)
            return 0

    async def query_cov_comparison(
        self,
        q: Optional[str] = None,
        keyword: Optional[str] = None,  # 添加keyword参数作为q的别名
        sort_by: Optional[str] = None,
        sort_dir: str = "asc",
        page: int = 1,
        page_size: int = 50,
        min_premium: Optional[float] = None,
        max_premium: Optional[float] = None,
    ) -> Dict[str, Any]:
        """查询可转债比价表
        
        Args:
            q: 搜索关键词（代码或名称）
            keyword: 搜索关键词别名（与q等效）
            sort_by: 排序字段
            sort_dir: 排序方向（asc/desc）
            page: 页码
            page_size: 每页数量
            min_premium: 最小转股溢价率
            max_premium: 最大转股溢价率
            
        Returns:
            查询结果字典
        """
        import logging
        logger = logging.getLogger("webapi")
        
        # keyword是q的别名
        if keyword and not q:
            q = keyword
        
        # 构建过滤条件
        filt: Dict[str, Any] = {}
        
        # 关键词搜索
        if q:
            q_regex = {"$regex": q, "$options": "i"}
            filt["$or"] = [{"code": q_regex}, {"name": q_regex}]
        
        # 溢价率范围过滤（在数据库层过滤，提升性能）
        if min_premium is not None or max_premium is not None:
            premium_filter = {}
            if min_premium is not None:
                premium_filter["$gte"] = min_premium
            if max_premium is not None:
                premium_filter["$lte"] = max_premium
            if premium_filter:
                filt["convert_premium_rate"] = premium_filter
        
        logger.debug(f"🔍 [可转债查询] 过滤条件: {filt}")
        
        # 计数
        total = await self.col_cb_comparison.count_documents(filt)
        if total == 0:
            return {"total": 0, "items": []}
        
        # 分页和排序
        skip = max(0, (page - 1) * page_size)
        field = (sort_by or "code").lower()
        direc = 1 if str(sort_dir).lower() != "desc" else -1
        
        cursor = self.col_cb_comparison.find(filt).sort([(field, direc)]).skip(skip).limit(page_size)
        items = []
        async for doc in cursor:
            if "_id" in doc:
                doc.pop("_id", None)
            items.append(doc)
        
        logger.debug(f"📊 [可转债查询] 返回 {len(items)}/{total} 条数据")
        
        return {"total": total, "items": items}

    async def query_cov_value_analysis(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """查询可转债价值分析历史数据"""
        from tradingagents.utils.instrument_validator import normalize_bond_code
        norm = normalize_bond_code(code)
        code_std = norm.get("code_std") or code
        
        filt = {"code": code_std}
        if start_date:
            filt["date"] = {"$gte": start_date}
        if end_date:
            if "date" in filt:
                filt["date"]["$lte"] = end_date
            else:
                filt["date"] = {"$lte": end_date}
        
        cursor = self.col_cb_valuation.find(filt).sort("date", -1).limit(limit)
        items = []
        async for doc in cursor:
            if "_id" in doc:
                doc.pop("_id", None)
            items.append(doc)
        
        return {"total": len(items), "items": items}
    
    async def query_spot_deals(
        self,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """查询现券成交行情
        
        Args:
            limit: 返回数量限制
            skip: 跳过数量
            
        Returns:
            查询结果字典 {"total": int, "items": list}
        """
        import logging
        logger = logging.getLogger("webapi")
        
        try:
            total = await self.col_spot_deals.count_documents({})
            
            if total == 0:
                return {"total": 0, "items": []}
            
            cursor = self.col_spot_deals.find({}).skip(skip).limit(limit)
            items = []
            async for doc in cursor:
                if "_id" in doc:
                    doc.pop("_id", None)
                items.append(doc)
            
            logger.debug(f"📊 [现券成交] 查询成功: {len(items)}/{total}")
            return {"total": total, "items": items}
        except Exception as e:
            logger.error(f"❌ [现券成交] 查询失败: {e}", exc_info=True)
            return {"total": 0, "items": []}
    
    async def query_spot_quotes(
        self,
        category: Optional[str] = None,
        bond_name: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """查询现券做市报价
        
        Args:
            category: 分类过滤
            bond_name: 债券名称关键词
            limit: 返回数量限制
            skip: 跳过数量
            
        Returns:
            查询结果字典 {"total": int, "items": list}
        """
        import logging
        logger = logging.getLogger("webapi")
        
        try:
            filt: Dict[str, Any] = {}
            
            if category:
                filt["category"] = category
            
            if bond_name:
                filt["债券简称"] = {"$regex": bond_name, "$options": "i"}
            
            total = await self.col_spot.count_documents(filt)
            
            if total == 0:
                return {"total": 0, "items": []}
            
            cursor = self.col_spot.find(filt).skip(skip).limit(limit)
            items = []
            async for doc in cursor:
                if "_id" in doc:
                    doc.pop("_id", None)
                items.append(doc)
            
            logger.debug(f"📊 [现券报价] 查询成功: {len(items)}/{total}")
            return {"total": total, "items": items}
        except Exception as e:
            logger.error(f"❌ [现券报价] 查询失败: {e}", exc_info=True)
            return {"total": 0, "items": []}
    
    async def query_historical_data(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """查询债券历史行情数据
        
        Args:
            code: 债券代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            limit: 返回数量限制
            
        Returns:
            查询结果字典 {"total": int, "items": list}
        """
        import logging
        logger = logging.getLogger("webapi")
        
        try:
            from tradingagents.utils.instrument_validator import normalize_bond_code
            norm = normalize_bond_code(code)
            code_std = norm.get("code_std") or code
            
            filt: Dict[str, Any] = {"code": code_std}
            
            if start_date or end_date:
                date_filter = {}
                if start_date:
                    date_filter["$gte"] = start_date
                if end_date:
                    date_filter["$lte"] = end_date
                filt["date"] = date_filter
            
            total = await self.col_daily.count_documents(filt)
            
            if total == 0:
                return {"total": 0, "items": []}
            
            cursor = self.col_daily.find(filt).sort("date", -1).limit(limit)
            items = []
            async for doc in cursor:
                if "_id" in doc:
                    doc.pop("_id", None)
                items.append(doc)
            
            logger.debug(f"📊 [日线数据] 查询成功: {len(items)}/{total}")
            return {"total": total, "items": items}
        except Exception as e:
            logger.error(f"❌ [日线数据] 查询失败: {e}", exc_info=True)
            return {"total": 0, "items": []}
    
    async def save_historical_data(self, df: pd.DataFrame, code: str) -> int:
        """保存债券历史数据 (save_bond_daily的别名)
        
        Args:
            df: 数据DataFrame
            code: 债券代码
            
        Returns:
            保存数量
        """
        return await self.save_bond_daily(code, df)
