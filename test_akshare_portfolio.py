#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test AKShare fund_portfolio_hold_em API parameter format"""
import akshare as ak

# Test different date formats
symbol = "000001"

print("=" * 60)
print("Test AKShare fund_portfolio_hold_em API")
print("=" * 60)

# Test 1: Using year
print("\nTest 1: Using year '2024'")
try:
    df = ak.fund_portfolio_hold_em(symbol=symbol, date="2024")
    print(f"[OK] Success! Got {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    if not df.empty:
        print(f"First 3 rows:\n{df.head(3)}")
except Exception as e:
    print(f"[ERROR] Failed: {e}")

# Test 2: Using quarter end date
print("\nTest 2: Using quarter date '2024-09-30'")
try:
    df = ak.fund_portfolio_hold_em(symbol=symbol, date="2024-09-30")
    print(f"[OK] Success! Got {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    if not df.empty:
        print(f"First 3 rows:\n{df.head(3)}")
except Exception as e:
    print(f"[ERROR] Failed: {e}")

# Test 3: Using quarter format
print("\nTest 3: Using quarter format '2024-Q3'")
try:
    df = ak.fund_portfolio_hold_em(symbol=symbol, date="2024-Q3")
    print(f"[OK] Success! Got {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    if not df.empty:
        print(f"First 3 rows:\n{df.head(3)}")
except Exception as e:
    print(f"[ERROR] Failed: {e}")

print("\n" + "=" * 60)
