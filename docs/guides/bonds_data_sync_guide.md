# 债券数据同步完整指南

## 📋 概述

**文档目的**: 提供债券数据首次触发和定时下载的完整操作指南  
**适用场景**: 首次部署、数据初始化、定时任务配置、数据维护  
**数据来源**: AKShare  
**更新时间**: 2025-01-XX  
**版本**: v1.0

### 核心功能

TradingAgents-CN 提供了完整的债券数据同步系统，支持：

- ✅ **债券基础信息列表** - 代码、名称、类别、发行人、到期日等
- ✅ **收益率曲线** - 国债收益率曲线数据
- ✅ **历史行情数据** - 债券日线历史数据
- ✅ **现货快照** - 实时债券报价数据
- ✅ **债券指数** - 各类债券指数数据
- ✅ **可转债数据** - 可转债档案、事件、估值等
- ✅ **发行公告** - 债券发行相关信息
- ✅ **回购数据** - 债券回购历史记录

### 数据存储

所有债券数据存储在 MongoDB 数据库中，主要集合包括：

- `bond_basic_info` - 债券基础信息
- `bond_daily` - 债券日线数据
- `yield_curve_daily` - 收益率曲线数据
- `bond_spot_quotes` - 现货报价数据
- `bond_indices_daily` - 债券指数数据
- `bond_cb_profiles` - 可转债档案
- `bond_events` - 债券事件数据
- 以及其他相关集合

---

## 🚀 首次部署和初始化

### 前置条件

1. **环境准备**
   - MongoDB 数据库已启动并连接
   - Python 环境已安装（Python 3.8+）
   - AKShare 库已安装：`pip install akshare`
   - 应用已启动并运行

2. **配置检查**
   ```bash
   # 检查 .env 文件中的配置
   BONDS_SYNC_ENABLED=true
   TIMEZONE=Asia/Shanghai
   ```

### 方式一：通过 API 手动触发（推荐）

#### 1. 同步债券基础信息列表（必须首先执行）

这是最重要的步骤，因为其他数据同步可能依赖基础信息列表。

**使用 curl 命令：**
```bash
# 获取访问令牌（需要先登录）
TOKEN="your_access_token"

# 触发债券基础信息列表同步
curl -X POST "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/trigger" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

**使用 Python 脚本：**
```python
import requests

# 配置
API_BASE_URL = "http://localhost:8000"
TOKEN = "your_access_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 触发债券基础信息列表同步
response = requests.post(
    f"{API_BASE_URL}/api/scheduler/jobs/bonds_basic_list_sync/trigger",
    headers=headers
)

if response.status_code == 200:
    print("✅ 债券基础信息列表同步已触发")
    print(response.json())
else:
    print(f"❌ 触发失败: {response.status_code}")
    print(response.text)
```

**预期结果：**
- 同步成功后会返回类似：`{"success": true, "saved": 5000, "count": 5000}`
- 数据库中 `bond_basic_info` 集合会有数据

#### 2. 同步其他债券数据

基础信息同步完成后，可以按需同步其他数据：

```python
# 同步收益率曲线
requests.post(
    f"{API_BASE_URL}/api/scheduler/jobs/bonds_yield_curve_sync/trigger",
    headers=headers
)

# 同步债券指数
requests.post(
    f"{API_BASE_URL}/api/scheduler/jobs/bonds_indices_sync/trigger",
    headers=headers
)

