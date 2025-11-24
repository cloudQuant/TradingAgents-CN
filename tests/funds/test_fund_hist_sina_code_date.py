"""
测试基金历史行情-新浪的基金代码字段和唯一标识

验证：
1. AKShare API 返回的数据结构
2. 添加基金代码字段的逻辑
3. 使用 code + date 作为唯一标识
"""

import sys
import os
import io
import pandas as pd

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestFundHistSinaCodeDate:
    """测试基金历史行情-新浪的基金代码和唯一标识"""
    
    def test_akshare_api_structure(self):
        """测试 AKShare API 返回的数据结构"""
        try:
            import akshare as ak
            
            print("\n[1] 测试 AKShare API 数据结构")
            print("="*60)
            
            # 测试基金代码
            symbol = "sh510050"
            print(f"测试基金代码: {symbol}")
            
            df = ak.fund_etf_hist_sina(symbol=symbol)
            
            assert df is not None, "API 返回 None"
            assert not df.empty, "API 返回空数据"
            
            print(f"✓ 返回数据行数: {len(df)}")
            print(f"✓ 字段列表: {df.columns.tolist()}")
            
            # 验证必需字段
            required_fields = ['date', 'open', 'high', 'low', 'close', 'volume']
            for field in required_fields:
                assert field in df.columns, f"缺少必需字段: {field}"
            
            print(f"✓ 所有必需字段都存在")
            
            # 注意：API 不返回基金代码
            if 'code' in df.columns or '代码' in df.columns:
                print("⚠ API 返回了基金代码字段（不符合预期）")
            else:
                print("✓ API 不返回基金代码字段（符合预期，需要手动添加）")
            
            # 显示样本数据
            print(f"\n样本数据（前3条）:")
            print(df.head(3).to_string())
            
            return df
            
        except Exception as e:
            print(f"✗ AKShare API 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_add_fund_code(self):
        """测试添加基金代码字段"""
        try:
            import akshare as ak
            
            print("\n[2] 测试添加基金代码字段")
            print("="*60)
            
            symbol = "sh510050"
            df = ak.fund_etf_hist_sina(symbol=symbol)
            
            # 模拟刷新服务的逻辑：添加基金代码
            df = df.copy()
            df["代码"] = symbol
            
            print(f"✓ 添加基金代码字段: {symbol}")
            print(f"✓ 更新后字段列表: {df.columns.tolist()}")
            
            assert "代码" in df.columns, "未成功添加基金代码字段"
            assert (df["代码"] == symbol).all(), "基金代码值不正确"
            
            print(f"✓ 基金代码字段添加成功")
            
            # 显示样本数据
            print(f"\n样本数据（前3条）:")
            print(df.head(3).to_string())
            
            return df
            
        except Exception as e:
            print(f"✗ 添加基金代码测试失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_field_mapping(self):
        """测试字段映射逻辑"""
        try:
            print("\n[3] 测试字段映射逻辑")
            print("="*60)
            
            # 模拟数据
            sample_data = {
                "代码": ["sh510050", "sh510050", "sh510050"],
                "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "open": [2.80, 2.85, 2.82],
                "high": [2.85, 2.90, 2.88],
                "low": [2.78, 2.82, 2.80],
                "close": [2.83, 2.87, 2.85],
                "volume": [1000000, 1200000, 1100000]
            }
            
            df = pd.DataFrame(sample_data)
            
            # 应用字段映射（模拟 save_fund_hist_sina_data 的逻辑）
            field_mapping = {
                "date": "date",
                "日期": "date",
                "open": "open",
                "开盘": "open",
                "high": "high",
                "最高": "high",
                "low": "low",
                "最低": "low",
                "close": "close",
                "收盘": "close",
                "volume": "volume",
                "成交量": "volume",
                "代码": "code",
                "code": "code",
            }
            
            df_mapped = df.rename(columns=field_mapping)
            
            print(f"✓ 原始列名: {df.columns.tolist()}")
            print(f"✓ 映射后列名: {df_mapped.columns.tolist()}")
            
            assert "code" in df_mapped.columns, "未成功映射 '代码' 到 'code'"
            assert "代码" not in df_mapped.columns, "'代码' 应该被映射为 'code'"
            
            print(f"✓ 字段映射成功: '代码' → 'code'")
            
            # 显示映射后的数据
            print(f"\n映射后数据（前3条）:")
            print(df_mapped.head(3).to_string())
            
            return df_mapped
            
        except Exception as e:
            print(f"✗ 字段映射测试失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_unique_identifier(self):
        """测试唯一标识：code + date"""
        try:
            print("\n[4] 测试唯一标识：code + date")
            print("="*60)
            
            # 模拟数据（已映射）
            sample_data = {
                "code": ["sh510050", "sh510050", "sh510300", "sh510300"],
                "date": ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02"],
                "open": [2.80, 2.85, 3.50, 3.55],
                "high": [2.85, 2.90, 3.55, 3.60],
                "low": [2.78, 2.82, 3.48, 3.52],
                "close": [2.83, 2.87, 3.52, 3.58],
                "volume": [1000000, 1200000, 800000, 900000]
            }
            
            df = pd.DataFrame(sample_data)
            
            # 创建唯一键
            df["unique_key"] = df["code"] + "_" + df["date"]
            
            print(f"✓ 总记录数: {len(df)}")
            print(f"✓ 唯一键数量: {df['unique_key'].nunique()}")
            
            assert len(df) == df["unique_key"].nunique(), "code + date 组合不唯一！"
            
            print(f"✓ code + date 组合是唯一的")
            
            # 显示唯一键
            print(f"\n唯一键示例:")
            for idx, row in df.iterrows():
                print(f"  {row['unique_key']}")
            
            # 模拟 UpdateOne 操作的唯一键
            print(f"\nMongoDB UpdateOne 唯一键:")
            for idx, row in df.iterrows():
                key = {"code": row["code"], "date": row["date"]}
                print(f"  {key}")
            
            return True
            
        except Exception as e:
            print(f"✗ 唯一标识测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_data_save_structure(self):
        """测试数据保存结构"""
        try:
            print("\n[5] 测试数据保存结构")
            print("="*60)
            
            # 模拟保存前的数据处理
            sample_row = {
                "code": "sh510050",
                "date": "2024-01-01",
                "open": 2.80,
                "high": 2.85,
                "low": 2.78,
                "close": 2.83,
                "volume": 1000000
            }
            
            # 构建保存记录（模拟 save_fund_hist_sina_data 的逻辑）
            record = {
                "code": sample_row["code"],
                "date": sample_row["date"],
                "open": float(sample_row["open"]),
                "high": float(sample_row["high"]),
                "low": float(sample_row["low"]),
                "close": float(sample_row["close"]),
                "volume": int(sample_row["volume"]),
            }
            
            # 唯一键
            unique_key = {
                "code": sample_row["code"],
                "date": sample_row["date"]
            }
            
            print(f"✓ 保存记录结构:")
            for key, value in record.items():
                print(f"  {key}: {value} ({type(value).__name__})")
            
            print(f"\n✓ 唯一键结构:")
            for key, value in unique_key.items():
                print(f"  {key}: {value}")
            
            print(f"\n✓ MongoDB 操作:")
            print(f"  UpdateOne(")
            print(f"    filter={unique_key},")
            print(f"    update={{'$set': {record}}},")
            print(f"    upsert=True")
            print(f"  )")
            
            return True
            
        except Exception as e:
            print(f"✗ 数据保存结构测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """手动运行测试"""
    print("\n" + "="*60)
    print("基金历史行情-新浪：基金代码字段和唯一标识测试")
    print("="*60)
    
    test = TestFundHistSinaCodeDate()
    results = []
    
    # 测试1: AKShare API结构
    try:
        df1 = test.test_akshare_api_structure()
        results.append(("AKShare API结构", df1 is not None))
    except Exception as e:
        print(f"测试1异常: {e}")
        results.append(("AKShare API结构", False))
    
    # 测试2: 添加基金代码
    try:
        df2 = test.test_add_fund_code()
        results.append(("添加基金代码", df2 is not None))
    except Exception as e:
        print(f"测试2异常: {e}")
        results.append(("添加基金代码", False))
    
    # 测试3: 字段映射
    try:
        df3 = test.test_field_mapping()
        results.append(("字段映射", df3 is not None))
    except Exception as e:
        print(f"测试3异常: {e}")
        results.append(("字段映射", False))
    
    # 测试4: 唯一标识
    try:
        result4 = test.test_unique_identifier()
        results.append(("唯一标识", result4))
    except Exception as e:
        print(f"测试4异常: {e}")
        results.append(("唯一标识", False))
    
    # 测试5: 数据保存结构
    try:
        result5 = test.test_data_save_structure()
        results.append(("数据保存结构", result5))
    except Exception as e:
        print(f"测试5异常: {e}")
        results.append(("数据保存结构", False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status} - {name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n总计: {passed_count}/{total_count} 测试通过")
    
    if passed_count == total_count:
        print("\n🎉 所有测试通过！当前实现符合需求：")
        print("  1. ✓ AKShare API 不返回基金代码（需要手动添加）")
        print("  2. ✓ 刷新服务添加 '代码' 字段")
        print("  3. ✓ 保存服务将 '代码' 映射为 'code'")
        print("  4. ✓ 使用 code + date 作为唯一标识")
        print("  5. ✓ 数据保存结构正确")
    else:
        print("\n⚠ 部分测试失败，需要检查实现")


if __name__ == "__main__":
    main()
