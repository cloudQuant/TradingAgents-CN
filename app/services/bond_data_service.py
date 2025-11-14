from typing import Optional, Iterable, Dict, Any
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

    async def ensure_indexes(self) -> None:
        await self.col_basic.create_index("code", unique=True)
        await self.col_basic.create_index("category")
        await self.col_basic.create_index("maturity_date")
        await self.col_daily.create_index([("code", 1), ("date", 1)], unique=True)
        await self.col_curve.create_index([("date", 1), ("tenor", 1)], unique=True)
        await self.col_events.create_index([("code", 1), ("date", 1), ("event_type", 1)])
        await self.col_spot.create_index([("code", 1), ("timestamp", 1), ("category", 1)], unique=True)
        await self.col_indices.create_index([("index_id", 1), ("date", 1)], unique=True)
        await self.col_us_yield.create_index([("date", 1), ("tenor", 1)], unique=True)
        await self.col_cb_profiles.create_index("code", unique=True)
        await self.col_buybacks.create_index([("exchange", 1), ("date", 1), ("code", 1)])
        # 新增索引
        await self.col_issues.create_index([("issue_type", 1), ("code", 1), ("date", 1)])
        await self.col_cb_adjustments.create_index([("code", 1), ("date", 1)])
        await self.col_cb_redeems.create_index([("code", 1), ("date", 1)])
        await self.col_cb_summary.create_index("code")
        await self.col_cb_valuation.create_index([("code", 1), ("date", 1)])
        await self.col_cb_comparison.create_index("date")
        await self.col_spot_quote_detail.create_index([("code", 1), ("timestamp", 1)])
        await self.col_spot_deals.create_index([("code", 1), ("timestamp", 1)])
        await self.col_deal_summary.create_index([("date", 1)])
        await self.col_cash_summary.create_index([("date", 1)])
        await self.col_nafmii.create_index([("code", 1), ("date", 1)])
        await self.col_info_cm.create_index("code")
        await self.col_info_cm.create_index([("code", 1), ("endpoint", 1)], unique=False)
        await self.col_curve_map.create_index("date")
        await self.col_buybacks_hist.create_index([("exchange", 1), ("date", 1)])
        await self.col_cb_list_jsl.create_index("code", unique=True)
        await self.col_cov_list.create_index("code", unique=True)

    async def save_yield_curve(self, df: pd.DataFrame) -> int:
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
            ops.append(
                UpdateOne({"date": doc["date"], "tenor": doc["tenor"]}, {"$set": doc}, upsert=True)
            )
        if ops:
            res = await self.col_curve.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
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
        ops = []
        for it in items:
            code = str(it.get("code") or "").strip()
            if not code:
                continue
            doc = {
                "code": code,
                "name": it.get("name"),
                "exchange": it.get("exchange"),
                "category": (it.get("category") or "").lower() or None,
                "issuer": it.get("issuer"),
                "list_date": str(it.get("list_date")) if it.get("list_date") else None,
                "maturity_date": str(it.get("maturity_date")) if it.get("maturity_date") else None,
                "coupon_rate": it.get("coupon_rate"),
                "source": "akshare",
            }
            ops.append(UpdateOne({"code": code}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_basic.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
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
        items = [doc async for doc in cursor]
        return {"total": total, "items": items}

    async def save_spot_quotes(self, df: pd.DataFrame, category: str) -> int:
        if df is None or df.empty:
            return 0
        ops = []
        for _, r in df.iterrows():
            code = str(r.get("code") or r.get("债券代码") or r.get("可转债代码") or r.get("代码") or "").strip()
            if not code:
                continue
            ts = str(r.get("timestamp") or r.get("time") or r.get("日期") or r.get("date") or "").strip()
            doc = r.to_dict()
            doc.update({
                "code": code,
                "timestamp": ts,
                "category": category,
                "source": "akshare",
            })
            ops.append(
                UpdateOne({"code": code, "timestamp": ts, "category": category}, {"$set": doc}, upsert=True)
            )
        if ops:
            res = await self.col_spot.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
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
        for k in ("code", "证券代码", "债券代码", "可转债代码"):
            v = row.get(k)
            if v is not None and str(v).strip():
                return str(v).strip()
        return ""

    @staticmethod
    def _norm_date(row: dict) -> str:
        for k in ("date", "日期", "公告日期", "list_date", "上市日期"):
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
            filt = {"date": date}
            doc = row
            doc.update({"date": date, "source": "akshare"})
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
            ts = str(row.get("timestamp") or row.get("time") or row.get("时间") or row.get("日期") or "")
            doc = row
            doc.update({"code": code, "timestamp": ts, "source": "akshare"})
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
            doc.update({"code": code, "date": date, "source": "akshare"})
            ops.append(UpdateOne({"code": code, "date": date}, {"$set": doc}, upsert=True))
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
        ops = []
        for _, r in df.iterrows():
            row = r.to_dict()
            code = self._norm_code(row)
            doc = row
            doc.update({"code": code, "source": "akshare", "endpoint": "bond_info_detail_cm"})
            ops.append(UpdateOne({"code": code, "endpoint": "bond_info_detail_cm"}, {"$set": doc}, upsert=True))
        if ops:
            res = await self.col_info_cm.bulk_write(ops, ordered=False)
            return (res.upserted_count or 0) + (res.modified_count or 0)
        return 0