# 同步可转债档案（可能需要较长时间）
requests.post(
    f"{API_BASE_URL}/api/scheduler/jobs/bonds_cb_profiles_sync/trigger",
    headers=headers
)
```

### 方式二：通过前端界面操作

1. **登录系统**
   - 访问前端地址（如：http://localhost:5173）
   - 使用管理员账号登录

2. **进入调度器管理页面**
   - 导航到：`系统管理` → `定时任务管理`
   - 或直接访问：`/scheduler`

3. **查找债券相关任务**
   - 在任务列表中查找以 `bonds_` 开头的任务
   - 找到 `bonds_basic_list_sync` 任务

4. **手动触发任务**
   - 点击任务右侧的 `触发` 按钮
   - 等待任务执行完成
   - 查看执行结果和日志

5. **查找债券基础信息同步任务**
   - 在任务列表中搜索：`债券基础信息` 或 `bonds_basic_list_sync`
   - 如果找不到，检查筛选条件：
     - 确保"状态"筛选器选择"全部状态"（不要只选"运行中"）
     - 确保"数据源"筛选器选择"全部数据源"或"AKShare"
   - 任务名称：`债券基础信息同步 - 代码、名称、类别等（AKShare）`
   - 任务ID：`bonds_basic_list_sync`

6. **按顺序触发其他任务**
   - 建议按以下顺序触发：
     1. `bonds_basic_list_sync` - 债券基础信息同步（必须）
     2. `bonds_yield_curve_sync` - 国债收益率曲线同步
     3. `bonds_indices_sync` - 债券指数同步
     4. `bonds_spot_sync` - 债券现货报价同步
     5. 其他任务按需触发

### 方式三：通过 Python 脚本直接调用

如果需要批量初始化或自定义逻辑，可以直接调用服务：

```python
import asyncio
from app.worker.bonds_sync_service import BondSyncService

async def init_bonds_data():
    """初始化债券数据"""
    svc = BondSyncService()
    
    # 确保索引已创建
    await svc.ensure_indexes()
    
    # 1. 同步基础信息列表
    print("🔄 同步债券基础信息列表...")
    result = await svc.sync_basic_list()
    print(f"✅ 完成: {result}")
    
    # 2. 同步收益率曲线
    print("🔄 同步收益率曲线...")
    result = await svc.sync_yield_curve()
    print(f"✅ 完成: {result}")
    
    # 3. 同步债券指数
    print("🔄 同步债券指数...")
    result = await svc.sync_indices()
    print(f"✅ 完成: {result}")
    
    # 4. 同步现货快照
    print("🔄 同步现货快照...")
    result = await svc.sync_spot_quotes()
    print(f"✅ 完成: {result}")

# 运行
if __name__ == "__main__":
    asyncio.run(init_bonds_data())
```

---

## ⏰ 定时任务配置

### 任务列表和默认时间

系统已配置以下定时任务，默认时间安排如下：

#### 每日任务（工作日）

| 任务名称 | 任务ID | 默认时间 | 说明 |
|---------|--------|---------|------|
| 债券基础信息列表同步 | `bonds_basic_list_sync` | 每日 01:00 | 同步所有债券基础信息 |
| 收益率曲线映射同步 | `bonds_curve_map_sync` | 工作日 18:05 | 同步收益率曲线映射 |
| 收益率曲线同步 | `bonds_yield_curve_sync` | 工作日 18:00 | 同步国债收益率曲线 |
| 债券现货快照同步 | `bonds_spot_sync` | 工作日 18:10 | 同步现货快照 |
| 债券指数同步 | `bonds_indices_sync` | 工作日 18:20 | 同步债券指数 |
| 美国国债收益率同步 | `bonds_us_yield_sync` | 工作日 18:30 | 同步美国国债收益率 |
| 债券历史日线同步 | `bonds_history_sync` | 工作日 18:30 | 同步历史日线（默认关闭） |
| 现货报价/成交明细同步 | `bonds_spot_detail_sync` | 工作日 18:40 | 同步报价和成交明细 |
| 上交所成交/资金摘要同步 | `bonds_sse_summary_sync` | 工作日 18:50 | 同步上交所摘要 |
| 可转债事件/估值同步 | `bonds_cb_events_sync` | 工作日 19:00 | 同步可转债事件和估值 |

#### 每周任务（周日）

| 任务名称 | 任务ID | 默认时间 | 说明 |
|---------|--------|---------|------|
| 债券发行公告同步 | `bonds_cninfo_issues_sync` | 周日 02:00 | 同步发行公告 |
| NAFMII银行间债务同步 | `bonds_nafmii_sync` | 周日 02:30 | 同步银行间债务 |
| 可转债档案同步 | `bonds_cb_profiles_sync` | 周日 03:00 | 同步可转债档案 |
| 中债信息cm同步 | `bonds_info_cm_sync` | 周日 03:30 | 同步中债信息 |
| 可转债列表同步 | `bonds_cb_lists_sync` | 周日 03:45 | 同步可转债列表 |
| 中债信息查询/详情同步 | `bonds_info_cm_queries_sync` | 周日 04:00 | 同步查询和详情 |
| 债券回购数据同步 | `bonds_buybacks_sync` | 周日 04:00 | 同步回购数据 |
| 回购历史同步 | `bonds_buybacks_hist_sync` | 周日 04:10 | 同步回购历史 |

### 配置方法

#### 方法一：通过环境变量配置（推荐）

在 `.env` 文件中添加或修改配置：

```bash
# 启用/禁用所有债券同步任务
BONDS_SYNC_ENABLED=true

