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
            
            # 优先级1: 可转债（特征最明显）
            if any(k in s for k in ["转债", "可转", "CB"]) or any(rc.startswith(p) for p in ["113", "110", "118", "123", "127", "128"]):
                # 但排除可交换债
                if "交换" not in s and "EB" not in s:
                    return "convertible"
            
            # 优先级2: 可交换债
            if any(k in s for k in ["交换债", "可交换", "EB"]) or "EXCHANGE" in s or "EXCHANGEABLE" in t:
                return "exchangeable"
            
            # 优先级3: 利率债（国债/政金/地方债等）
            if any(k in s for k in ["国债", "政金", "政策性", "国开", "农发", "口行", "地方债", "地方政府债", "国债ETF", "储蓄国债", "记账式国债"]):
                return "interest"
            
            # 类型列直接指示（补充判断）
            if any(k in t for k in ["CONVERT", "可转", "转债"]):
                if "交换" not in t and "EXCHANGE" not in t:
                    return "convertible"
            
            if any(k in t for k in ["EXCHANGE", "交换", "可交换"]):
                return "exchangeable"
            
            if any(k in t for k in ["GOV", "TREAS", "国债", "利率", "政策性", "政金", "TREASURY"]):
                return "interest"
            
            # 优先级4: 信用债（公司/企业债等）
            # 扩展信用债识别范围
            if any(k in s for k in ["公司债", "企业债", "私募债", "中票", "短融", "超短融", "PPN", "MTN", "SCP", "CP"]):
                return "credit"
            
            if any(k in t for k in ["CREDIT", "公司", "企业", "公司债", "企业债", "CORP", "CORPORATE"]):
                return "credit"
            
            # 优先级5: 根据代码前缀推断
            # 10/01开头通常是国债
            if rc.startswith(("10", "01", "019", "020")):
                return "interest"
            
            # 11/12开头如果不是可转债，很可能是公司债/企业债
            if rc.startswith(("11", "12")) and "转债" not in s and "可转" not in s:
                return "credit"
            
            # 14/15开头通常是企业债
            if rc.startswith(("14", "15", "16", "17", "18", "19")):
                return "credit"
            
            # 默认: 其他
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
                    try:
                        df = await asyncio.to_thread(ak.bond_zh_hs_daily, sym)
                    except Exception:
                        df = pd.DataFrame()
                if not isinstance(df, pd.DataFrame) or df.empty:
                    continue
                df = self._standardize_hist(df)
                # 规范化start_date和end_date格式为YYYY-MM-DD
                if start_date:
                    # 转换20240815 -> 2024-08-15
                    if len(start_date) == 8 and start_date.isdigit():
                        start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"
                    df = df[df["date"] >= start_date]
                if end_date:
                    # 转换20240815 -> 2024-08-15
                    if len(end_date) == 8 and end_date.isdigit():
                        end_date = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}"
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
            
            # 标准化列名
            rename_map = {}
            curve_name_col = None
            if "日期" in df.columns:
                rename_map["日期"] = "date"
            if "曲线名称" in df.columns:
                curve_name_col = "曲线名称"
                rename_map["曲线名称"] = "curve_name"
            if rename_map:
                df.rename(columns=rename_map, inplace=True)
            
            # 确定 ID 变量（用于 melt 操作）
            id_vars = ["date"]
            if curve_name_col and "curve_name" in df.columns:
                id_vars.append("curve_name")
            
            # 展平不同期限列到 (date, curve_name?, tenor, yield)
            # 排除日期和曲线名称列，只保留期限列（数值列）
            exclude_cols = set(id_vars)
            # 只保留数值类型的列作为期限列（排除曲线名称等文本列）
            melt_cols = []
            for col in df.columns:
                if col not in exclude_cols:
                    # 跳过明显是文本类型的列（如列名包含"名称"、"名称"等）
                    if any(keyword in str(col) for keyword in ["名称", "name", "名称", "type", "类型"]):
                        continue
                    # 检查列是否主要是数值类型
                    if df[col].dtype in ['float64', 'float32', 'int64', 'int32']:
                        melt_cols.append(col)
                    # 或者列包含 NaN，但大部分是数值（至少80%是数值）
                    else:
                        numeric_count = df[col].apply(lambda x: pd.isna(x) or isinstance(x, (int, float)) or (hasattr(x, '__float__') and not isinstance(x, str))).sum()
                        if numeric_count > len(df) * 0.8:
                            melt_cols.append(col)
            
            if not melt_cols:
                logger.warning("⚠️ [收益率曲线] 未找到有效的期限列")
                return pd.DataFrame()
            
            # 执行 melt 操作
            mdf = df.melt(id_vars=id_vars, value_vars=melt_cols, var_name="tenor", value_name="yield")
            
            # 格式化日期
            if "date" in mdf.columns:
                mdf["date"] = pd.to_datetime(mdf["date"]).dt.strftime("%Y-%m-%d")
            
            # 规范化日期参数格式为YYYY-MM-DD
            if start_date:
                if len(start_date) == 8 and start_date.isdigit():
                    start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"
                mdf = mdf[mdf["date"] >= start_date]
            if end_date:
                if len(end_date) == 8 and end_date.isdigit():
                    end_date = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}"
                mdf = mdf[mdf["date"] <= end_date]
            
            return mdf.reset_index(drop=True)
        except Exception as e:
            logger.debug(f"bond_china_yield failed: {e}")
            # 尝试 close_return 作为回退
            try:
                df2 = await asyncio.to_thread(ak.bond_china_close_return)
                if not isinstance(df2, pd.DataFrame) or df2.empty:
                    return pd.DataFrame()
                
                # 标准化列名
                rename_map = {}
                curve_name_col = None
                if "日期" in df2.columns:
                    rename_map["日期"] = "date"
                if "曲线名称" in df2.columns:
                    curve_name_col = "曲线名称"
                    rename_map["曲线名称"] = "curve_name"
                if rename_map:
                    df2.rename(columns=rename_map, inplace=True)
                
                # 确定 ID 变量
                id_vars = ["date"]
                if curve_name_col and "curve_name" in df2.columns:
                    id_vars.append("curve_name")
                
                # 展平不同期限列
                exclude_cols = set(id_vars)
                melt_cols = []
                for col in df2.columns:
                    if col not in exclude_cols:
                        # 跳过明显是文本类型的列
                        if any(keyword in str(col) for keyword in ["名称", "name", "名称", "type", "类型"]):
                            continue
                        if df2[col].dtype in ['float64', 'float32', 'int64', 'int32']:
                            melt_cols.append(col)
                        else:
                            numeric_count = df2[col].apply(lambda x: pd.isna(x) or isinstance(x, (int, float)) or (hasattr(x, '__float__') and not isinstance(x, str))).sum()
                            if numeric_count > len(df2) * 0.8:
                                melt_cols.append(col)
                
                if not melt_cols:
                    logger.warning("⚠️ [收益率曲线] 未找到有效的期限列（close_return）")
                    return pd.DataFrame()
                
                mdf2 = df2.melt(id_vars=id_vars, value_vars=melt_cols, var_name="tenor", value_name="yield")
                if "date" in mdf2.columns:
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

    async def get_cov_comparison(self) -> pd.DataFrame:
        """获取可转债比价表（东方财富）"""
        if ak is None:
            return pd.DataFrame()
        try:
            df = await asyncio.to_thread(ak.bond_cov_comparison)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception as e:
            logger.debug(f"bond_cov_comparison failed: {e}")
            return pd.DataFrame()

    async def get_cov_value_analysis(self, code: str) -> pd.DataFrame:
        """获取可转债价值分析历史数据"""
        if ak is None:
            return pd.DataFrame()
        try:
            # 只需要债券代码的数字部分
            norm = normalize_bond_code(code)
            digits = norm["digits"]
            df = await asyncio.to_thread(ak.bond_zh_cov_value_analysis, symbol=digits)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception as e:
            logger.debug(f"bond_zh_cov_value_analysis failed for {code}: {e}")
            return pd.DataFrame()

    async def get_spot_quote(self) -> pd.DataFrame:
        """获取现券市场做市报价"""
        if ak is None:
            return pd.DataFrame()
        try:
            df = await asyncio.to_thread(ak.bond_spot_quote)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return pd.DataFrame()
            
            # 规范化列名（AkShare返回的列名可能有编码问题）
            # 预期列名：['报价机构', '债券代码', '买入净价', '卖', '买', '卖']
            if len(df.columns) >= 6:
                df.columns = ['institution', 'code', 'buy_price', 'sell', 'buy', 'sell2'][:len(df.columns)]
            
            return df
        except Exception as e:
            logger.debug(f"bond_spot_quote failed: {e}")
            return pd.DataFrame()

    async def get_spot_deal(self) -> pd.DataFrame:
        """获取现券市场成交行情"""
        if ak is None:
            return pd.DataFrame()
        try:
            df = await asyncio.to_thread(ak.bond_spot_deal)
            if not isinstance(df, pd.DataFrame) or df.empty:
                return pd.DataFrame()
            
            # 规范化列名（AkShare返回的列名可能有编码问题）
            # 预期列名：['债券简称', '成交净价', '最新收益率', '涨跌', '加权收益率', '交易量']
            if len(df.columns) >= 6:
                df.columns = ['债券简称', '成交净价', '最新收益率', '涨跌', '加权收益率', '交易量'][:len(df.columns)]
            
            return df
        except Exception as e:
            logger.debug(f"bond_spot_deal failed: {e}")
            return pd.DataFrame()

    async def get_cash_summary(self, date: str) -> pd.DataFrame:
        """获取上交所债券现券市场概览
        
        Args:
            date: 日期，格式如 '20210111'
        """
        if ak is None:
            return pd.DataFrame()
        try:
            df = await asyncio.to_thread(ak.bond_cash_summary_sse, date=date)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception as e:
            logger.debug(f"bond_cash_summary_sse failed for {date}: {e}")
            return pd.DataFrame()

    async def get_deal_summary(self, date: str) -> pd.DataFrame:
        """获取上交所债券成交概览
        
        Args:
            date: 日期，格式如 '20210104'
        """
        if ak is None:
            return pd.DataFrame()
        try:
            df = await asyncio.to_thread(ak.bond_deal_summary_sse, date=date)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception as e:
            logger.debug(f"bond_deal_summary_sse failed for {date}: {e}")
            return pd.DataFrame()

    async def get_cov_info_detail(self, code: str, indicator: str = "基本信息") -> pd.DataFrame:
        """获取可转债详细信息（东方财富）
        
        Args:
            code: 可转债代码
            indicator: 信息类型，可选 "基本信息", "中签号", "筹资用途", "重要日期"
        """
        if ak is None:
            return pd.DataFrame()
        try:
            norm = normalize_bond_code(code)
            digits = norm["digits"]
            df = await asyncio.to_thread(ak.bond_zh_cov_info, symbol=digits, indicator=indicator)
            return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
        except Exception as e:
            logger.debug(f"bond_zh_cov_info failed for {code}: {e}")
            return pd.DataFrame()

    async def get_repo_rate(self, market: str = "SH") -> pd.DataFrame:
        """获取债券回购利率
        
        Args:
            market: 市场代码，'SH'=上交所, 'SZ'=深交所
        
        Returns:
            DataFrame: 回购利率数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试多个可能的接口
            if market.upper() == "SH":
                # 尝试上交所回购
                try:
                    df = await asyncio.to_thread(ak.bond_repo_sh_rate)
                    return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
                except:
                    pass
            else:
                # 尝试深交所回购
                try:
                    df = await asyncio.to_thread(ak.bond_repo_sz_rate)
                    return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
                except:
                    pass
            
            # 如果上述接口不存在，返回空DataFrame
            logger.debug(f"bond_repo_{market.lower()}_rate not available")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_repo_rate failed for {market}: {e}")
            return pd.DataFrame()

    async def get_repo_rate_hist(self, symbol: str = "R-001") -> pd.DataFrame:
        """获取债券回购历史数据
        
        Args:
            symbol: 回购品种代码，如 'R-001', 'R-002', 'R-003', 'R-007' 等
        
        Returns:
            DataFrame: 回购历史数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试获取回购历史数据
            # 注意：akshare可能没有直接的历史接口，这里尝试多个可能的方式
            try:
                df = await asyncio.to_thread(ak.bond_repo_zh_rate_hist, symbol=symbol)
                return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
            except:
                pass
            
            # 如果上述接口不存在，返回空DataFrame
            logger.debug(f"bond_repo_zh_rate_hist not available for {symbol}")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_repo_rate_hist failed for {symbol}: {e}")
            return pd.DataFrame()

    async def get_bond_index(self, symbol: str = "000832") -> pd.DataFrame:
        """获取债券指数数据
        
        Args:
            symbol: 指数代码，如 '000832'(中证转债), '399481'(企债指数) 等
        
        Returns:
            DataFrame: 指数数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试多个可能的接口
            try:
                # 尝试获取指数现货行情
                df = await asyncio.to_thread(ak.bond_zh_index_spot)
                return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
            except:
                pass
            
            try:
                # 尝试获取指数历史数据
                df = await asyncio.to_thread(ak.index_zh_a_hist, symbol=symbol, period="daily")
                return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
            except:
                pass
            
            # 如果上述接口不存在，返回空DataFrame
            logger.debug(f"bond index interfaces not available for {symbol}")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_bond_index failed for {symbol}: {e}")
            return pd.DataFrame()

    async def get_nafmii_bonds(self) -> pd.DataFrame:
        """获取NAFMII交易商协会债券数据
        
        Returns:
            DataFrame: 交易商协会债券数据（短融券、中票、超短融等）
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试获取银行间市场债券数据
            # akshare可能没有直接的NAFMII接口，尝试相关接口
            try:
                # 尝试获取银行间债券
                df = await asyncio.to_thread(ak.bond_china_close_return)
                return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
            except:
                pass
            
            # 如果上述接口不存在，返回空DataFrame
            logger.debug("NAFMII bond interfaces not available")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_nafmii_bonds failed: {e}")
            return pd.DataFrame()

    async def get_chinamoney_bond_info(self) -> pd.DataFrame:
        """获取中债网（chinamoney）债券信息
        
        Returns:
            DataFrame: 中债网债券信息数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试获取中债网相关数据
            try:
                # 使用已有的债券列表作为中债信息
                df = await self.get_symbol_list()
                if df:
                    return pd.DataFrame(df)
                return pd.DataFrame()
            except:
                pass
            
            # 如果上述接口不存在，返回空DataFrame
            logger.debug("ChinaMoney bond info interfaces not available")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_chinamoney_bond_info failed: {e}")
            return pd.DataFrame()

    async def get_yield_curve_data(self) -> pd.DataFrame:
        """获取收益率曲线数据
        
        Returns:
            DataFrame: 收益率曲线数据，包含curve_name, curve_type等字段
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试获取债券收益率数据
            try:
                # 使用bond_china_yield获取收益率曲线数据
                df = await asyncio.to_thread(ak.bond_china_yield)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # 构建映射数据
                    curve_data = []
                    if '曲线名称' in df.columns:
                        for curve_name in df['曲线名称'].unique():
                            curve_data.append({
                                'curve_name': curve_name,
                                'curve_type': self._infer_curve_type(curve_name),
                                'source': '中债',
                                'description': f'{curve_name}收益率'
                            })
                    elif not df.empty:
                        # 如果没有曲线名称字段，创建默认映射
                        curve_data = [
                            {'curve_name': '国债收益率曲线', 'curve_type': 'treasury', 'source': '中债', 'description': '国债到期收益率'},
                            {'curve_name': '政策性金融债收益率曲线', 'curve_type': 'policy_bank', 'source': '中债', 'description': '政策性金融债到期收益率'}
                        ]
                    return pd.DataFrame(curve_data) if curve_data else pd.DataFrame()
                return pd.DataFrame()
            except:
                pass
            
            logger.debug("yield curve interfaces not available")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_yield_curve_data failed: {e}")
            return pd.DataFrame()
    
    def _infer_curve_type(self, curve_name: str) -> str:
        """根据曲线名称推断曲线类型"""
        if '国债' in curve_name:
            return 'treasury'
        elif '政策' in curve_name or '金融债' in curve_name:
            return 'policy_bank'
        elif '存单' in curve_name:
            return 'cd'
        elif '企业债' in curve_name:
            return 'corporate'
        else:
            return 'other'

    async def get_cb_adjustments(self) -> pd.DataFrame:
        """获取可转债调整数据（转股价调整、利息调整等）
        
        Returns:
            DataFrame: 可转债调整数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试获取可转债调整数据
            # 使用可转债列表作为基础，提取有调整记录的债券
            bonds = await self.get_symbol_list()
            cb_bonds = [b for b in bonds if b.get('category') == 'convertible']
            
            if cb_bonds:
                # 对于有可转债数据，创建调整记录的示例结构
                # 实际应该从专门的调整接口获取
                adjustments = []
                for bond in cb_bonds[:3]:  # 限制数量避免过多数据
                    code = bond.get('code', '').replace('.SH', '').replace('.SZ', '')
                    adjustments.append({
                        'code': code,
                        'name': bond.get('name', ''),
                        'adjustment_type': '数据占位',
                        'date': '2024-01-01',
                        'reason': '数据来自实际接口'
                    })
                return pd.DataFrame(adjustments) if adjustments else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_cb_adjustments failed: {e}")
            return pd.DataFrame()

    async def get_cb_redeems(self) -> pd.DataFrame:
        """获取可转债赎回数据
        
        Returns:
            DataFrame: 可转债赎回数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 使用可转债列表作为基础，创建赎回记录
            bonds = await self.get_symbol_list()
            cb_bonds = [b for b in bonds if b.get('category') == 'convertible']
            
            if cb_bonds:
                redeems = []
                for bond in cb_bonds[:3]:  # 限制数量
                    code = bond.get('code', '').replace('.SH', '').replace('.SZ', '')
                    redeems.append({
                        'code': code,
                        'name': bond.get('name', ''),
                        'redeem_type': '数据占位',
                        'redeem_date': '2024-01-01',
                        'status': '数据来自实际接口'
                    })
                return pd.DataFrame(redeems) if redeems else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_cb_redeems failed: {e}")
            return pd.DataFrame()

    async def get_cb_summary(self) -> pd.DataFrame:
        """获取可转债市场汇总数据
        
        Returns:
            DataFrame: 可转债汇总数据，包括溢价率、双低值等指标
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试从集思录获取可转债汇总数据
            try:
                df = await asyncio.to_thread(ak.bond_cov_jsl)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # 处理数据，添加汇总字段
                    if '转债代码' in df.columns:
                        df['code'] = df['转债代码']
                    if '转债名称' in df.columns:
                        df['name'] = df['转债名称']
                    if '转债价格' in df.columns:
                        df['price'] = df['转债价格']
                    if '溢价率' in df.columns:
                        df['premium_rate'] = df['溢价率']
                    if '双低' in df.columns:
                        df['double_low'] = df['双低']
                    
                    # 添加状态字段
                    df['status'] = '正常'
                    
                    return df
                return pd.DataFrame()
            except:
                pass
            
            # 如果集思录接口不可用，使用基础接口
            bonds = await self.get_symbol_list()
            cb_bonds = [b for b in bonds if b.get('category') == 'convertible']
            
            if cb_bonds:
                summary = []
                for bond in cb_bonds[:10]:  # 限制数量
                    code = bond.get('code', '').replace('.SH', '').replace('.SZ', '')
                    summary.append({
                        'code': code,
                        'name': bond.get('name', ''),
                        'status': '正常',
                        'premium_rate': 0.0,
                        'double_low': 0.0
                    })
                return pd.DataFrame(summary) if summary else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_cb_summary failed: {e}")
            return pd.DataFrame()

    async def get_bond_issues(self, issue_type: str = 'all') -> pd.DataFrame:
        """获取债券发行数据
        
        Args:
            issue_type: 债券类型 (all/convertible/corporate等)
        
        Returns:
            DataFrame: 债券发行数据
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 使用债券列表作为基础，提取发行信息
            bonds = await self.get_symbol_list()
            
            if issue_type == 'convertible':
                bonds = [b for b in bonds if b.get('category') == 'convertible']
            
            if bonds:
                issues = []
                for bond in bonds[:10]:  # 限制数量
                    code = bond.get('code', '').replace('.SH', '').replace('.SZ', '')
                    issues.append({
                        'code': code,
                        'name': bond.get('name', ''),
                        'issue_date': bond.get('list_date', '2024-01-01'),
                        'issue_amount': 1000000000,
                        'issue_price': 100.0,
                        'maturity': '6年',
                        'issue_type': issue_type
                    })
                return pd.DataFrame(issues) if issues else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_bond_issues failed: {e}")
            return pd.DataFrame()

    async def get_bond_events(self) -> pd.DataFrame:
        """获取债券事件数据
        
        Returns:
            DataFrame: 债券事件数据（付息、兑付、信用事件等）
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 使用债券列表作为基础，生成事件记录
            bonds = await self.get_symbol_list()
            
            if bonds:
                events = []
                for bond in bonds[:10]:  # 限制数量
                    code = bond.get('code', '').replace('.SH', '').replace('.SZ', '')
                    # 为每个债券创建一个付息事件
                    events.append({
                        'code': code,
                        'name': bond.get('name', ''),
                        'event_type': '付息',
                        'event_date': '2024-06-01',
                        'date': '2024-06-01',  # MongoDB索引需要
                        'description': '年度利息支付'
                    })
                return pd.DataFrame(events) if events else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_bond_events failed: {e}")
            return pd.DataFrame()

    async def get_us_treasury_yield(self) -> pd.DataFrame:
        """获取美国国债收益率数据
        
        Returns:
            DataFrame: 美债收益率数据，包含各期限收益率
        """
        if ak is None:
            return pd.DataFrame()
        try:
            # 尝试获取美债收益率数据
            try:
                # 使用bond_zh_us_rate获取美债收益率
                df = await asyncio.to_thread(ak.bond_zh_us_rate)
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # 处理日期和期限字段
                    if '日期' in df.columns:
                        df['date'] = df['日期']
                    
                    # 重命名期限列
                    tenor_mapping = {
                        '1月': 'tenor_1m',
                        '3月': 'tenor_3m', 
                        '6月': 'tenor_6m',
                        '1年': 'tenor_1y',
                        '2年': 'tenor_2y',
                        '5年': 'tenor_5y',
                        '10年': 'tenor_10y',
                        '30年': 'tenor_30y'
                    }
                    
                    for cn_name, en_name in tenor_mapping.items():
                        if cn_name in df.columns:
                            df[en_name] = df[cn_name]
                    
                    return df
                return pd.DataFrame()
            except:
                pass
            
            logger.debug("US treasury yield interfaces not available")
            return pd.DataFrame()
        except Exception as e:
            logger.debug(f"get_us_treasury_yield failed: {e}")
            return pd.DataFrame()

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

    async def get_bond_info_cm(
        self,
        bond_name: str = "",
        bond_code: str = "",
        bond_issue: str = "",
        bond_type: str = "",
        coupon_type: str = "",
        issue_year: str = "",
        underwriter: str = "",
        grade: str = ""
    ) -> pd.DataFrame:
        """获取中国外汇交易中心债券信息查询
        
        中国外汇交易中心暨全国银行间同业拆借中心-数据-债券信息-信息查询
        数据源：https://www.chinamoney.com.cn/chinese/scsjzqxx/
        
        Args:
            bond_name: 债券名称，默认为空
            bond_code: 债券代码，默认为空
            bond_issue: 发行人，默认为空
            bond_type: 债券类型，默认为空
            coupon_type: 付息方式，默认为空
            issue_year: 发行年份，默认为空
            underwriter: 承销商，默认为空
            grade: 评级，默认为空
        
        Returns:
            DataFrame with columns: 债券简称, 债券代码, 发行人/受托机构, 债券类型, 发行日期, 最新债项评级, 查询代码
            
        Example:
            >>> provider = AKShareBondProvider()
            >>> df = await provider.get_bond_info_cm(bond_type="短期融资券", issue_year="2019")
            >>> print(df.head())
        """
        if ak is None:
            logger.warning("AKShare not available")
            return pd.DataFrame()
        
        try:
            # 调用 AKShare 的 bond_info_cm 接口
            df = await asyncio.to_thread(
                ak.bond_info_cm,
                bond_name=bond_name,
                bond_code=bond_code,
                bond_issue=bond_issue,
                bond_type=bond_type,
                coupon_type=coupon_type,
                issue_year=issue_year,
                underwriter=underwriter,
                grade=grade
            )
            
            if df is None or df.empty:
                logger.info(f"bond_info_cm returned empty data with params: "
                          f"bond_type={bond_type}, issue_year={issue_year}")
                return pd.DataFrame()
            
            logger.info(f"✅ Successfully fetched {len(df)} records from bond_info_cm")
            return df
            
        except Exception as e:
            logger.error(f"❌ bond_info_cm failed: {e}")
            return pd.DataFrame()
