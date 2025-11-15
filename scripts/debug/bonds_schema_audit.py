import asyncio
import logging
import argparse
from typing import Dict, Any, List, Optional

import pandas as pd

from app.core.database import init_database, close_database, get_mongo_db
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def fetch_df(name: str) -> Optional[pd.DataFrame]:
    try:
        import akshare as ak  # type: ignore
    except Exception:
        logging.error("AKShare not available")
        return None
    try:
        fn = getattr(ak, name)
    except AttributeError:
        logging.warning(f"Missing AKShare endpoint: {name}")
        return None
    try:
        if name in {"bond_spot_quote", "bond_spot_deal", "bond_cash_summary_sse", "bond_deal_summary_sse", "bond_debt_nafmii"}:
            df = await asyncio.to_thread(fn)
        elif name in {"bond_china_yield"}:
            # Without date range this returns latest or may fail; try without args
            df = await asyncio.to_thread(fn)
        elif name in {"bond_zh_us_rate"}:
            df = await asyncio.to_thread(fn)
        elif name in {"bond_zh_hs_spot", "bond_zh_hs_cov_spot"}:
            df = await asyncio.to_thread(fn)
        elif name in {"bond_info_cm", "bond_info_cm_query", "bond_info_detail_cm"}:
            # These require params; skip raw fetch here
            return None
        else:
            df = await asyncio.to_thread(fn)
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
        return None
    except Exception as e:
        logging.warning(f"Fetch failed for {name}: {e}")
        return None