# 债券基础信息列表同步
BONDS_BASIC_LIST_SYNC_ENABLED=true
BONDS_BASIC_LIST_SYNC_CRON="0 1 * * *"  # 每日 01:00

# 收益率曲线同步
BONDS_YIELD_CURVE_SYNC_CRON="0 18 * * 1-5"  # 工作日 18:00

# 债券指数同步
BONDS_INDICES_SYNC_ENABLED=true
BONDS_INDICES_SYNC_CRON="20 18 * * 1-5"  # 工作日 18:20

# 可转债档案同步（周度）
BONDS_CB_PROFILES_SYNC_ENABLED=true
BONDS_CB_PROFILES_SYNC_CRON="0 3 * * 0"  # 周日 03:00

# 其他任务配置...
```

#### 方法二：通过配置文件

在 `config/settings.json` 中配置（如果使用文件配置）：

```json
{
  "bonds_sync": {
    "enabled": true,
    "basic_list_sync": {
      "enabled": true,
      "cron": "0 1 * * *"
    },
    "yield_curve_sync": {
      "enabled": true,
      "cron": "0 18 * * 1-5"
    }
  }
}
```

#### CRON 表达式说明

CRON 表达式格式：`分 时 日 月 星期`

常用示例：

```bash
# 每日 01:00
"0 1 * * *"

# 工作日 18:00
"0 18 * * 1-5"

# 周日 03:00
"0 3 * * 0"

# 每5分钟（交易时间）
"*/5 9-15 * * 1-5"

# 每小时
"0 * * * *"

# 每周一 02:00
"0 2 * * 1"
```

### 启用/禁用任务

#### 禁用单个任务

```bash
# 在 .env 文件中
BONDS_HISTORY_SYNC_ENABLED=false  # 禁用历史数据同步
```

#### 禁用所有债券任务

```bash
# 在 .env 文件中
BONDS_SYNC_ENABLED=false  # 禁用所有债券同步任务
```

#### 通过前端界面

1. 进入 `系统管理` → `定时任务管理`
2. 找到对应的债券任务
3. 点击 `暂停` 按钮暂停任务
4. 点击 `恢复` 按钮恢复任务

---

## 🔍 监控和管理

### 查看任务状态

#### 通过 API

```bash
# 获取所有任务列表
curl -X GET "http://localhost:8000/api/scheduler/jobs" \
  -H "Authorization: Bearer $TOKEN"

# 获取特定任务详情
curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync" \
  -H "Authorization: Bearer $TOKEN"
```

#### 通过前端界面

1. 访问 `/scheduler` 页面
2. 查看任务列表，包括：
   - 任务名称和ID
   - 下次执行时间
   - 上次执行时间
   - 执行状态（运行中/等待/暂停）
   - 执行历史

### 查看执行历史

#### 通过 API

```bash
# 获取任务执行历史
curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/history?page=1&page_size=20" \
  -H "Authorization: Bearer $TOKEN"
```

#### 通过前端界面

1. 在任务列表中点击任务名称
2. 查看执行历史记录，包括：
   - 执行时间
   - 执行状态（成功/失败）
   - 执行耗时
   - 错误信息（如果有）

### 查看日志

#### 应用日志

```bash
# 查看应用日志
tail -f logs/tradingagents.log | grep -i bond

# 查看错误日志
tail -f logs/error.log | grep -i bond
```

#### 任务执行日志

任务执行日志会记录在 MongoDB 的 `scheduler_job_history` 集合中：

```python
from app.core.database import get_mongo_db

db = get_mongo_db()
history = await db.scheduler_job_history.find(
    {"job_id": "bonds_basic_list_sync"}
).sort("run_time", -1).limit(10).to_list(length=10)

