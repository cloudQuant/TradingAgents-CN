#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test AKShare fund_portfolio_bond_hold_em API parameter format"""
import akshare as ak
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test different date formats
symbol = "000001"

print("=" * 60)
print("Test AKShare fund_portfolio_bond_hold_em API")
print("=" * 60)

# Test 1: Using year
print("\nTest 1: Using year '2024'")
try:
    df = ak.fund_portfolio_bond_hold_em(symbol=symbol, date="2024")
    print(f"[OK] Success! Got {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nColumn details:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    if not df.empty:
        print(f"\nFirst 3 rows:")
        print(df.head(3).to_string())
        print(f"\nData types:")
        print(df.dtypes)
except Exception as e:
    print(f"[ERROR] Failed: {e}")

# Test 2: Using quarter end date
print("\nTest 2: Using quarter date '2024-09-30'")
try:
    df = ak.fund_portfolio_bond_hold_em(symbol=symbol, date="2024-09-30")
    print(f"[OK] Success! Got {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    if not df.empty:
        print(f"First 3 rows:\n{df.head(3)}")
except Exception as e:
    print(f"[ERROR] Failed: {e}")

print("\n" + "=" * 60)
print("Conclusion:")
print("Based on the results above, fund_portfolio_bond_hold_em")
print("should use the same parameter format as fund_portfolio_hold_em")
print("=" * 60)
