#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test AKShare fund_portfolio_change_em API"""
import akshare as ak
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test fund_portfolio_change_em
symbol = "000001"
indicator = "累计买入"  # 或 "累计卖出"
date = "2023"

print("=" * 60)
print("Test AKShare fund_portfolio_change_em API")
print("=" * 60)
print(f"\n基金代码: {symbol}")
print(f"指标: {indicator}")
print(f"年份: {date}")

try:
    df = ak.fund_portfolio_change_em(symbol=symbol, indicator=indicator, date=date)
    print(f"\n[OK] Success! Got {len(df)} records")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nColumn details:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    if not df.empty:
        print(f"\nFirst 3 rows:")
        print(df.head(3).to_string())
        print(f"\nData types:")
        print(df.dtypes)
        
        # 检查唯一值
        print(f"\n唯一值统计:")
        for col in df.columns:
            unique_count = df[col].nunique()
            print(f"  {col}: {unique_count} 个唯一值")
            
except Exception as e:
    print(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试不同指标:")
print("=" * 60)

for indicator in ["累计买入", "累计卖出"]:
    print(f"\n指标: {indicator}")
    try:
        df = ak.fund_portfolio_change_em(symbol=symbol, indicator=indicator, date=date)
        print(f"  [OK] 成功获取 {len(df)} 条记录")
    except Exception as e:
        print(f"  [ERROR] 失败: {e}")

print("\n" + "=" * 60)