for record in history:
    print(f"执行时间: {record['run_time']}")
    print(f"状态: {record['status']}")
    print(f"耗时: {record.get('duration', 0)}秒")
```

### 手动触发任务

#### 通过 API

```bash
# 触发任务执行
curl -X POST "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/trigger" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

#### 通过前端界面

1. 在任务列表中找到目标任务
2. 点击 `触发` 按钮
3. 等待执行完成
4. 查看执行结果

---

## 🛠️ 故障排查

### 常见问题

#### 1. 任务未执行

**症状**: 任务到了预定时间但没有执行

**排查步骤**:
1. 检查任务是否启用：
   ```bash
   # 检查配置
   echo $BONDS_SYNC_ENABLED
   echo $BONDS_BASIC_LIST_SYNC_ENABLED
   ```

2. 检查任务状态：
   ```bash
   # 通过 API 查看任务状态
   curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync" \
     -H "Authorization: Bearer $TOKEN"
   ```

3. 检查应用日志：
   ```bash
   tail -f logs/tradingagents.log | grep -i scheduler
   ```

**解决方案**:
- 确保 `BONDS_SYNC_ENABLED=true`
- 确保具体任务的 `*_ENABLED=true`
- 检查 CRON 表达式是否正确
- 重启应用使配置生效

#### 2. 数据同步失败

**症状**: 任务执行但返回错误

**排查步骤**:
1. 查看任务执行历史：
   ```bash
   # 查看最近的执行记录
   curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/history?page=1&page_size=5" \
     -H "Authorization: Bearer $TOKEN"
   ```

2. 检查错误日志：
   ```bash
   tail -f logs/error.log | grep -i bond
   ```

3. 检查网络连接：
   ```python
   # 测试 AKShare 连接
   import akshare as ak
   try:
       df = ak.bond_zh_hs_cov_spot()
       print(f"✅ AKShare 连接正常，获取到 {len(df)} 条数据")
   except Exception as e:
       print(f"❌ AKShare 连接失败: {e}")
   ```

**解决方案**:
- 检查网络连接
- 检查 AKShare 库版本：`pip install --upgrade akshare`
- 检查 MongoDB 连接
- 查看具体错误信息并针对性解决

#### 3. 数据不完整

**症状**: 同步成功但数据量少于预期

**排查步骤**:
1. 检查数据库中的数据量：
   ```python
   from app.core.database import get_mongo_db
   
   db = get_mongo_db()
   count = await db.bond_basic_info.count_documents({})
   print(f"债券基础信息数量: {count}")
   ```

2. 检查数据源：
   ```python
   import akshare as ak
   df = ak.bond_zh_hs_cov_spot()
   print(f"数据源返回数量: {len(df)}")
   ```

**解决方案**:
- 重新触发同步任务
- 检查数据源是否有更新
- 检查过滤条件是否正确

#### 4. 任务执行时间过长

**症状**: 任务执行时间超过预期

**排查步骤**:
1. 查看任务执行历史，检查耗时
2. 检查网络延迟
3. 检查数据库性能

**解决方案**:
- 调整任务执行时间，避开高峰期
- 优化数据库索引
- 考虑分批处理大量数据

### 调试技巧

#### 启用详细日志

在 `.env` 文件中：

```bash
LOG_LEVEL=DEBUG
```

#### 手动测试同步方法

```python
import asyncio
from app.worker.bonds_sync_service import BondSyncService

async def test_sync():
    svc = BondSyncService()
    await svc.ensure_indexes()
    
    # 测试基础信息列表同步
    result = await svc.sync_basic_list()
    print(f"同步结果: {result}")

asyncio.run(test_sync())
```

---

## 📊 最佳实践

### 首次部署建议

1. **按顺序执行**
   - 首先同步基础信息列表
   - 然后同步其他数据
   - 避免并发执行大量任务

2. **分批初始化**
   - 首次部署时，建议分批触发任务
   - 先同步基础数据，再同步历史数据
   - 历史数据同步可能需要较长时间

3. **监控执行**
   - 首次执行时密切关注日志
   - 检查数据是否正确写入数据库
   - 验证数据完整性

### 定时任务优化

