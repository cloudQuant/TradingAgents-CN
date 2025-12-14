# 云子量化 数据集合同步方案

> 目标：设计一套**应用层的数据集合同步系统**，支持任意两个节点之间的集合级别推送/拉取，覆盖局域网、服务器-本地、互联网等多种网络场景。实现的时候需要集成到数据集合的远程同步的界面中，更新这个远程同步的弹出的对话框；另外就是一个单独的界面，用于管理节点和同步任务。

---

## 一、设计理念

### 1.1 核心思想

**去中心化 + 集合粒度 + HTTP API 传输**

- **去中心化**：没有固定的主从关系，任意节点都可以作为数据源或目标
- **集合粒度**：以 MongoDB Collection 为同步单位，精确控制同步范围
- **HTTP API**：通过 REST API 传输数据，无需直接暴露 MongoDB 端口，更安全灵活

### 1.2 与传统方案对比

| 特性 | 传统方案 (Replica Set) | 本方案 (应用层同步) |
|------|----------------------|-------------------|
| 同步粒度 | 整库 | 集合级别 |
| 网络要求 | MongoDB 端口互通 | HTTP 端口即可 |
| 方向控制 | 单向 (Primary→Secondary) | 双向 (Push/Pull) |
| 节点关系 | 固定主从 | 对等节点 |
| 安全性 | 需要暴露 MongoDB | 仅暴露 HTTP API |
| 部署复杂度 | 高 (副本集配置) | 低 (启动 API 服务即可) |

---

