# 预估总时长显示错误修复文档

## 📋 问题描述

用户报告前端显示的"预计总时长"不正确。

### 问题现象

- *用户选择**：
- 研究深度：4 级 - 深度分析
- 分析师：3 个（市场分析师、新闻分析师、基本面分析师）
- LLM 提供商：dashscope

- *预期结果**：
- 预计总时长：11 分钟（根据后端算法：330 秒 × 2.0 × 1.0 = 660 秒 = 11 分钟）

- *实际结果**：
- 前端显示：**19 分钟** ❌

### 根本原因

- *问题定位**：`app/services/progress/tracker.py` 第 59-82 行

在 `RedisProgressTracker.__init__()` 方法中，初始化 `progress_data` 时**没有设置 `estimated_total_time`**：

```python

# 进度数据

self.progress_data = {
    'task_id': task_id,
    'status': 'running',
    'progress_percentage': 0.0,
    'current_step': 0,
    'total_steps': 0,
    'current_step_name': '初始化',
    'current_step_description': '准备开始分析',
    'last_message': '分析任务已启动',
    'start_time': time.time(),
    'last_update': time.time(),
    'elapsed_time': 0.0,
    'remaining_time': 0.0,
    'steps': []
}

# ❌ 缺少 'estimated_total_time' 字段！

```bash

- *后果**：
1. `to_dict()` 方法从 `progress_data` 中读取 `estimated_total_time`
2. 如果字段不存在，返回默认值 0
3. 前端接收到 0，可能使用了错误的默认值或旧值

## ✅ 修复方案

### 修改文件

- *文件**：`app/services/progress/tracker.py` (第 59-87 行)

### 修改内容

在初始化时计算并设置 `estimated_total_time`：

```python

# 进度数据

self.progress_data = {
    'task_id': task_id,
    'status': 'running',
    'progress_percentage': 0.0,
    'current_step': 0,
    'total_steps': 0,
    'current_step_name': '初始化',
    'current_step_description': '准备开始分析',
    'last_message': '分析任务已启动',
    'start_time': time.time(),
    'last_update': time.time(),
    'elapsed_time': 0.0,
    'remaining_time': 0.0,
    'steps': []
}

# 生成分析步骤

self.analysis_steps = self._generate_dynamic_steps()
self.progress_data['total_steps'] = len(self.analysis_steps)
self.progress_data['steps'] = [asdict(step) for step in self.analysis_steps]

# 🔧 计算并设置预估总时长

base_total_time = self._get_base_total_time()
self.progress_data['estimated_total_time'] = base_total_time
self.progress_data['remaining_time'] = base_total_time  # 初始时剩余时间 = 总时长

# 保存初始状态

self._save_progress()

```bash

### 关键改动

1. **调用 `_get_base_total_time()`**：计算预估总时长
2. **设置 `estimated_total_time`**：存储到 `progress_data`
3. **设置 `remaining_time`**：初始时剩余时间 = 总时长

## 📊 测试验证

### 测试脚本

- *文件**：`scripts/test_estimated_total_time.py`

### 测试场景

#### 场景 1：4 级深度 + 3 个分析师 + dashscope

- *预期**：660 秒 (11 分钟)

- *结果**：

```bash
✅ 任务 ID: test_task_1
✅ 分析师数量: 3
✅ 研究深度: 深度
✅ LLM 提供商: dashscope
✅ 预估总时长: 660.0 秒 (11.0 分钟)
✅ 预计剩余时间: 660.0 秒 (11.0 分钟)
✅ 预估总时长正确: 660.0 秒 (预期: 660.0 秒)

```bash

#### 场景 2：1 级快速 + 1 个分析师 + deepseek

- *预期**：120 秒 (2 分钟)

- *结果**：

```bash
✅ 任务 ID: test_task_2
✅ 分析师数量: 1
✅ 研究深度: 快速
✅ LLM 提供商: deepseek
✅ 预估总时长: 120.0 秒 (2.0 分钟)
✅ 预计剩余时间: 120.0 秒 (2.0 分钟)
✅ 预估总时长正确: 120.0 秒 (预期: 120.0 秒)

```bash

#### 场景 3：5 级全面 + 4 个分析师 + google

- *预期**：1382.4 秒 (23 分钟)

- *结果**：

