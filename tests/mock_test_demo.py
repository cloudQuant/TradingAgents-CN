#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟演示测试输出效果
展示优化后的日志信息格式
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.options.collections.test_collections_page import parse_requirements

def mock_api_collections_response():
    """模拟后端 /api/options/collections 返回的集合列表"""
    # 这里模拟后端现有的集合（从 app/routers/options.py 中获取的部分）
    existing_collections = [
        "options_basic_info",
        "options_daily_quotes", 
        "options_greeks",
        "option_contract_info_ctp",
        "option_finance_board",
        "option_risk_indicator_sse",
        "option_current_day_sse",
        "option_current_day_szse",
        "option_daily_stats_sse",
        "option_daily_stats_szse",
        "option_cffex_sz50_list_sina",
        "option_cffex_hs300_list_sina",
        "option_cffex_zz1000_list_sina",
        "option_current_em",
        "option_sse_underlying_spot_price_sina",
        "option_sse_greeks_sina",
        "option_sse_minute_sina",
        "option_sse_daily_sina",
        # 故意遗漏一些集合来模拟缺失情况
    ]
    return existing_collections

def mock_failed_collections():
    """模拟一些打开失败的集合"""
    return [
        "option_sse_spot_price_sina",  # HTTP 404
        "option_finance_minute_sina",  # 响应异常
    ]

def demonstrate_test_output():
    print("=" * 80)
    print("期权数据集合测试 - 详细日志输出演示")
    print("=" * 80)
    
    # 解析需求文档
    req_dir = os.path.join(os.path.dirname(__file__), "options", "requirements")
    expected_from_requirements = parse_requirements(req_dir)
    expected_slugs = [it["slug"] for it in expected_from_requirements]
    
    # 模拟后端API返回
    api_collections = mock_api_collections_response()
    
    # 统计和对比
    print("\n[统计] 需求文档中需要验证的数据集合数量:", len(expected_slugs))
    print("[统计] 页面/API 返回的数据集合数量:", len(api_collections))
    print("[列表] 需求集合(slugs):", expected_slugs[:5], "... (显示前5个)")
    print("[列表] 页面集合(names):", sorted(api_collections)[:5], "... (显示前5个)")
    
    # 查找缺失的集合
    missing = []
    for item in expected_from_requirements:
        slug = item["slug"]
        if slug not in api_collections:
            missing.append(f"{slug}  <- {os.path.basename(item['doc_path'])}")
    
    print("[统计] 缺少的数据集合数量:", len(missing))
    if missing:
        print("[缺少清单] 以下集合在需求文档中定义但未在页面/API 返回中找到:")
        for m in missing[:10]:  # 只显示前10个
            print("  -", m)
        if len(missing) > 10:
            print(f"  - ... 还有 {len(missing) - 10} 个缺失集合")
    
    # 可打开性验证
    print("\n[检查] 开始验证集合可打开性: 共", len(expected_slugs), "个")
    
    # 模拟一些失败的集合
    failed_collections = mock_failed_collections()
    failed = []
    for slug in failed_collections:
        for item in expected_from_requirements:
            if item["slug"] == slug:
                if slug == "option_sse_spot_price_sina":
                    failed.append(f"{slug} -> HTTP 404  文档: {os.path.basename(item['doc_path'])}")
                elif slug == "option_finance_minute_sina":
                    failed.append(f"{slug} -> 响应异常: {{'success': False}}  文档: {os.path.basename(item['doc_path'])}")
    
    success_count = len(expected_slugs) - len(missing) - len(failed)
    print("[统计] 可打开性验证完成: 需验证", len(expected_slugs), "个, 失败", len(failed), "个")
    if failed:
        print("[失败清单] 以下集合打开失败:")
        for f in failed:
            print("  -", f)
    
    print("\n" + "=" * 80)
    print("测试结果总结:")
    print(f"  需要验证的总数量: {len(expected_slugs)} 个")
    print(f"  API返回的数量: {len(api_collections)} 个") 
    print(f"  缺失数量: {len(missing)} 个")
    print(f"  打开失败数量: {len(failed)} 个")
    print(f"  成功数量: {success_count} 个")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_test_output()
