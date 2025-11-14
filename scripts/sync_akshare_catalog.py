#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync AKShare documentation catalog (data dictionary) to local, grouped by asset classes.
- Crawls pages under /data/ from base URL (depth-limited)
- Extracts function names, title, brief, tries to parse parameter/return tables (best-effort)
- Classifies endpoints to asset classes via heuristics
- Saves per-endpoint JSON files and a flat index, plus optional raw HTML snapshots

Usage (PowerShell):
  python scripts/sync_akshare_catalog.py `
    --base-url https://akshare.akfamily.xyz/data/index.html `
    --out docs/akshare_catalog `
    --max-workers 8 `
    --max-pages 2000 `
    --depth 2 `
    --include-raw-html `
    --overwrite

Dependencies:
  pip install requests beautifulsoup4

Proxy:
  Set HTTP_PROXY / HTTPS_PROXY env if needed.
"""

import argparse
import concurrent.futures as futures
import datetime as dt
import itertools
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse


@dataclass
class EndpointMeta:
    asset_class: str
    source: str
    endpoint_name: str
    title: str
    category: List[str]
    doc_url: str
    description: str
    parameters: List[Dict]
    return_schema: Dict
    examples: List[str]
    tags: List[str]
    last_crawled: str
    version_hint: Optional[str]
    notes: Optional[str]
    raw_html_file: Optional[str]


def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def sanitize_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", name)[:200]


def same_domain(u1: str, u2: str) -> bool:
    return urlparse(u1).netloc == urlparse(u2).netloc


def normalize_url(base: str, href: str) -> Optional[str]:
    if not href:
        return None
    try:
        u = urljoin(base, href)
        # remove fragments
        p = urlparse(u)
        u = urlunparse((p.scheme, p.netloc, p.path, p.params, p.query, ""))
        return u
    except Exception:
        return None


def is_under_data_path(url: str) -> bool:
    return "/data/" in urlparse(url).path


def fetch(session: requests.Session, url: str, timeout: int = 20) -> Optional[str]:
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[WARN] fetch failed: {url} -> {e}", file=sys.stderr)
        return None


def guess_asset_class(fn: str, title: str, url: str) -> str:
    fn = fn or ""
    t = (title or "").lower()
    u = url.lower()
    # Heuristic patterns
    if fn.startswith("stock_zh_a_") or "a股" in t:
        return "equity_cn"
    if fn.startswith("stock_hk_") or "港股" in t:
        return "equity_hk"
    if fn.startswith("stock_us_") or "美股" in t or "us" in u:
        return "equity_us"
    if fn.startswith("fund_"):
        return "fund_cn"
    if fn.startswith("index_zh_") or "指数" in t:
        # If global hints present
        if any(x in (t + u) for x in ["global", "世界", "国际", "sp500", "nasdaq", "dowjones", "dax", "ftse"]):
            return "index_global"
        return "index_cn"
    if fn.startswith("futures_") or "期货" in t:
        return "futures_cn"
    if fn.startswith("bond_") or "债券" in t:
        return "bond_cn"
    if fn.startswith("macro_"):
        return "macro"
    if any(fn.startswith(p) for p in ["fx_", "forex_"]):
        return "forex"
    if any(x in fn for x in ["crypto", "bitcoin", "blockchain"]):
        return "crypto"
    if any(x in fn for x in ["option", "opt_"]):
        return "options_cn"
    return "others"


def extract_functions(text: str) -> List[str]:
    # Look for ak.<function> occurrences
    fns = set(re.findall(r"ak\s*\.\s*([a-zA-Z_][a-zA-Z0-9_]*)", text or ""))
    # Also consider code blocks using just function name (less reliable)
    fns |= set(re.findall(r"\n([a-zA-Z_][a-zA-Z0-9_]*)\(", text or ""))
    return sorted(fns)


def parse_parameters_table(soup: BeautifulSoup) -> List[Dict]:
    # Best-effort: find a table with headers resembling '参数/参数名称/name' etc.
    param_headers = {"参数", "参数名称", "name", "参数名"}
    result = []
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if not headers:
            # try first row
            first_row = table.find("tr")
            if first_row:
                headers = [td.get_text(strip=True).lower() for td in first_row.find_all(["th", "td"])]
        if not headers:
            continue
        if any(h in headers for h in ["参数", "参数名称", "name", "参数名"]):
            # parse rows
            rows = table.find_all("tr")[1:]
            for tr in rows:
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if len(cols) < 1:
                    continue
                entry = {
                    "name": cols[0] if len(cols) > 0 else "",
                    "type": cols[1] if len(cols) > 1 else "",
                    "required": None,
                    "default": cols[2] if len(cols) > 2 else "",
                    "choices": [],
                    "description": cols[3] if len(cols) > 3 else "",
                }
                result.append(entry)
            if result:
                return result
    return result


def parse_return_schema(soup: BeautifulSoup) -> Dict:
    # Best-effort: find a table that looks like dataframe columns
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if any(h in headers for h in ["字段", "列名", "column", "字段名", "columns"]):
            rows = table.find_all("tr")[1:]
            columns = []
            for tr in rows:
                cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if not cols:
                    continue
                columns.append({
                    "name": cols[0],
                    "type": cols[1] if len(cols) > 1 else "",
                    "description": cols[2] if len(cols) > 2 else "",
                })
            if columns:
                return {"type": "dataframe", "columns": columns}
    return {}


def parse_description(soup: BeautifulSoup) -> str:
    # First paragraph following h1/h2
    h1 = soup.find(["h1", "h2"])
    if h1:
        p = h1.find_next("p")
        if p:
            return p.get_text(strip=True)[:1000]
    # fallback
    p = soup.find("p")
    return p.get_text(strip=True)[:1000] if p else ""


def parse_examples(soup: BeautifulSoup) -> List[str]:
    examples = []
    for code in soup.find_all("code"):
        txt = code.get_text("\n", strip=True)
        if any(k in txt for k in ["ak.", "import akshare", "from akshare"]):
            examples.append(txt[:1000])
        if len(examples) >= 5:
            break
    return examples


def parse_title_and_category(soup: BeautifulSoup) -> Tuple[str, List[str]]:
    title = soup.title.get_text(strip=True) if soup.title else ""
    # mkdocs-material breadcrumb-like nav
    category = []
    nav = soup.find("nav")
    if nav:
        crumbs = [a.get_text(strip=True) for a in nav.find_all("a") if a.get_text(strip=True)]
        if crumbs:
            category = crumbs[:6]
    return title, category


def ensure_dirs(root: str, *parts: str) -> str:
    path = os.path.join(root, *parts)
    os.makedirs(path, exist_ok=True)
    return path


def save_json(fp: str, data: Dict):
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(fp: str, text: str):
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(text)


def crawl(base_url: str, depth: int, max_pages: int, max_workers: int, out_dir: str, include_raw_html: bool, overwrite: bool) -> Dict:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36"
    })

    visited: Set[str] = set()
    queue: List[Tuple[str, int]] = [(base_url, 0)]
    candidates: List[str] = []

    while queue and len(candidates) < max_pages:
        url, d = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        html = fetch(session, url)
        if html is None:
            continue
        candidates.append(url)
        if d >= depth:
            continue
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            nu = normalize_url(url, a['href'])
            if not nu:
                continue
            if not same_domain(base_url, nu):
                continue
            if not is_under_data_path(nu):
                continue
            if nu not in visited:
                queue.append((nu, d + 1))

    print(f"[INFO] discovered {len(candidates)} candidate pages (depth<={depth})")

    endpoint_map: Dict[str, Dict] = {}
    endpoints_per_asset: Dict[str, int] = {}

    raw_dir = ensure_dirs(out_dir, "raw_html") if include_raw_html else None
    endpoints_dir = ensure_dirs(out_dir, "assets")

    def process(url: str) -> Tuple[str, Optional[List[EndpointMeta]]]:
        html = fetch(session, url)
        if html is None:
            return url, None
        soup = BeautifulSoup(html, "html.parser")
        title, category = parse_title_and_category(soup)
        desc = parse_description(soup)
        params = parse_parameters_table(soup)
        ret = parse_return_schema(soup)
        examples = parse_examples(soup)
        fns = extract_functions(html)
        metas: List[EndpointMeta] = []
        raw_file_rel = None
        if include_raw_html and raw_dir:
            slug = sanitize_filename(urlparse(url).path.strip("/").replace("/", "_")) or "index"
            raw_path = os.path.join(raw_dir, f"{slug}.html")
            save_text(raw_path, html)
            raw_file_rel = os.path.relpath(raw_path, out_dir)
        for fn in fns:
            asset = guess_asset_class(fn, title, url)
            meta = EndpointMeta(
                asset_class=asset,
                source="akshare",
                endpoint_name=fn,
                title=title or fn,
                category=category,
                doc_url=url,
                description=desc,
                parameters=params,
                return_schema=ret,
                examples=examples,
                tags=[],
                last_crawled=now_iso(),
                version_hint=None,
                notes=None,
                raw_html_file=raw_file_rel,
            )
            metas.append(meta)
        return url, metas

    with futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        results = list(ex.map(process, candidates))

    count_pages = 0
    count_endpoints = 0

    for url, metas in results:
        if metas is None:
            continue
        count_pages += 1
        for m in metas:
            count_endpoints += 1
            endpoints_per_asset[m.asset_class] = endpoints_per_asset.get(m.asset_class, 0) + 1
            # Save endpoint file
            asset_dir = ensure_dirs(endpoints_dir, m.asset_class, "endpoints")
            endpoint_fp = os.path.join(asset_dir, f"{m.endpoint_name}.json")
            if (not overwrite) and os.path.exists(endpoint_fp):
                # merge minimal fields if exists
                try:
                    old = json.loads(open(endpoint_fp, "r", encoding="utf-8").read())
                    # prefer existing description/parameters if populated
                    obj = {**m.__dict__, **old}
                except Exception:
                    obj = m.__dict__
            else:
                obj = m.__dict__
            save_json(endpoint_fp, obj)
            # flat map
            endpoint_map[m.endpoint_name] = {
                "asset_class": m.asset_class,
                "doc_url": m.doc_url,
                "title": m.title,
                "source": m.source,
                "raw_html_file": m.raw_html_file,
            }

    # Save indices
    save_json(os.path.join(out_dir, "endpoints_flat.json"), endpoint_map)
    save_json(
        os.path.join(out_dir, "index.json"),
        {
            "base_url": base_url,
            "generated_at": now_iso(),
            "page_count": count_pages,
            "endpoint_count": count_endpoints,
            "asset_class_counts": endpoints_per_asset,
            "include_raw_html": bool(include_raw_html),
            "depth": depth,
            "max_pages": max_pages,
        },
    )

    print(f"[DONE] pages={count_pages}, endpoints={count_endpoints}")


def main():
    ap = argparse.ArgumentParser(description="Sync AKShare docs catalog to local.")
    ap.add_argument("--base-url", default="https://akshare.akfamily.xyz/data/index.html")
    ap.add_argument("--out", default=os.path.join("docs", "akshare_catalog"))
    ap.add_argument("--max-workers", type=int, default=8)
    ap.add_argument("--max-pages", type=int, default=1500)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--include-raw-html", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    start = time.time()
    crawl(
        base_url=args.base_url,
        depth=args.depth,
        max_pages=args.max_pages,
        max_workers=args.max_workers,
        out_dir=out_dir,
        include_raw_html=args.include_raw_html,
        overwrite=args.overwrite,
    )
    dur = time.time() - start
    print(f"[TIME] {dur:.1f}s")


if __name__ == "__main__":
    main()
