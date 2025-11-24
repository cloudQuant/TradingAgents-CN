import argparse
import asyncio
import logging
from typing import List

from app.core.database import init_database, close_database, get_mongo_db
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider


# 仅保留债券数据查询和债券基础信息两个集合
BOND_COLLECTIONS: List[str] = [
    "bond_info_cm",      # 债券数据查询
    "bond_basic_info",   # 债券基础信息
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


async def refill_minimal(svc: BondDataService) -> dict:
    """Refill minimal datasets required: bond_basic_info.
    """
    provider = AKShareBondProvider()
    result = {"basic_saved": 0, "basic_count": 0}

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
            logging.info("📥 Refilling minimal datasets (basic list)...")
            res = await refill_minimal(svc)
            logging.info(f"✅ Refill done: {res}")
    finally:
        await close_database()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset bond collections: drop, reindex, refill (仅保留bond_info_cm和bond_basic_info)")
    parser.add_argument("--drop", action="store_true", help="Drop bond collections (bond_info_cm, bond_basic_info)")
    parser.add_argument("--refill", action="store_true", help="Refill minimal datasets (bond_basic_info)")
    args = parser.parse_args()

    asyncio.run(main(args))
