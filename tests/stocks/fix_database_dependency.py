"""
修复API路由中的数据库依赖函数名
"""
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent.parent
stocks_router_file = project_root / "app" / "routers" / "stocks.py"

print("="*80)
print("修复数据库依赖函数名")
print("="*80)

# 读取文件
content = stocks_router_file.read_text(encoding='utf-8')

print(f"\n原文件大小: {len(content)} 字符")

# 检查导入语句
print("\n检查导入语句（前30行）:")
lines = content.split('\n')[:30]
for line in lines:
    if 'import' in line.lower():
        print(f"  {line}")

# 检查使用的函数名
print(f"\n函数使用统计:")
print(f"  get_database: {content.count('get_database')} 次")
print(f"  get_mongo_db: {content.count('get_mongo_db')} 次")

# 判断应该使用哪个函数名
if 'from app.core.database import get_mongo_db' in content:
    correct_function = 'get_mongo_db'
    print(f"\n[+] Correct function name: {correct_function}")
elif 'from app.core.database import get_database' in content:
    correct_function = 'get_database'
    print(f"\n[+] Correct function name: {correct_function}")
else:
    print("\n错误: 找不到数据库依赖函数的导入")
    exit(1)

# 如果使用了错误的函数名，进行替换
if content.count('get_database') > 0 and correct_function == 'get_mongo_db':
    print(f"\n需要替换: get_database -> get_mongo_db")
    
    # 替换所有的 get_database 为 get_mongo_db
    new_content = content.replace('get_database', 'get_mongo_db')
    
    print(f"\n替换后:")
    print(f"  get_database: {new_content.count('get_database')} 次")
    print(f"  get_mongo_db: {new_content.count('get_mongo_db')} 次")
    
    # 保存文件
    stocks_router_file.write_text(new_content, encoding='utf-8')
    print(f"\n已保存: {stocks_router_file}")
    
elif content.count('get_mongo_db') > 0 and correct_function == 'get_database':
    print(f"\n需要替换: get_mongo_db -> get_database")
    
    # 替换所有的 get_mongo_db 为 get_database
    new_content = content.replace('get_mongo_db', 'get_database')
    
    print(f"\n替换后:")
    print(f"  get_database: {new_content.count('get_database')} 次")
    print(f"  get_mongo_db: {new_content.count('get_mongo_db')} 次")
    
    # 保存文件
    stocks_router_file.write_text(new_content, encoding='utf-8')
    print(f"\n已保存: {stocks_router_file}")
else:
    print(f"\n[+] Function names are correct, no changes needed")

print("\n" + "="*80)
print("修复完成！")
print("="*80)
print("\n请重启后端服务：")
print("  cd F:\\source_code\\TradingAgents-CN")
print("  uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload")
print("="*80)
