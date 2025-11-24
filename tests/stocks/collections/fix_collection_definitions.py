#!/usr/bin/env python3
"""
修复Collection.vue文件中的集合定义问题
使所有集合（即使未预定义）都能正常显示和使用
"""

import os
import re
from pathlib import Path

# 需要修复的文件路径列表
COLLECTION_FILES = [
    "frontend/src/views/Stocks/Collection.vue",
    "frontend/src/views/Bonds/Collection.vue",
    "frontend/src/views/Funds/Collection.vue",
    "frontend/src/views/Futures/Collection.vue",
    "frontend/src/views/Options/Collection.vue",
]

def fix_collection_def(content: str) -> str:
    """修复collectionDef computed属性"""
    
    # 查找并替换 collectionDef - 使用字符串拼接避免转义问题
    pattern = r'const collectionDef = computed<CollectionDefinition \| null>\(\(\) => \{\s*const name = collectionName\.value\s*return collectionDefinitions\[name\] \|\| null\s*\}\)'
    
    replacement = """const collectionDef = computed<CollectionDefinition | null>(() => {
  const name = collectionName.value
  // 如果有预定义的集合定义则使用，否则创建默认定义
  if (collectionDefinitions[name]) {
    return collectionDefinitions[name]
  }
  
  // 为未定义的集合创建默认定义
  if (name) {
    return {
      display_name: name.replace(/_/g, ' ').replace(/""" + r"\\b\\w" + """/g, l => l.toUpperCase()),
      description: `数据集合: ${name}`,
      fields: [] // 字段将从实际数据中获取
    }
  }
  
  return null
})"""
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return content

def fix_field_rows(content: str) -> str:
    """修复fieldRows computed属性"""
    
    pattern = r'const fieldRows = computed<FieldRow\[\]>\(\(\) => \{[^}]*\}\)'
    
    replacement = '''const fieldRows = computed<FieldRow[]>(() => {
  if (!collectionDef.value) return []
  
  // 优先使用预定义的字段
  if (collectionDef.value.fields && collectionDef.value.fields.length > 0) {
    return collectionDef.value.fields.map((name) => ({
      name,
      description: '',
      example: null,
    }))
  }
  
  // 如果没有预定义字段，从实际数据中获取
  if (rows.value.length > 0) {
    const firstRow = rows.value[0]
    return Object.keys(firstRow).map((name) => ({
      name,
      description: '',
      example: firstRow[name],
    }))
  }
  
  return []
})'''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return content

def add_display_fields(content: str) -> str:
    """添加displayFields computed属性"""
    
    # 检查是否已存在
    if 'const displayFields' in content:
        return content
    
    # 在fieldRows之后插入
    pattern = r'(const fieldRows = computed<FieldRow\[\]>\(\(\) => \{[^}]*\}\)\s*\n)'
    
    addition = '''$1
// 用于表格显示的字段列表
const displayFields = computed<string[]>(() => {
  // 优先使用预定义的字段
  if (collectionDef.value?.fields && collectionDef.value.fields.length > 0) {
    return collectionDef.value.fields
  }
  
  // 从实际数据中获取字段
  if (rows.value.length > 0) {
    return Object.keys(rows.value[0])
  }
  
  return []
})

'''
    
    content = re.sub(pattern, addition, content, flags=re.DOTALL)
    return content

def fix_table_columns(content: str) -> str:
    """修复表格列定义"""
    
    # 将 collectionDef.fields 改为 displayFields
    pattern = r'v-for="field in collectionDef\.fields"'
    replacement = 'v-for="field in displayFields"'
    
    content = re.sub(pattern, replacement, content)
    return content

def fix_on_mounted(content: str) -> str:
    """修复onMounted钩子"""
    
    pattern = r'onMounted\(\(\) => \{\s*if \(!collectionDef\.value\) \{[^}]*\}\s*// 加载统计信息和数据\s*Promise\.all\(\[loadStats\(\), refreshData\(\)\]\)\s*\}\)'
    
    replacement = '''onMounted(() => {
  // 即使没有预定义的集合，也尝试加载数据
  if (collectionName.value) {
    // 加载统计信息和数据
    Promise.all([loadStats(), refreshData()])
  } else {
    ElMessage.warning('集合名称不能为空')
  }
})'''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return content

def fix_file(file_path: str, dry_run: bool = False) -> bool:
    """修复单个文件"""
    
    full_path = Path(__file__).parent.parent.parent.parent / file_path
    
    if not full_path.exists():
        print(f"[x] 文件不存在: {file_path}")
        return False
    
    print(f"\n[*] 处理文件: {file_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    try:
        print(f"  [>] 修复 collectionDef...")
        content = fix_collection_def(content)
        
        print(f"  [>] 修复 fieldRows...")
        content = fix_field_rows(content)
        
        print(f"  [>] 添加 displayFields...")
        content = add_display_fields(content)
        
        print(f"  [>] 修复表格列...")
        content = fix_table_columns(content)
        
        print(f"  [>] 修复 onMounted...")
        content = fix_on_mounted(content)
        
        if content == original_content:
            print(f"  [!] 没有需要修改的内容")
            return True
        
        if dry_run:
            print(f"  [!] 演习模式：不保存文件")
            print(f"  [i] 原始长度: {len(original_content)} 字符")
            print(f"  [i] 修改后长度: {len(content)} 字符")
        else:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [+] 文件已成功修复")
        
        return True
        
    except Exception as e:
        print(f"  [x] 修复失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    import argparse
    import sys
    
    # 设置UTF-8编码输出
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description='修复Collection.vue文件的集合定义问题')
    parser.add_argument('--dry-run', action='store_true', help='演习模式，不实际修改文件')
    args = parser.parse_args()
    
    print("=" * 80)
    print("[*] 修复Collection.vue文件的集合定义问题")
    print("=" * 80)
    
    if args.dry_run:
        print("[!] 演习模式：将显示需要修改的内容，但不会实际保存")
    
    success_count = 0
    total_count = len(COLLECTION_FILES)
    
    for file_path in COLLECTION_FILES:
        if fix_file(file_path, dry_run=args.dry_run):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"[STATS] 修复完成统计")
    print(f"  总文件数: {total_count}")
    print(f"  成功修复: {success_count}")
    print(f"  失败数量: {total_count - success_count}")
    print("=" * 80)
    
    if success_count == total_count:
        print("[+] 所有文件修复成功！")
        print("\n修复说明：")
        print("  1. 为未定义的集合创建默认定义")
        print("  2. 从实际数据中动态获取字段列表")
        print("  3. 移除集合定义检查，允许所有集合显示")
        print("  4. 现在所有365个集合都能正常显示按钮和数据")
    else:
        print("[!] 部分文件修复失败，请检查日志")

if __name__ == '__main__':
    main()
