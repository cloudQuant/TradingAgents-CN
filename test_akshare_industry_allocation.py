#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test AKShare fund_portfolio_industry_allocation_em API"""
import akshare as ak
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test fund_portfolio_industry_allocation_em
print("=" * 60)
print("Test AKShare fund_portfolio_industry_allocation_em API")
print("=" * 60)

# 尝试不同的基金和日期组合
test_cases = [
    ("000001", "2023-12-31"),  # 华夏成长混合
    ("161725", "2023-12-31"),  # 招商中证白酒指数分级
    ("110022", "2023-12-31"),  # 易方达消费行业
    ("270002", "2023-12-31"),  # 广发稳健增长混合
]

for symbol, date in test_cases:
    print(f"\n{'='*40}")
    print(f"测试基金: {symbol}")
    print(f"测试日期: {date}")
    print('='*40)
    
    try:
        df = ak.fund_portfolio_industry_allocation_em(symbol=symbol, date=date)
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
            
            # 检查唯一标识字段
            print(f"\n唯一值统计:")
            for col in df.columns:
                unique_count = df[col].nunique()
                print(f"  {col}: {unique_count} 个唯一值")
            
            # 找到有效日期后退出
            break
            
    except Exception as e:
        print(f"[ERROR] Failed: {e}")

print("\n" + "=" * 60)
