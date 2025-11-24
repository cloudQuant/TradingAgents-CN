"""
修复stocks.py中缺失的导入
"""
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent.parent
stocks_router_file = project_root / "app" / "routers" / "stocks.py"

print("="*80)
print("修复导入语句")
print("="*80)

# 读取文件
content = stocks_router_file.read_text(encoding='utf-8')

print(f"\n原文件大小: {len(content)} 字符")

# 检查是否已经导入了 AsyncIOMotorClient
if 'AsyncIOMotorClient' in content and 'from motor.motor_asyncio import AsyncIOMotorClient' not in content:
    print("\n发现使用了 AsyncIOMotorClient 但未导入")
    
    # 找到其他 motor 相关的导入，或者 from typing 导入的位置
    lines = content.split('\n')
    insert_line = -1
    
    # 查找合适的插入位置（在 from typing 之后，在第一个非导入语句之前）
    for i, line in enumerate(lines):
        if line.startswith('from typing import'):
            insert_line = i + 1
            break
    
    if insert_line == -1:
        # 如果找不到 from typing，就在第一个 import 语句之后
        for i, line in enumerate(lines):
            if line.startswith('from ') or line.startswith('import '):
                insert_line = i + 1
    
    if insert_line != -1:
        print(f"\n将在第 {insert_line + 1} 行插入导入语句")
        
        # 插入导入
        lines.insert(insert_line, 'from motor.motor_asyncio import AsyncIOMotorClient')
        
        new_content = '\n'.join(lines)
        
        # 保存文件
        stocks_router_file.write_text(new_content, encoding='utf-8')
        print(f"\n已添加导入: from motor.motor_asyncio import AsyncIOMotorClient")
        print(f"已保存: {stocks_router_file}")
    else:
        print("\n错误: 找不到合适的插入位置")
        exit(1)
        
elif 'from motor.motor_asyncio import AsyncIOMotorClient' in content:
    print("\n[+] AsyncIOMotorClient 已正确导入")
else:
    print("\n[+] 未使用 AsyncIOMotorClient，无需导入")

# 检查其他可能缺失的导入
print("\n检查其他导入:")
imports_to_check = [
    ('FastAPI', 'from fastapi import FastAPI'),
    ('Depends', 'from fastapi import'),
    ('get_mongo_db', 'from app.core.database import get_mongo_db'),
]

for item_name, import_pattern in imports_to_check:
    if item_name in content:
        if import_pattern in content:
            print(f"  [+] {item_name}: OK")
        else:
            print(f"  [!] {item_name}: Used but might not be imported correctly")
    else:
        print(f"  [-] {item_name}: Not used")

print("\n" + "="*80)
print("修复完成！")
print("="*80)
print("\n请重启后端服务：")
print("  cd F:\\source_code\\TradingAgents-CN")
print("  uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload")
print("="*80)
