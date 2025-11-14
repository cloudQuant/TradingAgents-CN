from typing import Iterable, Optional, List, Dict, Any
import asyncio
from datetime import datetime

import pandas as pd

from app.core.database import get_mongo_db
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
from tradingagents.utils.instrument_validator import normalize_bond_code


class BondSyncService:
    def __init__(self) -> None:
        self._provider = AKShareBondProvider()
        self._db = get_mongo_db()
        self._svc = BondDataService(self._db)

    async def ensure_indexes(self) -> None:
        await self._svc.ensure_indexes()

    async def sync_basic_list(self) -> dict:
        """同步债券基础信息列表（每日）。"""
        await self.ensure_indexes()
        try:
            items = await self._provider.get_symbol_list()
            if not items:
                return {"success": True, "saved": 0, "count": 0}
            saved = await self._svc.save_basic_list(items)
            return {"success": True, "saved": saved, "count": len(items)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_yield_curve(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
        await self.ensure_indexes()
        df = await self._provider.get_yield_curve(start_date, end_date)
        saved = await self._svc.save_yield_curve(df)
        return {
            "success": True,
            "saved": saved,
            "rows": 0 if df is None else len(df),
            "start": start_date,
            "end": end_date,
        }

    async def sync_bond_history(self, codes: Iterable[str], start_date: str, end_date: str) -> dict:
        await self.ensure_indexes()
        total_saved = 0
        total_rows = 0
        results = []
        for code in codes:
            df = await self._provider.get_historical_data(code, start_date, end_date, period="daily")
            norm = normalize_bond_code(code)
            code_std = norm.get("code_std") or code
            saved = await self._svc.save_bond_daily(code_std, df)
            rows = 0 if df is None else len(df)
            total_saved += saved
            total_rows += rows
            results.append({"code": code_std, "saved": saved, "rows": rows})
        return {
            "success": True,
            "total_saved": total_saved,
            "total_rows": total_rows,
            "items": results,
            "start": start_date,
            "end": end_date,
        }

    async def sync_spot_quotes(self) -> dict:
        """同步可转债和全部债券现货快照（EOD运行）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            saved_cov = 0
            saved_all = 0

            # 可转债现货
            try:
                df_cov = await asyncio.to_thread(ak.bond_zh_hs_cov_spot)
                if isinstance(df_cov, pd.DataFrame) and not df_cov.empty:
                    df_cov = df_cov.copy()
                    df_cov["timestamp"] = now_str
                    saved_cov = await self._svc.save_spot_quotes(df_cov, category="cov_spot")
            except Exception:
                pass

            # 全部债券现货
            try:
                df_all = await asyncio.to_thread(ak.bond_zh_hs_spot)
                if isinstance(df_all, pd.DataFrame) and not df_all.empty:
                    df_all = df_all.copy()
                    df_all["timestamp"] = now_str
                    saved_all = await self._svc.save_spot_quotes(df_all, category="hs_spot")
            except Exception:
                pass

            return {"success": True, "saved_cov": saved_cov, "saved_all": saved_all}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_us_yields(self) -> dict:
        """同步美国国债收益率（日度）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            df = await asyncio.to_thread(ak.bond_zh_us_rate)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return {"success": True, "saved": 0, "rows": 0}
            # 标准化到 (date, tenor, yield)
            if "日期" in df.columns:
                df = df.rename(columns={"日期": "date"})
            melt_cols = [c for c in df.columns if c != "date"]
            mdf = df.melt(id_vars=["date"], value_vars=melt_cols, var_name="tenor", value_name="yield")
            mdf["date"] = pd.to_datetime(mdf["date"]).dt.strftime("%Y-%m-%d")
            saved = await self._svc.save_us_yields(mdf)
            return {"success": True, "saved": saved, "rows": len(mdf)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_indices(self) -> dict:
        """同步债券相关指数（每日）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            total_rows = 0

            async def _save_index(df: pd.DataFrame, index_id: str) -> Dict[str, Any]:
                nonlocal total_saved, total_rows
                if not isinstance(df, pd.DataFrame) or df.empty:
                    return {"index_id": index_id, "saved": 0, "rows": 0}
                d = df.copy()
                # 规范日期列
                if "日期" in d.columns and "date" not in d.columns:
                    d.rename(columns={"日期": "date"}, inplace=True)
                # 选择 value 列
                value_col = None
                for c in ("收盘", "close", "指数", "value"):
                    if c in d.columns:
                        value_col = c
                        break
                if value_col is None:
                    # 若无常见列，则选择第一非日期列
                    value_candidates = [c for c in d.columns if c != "date"]
                    if not value_candidates:
                        return {"index_id": index_id, "saved": 0, "rows": 0}
                    value_col = value_candidates[0]
                d["date"] = pd.to_datetime(d["date"]).dt.strftime("%Y-%m-%d")
                saved = await self._svc.save_indices(d[["date", value_col]], index_id=index_id, value_column=value_col)
                rows = len(d)
                total_saved += saved
                total_rows += rows
                return {"index_id": index_id, "saved": saved, "rows": rows}

            results: List[Dict[str, Any]] = []
            try:
                df1 = await asyncio.to_thread(ak.bond_composite_index_cbond)
                results.append(await _save_index(df1, index_id="cbond_composite"))
            except Exception:
                results.append({"index_id": "cbond_composite", "saved": 0, "rows": 0, "error": "fetch_failed"})

            try:
                df2 = await asyncio.to_thread(ak.bond_new_composite_index_cbond)
                results.append(await _save_index(df2, index_id="cbond_new_composite"))
            except Exception:
                results.append({"index_id": "cbond_new_composite", "saved": 0, "rows": 0, "error": "fetch_failed"})

            try:
                df3 = await asyncio.to_thread(ak.bond_cb_index_jsl)
                results.append(await _save_index(df3, index_id="cb_jsl"))
            except Exception:
                results.append({"index_id": "cb_jsl", "saved": 0, "rows": 0, "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "total_rows": total_rows, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_cninfo_issues(self) -> dict:
        """同步发行公告（cninfo）。周度或日度运行。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            results: List[Dict[str, Any]] = []

            async def _save(df: pd.DataFrame, issue_type: str, endpoint: str):
                nonlocal total_saved
                if not isinstance(df, pd.DataFrame) or df.empty:
                    results.append({"endpoint": endpoint, "issue_type": issue_type, "saved": 0, "rows": 0})
                    return
                saved = await self._svc.save_cninfo_issues(df, issue_type=issue_type, endpoint=endpoint)
                total_saved += saved
                results.append({"endpoint": endpoint, "issue_type": issue_type, "saved": saved, "rows": len(df)})

            try:
                df1 = await asyncio.to_thread(ak.bond_corporate_issue_cninfo)
                await _save(df1, "corporate", "bond_corporate_issue_cninfo")
            except Exception:
                results.append({"endpoint": "bond_corporate_issue_cninfo", "error": "fetch_failed"})

            try:
                df2 = await asyncio.to_thread(ak.bond_local_government_issue_cninfo)
                await _save(df2, "local_government", "bond_local_government_issue_cninfo")
            except Exception:
                results.append({"endpoint": "bond_local_government_issue_cninfo", "error": "fetch_failed"})

            try:
                df3 = await asyncio.to_thread(ak.bond_treasure_issue_cninfo)
                await _save(df3, "treasury", "bond_treasure_issue_cninfo")
            except Exception:
                results.append({"endpoint": "bond_treasure_issue_cninfo", "error": "fetch_failed"})

            try:
                df4 = await asyncio.to_thread(ak.bond_cov_issue_cninfo)
                await _save(df4, "convertible", "bond_cov_issue_cninfo")
            except Exception:
                results.append({"endpoint": "bond_cov_issue_cninfo", "error": "fetch_failed"})

            try:
                df5 = await asyncio.to_thread(ak.bond_cov_stock_issue_cninfo)
                await _save(df5, "convertible_stock", "bond_cov_stock_issue_cninfo")
            except Exception:
                results.append({"endpoint": "bond_cov_stock_issue_cninfo", "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_cb_events_and_valuation(self) -> dict:
        """同步可转债调整、赎回、摘要、估值、对比（JS/新浪）。日度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            results: List[Dict[str, Any]] = []
            total_saved = 0

            async def _save_df(df: pd.DataFrame, save_fn: str, endpoint: str):
                nonlocal total_saved
                if not isinstance(df, pd.DataFrame) or df.empty:
                    results.append({"endpoint": endpoint, "saved": 0, "rows": 0})
                    return
                fn = getattr(self._svc, save_fn)
                saved = await fn(df)
                total_saved += saved
                results.append({"endpoint": endpoint, "saved": saved, "rows": len(df)})

            try:
                df1 = await asyncio.to_thread(ak.bond_cb_adj_logs_jsl)
                await _save_df(df1, "save_cb_adjustments", "bond_cb_adj_logs_jsl")
            except Exception:
                results.append({"endpoint": "bond_cb_adj_logs_jsl", "error": "fetch_failed"})
            try:
                df2 = await asyncio.to_thread(ak.bond_cb_redeem_jsl)
                await _save_df(df2, "save_cb_redeems", "bond_cb_redeem_jsl")
            except Exception:
                results.append({"endpoint": "bond_cb_redeem_jsl", "error": "fetch_failed"})
            try:
                df3 = await asyncio.to_thread(ak.bond_cb_summary_sina)
                await _save_df(df3, "save_cb_summary", "bond_cb_summary_sina")
            except Exception:
                results.append({"endpoint": "bond_cb_summary_sina", "error": "fetch_failed"})
            try:
                df4 = await asyncio.to_thread(ak.bond_zh_cov_value_analysis)
                await _save_df(df4, "save_cb_valuation", "bond_zh_cov_value_analysis")
            except Exception:
                results.append({"endpoint": "bond_zh_cov_value_analysis", "error": "fetch_failed"})
            try:
                df5 = await asyncio.to_thread(ak.bond_cov_comparison)
                await _save_df(df5, "save_cb_comparison", "bond_cov_comparison")
            except Exception:
                results.append({"endpoint": "bond_cov_comparison", "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_spot_quote_and_deals(self) -> dict:
        """同步现货报价与成交明细（日度或交易时段）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            results: List[Dict[str, Any]] = []

            try:
                dfq = await asyncio.to_thread(ak.bond_spot_quote)
                if isinstance(dfq, pd.DataFrame) and not dfq.empty:
                    saved = await self._svc.save_spot_quote_detail(dfq)
                    total_saved += saved
                    results.append({"endpoint": "bond_spot_quote", "saved": saved, "rows": len(dfq)})
            except Exception:
                results.append({"endpoint": "bond_spot_quote", "error": "fetch_failed"})

            try:
                dfd = await asyncio.to_thread(ak.bond_spot_deal)
                if isinstance(dfd, pd.DataFrame) and not dfd.empty:
                    saved = await self._svc.save_spot_deals(dfd)
                    total_saved += saved
                    results.append({"endpoint": "bond_spot_deal", "saved": saved, "rows": len(dfd)})
            except Exception:
                results.append({"endpoint": "bond_spot_deal", "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_sse_summaries(self) -> dict:
        """同步上交所成交/资金摘要（EOD）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            results: List[Dict[str, Any]] = []

            try:
                dfs = await asyncio.to_thread(ak.bond_deal_summary_sse)
                if isinstance(dfs, pd.DataFrame) and not dfs.empty:
                    saved = await self._svc.save_deal_summary(dfs)
                    total_saved += saved
                    results.append({"endpoint": "bond_deal_summary_sse", "saved": saved, "rows": len(dfs)})
            except Exception:
                results.append({"endpoint": "bond_deal_summary_sse", "error": "fetch_failed"})

            try:
                dfc = await asyncio.to_thread(ak.bond_cash_summary_sse)
                if isinstance(dfc, pd.DataFrame) and not dfc.empty:
                    saved = await self._svc.save_cash_summary(dfc)
                    total_saved += saved
                    results.append({"endpoint": "bond_cash_summary_sse", "saved": saved, "rows": len(dfc)})
            except Exception:
                results.append({"endpoint": "bond_cash_summary_sse", "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_nafmii(self) -> dict:
        """同步银行间市场（NAFMII）。周度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            df = await asyncio.to_thread(ak.bond_debt_nafmii)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return {"success": True, "saved": 0, "rows": 0}
            saved = await self._svc.save_nafmii(df)
            return {"success": True, "saved": saved, "rows": len(df)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_info_cm(self) -> dict:
        """同步中债信息（cm）。周度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            df = await asyncio.to_thread(ak.bond_info_cm)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return {"success": True, "saved": 0, "rows": 0}
            saved = await self._svc.save_info_cm(df)
            return {"success": True, "saved": saved, "rows": len(df)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_yield_curve_map(self) -> dict:
        """同步收益率曲线映射（close_return_map）。日度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            df = await asyncio.to_thread(ak.bond_china_close_return_map)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return {"success": True, "saved": 0, "rows": 0}
            saved = await self._svc.save_yield_curve_map(df)
            return {"success": True, "saved": saved, "rows": len(df)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_buybacks_history(self) -> dict:
        """同步回购历史。周度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            df = await asyncio.to_thread(ak.bond_buy_back_hist_em)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return {"success": True, "saved": 0, "rows": 0}
            saved = await self._svc.save_buybacks_history(df)
            return {"success": True, "saved": saved, "rows": len(df)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_cb_lists(self) -> dict:
        """同步可转债列表（集思录/东方财富）。周度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            results: List[Dict[str, Any]] = []
            try:
                df1 = await asyncio.to_thread(ak.bond_cb_jsl)
                if isinstance(df1, pd.DataFrame) and not df1.empty:
                    s1 = await self._svc.save_cb_list_jsl(df1)
                    total_saved += s1
                    results.append({"endpoint": "bond_cb_jsl", "saved": s1, "rows": len(df1)})
            except Exception:
                results.append({"endpoint": "bond_cb_jsl", "error": "fetch_failed"})
            try:
                df2 = await asyncio.to_thread(ak.bond_zh_cov)
                if isinstance(df2, pd.DataFrame) and not df2.empty:
                    s2 = await self._svc.save_cov_list(df2)
                    total_saved += s2
                    results.append({"endpoint": "bond_zh_cov", "saved": s2, "rows": len(df2)})
            except Exception:
                results.append({"endpoint": "bond_zh_cov", "error": "fetch_failed"})
            return {"success": True, "total_saved": total_saved, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_info_cm_queries(self) -> dict:
        """同步中债信息的查询与详情（cm_query/detail）。周度。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            results: List[Dict[str, Any]] = []
            try:
                dfq = await asyncio.to_thread(ak.bond_info_cm_query)
                if isinstance(dfq, pd.DataFrame) and not dfq.empty:
                    sq = await self._svc.save_info_cm_query(dfq)
                    total_saved += sq
                    results.append({"endpoint": "bond_info_cm_query", "saved": sq, "rows": len(dfq)})
            except Exception:
                results.append({"endpoint": "bond_info_cm_query", "error": "fetch_failed"})

            try:
                dfd = await asyncio.to_thread(ak.bond_info_detail_cm)
                if isinstance(dfd, pd.DataFrame) and not dfd.empty:
                    sd = await self._svc.save_info_cm_detail(dfd)
                    total_saved += sd
                    results.append({"endpoint": "bond_info_detail_cm", "saved": sd, "rows": len(dfd)})
            except Exception:
                results.append({"endpoint": "bond_info_detail_cm", "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_cb_profiles(self, limit: int = 200) -> dict:
        """每周同步可转债档案（批量、受限速）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            items = await self._provider.get_symbol_list()
            codes = [it.get("code") for it in items if it.get("code")][:limit]
            profiles: List[Dict[str, Any]] = []
            for code in codes:
                try:
                    # 使用多候选符号
                    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
                    prov = AKShareBondProvider()
                    cands = prov._symbol_candidates_for_ak(code)
                    df = None
                    for sym in cands:
                        try:
                            df = await asyncio.to_thread(ak.bond_cb_profile_sina, sym)
                            if isinstance(df, pd.DataFrame) and not df.empty:
                                break
                        except Exception:
                            continue
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        rec = {"code": code, "source": "akshare", "provider_symbol": sym}
                        # 将 DataFrame 转为键值映射
                        try:
                            dct = df.set_index(df.columns[0]).iloc[:, 0].to_dict()
                            rec.update({str(k): dct[k] for k in dct})
                        except Exception:
                            rec["raw"] = df.to_dict(orient="records")
                        profiles.append(rec)
                except Exception:
                    continue
            saved = await self._svc.save_cb_profiles(profiles)
            return {"success": True, "saved": saved, "count": len(profiles)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def sync_buybacks(self) -> dict:
        """每周同步回购数据（上交所、深交所）。"""
        await self.ensure_indexes()
        try:
            try:
                import akshare as ak  # type: ignore
            except Exception:
                return {"success": False, "error": "akshare_not_available"}

            total_saved = 0
            total_rows = 0
            results = []
            try:
                df_sh = await asyncio.to_thread(ak.bond_sh_buy_back_em)
                if isinstance(df_sh, pd.DataFrame) and not df_sh.empty:
                    saved = await self._svc.save_buybacks(df_sh, exchange="SH")
                    total_saved += saved
                    total_rows += len(df_sh)
                    results.append({"exchange": "SH", "saved": saved, "rows": len(df_sh)})
            except Exception:
                results.append({"exchange": "SH", "saved": 0, "rows": 0, "error": "fetch_failed"})

            try:
                df_sz = await asyncio.to_thread(ak.bond_sz_buy_back_em)
                if isinstance(df_sz, pd.DataFrame) and not df_sz.empty:
                    saved = await self._svc.save_buybacks(df_sz, exchange="SZ")
                    total_saved += saved
                    total_rows += len(df_sz)
                    results.append({"exchange": "SZ", "saved": saved, "rows": len(df_sz)})
            except Exception:
                results.append({"exchange": "SZ", "saved": 0, "rows": 0, "error": "fetch_failed"})

            return {"success": True, "total_saved": total_saved, "total_rows": total_rows, "items": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
