#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.options.collections.test_collections_page import parse_requirements

def main():
    req_dir = os.path.join(os.path.dirname(__file__), "options", "requirements")
    print("=== 期权数据集合需求文档解析统计 ===")
    expected = parse_requirements(req_dir)
    print(f"需求文档目录: {req_dir}")
    print(f"解析到的集合数量: {len(expected)}")
    
    print("\n=== 解析结果详细列表 ===")
    for i, item in enumerate(expected, 1):
        slug = item["slug"]
        display_name = item["display_name"] 
        doc_path = item["doc_path"]
        print(f"{i:2d}. {slug}")
        print(f"    显示名称: {display_name}")
        print(f"    文档文件: {os.path.basename(doc_path)}")
        print()

    print("=== 需要验证的数据集合 slugs ===")
    slugs = [item["slug"] for item in expected]
    print(slugs)
    
    print(f"\n=== 总结 ===")
    print(f"共需要验证 {len(expected)} 个数据集合")

if __name__ == "__main__":
    main()
