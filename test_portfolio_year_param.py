#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test fund_portfolio_hold_em with year parameter"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

async def test_single_update():
    """Test single fund update with year parameter"""
    print("=" * 60)
    print("Test Single Fund Update with Year Parameter")
    print("=" * 60)
    
    try:
        from app.services.fund_refresh_service import FundRefreshService
        from app.core.database import get_mongo_db
        
        db = get_mongo_db()
        service = FundRefreshService(db)
        
        # Create a test task
        task_id = "test_task_001"
        params = {
            "fund_code": "000001",
            "year": "2024"
        }
        
        print(f"\n[TEST] Single update with params: {params}")
        result = await service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print(f"[OK] Success!")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_batch_update():
    """Test batch update with year parameter"""
    print("\n" + "=" * 60)
    print("Test Batch Update with Year Parameter")
    print("=" * 60)
    
    try:
        from app.services.fund_refresh_service import FundRefreshService
        from app.core.database import get_mongo_db
        
        db = get_mongo_db()
        service = FundRefreshService(db)
        
        # Create a test task
        task_id = "test_task_002"
        params = {
            "batch": True,
            "year": "2024",
            "concurrency": 2
        }
        
        print(f"\n[TEST] Batch update with params: {params}")
        print("[INFO] This will take some time...")
        
        # Note: In real scenario, this will process many funds
        # For testing, just verify it can start without error
        result = await service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print(f"[OK] Success!")
        print(f"Result summary:")
        print(f"  - Total saved: {result.get('saved', 0)}")
        print(f"  - Success count: {result.get('success_count', 0)}")
        print(f"  - Failed count: {result.get('failed_count', 0)}")
        print(f"  - Total tasks: {result.get('total_tasks', 0)}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_error_handling():
    """Test error handling when year is missing"""
    print("\n" + "=" * 60)
    print("Test Error Handling (Missing Year Parameter)")
    print("=" * 60)
    
    try:
        from app.services.fund_refresh_service import FundRefreshService
        from app.core.database import get_mongo_db
        
        db = get_mongo_db()
        service = FundRefreshService(db)
        
        # Create a test task without year parameter
        task_id = "test_task_003"
        params = {
            "fund_code": "000001"
            # Missing year parameter
        }
        
        print(f"\n[TEST] Update without year parameter: {params}")
        result = await service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print(f"[ERROR] Should have raised ValueError!")
        return False
        
    except ValueError as e:
        print(f"[OK] Correctly raised ValueError: {e}")
        return True
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

async def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("TESTING fund_portfolio_hold_em WITH YEAR PARAMETER")
    print("=" * 80)
    
    results = []
    
    # Test 1: Error handling (fast test)
    result1 = await test_error_handling()
    results.append(("Error Handling", result1))
    
    # Test 2: Single update (may take 30-60 seconds)
    print("\n[INFO] Test 2 may take 30-60 seconds...")
    result2 = await test_single_update()
    results.append(("Single Update", result2))
    
    # Test 3: Batch update (will take several minutes, skip for now)
    print("\n[INFO] Skipping batch update test (would take too long)")
    # result3 = await test_batch_update()
    # results.append(("Batch Update", result3))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test_name}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + "=" * 80)
    if all_passed:
        print("[SUCCESS] All tests passed!")
    else:
        print("[FAILURE] Some tests failed!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
