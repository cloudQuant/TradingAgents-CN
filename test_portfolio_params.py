#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify fund_portfolio_hold_em parameter changes"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

print("=" * 80)
print("VERIFY fund_portfolio_hold_em PARAMETER CHANGES")
print("=" * 80)

# Test 1: Check function signature
print("\n[TEST 1] Checking _fetch_fund_portfolio_hold_em signature...")
try:
    from app.services.fund_refresh_service import FundRefreshService
    import inspect
    
    sig = inspect.signature(FundRefreshService._fetch_fund_portfolio_hold_em)
    params = list(sig.parameters.keys())
    
    print(f"Parameters: {params}")
    
    if 'year' in params and 'date' not in params:
        print("[PASS] Function signature updated correctly (has 'year', no 'date')")
    elif 'date' in params:
        print("[FAIL] Function still has 'date' parameter instead of 'year'")
    else:
        print(f"[WARN] Unexpected parameters: {params}")
        
except Exception as e:
    print(f"[ERROR] {e}")

# Test 2: Check docstring
print("\n[TEST 2] Checking _refresh_fund_portfolio_hold_em docstring...")
try:
    from app.services.fund_refresh_service import FundRefreshService
    
    docstring = FundRefreshService._refresh_fund_portfolio_hold_em.__doc__
    
    if docstring:
        if 'year' in docstring and 'YYYY' in docstring:
            print("[PASS] Docstring mentions 'year' parameter with format YYYY")
        else:
            print("[WARN] Docstring may need update")
        
        if 'date' in docstring.lower() and 'YYYY-MM-DD' in docstring:
            print("[WARN] Docstring still mentions date with YYYY-MM-DD format")
    else:
        print("[WARN] No docstring found")
        
except Exception as e:
    print(f"[ERROR] {e}")

# Test 3: Read source code directly to verify changes
print("\n[TEST 3] Verifying source code changes...")
try:
    with open('app/services/fund_refresh_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    checks = [
        ("Year parameter in function def", "def _fetch_fund_portfolio_hold_em(self, symbol: str, year: str):"),
        ("Year docstring in fetch", "year: 查询年份 (YYYY)"),
        ("Year parameter in refresh", "year: 查询年份 (单个更新必须，格式: YYYY)"),
        ("Year validation", '单个更新必须提供 year 参数'),
        ("Year in update_one function", "async def update_one(code, y):"),
        ("Years list generation", "years = [str(y) for y in range(2010, current_year + 1)]"),
        ("total_years in result", '"total_years": len(years)'),
    ]
    
    passed = 0
    failed = 0
    
    for check_name, check_str in checks:
        if check_str in content:
            print(f"  [PASS] {check_name}")
            passed += 1
        else:
            print(f"  [FAIL] {check_name}")
            failed += 1
    
    print(f"\nCode verification: {passed} passed, {failed} failed")
    
except Exception as e:
    print(f"[ERROR] {e}")

# Test 4: Check that old quarter-based code is removed
print("\n[TEST 4] Checking for removed quarter-based code...")
try:
    with open('app/services/fund_refresh_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_patterns = [
        ("Quarter dates generation", "quarter_dates = []"),
        ("Quarter format MM-DD", '"-03-31"'),
        ("total_quarters in result", '"total_quarters"'),
    ]
    
    issues = 0
    for pattern_name, pattern_str in old_patterns:
        # Count occurrences in the portfolio_hold_em function
        if pattern_str in content:
            # Find the context
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if pattern_str in line:
                    # Check if it's in the _refresh_fund_portfolio_hold_em function
                    # by looking backwards for the function definition
                    for j in range(i, max(0, i-100), -1):
                        if '_refresh_fund_portfolio_hold_em' in lines[j]:
                            print(f"  [WARN] Found old pattern '{pattern_name}' near line {i+1}")
                            issues += 1
                            break
                        elif '_refresh_fund_portfolio_bond_hold_em' in lines[j]:
                            # It's in a different function, that's okay
                            break
    
    if issues == 0:
        print("  [PASS] No old quarter-based patterns found in portfolio_hold_em function")
    else:
        print(f"  [WARN] Found {issues} potential old patterns")
        
except Exception as e:
    print(f"[ERROR] {e}")

# Test 5: Verify test file changes
print("\n[TEST 5] Checking test file updates...")
try:
    with open('tests/funds/test_fund_portfolio_hold_em.py', 'r', encoding='utf-8') as f:
        test_content = f.read()
        
    if '"year": "2024"' in test_content:
        print("  [PASS] Test file uses 'year' parameter")
    else:
        print("  [FAIL] Test file doesn't use 'year' parameter")
        
    if '"date": "2024-09-30"' in test_content:
        print("  [WARN] Test file still has old 'date' parameter with quarter format")
    else:
        print("  [PASS] Old 'date' parameter removed from tests")
        
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
print("\nSummary:")
print("- Parameter changed from 'date' (quarter) to 'year' (YYYY)")
print("- Batch update now iterates over years instead of quarters")
print("- Function signatures and docstrings updated")
print("- Test files updated")
print("\nNext steps:")
print("1. Test with actual MongoDB connection and real data")
print("2. Update frontend if it sends quarter dates")
print("3. Run full test suite")
print("=" * 80)
