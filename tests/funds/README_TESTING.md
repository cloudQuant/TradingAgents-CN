# 基金数据集合测试指南

## 测试目的

验证 funds/collections 页面的数据集合是否完整包含 requirements 文件夹中需求文档定义的所有数据集合，并确保这些集合能够正确打开。

## 测试文件

| 文件 | 说明 |
|------|------|
| `test_collections_completeness.py` | 主测试脚本 - 自动化检测数据集合完整性 |
| `TEST_SUMMARY.md` | 测试摘要 - 快速查看测试结果 |
| `collections_test_report.md` | 详细报告 - 完整的测试结果和分析 |
| `README_TESTING.md` | 本文档 - 测试指南 |

## 快速开始

### 1. 运行测试

```bash
cd F:\source_code\TradingAgents-CN

# 运行测试
python tests\funds\test_collections_completeness.py

# 或者将结果输出到文件
python tests\funds\test_collections_completeness.py > tests\funds\test_result.txt 2>&1
```

### 2. 查看结果

```bash
# 查看测试摘要
type tests\funds\TEST_SUMMARY.md

# 查看详细报告
type tests\funds\collections_test_report.md
```

## 测试内容

### 测试项 1: 集合完整性检查

**检查内容：**
- 从 `tests/funds/` 目录下的需求文档中提取所有数据集合接口
- 从 `app/routers/funds.py` 提取后端已实现的数据集合
- 对比两者，找出缺失或命名不匹配的集合

**验收标准：**
- ✅ 所有需求文档中的集合都在后端有对应实现
- ⚠️ 允许命名差异（如添加数据源后缀 `_em`）

### 测试项 2: 字段完整性检查

**检查内容：**
- 验证每个集合定义是否包含必需字段：
  - `name` - 集合名称
  - `display_name` - 显示名称
  - `description` - 描述信息
  - `route` - 路由路径
  - `fields` - 字段列表

**验收标准：**
- ✅ 所有集合定义都包含这 5 个必需字段

## 测试结果解读

### 成功标志

```
[SUCCESS] 测试通过：所有需求文档中的数据集合都已实现
[SUCCESS] 所有集合定义都包含必需字段
[SUCCESS] 所有测试通过！
```

### 警告标志

```
[WARNING] 发现 X 个集合在后端未实现
[WARNING] 集合 'xxx' 缺少字段: xxx
```

### 信息标志

```
[INFO] 后端额外实现了 X 个集合（不在需求文档中）
```

## 常见问题

### Q1: 为什么有些集合"缺失"但实际能用？

**A:** 这是命名规范差异导致的。例如：
- 需求文档：`fund_rating_all`
- 后端实现：`fund_rating_all_em`

后端统一添加了数据源后缀（`_em` 表示东方财富），这不是真正的缺失。

### Q2: 如何修复命名不匹配？

**A:** 有两种方案：

**方案 1（推荐）：** 更新需求文档
```bash
# 在需求文档中将接口名称改为与后端一致
fund_rating_all -> fund_rating_all_em
```

**方案 2：** 修改后端
```python
# 在 app/routers/funds.py 中修改集合定义
{
    "name": "fund_rating_all",  # 改为与需求文档一致
    ...
}
```

### Q3: 如何添加新的数据集合？

**步骤：**

1. 在需求文档中定义接口（如 `99_新集合.md`）
2. 在 `app/routers/funds.py` 的 `collections` 列表中添加：

```python
{
    "name": "new_collection_name",
    "display_name": "新集合显示名称",
    "description": "集合描述",
    "route": "/funds/collections/new_collection_name",
    "fields": ["字段1", "字段2", ...],
}
```

3. 在 `collection_map` 中添加数据库映射：

```python
collection_map = {
    ...
    "new_collection_name": db.get_collection("new_collection_name"),
}
```

4. 重新运行测试验证

### Q4: 测试运行出现编码错误？

**A:** Windows 系统可能遇到 GBK 编码问题。解决方案：

```bash
# 将结果输出到文件
python tests\funds\test_collections_completeness.py > test_result.txt 2>&1

# 然后用支持 UTF-8 的编辑器查看 test_result.txt
```

或者在 PowerShell 中设置编码：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python tests\funds\test_collections_completeness.py
```

## 测试维护

### 何时需要重新运行测试？

✅ **必须运行：**
- 添加新的需求文档时
- 修改后端集合定义时
- 重构数据集合相关代码时

⚠️ **建议运行：**
- 每次发布前
- 每周一次定期检查

### 如何扩展测试？

测试脚本是模块化设计的，可以轻松扩展：

```python
# 添加新的测试方法
def test_new_feature(self):
    """测试新功能"""
    # 实现测试逻辑
    pass

# 在 run_all_tests() 中调用
def run_all_tests():
    tester = TestCollectionsCompleteness()
    test1_passed = tester.test_collections_completeness()
    test2_passed = tester.test_backend_collections_have_required_fields()
    test3_passed = tester.test_new_feature()  # 新增
    ...
```

## 相关文档

- [基金投研功能实现总结](基金投研功能实现总结.md)
- [需求文档清单](需求文档清单_26-65.md)
- [Collections 详细报告](collections_test_report.md)
- [测试摘要](TEST_SUMMARY.md)

## 技术细节

### 测试原理

1. **需求文档解析**：
   - 扫描 `tests/funds/*.md` 文件
   - 使用正则表达式提取 `接口: xxx` 标记
   - 收集接口名称和对应的需求文档

2. **后端代码解析**：
   - 读取 `app/routers/funds.py`
   - 提取所有 `"name": "xxx"` 定义
   - 构建后端集合集合

3. **对比分析**：
   - 计算差集找出缺失项
   - 计算交集找出匹配项
   - 生成详细报告和修复建议

### 依赖

- Python 3.7+
- 标准库：`os`, `sys`, `re`, `typing`
- 无第三方依赖

## 联系方式

如有问题或建议，请：
1. 查看 [详细报告](collections_test_report.md)
2. 查看测试代码中的注释
3. 提交 Issue 或 PR

---

**最后更新**: 2025-11-23  
**测试版本**: v1.0  
**维护者**: TradingAgents-CN Team