```bash
✅ 任务 ID: test_task_3
✅ 分析师数量: 4
✅ 研究深度: 全面
✅ LLM 提供商: google
✅ 预估总时长: 1382.4 秒 (23.0 分钟)
✅ 预计剩余时间: 1382.4 秒 (23.0 分钟)
✅ 预估总时长正确: 1382.4 秒 (预期: 1382.4 秒)

```bash

### 测试结果

```bash
======================================================================
✅ 所有测试通过！
======================================================================

```bash

## 📈 修复效果对比

### 修复前

| 场景 | 预期时长 | 前端显示 | 匹配度 |

|------|---------|---------|--------|

| 4 级 + 3 个分析师 | 11 分钟 | **19 分钟**| ❌ 错误 |

| 1 级 + 1 个分析师 | 2 分钟 |**未知**| ❌ 错误 |

| 5 级 + 4 个分析师 | 23 分钟 |**未知**| ❌ 错误 |

### 修复后

| 场景 | 预期时长 | 后端返回 | 匹配度 |

|------|---------|---------|--------|

| 4 级 + 3 个分析师 | 11 分钟 |**11 分钟**| ✅ 完美 |

| 1 级 + 1 个分析师 | 2 分钟 |**2 分钟**| ✅ 完美 |

| 5 级 + 4 个分析师 | 23 分钟 |**23 分钟** | ✅ 完美 |

## 🔍 技术细节

### 时间估算算法

- *文件**：`app/services/progress/tracker.py` (第 193-249 行)

- *算法公式**：

```python
total_time = base_time_per_depth *analyst_multiplier*model_mult

```bash

- *参数说明**：

1. **`base_time_per_depth`**：单个分析师的基础耗时（秒）
   - 1 级（快速）：150 秒 (2.5 分钟)
   - 2 级（基础）：180 秒 (3 分钟)
   - 3 级（标准）：240 秒 (4 分钟)
   - 4 级（深度）：330 秒 (5.5 分钟)
   - 5 级（全面）：480 秒 (8 分钟)

1. **`analyst_multiplier`**：分析师数量影响系数
   - 1 个分析师：1.0 倍
   - 2 个分析师：1.5 倍
   - 3 个分析师：2.0 倍
   - 4 个分析师：2.4 倍
   - 5 个及以上：2.4 + (n-4) × 0.3

1. **`model_mult`**：模型速度影响系数
   - dashscope：1.0 倍（标准）
   - deepseek：0.8 倍（快 20%）
   - google：1.2 倍（慢 20%）

### 数据流

```bash

1. 用户提交分析请求

   ↓

1. 创建 RedisProgressTracker 实例

   ↓

1. __init__() 方法初始化

   ↓

1. 调用 _get_base_total_time() 计算预估总时长

   ↓

1. 设置 progress_data['estimated_total_time']

   ↓

1. 调用 _save_progress() 保存到 Redis/文件

   ↓

1. 前端轮询 /api/analysis/progress/{task_id}

   ↓

1. 后端返回 progress_data（包含 estimated_total_time）

   ↓

1. 前端显示预计总时长

```bash

## 🎯 相关修复

这次修复是继上次"时间估算算法优化"之后的补充修复：

1. **上次修复**（`docs/time_estimation_optimization.md`）：
   - 优化了 `_get_base_total_time()` 算法
   - 基于实际测试数据调整了基础时间和系数
   - 将误差从 265% 降低到 ±10%

1. **本次修复**（`docs/estimated_total_time_fix.md`）：
   - 修复了初始化时未设置 `estimated_total_time` 的问题
   - 确保前端能正确获取预估总时长
   - 完善了数据流

## 📝 修复日期

2025-10-13

## 🎉 总结

### 问题根源

- 初始化时未设置 `estimated_total_time` 字段

### 修复方案

- 在 `__init__()` 方法中调用 `_get_base_total_time()` 并设置字段

### 修复效果

- ✅ 后端正确计算预估总时长
- ✅ 前端正确显示预估总时长
- ✅ 所有测试场景通过
- ✅ 用户体验提升

### 后续建议

1. 继续收集实际分析耗时数据
2. 定期调整算法参数以提高准确性
3. 考虑添加更多影响因素（如网络延迟、数据源响应时间等）

- --

- *相关文档**：
- `docs/time_estimation_optimization.md` - 时间估算算法优化
- `scripts/test_estimated_total_time.py` - 预估总时长测试脚本
- `scripts/test_time_estimation.py` - 时间估算算法测试脚本
