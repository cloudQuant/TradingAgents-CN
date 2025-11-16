"""
验证评级选项是否完整
"""
import os

# 完整的27个评级列表（按顺序）
required_grades = [
    'AAA+', 'AAA', 'AAA-',
    'AA+', 'AA', 'AA-',
    'A+', 'A', 'A-',
    'A-1', 'A-2', 'A-3',
    'BBB+', 'BBB', 'BBB-',
    'BB+', 'BB', 'BB-',
    'B+', 'B', 'B-',
    'CCC+', 'CCC', 'CCC-',
    'CC', 'C', 'D'
]

print("=" * 60)
print("验证评级选项完整性")
print("=" * 60)

# 读取Vue文件
vue_file_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'views', 'Bonds', 'Collection.vue'
)
vue_file_path = os.path.abspath(vue_file_path)

if not os.path.exists(vue_file_path):
    print(f"[FAILED] 文件不存在: {vue_file_path}")
    exit(1)

with open(vue_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"\n[检查] 文件: {vue_file_path}")

# 查找评级下拉框部分
grade_section_start = content.find('<el-form-item label="评级">')
if grade_section_start < 0:
    print("[FAILED] 找不到评级表单项")
    exit(1)

grade_section_end = content.find('</el-select>', grade_section_start)
grade_section = content[grade_section_start:grade_section_end + 12]

print("\n[检查] 评级选项:")
print("-" * 60)

missing_grades = []
found_count = 0

for grade in required_grades:
    option_pattern = f'<el-option label="{grade}" value="{grade}" />'
    if option_pattern in grade_section:
        print(f"  [OK] {grade:6s} - 已找到")
        found_count += 1
    else:
        print(f"  [MISS] {grade:6s} - 缺失")
        missing_grades.append(grade)

print("-" * 60)
print(f"\n统计:")
print(f"  - 应有评级数: {len(required_grades)}")
print(f"  - 已找到: {found_count}")
print(f"  - 缺失: {len(missing_grades)}")

if missing_grades:
    print(f"\n[FAILED] 缺失的评级: {', '.join(missing_grades)}")
    exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] 评级选项完整！")
print("=" * 60)

# 显示评级分类
print("\n评级分类:")
print("  投资级 (Investment Grade):")
print("    - AAA级: AAA+, AAA, AAA-")
print("    - AA级:  AA+, AA, AA-")
print("    - A级:   A+, A, A-")
print("    - BBB级: BBB+, BBB, BBB-")
print("\n  投机级 (Speculative Grade):")
print("    - BB级:  BB+, BB, BB-")
print("    - B级:   B+, B, B-")
print("    - CCC级: CCC+, CCC, CCC-")
print("    - 其他:  CC, C, D")
print("\n  短期评级:")
print("    - A-1 (最高)")
print("    - A-2 (高)")
print("    - A-3 (良好)")
