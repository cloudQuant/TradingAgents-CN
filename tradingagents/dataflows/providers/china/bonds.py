import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

import pandas as pd

try:
    import akshare as ak
except Exception:  # pragma: no cover
    ak = None  # type: ignore

from tradingagents.utils.logging_manager import get_logger
from tradingagents.utils.instrument_validator import normalize_bond_code

logger = get_logger("akshare_bonds_provider")


class AKShareBondProvider:
    def __init__(self) -> None:
        if ak is None:
            logger.warning("AKShare is not available. Bond provider will be limited.")

    async def get_symbol_list(self) -> List[Dict[str, Any]]:
        if ak is None:
            return []
        df_cov: Optional[pd.DataFrame] = None
        df_all: Optional[pd.DataFrame] = None
        # 同时尝试获取可转债与全部债券现货，合并后分类
        try:
            df_cov = await asyncio.to_thread(ak.bond_zh_hs_cov_spot)
        except Exception as e:
            logger.debug(f"bond_zh_hs_cov_spot failed: {e}")
        try:
            df_all = await asyncio.to_thread(ak.bond_zh_hs_spot)
        except Exception as e2:
            logger.debug(f"bond_zh_hs_spot failed: {e2}")

        if df_cov is None and df_all is None:
            return []
        if df_cov is not None and df_all is not None:
            try:
                df = pd.concat([df_cov, df_all], ignore_index=True)
            except Exception:
                df = df_cov if not df_cov.empty else df_all
        else:
            df = df_cov if df_cov is not None else df_all
        if df is None or df.empty:
            return []

        code_cols = [
            "债券代码",
            "可转债代码",
            "代码",
            "bond_code",
            "code",
        ]
        name_cols = [
            "债券名称",
            "可转债名称",
            "名称",
            "bond_name",
            "name",
        ]
        type_cols = [
            "债券类型",
            "类型",
            "bond_type",
            "type",
        ]
        maturity_cols = [
            "到期日",
            "到期日期",
            "债券到期日",
            "maturity",
            "maturity_date",
        ]
        issuer_cols = [
            "发行人",
            "发行主体",
            "发行人全称",
            "主体",
            "issuer",
            "issuer_name",
        ]
        list_date_cols = [
            "上市日期",
            "上市日",
            "list_date",
        ]
        coupon_cols = [
            "票面利率",
            "息票率",
            "利率",
            "coupon",
        ]

        code_col = next((c for c in code_cols if c in df.columns), None)
        name_col = next((c for c in name_cols if c in df.columns), None)
        type_col = next((c for c in type_cols if c in df.columns), None)
        maturity_col = next((c for c in maturity_cols if c in df.columns), None)
        issuer_col = next((c for c in issuer_cols if c in df.columns), None)
        list_date_col = next((c for c in list_date_cols if c in df.columns), None)
        coupon_col = next((c for c in coupon_cols if c in df.columns), None)
        if code_col is None:
            # 尝试从 index 提取，不行则返回空
            try:
                df = df.reset_index()
                code_col = next((c for c in code_cols if c in df.columns), None)
            except Exception:
                code_col = None
        if code_col is None:
            return []

        def _classify(name: str, raw_code: str, type_val: Optional[str]) -> str:
            s = (name or "").upper()
            t = (type_val or "").upper()
            rc = (raw_code or "").upper()
            # 可转债
            if any(k in s for k in ["转债", "可转", "CB"]) or any(rc.startswith(p) for p in ["113", "110", "118", "123", "127", "128"]):
                return "convertible"
            # 可交换债
            if "交换" in s or "EB" in s or "EXCHANGE" in s:
                return "exchangeable"
            # 利率债（国债/政金/地方债等）
            if any(k in s for k in ["国债", "政金", "政策性", "国开", "农发", "口行", "地方债", "地方政府债", "国债ETF"]):
                return "interest"
            # 信用债（公司/企业债等）
            if any(k in s for k in ["公司债", "企业债", "私募债", "中票", "短融", "公司"]) or "CORP" in t or "CORPORATE" in t:
                return "credit"
            # 类型列直接指示
            if any(k in t for k in ["CONVERT", "可转", "转债"]):
                return "convertible"
            if any(k in t for k in ["EXCHANGE", "交换"]):
                return "exchangeable"
            if any(k in t for k in ["GOV", "TREAS", "国债", "利率", "政策性", "政金"]):
                return "interest"
            if any(k in t for k in ["CREDIT", "公司", "企业", "公司债"]):
                return "credit"
            return "other"

        items: List[Dict[str, Any]] = []
        for _, row in df.iterrows():
            raw = str(row[code_col]).strip()
            nm = str(row[name_col]).strip() if name_col and row.get(name_col) is not None else ""
            tp = str(row[type_col]).strip() if type_col and row.get(type_col) is not None else None
            mt = row[maturity_col] if maturity_col and row.get(maturity_col) is not None else None
            # 规范日期格式
            if isinstance(mt, pd.Timestamp):
                mt_str = mt.strftime("%Y-%m-%d")
            else:
                try:
                    mt_str = pd.to_datetime(mt).strftime("%Y-%m-%d") if mt else None
                except Exception:
                    mt_str = None
            issuer = str(row[issuer_col]).strip() if issuer_col and row.get(issuer_col) is not None else None
            ld = row[list_date_col] if list_date_col and row.get(list_date_col) is not None else None
            if isinstance(ld, pd.Timestamp):
                list_date_str = ld.strftime("%Y-%m-%d")
            else:
                try:
                    list_date_str = pd.to_datetime(ld).strftime("%Y-%m-%d") if ld else None
                except Exception:
                    list_date_str = None
            coupon_val = row[coupon_col] if coupon_col and row.get(coupon_col) is not None else None
            coupon_rate: Optional[float] = None
            if coupon_val is not None:
                try:
                    if isinstance(coupon_val, str) and coupon_val.endswith('%'):
                        coupon_rate = float(coupon_val.strip('%'))
                    else:
                        coupon_rate = float(coupon_val)
                except Exception:
                    coupon_rate = None
            norm = normalize_bond_code(raw)
            cat = _classify(nm, raw, tp)
            items.append({
                "code": norm["code_std"],
                "name": nm,
                "raw_code": raw,
                "exchange": norm.get("exchange"),
                "category": cat,
                "maturity_date": mt_str,
                "type": tp,
                "issuer": issuer,
                "list_date": list_date_str,
                "coupon_rate": coupon_rate,
            })
        return items

    async def get_basic_info(self, code: str) -> Dict[str, Any]:
        if ak is None:
            return {"error": "akshare_not_available"}
        symbols = self._symbol_candidates_for_ak(code)
        last_err: Optional[str] = None
        for sym in symbols:
            for fn in ("bond_zh_cov_info", "bond_zh_cov_info_ths", "bond_cb_profile_sina"):
                try:
                    func = getattr(ak, fn)
                except AttributeError:
                    continue
                try:
                    df = await asyncio.to_thread(func, sym)
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        return {
                            "code": normalize_bond_code(code)["code_std"],
                            "provider_symbol": sym,
                            "data": df.to_dict(orient="records"),
                            "source": "akshare",
                            "f": fn,
                        }
                except Exception as e:
                    last_err = str(e)
                    continue
        return {
            "code": normalize_bond_code(code)["code_std"],
            "provider_symbol": symbols[0] if symbols else code,
            "error": last_err or "no_basic_info",
            "source": "akshare",
        }

    async def get_historical_data(
        self,
        code: str,
        start_date: Optional[str],
        end_date: Optional[str],
        period: str = "daily",
    ) -> pd.DataFrame:
        if ak is None:
            return pd.DataFrame()
        if period != "daily":
            logger.warning(f"Unsupported period for bonds: {period}, falling back to daily")
        symbols = self._symbol_candidates_for_ak(code)
        last_exc: Optional[Exception] = None
        for sym in symbols:
            try:
                df = await asyncio.to_thread(ak.bond_zh_hs_cov_daily, sym)
                if not isinstance(df, pd.DataFrame) or df.empty:
                    continue
                df = self._standardize_hist(df)
                if start_date:
                    df = df[df["date"] >= start_date]
                if end_date:
                    df = df[df["date"] <= end_date]
                return df.reset_index(drop=True)
            except Exception as e:
                last_exc = e
                continue
        logger.debug(f"get_historical_data failed. last_exc={last_exc}")
        return pd.DataFrame()

    async def get_realtime_quote(self, code: str) -> Dict[str, Any]:
        if ak is None:
            return {"error": "akshare_not_available"}
        try:
            df = await asyncio.to_thread(ak.bond_zh_hs_cov_spot)
            if isinstance(df, pd.DataFrame) and not df.empty:
                norm = normalize_bond_code(code)
                digits = norm["digits"]
                # 可能的代码列
                for c in ["债券代码", "可转债代码", "代码", "bond_code", "code"]:
                    if c in df.columns:
                        sub = df[df[c].astype(str).str.strip() == digits]
                        if not sub.empty:
                            return {
                                "code": norm["code_std"],
                                "snapshot": sub.iloc[0].to_dict(),
                                "source": "akshare",
                            }
        except Exception as e:
            return {"error": str(e)}
        return {"error": "not_found"}

    async def get_yield_curve(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        if ak is None:
            return pd.DataFrame()
        try:
            df = await asyncio.to_thread(ak.bond_china_yield)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return pd.DataFrame()
            # 标准化
            if "日期" in df.columns:
                df.rename(columns={"日期": "date"}, inplace=True)
            # 展平不同期限列到 (date, tenor, yield)
            melt_cols = [c for c in df.columns if c != "date"]
            mdf = df.melt(id_vars=["date"], value_vars=melt_cols, var_name="tenor", value_name="yield")
            mdf["date"] = pd.to_datetime(mdf["date"]).dt.strftime("%Y-%m-%d")
            if start_date:
                mdf = mdf[mdf["date"] >= start_date]
            if end_date:
                mdf = mdf[mdf["date"] <= end_date]
            return mdf.reset_index(drop=True)
        except Exception:
            # 尝试 close_return 作为回退
            try:
                df2 = await asyncio.to_thread(ak.bond_china_close_return)
                if not isinstance(df2, pd.DataFrame) or df2.empty:
                    return pd.DataFrame()
                if "日期" in df2.columns:
                    df2.rename(columns={"日期": "date"}, inplace=True)
                melt_cols = [c for c in df2.columns if c != "date"]
                mdf2 = df2.melt(id_vars=["date"], value_vars=melt_cols, var_name="tenor", value_name="yield")
                mdf2["date"] = pd.to_datetime(mdf2["date"]).dt.strftime("%Y-%m-%d")
                if start_date:
                    mdf2 = mdf2[mdf2["date"] >= start_date]
                if end_date:
                    mdf2 = mdf2[mdf2["date"] <= end_date]
                return mdf2.reset_index(drop=True)
            except Exception as e2:
                logger.debug(f"bond_china_yield/close_return failed: {e2}")
                return pd.DataFrame()

    def _standardize_hist(self, df: pd.DataFrame) -> pd.DataFrame:
        # 常见列标准化到统一输出
        rename_map = {
            "日期": "date",
            "交易日期": "date",
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close",
            "成交量": "volume",
            "成交额": "amount",
        }
        for k, v in rename_map.items():
            if k in df.columns and v not in df.columns:
                df.rename(columns={k: v}, inplace=True)
        if "date" in df.columns:
            try:
                df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            except Exception:
                pass
        # 仅保留常用列
        keep = [c for c in ["date", "open", "high", "low", "close", "volume", "amount"] if c in df.columns]
        return df[keep] if keep else df

    def _symbol_candidates_for_ak(self, code: str) -> List[str]:
        norm = normalize_bond_code(code)
        digits = norm["digits"]
        # 顺序：带前缀 → 裸码
        cands = [f"sh{digits}", f"sz{digits}", f"SH{digits}", f"SZ{digits}", digits]
        # 如果输入已经包含后缀，则优先按后缀推断
        if norm.get("exchange") == "SH":
            cands = [f"sh{digits}", f"SH{digits}"] + cands
        elif norm.get("exchange") == "SZ":
            cands = [f"sz{digits}", f"SZ{digits}"] + cands
        # 去重保持顺序
        seen = set()
        ordered: List[str] = []
        for s in cands:
            if s not in seen:
                seen.add(s)
                ordered.append(s)
        return ordered
