# 债券数据迁移指南

## 数据表重新设计说明

根据 AKShare 债券接口文档，重新设计了债券数据表结构，以更好地匹配接口返回的字段。

## 数据清理步骤

### 方法1: 使用清理脚本

```bash
cd F:\source_code\TradingAgents-CN
python scripts/cleanup_bond_data.py
```

脚本会清理所有债券相关的数据表。

### 方法2: 手动清理（使用 MongoDB）

```javascript
// 连接到 MongoDB
use your_database_name

// 清理各个集合
db.bond_basic_info.deleteMany({})
db.bond_daily.deleteMany({})
db.yield_curve_daily.deleteMany({})
db.bond_spot_quotes.deleteMany({})
db.bond_info_cm.deleteMany({})
// ... 其他集合
```

### 方法3: 使用 Python 脚本

```python
from app.core.database import get_mongo_db
import asyncio

async def cleanup():
    db = get_mongo_db()
    collections = [
        "bond_basic_info",
        "bond_daily",
        "yield_curve_daily",
        # ... 其他集合
    ]
    for col_name in collections:
        col = db.get_collection(col_name)
        await col.delete_many({})
        print(f"Cleaned {col_name}")

asyncio.run(cleanup())
```

## 重新同步数据

清理完成后，运行以下同步任务重新获取数据：

1. **债券基础信息同步** - 获取所有债券的基础信息
2. **债券收益率曲线同步** - 获取收益率曲线数据
3. **中债信息详情同步** - 获取债券详细信息

这些任务会按照新的数据表结构保存数据。

## 主要改进

1. **字段映射更清晰** - 根据 AKShare 接口文档精确映射字段
2. **唯一键设计更合理** - 使用合适的组合键确保数据唯一性
3. **支持曲线名称** - 收益率曲线表支持多个曲线类型
4. **更好的错误处理** - 添加了详细的日志和错误处理
5. **数据验证** - 保存前验证数据格式和类型

## 注意事项

- 清理数据前请确保已备份（如果需要）
- 数据可以随时从 AKShare 重新获取
- 建议在非业务高峰期执行清理和同步操作

