"""测试 fund_value_estimation_em 的列名处理逻辑"""
import akshare as ak
import pandas as pd
import re
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取数据
print("=" * 80)
print("1. 获取原始数据...")
df = ak.fund_value_estimation_em(symbol="全部")
print(f"原始数据形状: {df.shape}")
print(f"原始列名: {df.columns.tolist()}")
print("\n原始数据前3行:")
print(df.head(3))

# 处理列名
print("\n" + "=" * 80)
print("2. 处理列名和日期...")

# 提取日期
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
dates_found = set()

for col in df.columns:
    match = date_pattern.search(str(col))
    if match:
        dates_found.add(match.group(1))

if dates_found:
    estimation_date = sorted(dates_found, reverse=True)[0]
    print(f"提取到估算日期: {estimation_date}")
else:
    from datetime import datetime
    estimation_date = datetime.now().strftime('%Y-%m-%d')
    print(f"未找到日期，使用当前日期: {estimation_date}")

# 重命名列
new_columns = {}
for col in df.columns:
    if date_pattern.search(str(col)):
        new_col = date_pattern.sub('', str(col)).lstrip('-')
        new_columns[col] = new_col
        print(f"  {col} -> {new_col}")
    else:
        new_columns[col] = col

df = df.rename(columns=new_columns)

# 添加日期字段
df['日期'] = estimation_date

print("\n" + "=" * 80)
print("3. 处理后的数据结构:")
print(f"新数据形状: {df.shape}")
print(f"新列名: {df.columns.tolist()}")
print("\n处理后数据前3行:")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.head(3))

print("\n" + "=" * 80)
print("4. 验证唯一标识字段:")
print(f"基金代码示例: {df['基金代码'].iloc[0]}")
print(f"日期示例: {df['日期'].iloc[0]}")
print(f"唯一键: code={df['基金代码'].iloc[0]}, date={df['日期'].iloc[0]}")

print("\n✅ 处理逻辑验证完成！")