async def audit_collection(label: str, df: Optional[pd.DataFrame], sample_query: Dict[str, Any], collection_name: str, svc: BondDataService, saver: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
    """
    - df: fetched dataframe as expected field reference (can be None if not fetchable)
    - sample_query: used to fetch one document from DB for comparison
    - saver: method name on BondDataService to save df if we want to exercise write path
    """
    result = {"label": label, "expected": [], "db_fields": [], "missing_in_db": [], "extra_in_db": []}

    # expected fields from DataFrame
    if isinstance(df, pd.DataFrame) and not df.empty:
        result["expected"] = list(map(str, df.columns))
    
    # Optionally write a small sample to DB to make comparison meaningful
    if (not dry_run) and saver and isinstance(df, pd.DataFrame) and not df.empty:
        small = df.head(10).copy()
        try:
            fn = getattr(svc, saver)
            saved = await fn(small) if saver != "save_spot_quotes" else await fn(small, category=label)
            logging.info(f"[{label}] saved sample rows: {saved}")
        except Exception as e:
            logging.warning(f"[{label}] save failed: {e}")

    # Read back a sample document
    try:
        doc = await svc.db[collection_name].find_one(sample_query)  # type: ignore
        if doc:
            doc.pop("_id", None)
            result["db_fields"] = list(doc.keys())
            if result["expected"]:
                exp = set(result["expected"])  # type: ignore
                dbf = set(result["db_fields"])  # type: ignore
                result["missing_in_db"] = sorted(list(exp - dbf))
                result["extra_in_db"] = sorted(list(dbf - exp))
    except Exception as e:
        logging.warning(f"[{label}] read back failed: {e}")

    return result


async def main(args):
    await init_database()
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        prov = AKShareBondProvider()

        audits: List[Dict[str, Any]] = []

        # 1) 沪深债券现货 - bond_zh_hs_spot
        if (not args.only) or ("hs_spot" in args.only):
            df_spot = await fetch_df("bond_zh_hs_spot")
            audits.append(
                await audit_collection(
                    label="hs_spot",
                    df=df_spot,
                    sample_query={},
                    collection_name="bond_spot_quotes",
                    svc=svc,
                    saver="save_spot_quotes",
                    dry_run=args.dry_run,
                )
            )

        # 2) 现券市场做市报价 - bond_spot_quote
        if (not args.only) or ("spot_quote_detail" in args.only):
            df_quote = await fetch_df("bond_spot_quote")
            audits.append(
                await audit_collection(
                    label="spot_quote_detail",
                    df=df_quote,
                    sample_query={},
                    collection_name="bond_spot_quote_detail",
                    svc=svc,
                    saver="save_spot_quote_detail",
                    dry_run=args.dry_run,
                )
            )

        # 3) 现券市场成交行情 - bond_spot_deal
        if (not args.only) or ("spot_deal" in args.only):
            df_deal = await fetch_df("bond_spot_deal")
            audits.append(
                await audit_collection(
                    label="spot_deal",
                    df=df_deal,
                    sample_query={},
                    collection_name="bond_spot_deals",
                    svc=svc,
                    saver="save_spot_deals",
                    dry_run=args.dry_run,
                )
            )

        # 4) 国债及其他收益率曲线 - bond_china_yield (provider已标准化)
        if (not args.only) or ("yield_curve" in args.only):
            df_yield = await prov.get_yield_curve()
            audits.append(
                await audit_collection(
                    label="yield_curve",
                    df=df_yield,
                    sample_query={},
                    collection_name="yield_curve_daily",
                    svc=svc,
                    saver="save_yield_curve",
                    dry_run=args.dry_run,
                )
            )

        # 5) 上交所成交/资金摘要
        if (not args.only) or ("deal_summary_sse" in args.only):
            df_dsum = await fetch_df("bond_deal_summary_sse")
            audits.append(
                await audit_collection(
                    label="deal_summary_sse",
                    df=df_dsum,
                    sample_query={},
                    collection_name="bond_deal_summary",
                    svc=svc,
                    saver="save_deal_summary",
                    dry_run=args.dry_run,
                )
            )

        if (not args.only) or ("cash_summary_sse" in args.only):
            df_csum = await fetch_df("bond_cash_summary_sse")
            audits.append(
                await audit_collection(
                    label="cash_summary_sse",
                    df=df_csum,
                    sample_query={},
                    collection_name="bond_cash_summary",
                    svc=svc,
                    saver="save_cash_summary",
                    dry_run=args.dry_run,
                )
            )

        # 6) 银行间市场债券发行基础数据 - NAFMII
        if (not args.only) or ("nafmii_debt" in args.only):
            df_nafmii = await fetch_df("bond_debt_nafmii")
            audits.append(
                await audit_collection(
                    label="nafmii_debt",
                    df=df_nafmii,
                    sample_query={},
                    collection_name="bond_nafmii_debts",
                    svc=svc,
                    saver="save_nafmii",
                    dry_run=args.dry_run,
                )
            )

        # 7) 美国国债收益率 - bond_zh_us_rate
        if (not args.only) or ("us_yield" in args.only):
            df_usy = await fetch_df("bond_zh_us_rate")
            audits.append(
                await audit_collection(
                    label="us_yield",
                    df=df_usy,
                    sample_query={},
                    collection_name="us_yield_daily",
                    svc=svc,
                    saver="save_us_yields",
                    dry_run=args.dry_run,
                )
            )

        # 输出审计结果
        for a in audits:
            logging.info("==== AUDIT ====")
            logging.info(f"label={a['label']}")
            logging.info(f"expected_cols={a['expected'][:50] if a['expected'] else 'N/A'}")
            logging.info(f"db_fields={a['db_fields']}")
            logging.info(f"missing_in_db={a['missing_in_db']}")
            logging.info(f"extra_in_db={a['extra_in_db']}")

    finally:
        await close_database()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit bonds collections vs AKShare interfaces")
    parser.add_argument("--dry-run", action="store_true", help="Do not write any sample documents to DB")
    parser.add_argument("--only", nargs="*", default=None, help="Limit to labels: hs_spot, spot_quote_detail, spot_deal, yield_curve, deal_summary_sse, cash_summary_sse, nafmii_debt, us_yield")
    args = parser.parse_args()
    asyncio.run(main(args))