1. **时间安排**
   - 工作日任务安排在交易结束后（18:00后）
   - 周末任务安排在凌晨（02:00-04:00）
   - 避免在交易时间执行大量同步任务

2. **任务优先级**
   - 基础信息列表：每日优先执行
   - 实时数据：交易结束后尽快同步
   - 历史数据：可以安排在非高峰时段

3. **资源管理**
   - 避免同时执行多个大数据量任务
   - 合理设置任务间隔时间
   - 监控系统资源使用情况

### 数据维护

1. **定期检查**
   - 每周检查任务执行情况
   - 每月检查数据完整性
   - 及时处理失败的任务

2. **数据备份**
   - 定期备份 MongoDB 数据库
   - 重要数据建议额外备份

3. **性能优化**
   - 定期检查数据库索引
   - 清理过期数据（如需要）
   - 优化查询性能

### 安全建议

1. **访问控制**
   - 确保 API 访问需要认证
   - 限制管理员权限
   - 定期更新访问令牌

2. **数据安全**
   - 定期备份数据
   - 保护数据库访问凭证
   - 监控异常访问

---

## 📚 相关文档

- [定时任务管理指南](./scheduler_management.md)
- [AKShare 统一方案文档](./akshare_unified/README.md)
- [数据库备份恢复指南](./DATABASE_BACKUP_RESTORE.md)
- [API 文档](../api/)

---

## ❓ 常见问题 FAQ

### Q1: 首次部署需要同步哪些数据？

**A**: 建议按以下顺序同步：
1. 债券基础信息列表（必须）
2. 收益率曲线
3. 债券指数
4. 现货快照
5. 其他数据按需同步

### Q2: 定时任务多久执行一次？

**A**: 
- 基础信息列表：每日一次
- 实时数据：工作日每日一次
- 历史数据：按需同步（默认关闭）
- 周度数据：每周日执行

### Q3: 如何修改任务执行时间？

**A**: 在 `.env` 文件中修改对应的 CRON 表达式，然后重启应用。

### Q4: 任务执行失败怎么办？

**A**: 
1. 查看任务执行历史，了解失败原因
2. 检查错误日志
3. 手动触发任务重试
4. 如持续失败，检查网络和数据库连接

### Q5: 数据同步需要多长时间？

**A**: 
- 基础信息列表：通常 1-5 分钟
- 收益率曲线：通常 1-3 分钟
- 可转债档案：可能需要 10-30 分钟（取决于数量）
- 历史数据：取决于数据量和时间范围

### Q6: 如何验证数据同步成功？

**A**: 
1. 查看任务执行历史，确认状态为"成功"
2. 检查数据库中的数据量
3. 通过前端界面查看债券数据
4. 对比数据源和数据库中的数据

### Q7: 为什么在定时任务列表中找不到债券基础信息同步任务？

**A**: 可能的原因和解决方法：

1. **任务被暂停了**
   - 检查前端筛选器：确保"状态"选择"全部状态"，不要只选"运行中"
   - 即使任务被暂停，也应该在列表中显示（状态为"已暂停"）

2. **配置未启用**
   - 检查 `.env` 文件：
     ```bash
     BONDS_SYNC_ENABLED=true
     BONDS_BASIC_LIST_SYNC_ENABLED=true
     ```
   - 如果配置为 `false`，任务会被暂停，但仍应在列表中显示

3. **搜索关键词不对**
   - 尝试搜索：`债券基础信息` 或 `bonds_basic_list_sync`
   - 任务名称：`债券基础信息同步 - 代码、名称、类别等（AKShare）`

4. **应用未重启**
   - 如果刚修改了配置，需要重启应用使配置生效

5. **通过API验证任务是否存在**
   ```bash
   # 获取所有任务列表
   curl -X GET "http://localhost:8000/api/scheduler/jobs" \
     -H "Authorization: Bearer YOUR_TOKEN" | grep -i "bonds_basic"
   ```

---

## 📞 技术支持

如遇到问题，请：

1. 查看本文档的故障排查部分
2. 检查应用日志和错误日志
3. 查看 GitHub Issues
4. 联系技术支持团队

---

**文档版本**: v1.0  
**最后更新**: 2025-01-XX  
**维护者**: TradingAgents-CN Team