## 二、系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        节点 A (本地)                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  MongoDB    │◄───│ Sync Service│◄───│  HTTP API   │◄────────┤
│  │  (Local)    │    │             │    │  /sync/*    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTP (Push/Pull)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        节点 B (服务器)                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  MongoDB    │◄───│ Sync Service│◄───│  HTTP API   │◄────────┤
│  │  (Remote)   │    │             │    │  /sync/*    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件

1. **SyncNode（同步节点）**：代表一个可同步的端点，包含地址、认证信息
2. **SyncService（同步服务）**：执行实际的推送/拉取逻辑
3. **SyncAPI（同步接口）**：提供 HTTP 端点供远程调用
4. **SyncConfig（同步配置）**：管理节点列表和同步策略

---

## 三、数据模型

### 3.1 同步节点配置

```python
# 存储在 MongoDB: sync_nodes 集合
{
    "_id": ObjectId,
    "node_id": "server_main",           # 节点唯一标识
    "name": "主服务器",                   # 显示名称
    "url": "https://server.example.com", # 节点 API 地址
    "api_key": "encrypted_key",          # 认证密钥（加密存储）
    "description": "生产环境主服务器",
    "tags": ["production", "primary"],   # 标签，便于分组
    "status": "active",                  # active/inactive
    "last_sync_at": datetime,            # 上次同步时间
    "created_at": datetime,
    "updated_at": datetime
}
```

### 3.2 同步任务记录

```python
# 存储在 MongoDB: sync_tasks 集合
{
    "_id": ObjectId,
    "task_id": "uuid",
    "direction": "push",                 # push/pull
    "source_node": "local",              # 源节点
    "target_node": "server_main",        # 目标节点
    "collection": "stock_daily_kline",   # 同步的集合
    "filter": {"trade_date": {"$gte": "2024-01-01"}},  # 可选过滤条件
    "status": "completed",               # pending/running/completed/failed
    "stats": {
        "total_records": 10000,
        "transferred": 10000,
        "inserted": 5000,
        "updated": 5000,
        "failed": 0
    },
    "started_at": datetime,
    "completed_at": datetime,
    "error_message": null
}
```

### 3.3 集合元数据

```python
# 存储在 MongoDB: sync_collection_meta 集合
{
    "_id": ObjectId,
    "collection": "stock_daily_kline",
    "unique_keys": ["ts_code", "trade_date"],  # 用于 upsert 的唯一键
    "sync_strategy": "incremental",            # full/incremental
    "incremental_field": "trade_date",         # 增量同步字段
    "chunk_size": 5000,                        # 每批传输数量
    "description": "股票日线行情"
}
```

---

## 四、API 设计

### 4.1 节点管理 API

```yaml
# 节点列表
GET /api/sync/nodes
Response: { nodes: [...], total: N }

# 添加节点
POST /api/sync/nodes
Body: { node_id, name, url, api_key, description, tags }

# 测试节点连接
POST /api/sync/nodes/{node_id}/test
Response: { success: true, latency_ms: 50, version: "1.0.0" }

# 删除节点
DELETE /api/sync/nodes/{node_id}
```

### 4.2 同步操作 API

```yaml
# 拉取数据 (从远程节点获取数据到本地)
POST /api/sync/pull
Body: {
    "source_node": "server_main",
    "collection": "stock_daily_kline",
    "filter": {"trade_date": {"$gte": "2024-01-01"}},  # 可选
    "strategy": "incremental"  # full/incremental
}
Response: { task_id: "uuid", status: "started" }

# 推送数据 (将本地数据发送到远程节点)
POST /api/sync/push
Body: {
    "target_node": "server_main",
    "collection": "stock_daily_kline",
    "filter": {"trade_date": {"$gte": "2024-01-01"}},  # 可选
    "strategy": "incremental"
}
Response: { task_id: "uuid", status: "started" }

# 查询同步任务状态
GET /api/sync/tasks/{task_id}
Response: { task_id, status, stats, ... }

# 取消同步任务
POST /api/sync/tasks/{task_id}/cancel
```

### 4.3 数据传输 API（节点间调用）

```yaml
# 获取集合数据（供远程节点拉取）
POST /api/sync/data/export
Headers: { X-Sync-API-Key: "api_key" }
Body: {
    "collection": "stock_daily_kline",
    "filter": {...},
    "skip": 0,
    "limit": 5000
}
Response: {
    "data": [...],           # 数据数组
    "total": 100000,         # 总记录数
    "has_more": true,        # 是否还有更多
    "checksum": "md5hash"    # 数据校验
}

# 接收集合数据（供远程节点推送）
POST /api/sync/data/import
Headers: { X-Sync-API-Key: "api_key" }
Body: {
    "collection": "stock_daily_kline",
    "data": [...],
    "unique_keys": ["ts_code", "trade_date"],
    "mode": "upsert"  # upsert/insert/replace
}
Response: { inserted: N, updated: M, failed: K }

# 获取集合统计信息
POST /api/sync/data/stats
Headers: { X-Sync-API-Key: "api_key" }
Body: { "collection": "stock_daily_kline" }
Response: {
    "count": 100000,
    "latest_date": "2024-12-01",
    "oldest_date": "2020-01-01"
}
```

---

## 五、同步策略

### 5.1 全量同步 (Full Sync)

适用场景：首次同步、数据重建

```
1. 清空目标集合（可选）
2. 分批读取源集合全部数据
3. 批量 upsert 到目标集合
4. 验证数据一致性
```

### 5.2 增量同步 (Incremental Sync)

适用场景：日常更新

```
1. 获取目标集合的最新时间戳
2. 从源集合读取该时间戳之后的数据
3. 批量 upsert 到目标集合
```

### 5.3 差异同步 (Diff Sync)

适用场景：不确定哪边更新

```
1. 对比源和目标的记录数量、最新时间
2. 计算差异记录
3. 双向传输差异数据
```

### 5.4 冲突处理策略

```python
conflict_strategies = {
    "source_wins": "源数据覆盖目标",
    "target_wins": "保留目标数据",
    "newer_wins": "根据 updated_at 字段决定",
    "manual": "记录冲突，人工处理"
}
```

---

## 六、安全设计

### 6.1 认证机制

```python
# API Key 认证
# 每个节点配置唯一的 API Key
# 请求时通过 Header 传递: X-Sync-API-Key

# 可选: JWT Token 认证
# 支持更细粒度的权限控制
```

### 6.2 传输安全

- **HTTPS**：生产环境必须使用 HTTPS
- **数据压缩**：大批量数据传输时使用 gzip 压缩
- **校验和**：每批数据附带 checksum 验证完整性

### 6.3 权限控制

```python
# 节点权限配置
{
    "node_id": "readonly_node",
    "permissions": {
        "export": ["stock_*", "fund_*"],  # 允许导出的集合
        "import": []                       # 不允许导入
    }
}
```

---

## 七、使用场景示例

### 7.1 服务器 → 本地（Pull）

```bash
# 场景：从服务器拉取最新的股票日线数据到本地

POST /api/sync/pull
{
    "source_node": "production_server",
    "collection": "stock_daily_kline",
    "strategy": "incremental"
}

# 系统自动：
# 1. 查询本地最新日期: 2024-11-30
# 2. 从服务器拉取 2024-12-01 之后的数据
# 3. Upsert 到本地 MongoDB
```

### 7.2 本地 → 服务器（Push）

```bash
# 场景：将本地整理好的基金数据推送到服务器

POST /api/sync/push
{
    "target_node": "production_server",
    "collection": "fund_basic_info",
    "strategy": "full"
}
```

### 7.3 多节点同步

```bash
# 场景：将服务器 A 的数据同步到服务器 B 和本地

# Step 1: 本地从服务器 A 拉取
POST /api/sync/pull
{ "source_node": "server_a", "collection": "stock_info" }

# Step 2: 本地推送到服务器 B
POST /api/sync/push
{ "target_node": "server_b", "collection": "stock_info" }
```

### 7.4 互联网同步（NAT 穿透场景）

```bash
# 场景：家里的电脑无公网 IP，但想和云服务器同步

# 方案 1: 通过云服务器中转
# - 本地主动连接云服务器
# - 使用 Push 上传数据
# - 使用 Pull 下载数据

# 方案 2: 使用 FRP/Ngrok 等内网穿透工具
# - 将本地 API 服务暴露到公网
# - 云服务器可以主动连接本地
```

---

## 八、前端界面设计

### 8.1 节点管理页面

```
┌─────────────────────────────────────────────────────────────┐
│ 同步节点管理                                    [+ 添加节点] │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 🟢 主服务器 (server_main)                               │ │
│ │    URL: https://api.example.com                         │ │
│ │    上次同步: 2024-12-01 10:30:00                        │ │
│ │    [测试连接] [编辑] [删除]                              │ │
│ └─────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 🟡 备份服务器 (server_backup)                           │ │
│ │    URL: https://backup.example.com                      │ │
│ │    状态: 连接超时                                        │ │
│ │    [测试连接] [编辑] [删除]                              │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 同步操作页面

```
┌─────────────────────────────────────────────────────────────┐
│ 数据同步                                                    │
├─────────────────────────────────────────────────────────────┤
│ 选择集合: [stock_daily_kline        ▼]                     │
│                                                             │
│ ┌─────────────────────┐    ┌─────────────────────┐         │
│ │ 📥 从远程拉取 (Pull) │    │ 📤 推送到远程 (Push) │         │
│ ├─────────────────────┤    ├─────────────────────┤         │
│ │ 源节点:             │    │ 目标节点:            │         │
│ │ [主服务器      ▼]   │    │ [主服务器      ▼]   │         │
│ │                     │    │                     │         │
│ │ 同步策略:           │    │ 同步策略:           │         │
│ │ ○ 全量同步          │    │ ○ 全量同步          │         │
│ │ ● 增量同步          │    │ ● 增量同步          │         │
│ │                     │    │                     │         │
│ │ [开始拉取]          │    │ [开始推送]          │         │
│ └─────────────────────┘    └─────────────────────┘         │
│                                                             │
│ ─────────────────── 同步进度 ────────────────────          │
│ 任务ID: abc123                                              │
│ 状态: 进行中                                                │
│ 进度: [████████░░░░░░░░] 50% (5000/10000)                  │
│ 已插入: 3000 | 已更新: 2000 | 失败: 0                       │
└─────────────────────────────────────────────────────────────┘
```

### 8.3 同步历史页面

```
┌─────────────────────────────────────────────────────────────┐
│ 同步历史                                      [导出记录]    │
├─────────────────────────────────────────────────────────────┤
│ 时间             方向   集合              节点       状态   │
│ ─────────────────────────────────────────────────────────── │
│ 12-01 10:30:00   Pull   stock_daily_kline 主服务器   ✅     │
│ 12-01 09:00:00   Push   fund_basic_info   备份服务器 ✅     │
│ 11-30 18:00:00   Pull   bond_info         主服务器   ❌     │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 九、实现路线图

### Phase 1: 基础框架（1-2 天）

- [ ] 定义数据模型（SyncNode, SyncTask, CollectionMeta）
- [ ] 实现 SyncService 基础类
- [ ] 实现节点管理 API
- [ ] 实现节点连接测试

### Phase 2: 核心同步功能（2-3 天）

- [ ] 实现数据导出 API（export）
- [ ] 实现数据导入 API（import）
- [ ] 实现 Pull 同步流程
- [ ] 实现 Push 同步流程
- [ ] 实现增量同步逻辑

### Phase 3: 前端界面（2 天）

- [ ] 节点管理页面
- [ ] 同步操作页面
- [ ] 同步历史页面
- [ ] 实时进度展示

### Phase 4: 增强功能（可选）

- [ ] 批量同步多个集合
- [ ] 定时同步任务
- [ ] 同步模板（预设常用同步配置）
- [ ] 数据压缩传输
- [ ] 断点续传

---

## 十、配置示例

### 10.1 环境变量

```bash
# .env
SYNC_API_KEY=your_secret_api_key_here
SYNC_ENABLED=true
SYNC_MAX_CHUNK_SIZE=5000
SYNC_TIMEOUT_SECONDS=300
```

### 10.2 集合同步配置

```python
# 在代码中定义各集合的同步元数据
SYNC_COLLECTION_CONFIG = {
    "stock_daily_kline": {
        "unique_keys": ["ts_code", "trade_date"],
        "incremental_field": "trade_date",
        "chunk_size": 5000
    },
    "fund_basic_info": {
        "unique_keys": ["fund_code"],
        "incremental_field": None,  # 全量同步
        "chunk_size": 1000
    },
    "stock_info": {
        "unique_keys": ["ts_code"],
        "incremental_field": "list_date",
        "chunk_size": 2000
    }
}
```

---

## 十一、与现有系统集成

本方案与现有的 Collection 管理系统完全兼容：

1. **共享数据模型**：使用相同的 MongoDB 集合
2. **共享唯一键配置**：复用现有的 `unique_keys` 定义
3. **UI 集成**：在现有 Collection 页面添加"同步"标签页
4. **权限复用**：复用现有的认证系统

```vue
<!-- Collection.vue 中添加同步标签 -->
<el-tabs>
  <el-tab-pane label="数据管理">...</el-tab-pane>
  <el-tab-pane label="数据同步">
    <SyncPanel :collection="currentCollection" />
  </el-tab-pane>
</el-tabs>
