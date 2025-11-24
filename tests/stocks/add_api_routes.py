"""
添加生成的API路由到stocks.py
"""
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent.parent
stocks_router_file = project_root / "app" / "routers" / "stocks.py"

print("="*80)
print("添加API路由到stocks.py")
print("="*80)

# 读取当前的 stocks.py
content = stocks_router_file.read_text(encoding='utf-8')
print(f"\n当前文件大小: {len(content)} 字符")

# 读取生成的API路由
api_routes_file = Path(__file__).parent / "generated_api_routes.py"
api_routes_content = api_routes_file.read_text(encoding='utf-8')

# 提取API路由代码（去掉注释和文档字符串头部）
# 找到第一个@router出现的位置
import re
first_router = api_routes_content.find('@router')
if first_router == -1:
    print("错误: 找不到@router装饰器")
    exit(1)

api_routes_to_add = api_routes_content[first_router:].strip()

print(f"\nAPI路由代码大小: {len(api_routes_to_add)} 字符")
print(f"路由数量:")
print(f"  @router.get: {api_routes_to_add.count('@router.get')}")
print(f"  @router.post: {api_routes_to_add.count('@router.post')}")  
print(f"  @router.delete: {api_routes_to_add.count('@router.delete')}")

# 检查是否已经添加过
if "# ========== 自动生成的API路由" in content:
    print("\n警告: 检测到已存在的自动生成API路由标记")
    print("将替换现有的自动生成部分")
    
    # 找到标记位置并删除之后的所有内容
    marker_pos = content.find("# ========== 自动生成的API路由")
    content = content[:marker_pos].rstrip()

# 在文件末尾添加API路由
new_content = content + "\n\n\n# ========== 自动生成的API路由 (290个集合 x 4个端点 = 1160个端点) ==========\n\n"
new_content += api_routes_to_add
new_content += "\n"

# 保存文件
stocks_router_file.write_text(new_content, encoding='utf-8')

print(f"\n新文件大小: {len(new_content)} 字符")
print(f"已保存: {stocks_router_file}")

print("\n" + "="*80)
print("添加完成！")
print("="*80)
print("\n请重启后端服务：")
print("  cd F:\\source_code\\TradingAgents-CN")
print("  uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload")
print("="*80)
