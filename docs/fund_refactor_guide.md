# 基金数据模块重构指南

## 重构概述

本次重构将基金数据处理代码从单一的大文件拆分为模块化的provider和service结构，参考了stocks目录的实现方式。

## 重构内容

### 1. 新增目录结构

```
app/services/data_sources/funds/
├── providers/          # 31个provider文件
│   ├── __init__.py
│   ├── fund_name_em_provider.py
│   ├── fund_etf_spot_em_provider.py
│   └── ...
├── services/           # 31个service文件
│   ├── __init__.py
│   ├── fund_name_em_service.py
│   ├── fund_etf_spot_em_service.py
│   └── ...
└── README.md
```

### 2. 新增服务文件

- `app/services/fund_refresh_service_v2.py`: 重构后的刷新服务
- `app/services/fund_data_service_v2.py`: 重构后的通用数据服务

### 3. 保留的旧文件

- `app/services/fund_refresh_service.py`: 保留（向后兼容）
- `app/services/fund_data_service.py`: 保留（向后兼容）

## 使用方式

### 方式一：使用新的V2服务（推荐）

```python
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2

# 初始化
service = FundRefreshServiceV2(db)

# 刷新数据
result = await service.refresh_collection(
    collection_name="fund_name_em",
    task_id="task_001",
    params={}
)
```

### 方式二：直接使用具体的Service

```python
from app.services.data_sources.funds.services.fund_name_em_service import FundNameEmService

# 初始化
service = FundNameEmService(db)

# 刷新数据
result = await service.refresh_data()

# 查询数据
data = await service.get_data(skip=0, limit=100)
```

### 方式三：继续使用旧服务（向后兼容）

```python
from app.services.fund_refresh_service import FundRefreshService

# 旧代码继续可用
service = FundRefreshService(db)
await service._refresh_fund_name_em(task_id, params)
```

## 路由更新建议

### 当前路由（funds.py）

可以选择以下两种更新方式：

#### 选项1：渐进式迁移（推荐）

在`funds.py`中同时支持新旧两种服务：

```python
# 导入新服务
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2
from app.services.fund_data_service_v2 import FundDataServiceV2

# 导入旧服务（向后兼容）
from app.services.fund_refresh_service import FundRefreshService
from app.services.fund_data_service import FundDataService

# 使用环境变量控制使用哪个版本
import os
USE_V2 = os.getenv("USE_FUND_SERVICE_V2", "false").lower() == "true"

if USE_V2:
    refresh_service_class = FundRefreshServiceV2
    data_service_class = FundDataServiceV2
else:
    refresh_service_class = FundRefreshService
    data_service_class = FundDataService
```

#### 选项2：直接替换

直接使用新服务替换旧服务：

```python
# 只导入新服务
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2
from app.services.fund_data_service_v2 import FundDataServiceV2

# 在端点中使用
@router.post("/refresh/{collection_name}")
async def refresh_fund_data(collection_name: str, ...):
    service = FundRefreshServiceV2(db)
    result = await service.refresh_collection(collection_name, task_id, params)
    return result
```

## 主要变更点

### FundRefreshService -> FundRefreshServiceV2

| 旧方法 | 新方法 | 说明 |
|--------|--------|------|
| `_refresh_fund_name_em(task_id, params)` | `refresh_collection("fund_name_em", task_id, params)` | 统一接口 |
| `_refresh_fund_etf_spot(task_id, params)` | `refresh_collection("fund_etf_spot_em", task_id, params)` | 统一接口 |
| ... | ... | 所有`_refresh_*`方法都改为统一的`refresh_collection` |

### FundDataService -> FundDataServiceV2

| 旧方法 | 新方法 | 说明 |
|--------|--------|------|
| `save_fund_name_em_data(df, callback)` | 使用Service.refresh_data() | Provider自动调用 |
| `get_fund_name_em_stats()` | 使用Service.get_overview() | 标准化接口 |
| `clear_fund_name_em_data()` | 使用Service.clear_data() | 标准化接口 |
| `import_data_from_file(...)` | 保留在V2中 | 通用功能保留 |
| `sync_data_from_remote(...)` | 保留在V2中 | 通用功能保留 |

## 迁移步骤

### 步骤1：测试新服务

```bash
# 运行测试脚本
python tests/test_fund_services_v2.py
```

### 步骤2：更新环境变量（可选）

如果使用渐进式迁移，设置环境变量：

```bash
# .env 文件
USE_FUND_SERVICE_V2=true
```

### 步骤3：更新路由代码

根据选择的迁移方式更新`app/routers/funds.py`

### 步骤4：测试API端点

使用Postman或其他工具测试所有涉及的API端点

### 步骤5：监控和回滚

- 监控生产环境日志
- 如有问题，可通过环境变量快速回滚到旧版本

## 优势对比

### 新架构优势

1. **模块化**：每个数据集合独立管理
2. **可扩展**：添加新数据源无需修改大文件
3. **可测试**：每个模块可独立测试
4. **代码重用**：Provider和Service分离，可灵活组合
5. **统一接口**：所有Service都有相同的方法签名

### 兼容性

- ✅ 保留旧服务文件，向后兼容
- ✅ 新旧服务可并行运行
- ✅ 可通过配置切换新旧版本
- ✅ 数据库结构无变化

## 注意事项

1. **数据库集合名称**：新服务使用`db.funds.{collection_name}`，与旧服务一致
2. **字段一致性**：Provider添加的`scraped_at`字段与旧服务一致
3. **错误处理**：新服务保持与旧服务相同的错误处理逻辑
4. **性能**：新服务使用相同的异步模式，性能无差异

## 后续工作

1. ✅ 创建31个provider和service文件
2. ✅ 创建FundRefreshServiceV2和FundDataServiceV2
3. ⏳ 更新funds.py路由（可选，向后兼容）
4. ⏳ 添加更多单元测试
5. ⏳ 更新API文档

## 相关文件

- Provider和Service：`app/services/data_sources/funds/`
- 新刷新服务：`app/services/fund_refresh_service_v2.py`
- 新数据服务：`app/services/fund_data_service_v2.py`
- 测试脚本：`tests/test_fund_services_v2.py`
- 模块说明：`app/services/data_sources/funds/README.md`
- 迁移指南：`docs/fund_refactor_guide.md`（本文件）

## 技术支持

如有问题，请参考：
- `app/services/data_sources/stocks/` - stocks的实现示例
- `app/services/data_sources/funds/README.md` - 详细使用说明
