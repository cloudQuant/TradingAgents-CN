import argparse
import asyncio
import logging
from typing import List

from app.core.database import init_database, close_database, get_mongo_db
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


BOND_COLLECTIONS: List[str] = [
    "bond_basic_info",
    "bond_daily",
    "yield_curve_daily",
    "bond_events",
    "bond_spot_quotes",
    "bond_indices_daily",
    "us_yield_daily",
    "bond_cb_profiles",
    "bond_buybacks",
    "bond_issues",
    "bond_cb_adjustments",
    "bond_cb_redeems",
    "bond_cb_summary",
    "bond_cb_valuation_daily",
    "bond_cb_comparison",
    "bond_spot_quote_detail",
    "bond_spot_deals",
    "bond_deal_summary",
    "bond_cash_summary",
    "bond_nafmii_debts",
    "bond_info_cm",
    "yield_curve_map",
    "bond_buybacks_hist",
    "bond_cb_list_jsl",
    "bond_cov_list",
]


async def drop_collections(db, collections: List[str]) -> None:
    for name in collections:
        try:
            await db[name].drop()
            logging.info(f"✅ Dropped collection: {name}")
        except Exception as e:
            logging.warning(f"⚠️ Drop failed for {name}: {e}")


async def rebuild_indexes(svc: BondDataService) -> None:
    await svc.ensure_indexes()
    logging.info("✅ Indexes ensured for all bond collections")


async def refill_minimal(svc: BondDataService, yield_start: str | None = None, yield_end: str | None = None) -> dict:
    """Refill minimal datasets required by UI: basic list + yield curve.
    yield_start/yield_end: optional 'YYYY-MM-DD', the span should be < 1 year per AKShare.
    """
    provider = AKShareBondProvider()
    result = {"basic_saved": 0, "basic_count": 0, "yield_saved": 0, "yield_rows": 0}

    # Basic list
    try:
        items = await provider.get_symbol_list()
        result["basic_count"] = 0 if items is None else len(items)
        if items:
            result["basic_saved"] = await svc.save_basic_list(items)
            logging.info(f"💾 Saved basic list: saved={result['basic_saved']} count={result['basic_count']}")
        else:
            logging.warning("⚠️ No basic items fetched from AKShare")
    except Exception as e:
        logging.error(f"❌ Fetch/save basic list failed: {e}")

    # Yield curve
    try:
        df = await provider.get_yield_curve(start_date=yield_start, end_date=yield_end)
        if df is not None and not getattr(df, 'empty', True):
            result["yield_rows"] = len(df)
            result["yield_saved"] = await svc.save_yield_curve(df)
            logging.info(f"💾 Saved yield curve: saved={result['yield_saved']} rows={result['yield_rows']}")
        else:
            logging.warning("⚠️ No yield curve data fetched from AKShare")
    except Exception as e:
        logging.error(f"❌ Fetch/save yield curve failed: {e}")

    return result


async def main(args):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    await init_database()
    try:
        db = get_mongo_db()
        svc = BondDataService(db)

        if args.drop:
            logging.info("🔨 Dropping bond-related collections...")
            await drop_collections(db, BOND_COLLECTIONS)

        logging.info("🧱 Ensuring indexes...")
        await rebuild_indexes(svc)

        if args.refill:
            logging.info("📥 Refilling minimal datasets (basic list + yield curve)...")
            res = await refill_minimal(svc, yield_start=args.yield_start, yield_end=args.yield_end)
            logging.info(f"✅ Refill done: {res}")
    finally:
        await close_database()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset bond collections: drop, reindex, refill")
    parser.add_argument("--drop", action="store_true", help="Drop all bond-related collections")
    parser.add_argument("--refill", action="store_true", help="Refill minimal datasets (basic list + yield curve)")
    parser.add_argument("--yield-start", type=str, default=None, help="Yield curve start date YYYY-MM-DD (<1 year span)")
    parser.add_argument("--yield-end", type=str, default=None, help="Yield curve end date YYYY-MM-DD (<1 year span)")
    args = parser.parse_args()

    asyncio.run(main(args))
