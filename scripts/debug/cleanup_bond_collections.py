"""
清理债券数据库集合脚本

删除除bond_info_cm和bond_basic_info外的所有债券相关集合。
这些集合将在后续重新设计和实现。

使用方法:
    python scripts/debug/cleanup_bond_collections.py --confirm

警告: 此操作不可恢复！请确保已备份重要数据。
"""

import argparse
import asyncio
import logging
from typing import List

from app.core.database import init_database, close_database, get_mongo_db


# 需要删除的集合列表（保留bond_info_cm和bond_basic_info）
COLLECTIONS_TO_DELETE: List[str] = [
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
    "yield_curve_map",
    "bond_buybacks_hist",
    "bond_cb_list_jsl",
    "bond_cov_list",
    "bond_minute_quotes",
]

# 保留的集合
COLLECTIONS_TO_KEEP: List[str] = [
    "bond_info_cm",
    "bond_basic_info",
]


async def delete_collections(db, collections: List[str]) -> dict:
    """删除指定的集合"""
    result = {
        "deleted": [],
        "failed": [],
        "not_found": [],
    }
    
    # 获取数据库中所有集合名称
    existing_collections = await db.list_collection_names()
    
    for name in collections:
        try:
            if name not in existing_collections:
                logging.info(f"⏭️  Collection {name} does not exist, skipping")
                result["not_found"].append(name)
                continue
            
            # 获取集合文档数量
            count = await db[name].count_documents({})
            
            # 删除集合
            await db[name].drop()
            logging.info(f"✅ Deleted collection: {name} (had {count} documents)")
            result["deleted"].append({"name": name, "count": count})
        except Exception as e:
            logging.error(f"❌ Failed to delete {name}: {e}")
            result["failed"].append({"name": name, "error": str(e)})
    
    return result


async def verify_kept_collections(db) -> dict:
    """验证保留的集合是否存在"""
    result = {
        "kept": [],
        "missing": [],
    }
    
    existing_collections = await db.list_collection_names()
    
    for name in COLLECTIONS_TO_KEEP:
        if name in existing_collections:
            count = await db[name].count_documents({})
            logging.info(f"✅ Kept collection: {name} ({count} documents)")
            result["kept"].append({"name": name, "count": count})
        else:
            logging.warning(f"⚠️  Collection {name} does not exist")
            result["missing"].append(name)
    
    return result


async def main(args):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    if not args.confirm:
        logging.error("❌ 请使用 --confirm 参数确认删除操作")
        logging.info(f"将删除以下 {len(COLLECTIONS_TO_DELETE)} 个集合:")
        for name in COLLECTIONS_TO_DELETE:
            logging.info(f"  - {name}")
        logging.info(f"\n将保留以下 {len(COLLECTIONS_TO_KEEP)} 个集合:")
        for name in COLLECTIONS_TO_KEEP:
            logging.info(f"  - {name}")
        return
    
    logging.info("🚀 开始清理债券数据库集合...")
    
    await init_database()
    try:
        db = get_mongo_db()
        
        # 删除不需要的集合
        logging.info(f"🗑️  删除 {len(COLLECTIONS_TO_DELETE)} 个不需要的集合...")
        delete_result = await delete_collections(db, COLLECTIONS_TO_DELETE)
        
        # 验证保留的集合
        logging.info(f"\n✅ 验证保留的 {len(COLLECTIONS_TO_KEEP)} 个集合...")
        keep_result = await verify_kept_collections(db)
        
        # 输出总结
        logging.info("\n" + "="*60)
        logging.info("📊 清理总结:")
        logging.info(f"  ✅ 成功删除: {len(delete_result['deleted'])} 个集合")
        if delete_result['deleted']:
            total_docs = sum(item['count'] for item in delete_result['deleted'])
            logging.info(f"     共删除 {total_docs} 条文档")
        logging.info(f"  ⏭️  未找到: {len(delete_result['not_found'])} 个集合")
        logging.info(f"  ❌ 删除失败: {len(delete_result['failed'])} 个集合")
        logging.info(f"  ✅ 保留集合: {len(keep_result['kept'])} 个")
        if keep_result['kept']:
            total_kept = sum(item['count'] for item in keep_result['kept'])
            logging.info(f"     共保留 {total_kept} 条文档")
        logging.info(f"  ⚠️  缺失集合: {len(keep_result['missing'])} 个")
        logging.info("="*60)
        
        if delete_result['failed']:
            logging.error("\n失败的集合:")
            for item in delete_result['failed']:
                logging.error(f"  - {item['name']}: {item['error']}")
        
    finally:
        await close_database()
        logging.info("\n✨ 清理完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="清理债券数据库集合，只保留bond_info_cm和bond_basic_info"
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="确认删除操作（必需参数）"
    )
    args = parser.parse_args()
    
    asyncio.run(main(args))
