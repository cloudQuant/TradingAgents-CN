"""测试 fund_value_estimation_em 数据结构"""
import akshare as ak
import pandas as pd
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取数据
df = ak.fund_value_estimation_em(symbol="全部")

print("=" * 80)
print("数据形状:", df.shape)
print("\n" + "=" * 80)
print("列名列表:")
for col in df.columns:
    print(f"  - {col}")
print("\n" + "=" * 80)
print("前3行数据:")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.head(3).to_string())
print("\n" + "=" * 80)
print("数据类型:")
for col, dtype in df.dtypes.items():
    print(f"  {col}: {dtype}")
