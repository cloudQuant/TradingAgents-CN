"""Measure how long it takes to read an entire MongoDB collection once."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Ensure project root (repo root) is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import get_mongo_db_sync  # noqa: E402


def measure_full_read(collection_name: str, materialize: bool = True) -> None:
    """Read every document in a collection once and report timing stats."""
    db = get_mongo_db_sync()
    collection = db[collection_name]

    print("=" * 80)
    print(f"Collection: {collection_name}")
    print("=" * 80)

    total_start = time.perf_counter()
    count_start = time.perf_counter()
    total_docs = collection.count_documents({})
    count_duration = time.perf_counter() - count_start
    print(f"Estimated document count: {total_docs:,} (took {count_duration:.2f}s)")

    read_start = time.perf_counter()
    if materialize:
        # Simulate export by materializing all documents into memory
        docs = list(collection.find({}))
        read_count = len(docs)
    else:
        read_count = 0
        for _ in collection.find({}):
            read_count += 1
    read_duration = time.perf_counter() - read_start

    total_duration = time.perf_counter() - total_start
    avg_per_doc = (read_duration / read_count) if read_count else 0

    print(f"Read {read_count:,} documents without pagination.")
    print(f"Read duration: {read_duration:.2f}s | ~{avg_per_doc * 1000:.3f} ms/doc")
    print(f"Total script duration: {total_duration:.2f}s")

    if materialize:
        approx_bytes = sum(sys.getsizeof(doc) for doc in docs)
        mb = approx_bytes / (1024 * 1024)
        print(f"Approximate in-memory footprint: {mb:.2f} MB for {read_count:,} docs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure collection full-read time")
    parser.add_argument(
        "collection",
        nargs="?",
        default="fund_portfolio_hold_em",
        help="MongoDB collection name (default: fund_portfolio_hold_em)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream documents without materializing the full list",
    )
    args = parser.parse_args()

    measure_full_read(args.collection, materialize=not args.stream)
