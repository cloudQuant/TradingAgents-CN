# 债券数据同步快速参考

## 🚀 快速开始

### 首次部署（3步完成）

```bash
# 1. 确保配置已启用
echo "BONDS_SYNC_ENABLED=true" >> .env

# 2. 重启应用
# (根据你的部署方式重启)

# 3. 触发基础信息列表同步（必须）
curl -X POST "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/trigger" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 通过前端操作

1. 登录系统 → `系统管理` → `定时任务管理`
2. **查找任务**：
   - 搜索关键词：`债券基础信息` 或 `bonds_basic_list_sync`
   - 任务名称：`债券基础信息同步 - 代码、名称、类别等（AKShare）`
   - **重要**：确保筛选器"状态"选择"全部状态"（不要只选"运行中"）
   - **重要**：确保筛选器"数据源"选择"全部数据源"或"AKShare"
3. 找到任务后，点击 `触发` 按钮
4. 等待执行完成

**如果找不到任务**：
- 检查筛选条件是否限制了显示
- 检查配置：`BONDS_SYNC_ENABLED=true` 和 `BONDS_BASIC_LIST_SYNC_ENABLED=true`
- 重启应用使配置生效

---

## ⏰ 定时任务时间表

### 每日任务（工作日 18:00-19:00）

| 时间 | 任务 | 说明 |
|------|------|------|
| 18:00 | 收益率曲线 | 同步国债收益率曲线 |
| 18:05 | 收益率曲线映射 | 同步收益率曲线映射 |
| 18:10 | 现货快照 | 同步债券现货报价 |
| 18:20 | 债券指数 | 同步债券指数数据 |
| 18:30 | 美国国债收益率 | 同步美国国债收益率 |
| 18:40 | 现货报价/成交明细 | 同步报价和成交数据 |
| 18:50 | 上交所摘要 | 同步上交所成交摘要 |
| 19:00 | 可转债事件/估值 | 同步可转债事件数据 |

### 每日任务（每日 01:00）

| 时间 | 任务 | 说明 |
|------|------|------|
| 01:00 | 基础信息列表 | 同步所有债券基础信息 |

### 每周任务（周日 02:00-04:10）

| 时间 | 任务 | 说明 |
|------|------|------|
| 02:00 | 发行公告 | 同步债券发行公告 |
| 02:30 | NAFMII | 同步银行间债务 |
| 03:00 | 可转债档案 | 同步可转债档案 |
| 03:30 | 中债信息 | 同步中债信息 |
| 03:45 | 可转债列表 | 同步可转债列表 |
| 04:00 | 回购数据 | 同步债券回购数据 |
| 04:00 | 中债查询/详情 | 同步查询和详情 |
| 04:10 | 回购历史 | 同步回购历史 |

---

## 🔧 常用命令

### 查看任务状态

```bash
# 获取所有任务
curl -X GET "http://localhost:8000/api/scheduler/jobs" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取特定任务
curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 手动触发任务

```bash
# 触发基础信息列表同步
curl -X POST "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/trigger" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 触发收益率曲线同步
curl -X POST "http://localhost:8000/api/scheduler/jobs/bonds_yield_curve_sync/trigger" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 查看执行历史

```bash
# 查看最近5次执行记录
curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/history?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ⚙️ 配置速查

### 环境变量配置

```bash
# 启用/禁用所有债券任务
BONDS_SYNC_ENABLED=true

# 基础信息列表同步
BONDS_BASIC_LIST_SYNC_ENABLED=true
BONDS_BASIC_LIST_SYNC_CRON="0 1 * * *"

# 收益率曲线同步
BONDS_YIELD_CURVE_SYNC_CRON="0 18 * * 1-5"

# 债券指数同步
BONDS_INDICES_SYNC_ENABLED=true
BONDS_INDICES_SYNC_CRON="20 18 * * 1-5"
```

### CRON 表达式速查

```
0 1 * * *        # 每日 01:00
0 18 * * 1-5     # 工作日 18:00
0 3 * * 0        # 周日 03:00
*/5 9-15 * * 1-5 # 交易时间每5分钟
```

---

## 🐛 故障排查速查

### 任务未执行

```bash
# 1. 检查配置
echo $BONDS_SYNC_ENABLED
echo $BONDS_BASIC_LIST_SYNC_ENABLED

# 2. 检查任务状态
curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. 查看日志
tail -f logs/tradingagents.log | grep -i bond
```

### 数据同步失败

```bash
# 1. 查看执行历史
curl -X GET "http://localhost:8000/api/scheduler/jobs/bonds_basic_list_sync/history?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 2. 查看错误日志
tail -f logs/error.log | grep -i bond

# 3. 测试 AKShare 连接
python -c "import akshare as ak; print(len(ak.bond_zh_hs_cov_spot()))"
```

---

## 📊 数据验证

### 检查数据量

```python
from app.core.database import get_mongo_db
import asyncio

async def check_data():
    db = get_mongo_db()
    
    # 检查基础信息数量
    basic_count = await db.bond_basic_info.count_documents({})
    print(f"债券基础信息: {basic_count} 条")
    
    # 检查收益率曲线数据
    curve_count = await db.yield_curve_daily.count_documents({})
    print(f"收益率曲线: {curve_count} 条")
    
    # 检查现货报价数据
    spot_count = await db.bond_spot_quotes.count_documents({})
    print(f"现货报价: {spot_count} 条")

asyncio.run(check_data())
```

---

## 📚 相关文档

- [完整指南](./bonds_data_sync_guide.md) - 详细操作文档
- [定时任务管理](./scheduler_management.md) - 任务管理说明
- [AKShare 统一方案](./akshare_unified/README.md) - 数据源说明

---

**快速参考版本**: v1.0  
**完整文档**: [bonds_data_sync_guide.md](./bonds_data_sync_guide.md)

