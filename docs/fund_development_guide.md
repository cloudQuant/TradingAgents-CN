# 基金数据集合开发流程指南

## 📋 目录

1. [概述](#概述)
2. [架构说明](#架构说明)
3. [新增数据集合完整流程](#新增数据集合完整流程)
4. [详细步骤说明](#详细步骤说明)
5. [代码示例](#代码示例)
6. [最佳实践](#最佳实践)
7. [常见问题](#常见问题)
8. [测试验证](#测试验证)

---

## 概述

本文档详细说明如何在基金模块中新增一个数据集合。基金模块采用 **Provider-Service** 架构，实现了数据获取与业务逻辑的分离，支持自动注册、类型安全、统一错误处理等功能。

### 核心概念

- **Provider（数据提供者）**: 负责从数据源（如 akshare）获取原始数据，进行数据清洗和转换
- **Service（数据服务）**: 负责数据存储、批量更新、增量判断等业务逻辑
- **Collection（数据集合）**: MongoDB 中的一个集合，存储特定类型的数据

---

## 架构说明

### 目录结构

```
app/services/data_sources/funds/
├── providers/              # 数据提供者目录
│   ├── fund_name_em_provider.py
│   ├── fund_basic_info_provider.py
│   └── ...
├── services/               # 数据服务目录
│   ├── fund_basic_info_service.py
│   ├── fund_etf_spot_em_service.py
│   └── ...
├── collection_metadata.py  # 集合元信息（显示名称、描述、路由等）
├── provider_registry.py     # Provider 自动注册机制
└── README.md

app/config/
└── fund_update_config.py   # 更新参数配置（前端表单配置）

frontend/src/
├── views/Funds/collections/  # 前端页面组件
│   ├── index.vue            # 动态路由入口
│   ├── DefaultCollection.vue # 默认集合页面
│   └── [CollectionName].vue # 特定集合页面（可选）
└── types/funds.ts           # TypeScript 类型定义
```

### 数据流

```
用户请求 → API Router → Service → Provider → akshare → 数据清洗 → MongoDB
                ↓
           前端页面 ← API Response ← MongoDB
```

### 自动注册机制

系统会自动扫描 `providers/` 目录下的所有 Provider 类，并注册到系统中。你只需要：

1. 创建 Provider 文件
2. 创建 Service 文件
3. 添加元信息配置
4. 添加更新参数配置

系统会自动识别并注册，无需手动导入。

---

## 新增数据集合完整流程

### 流程图

```
1. 确定数据源和接口
   ↓
2. 创建 Provider 类
   ↓
3. 创建 Service 类
   ↓
4. 添加集合元信息
   ↓
5. 配置更新参数
   ↓
6. （可选）创建前端组件
   ↓
7. 测试验证
```

### 快速检查清单

- [ ] Provider 类已创建并继承正确的基类
- [ ] Service 类已创建并配置 provider_class
- [ ] collection_metadata.py 中添加了元信息
- [ ] fund_update_config.py 中配置了更新参数
- [ ] 测试了单条更新功能
- [ ] 测试了批量更新功能
- [ ] 前端页面可以正常显示数据

---

## 详细步骤说明

### 步骤 1: 确定数据源和接口

#### 1.1 查找 akshare 接口

首先确定要使用的 akshare 接口。例如：

```python
import akshare as ak

# 查看接口文档
help(ak.fund_name_em)

# 测试接口
df = ak.fund_name_em()
print(df.head())
```

#### 1.2 分析接口参数

确定接口需要哪些参数：

- **无参数接口**: 如 `fund_name_em()` - 直接调用
- **单参数接口**: 如 `fund_basic_info_xq(symbol="000001")` - 需要基金代码
- **多参数接口**: 如 `fund_portfolio_hold_em(symbol="000001", date="20231231")` - 需要基金代码和日期

#### 1.3 确定唯一键

分析返回数据的唯一标识字段，用于去重和增量更新：

- 单字段唯一: `["基金代码"]`
- 多字段组合唯一: `["基金代码", "净值日期"]`
- 多字段组合唯一: `["基金代码", "股票代码", "季度"]`

---

### 步骤 2: 创建 Provider 类

#### 2.1 选择基类

根据接口特点选择合适的基类：

- **SimpleProvider**: 无参数接口，直接调用 akshare 函数
- **BaseProvider**: 需要参数的接口，支持参数映射、数据转换等

#### 2.2 创建 Provider 文件

在 `app/services/data_sources/funds/providers/` 目录下创建文件：

**文件命名规范**: `{collection_name}_provider.py`

例如: `fund_new_example_provider.py`

#### 2.3 编写 Provider 代码

**示例 1: 无参数接口（使用 SimpleProvider）**

```python
"""
新基金示例-数据提供者
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundNewExampleProvider(SimpleProvider):
    """新基金示例-数据提供者"""
    
    # 集合名称（必须，用于 MongoDB 集合名）
    collection_name = "fund_new_example"
    
    # 显示名称（前端显示）
    display_name = "新基金示例"
    
    # akshare 函数名（必须）
    akshare_func = "fund_name_em"  # 替换为实际的 akshare 函数名
    
    # 唯一键（用于去重）
    unique_keys = ["基金代码"]
    
    # 集合描述（可选，会显示在前端）
    collection_description = "新基金示例数据，包括基金代码、名称等信息"
    
    # 路由路径（可选，默认 /funds/collections/{collection_name}）
    collection_route = "/funds/collections/fund_new_example"
    
    # 排序顺序（可选，默认 100）
    collection_order = 100
    
    # 字段信息（可选，用于前端显示字段说明）
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金唯一标识"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "基金类型", "type": "string", "description": "基金类型"},
    ]
```

**示例 2: 单参数接口（使用 BaseProvider）**

```python
"""
基金详情示例-数据提供者（需要基金代码参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundDetailExampleProvider(BaseProvider):
    """基金详情示例-数据提供者"""
    
    collection_name = "fund_detail_example"
    display_name = "基金详情示例"
    akshare_func = "fund_individual_basic_info_xq"  # 替换为实际的函数名
    unique_keys = ["基金代码"]
    
    collection_description = "基金详细信息，包括成立时间、规模、基金经理等"
    collection_route = "/funds/collections/fund_detail_example"
    collection_order = 101
    
    # 参数映射：将前端传入的参数映射到 akshare 函数参数
    param_mapping = {
        "fund_code": "symbol",  # 前端传 fund_code，映射到 akshare 的 symbol
        "symbol": "symbol",     # 也支持直接传 symbol
        "code": "symbol",       # 也支持直接传 code
    }
    
    # 必填参数
    required_params = ["symbol"]
    
    # 自动添加参数列：将参数值写入数据中的指定列
    add_param_columns = {
        "symbol": "基金代码",  # 将 symbol 参数值写入 "基金代码" 列
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金唯一标识"},
        {"name": "基金名称", "type": "string", "description": "基金全称"},
        {"name": "成立日期", "type": "date", "description": "基金成立日期"},
    ]
```

**示例 3: 多参数接口（使用 BaseProvider）**

```python
"""
基金持仓示例-数据提供者（需要基金代码和日期参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundHoldExampleProvider(BaseProvider):
    """基金持仓示例-数据提供者"""
    
    collection_name = "fund_hold_example"
    display_name = "基金持仓示例"
    akshare_func = "fund_portfolio_hold_em"  # 替换为实际的函数名
    unique_keys = ["基金代码", "股票代码", "季度"]  # 多字段组合唯一
    
    collection_description = "基金持仓股票信息，包括股票代码、持仓比例等"
    collection_route = "/funds/collections/fund_hold_example"
    collection_order = 102
    
    # 参数映射
    param_mapping = {
        "fund_code": "symbol",
        "symbol": "symbol",
        "code": "symbol",
        "date": "date",        # 日期参数，格式：YYYYMMDD
        "year": "date",        # 也支持传年份，会自动转换为日期
    }
    
    # 必填参数
    required_params = ["symbol", "date"]
    
    # 自动添加参数列
    add_param_columns = {
        "symbol": "基金代码",
        "date": "季度",  # 将日期参数写入 "季度" 列
    }
    
    # 数据转换（可选）：在保存前对数据进行处理
    def transform_data(self, df, params=None):
        """
        数据转换
        
        Args:
            df: pandas DataFrame
            params: 调用参数
            
        Returns:
            转换后的 DataFrame
        """
        if df is None or df.empty:
            return df
        
        # 示例：添加计算列
        if "持仓市值" in df.columns and "持仓数量" in df.columns:
            df["持仓比例"] = df["持仓市值"] / df["持仓市值"].sum() * 100
        
        return df
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金唯一标识"},
        {"name": "股票代码", "type": "string", "description": "持仓股票代码"},
        {"name": "季度", "type": "string", "description": "数据所属季度"},
        {"name": "持仓比例", "type": "float", "description": "持仓占比"},
    ]
```

#### 2.4 Provider 类属性说明

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collection_name` | str | ✅ | 集合名称，用于 MongoDB 集合名 |
| `akshare_func` | str | ✅ | akshare 函数名 |
| `unique_keys` | List[str] | ✅ | 唯一键列表，用于去重 |
| `display_name` | str | ❌ | 显示名称，默认从 metadata 读取 |
| `collection_description` | str | ❌ | 集合描述 |
| `collection_route` | str | ❌ | 路由路径 |
| `collection_order` | int | ❌ | 排序顺序，默认 100 |
| `param_mapping` | Dict[str, str] | ❌ | 参数映射字典 |
| `required_params` | List[str] | ❌ | 必填参数列表 |
| `add_param_columns` | Dict[str, str] | ❌ | 自动添加参数列 |
| `field_info` | List[Dict] | ❌ | 字段信息列表 |

---

### 步骤 3: 创建 Service 类

#### 3.1 创建 Service 文件

在 `app/services/data_sources/funds/services/` 目录下创建文件：

**文件命名规范**: `{collection_name}_service.py`

例如: `fund_new_example_service.py`

#### 3.2 编写 Service 代码

**示例 1: 简单 Service（无批量更新）**

```python
"""
新基金示例-数据服务
"""
from app.services.data_sources.base_service import BaseService
from ..providers.fund_new_example_provider import FundNewExampleProvider


class FundNewExampleService(BaseService):
    """新基金示例-数据服务"""
    
    # 集合名称（必须）
    collection_name = "fund_new_example"
    
    # Provider 类（必须）
    provider_class = FundNewExampleProvider
    
    # 并发控制（可选）
    batch_concurrency = 3  # 批量更新时的并发数
    
    # 进度更新间隔（可选）
    batch_progress_interval = 10  # 每处理 10 条更新一次进度
```

**示例 2: 需要批量更新的 Service（从其他集合获取数据源）**

```python
"""
基金详情示例-数据服务（批量更新时从 fund_name_em 获取基金代码列表）
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.fund_detail_example_provider import FundDetailExampleProvider


class FundDetailExampleService(BaseService):
    """基金详情示例-数据服务"""
    
    collection_name = "fund_detail_example"
    provider_class = FundDetailExampleProvider
    
    # 批量更新配置：从其他集合获取数据源
    batch_source_collection = "fund_name_em"  # 数据源集合
    batch_source_field = "基金代码"            # 数据源字段
    
    # 并发控制
    batch_concurrency = 5
    batch_progress_interval = 20
    
    # 增量更新：根据基金代码检查是否已存在
    incremental_check_fields = ["基金代码"]
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量更新参数
        
        Args:
            args[0]: 基金代码（从 batch_source_collection 获取）
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 1:
            return {"symbol": args[0]}
        return {}
```

**示例 3: 需要多参数的批量更新 Service**

```python
"""
基金持仓示例-数据服务（批量更新时需要基金代码和年份）
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.fund_hold_example_provider import FundHoldExampleProvider


class FundHoldExampleService(BaseService):
    """基金持仓示例-数据服务"""
    
    collection_name = "fund_hold_example"
    provider_class = FundHoldExampleProvider
    
    # 批量更新配置
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    
    # 年份范围配置
    batch_years_range = (2010, None)  # 从 2010 年到今年
    
    # 并发控制
    batch_concurrency = 3
    batch_progress_interval = 10
    
    # 增量更新：根据基金代码、股票代码、季度检查
    incremental_check_fields = ["基金代码", "股票代码", "季度"]
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量更新参数
        
        Args:
            args[0]: 基金代码
            args[1]: 年份
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 2:
            # 将年份转换为日期格式（季度末日期）
            year = args[1]
            date = f"{year}1231"  # 假设使用年末日期
            return {
                "symbol": args[0],
                "date": date
            }
        return {}
```

#### 3.3 Service 类属性说明

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collection_name` | str | ✅ | 集合名称，必须与 Provider 一致 |
| `provider_class` | Type[BaseProvider] | ✅ | Provider 类 |
| `batch_source_collection` | str | ❌ | 批量更新数据源集合 |
| `batch_source_field` | str | ❌ | 批量更新数据源字段 |
| `batch_years_range` | Tuple[int, Optional[int]] | ❌ | 年份范围，如 (2010, None) |
| `batch_concurrency` | int | ❌ | 并发数，默认 3 |
| `batch_progress_interval` | int | ❌ | 进度更新间隔，默认 10 |
| `incremental_check_fields` | List[str] | ❌ | 增量更新检查字段 |

---

### 步骤 4: 添加集合元信息

在 `app/services/data_sources/funds/collection_metadata.py` 文件中添加集合元信息：

```python
FUND_COLLECTION_METADATA = {
    # ... 其他集合 ...
    
    'fund_new_example': {
        'display_name': '新基金示例',
        'description': '新基金示例数据，包括基金代码、名称等信息',
        'route': '/funds/collections/fund_new_example',
        'order': 100,  # 设置合适的排序值
    },
}
```

**注意**: 
- `display_name`: 前端显示的名称
- `description`: 集合描述，会显示在前端
- `route`: 前端路由路径
- `order`: 排序顺序，数字越小越靠前

---

### 步骤 5: 配置更新参数

在 `app/config/fund_update_config.py` 文件中添加更新参数配置：

#### 5.1 无参数接口配置

```python
FUND_UPDATE_CONFIGS = {
    # ... 其他配置 ...
    
    "fund_new_example": {
        "display_name": "新基金示例",
        "update_description": "将从数据源获取所有新基金示例数据",
        "single_update": {
            "enabled": False,  # 无参数接口不支持单条更新
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有新基金示例数据",
            "params": []  # 无参数
        }
    },
}
```

#### 5.2 单参数接口配置

```python
"fund_detail_example": {
    "display_name": "基金详情示例",
    "update_description": "获取指定基金的详细信息",
    "single_update": {
        "enabled": True,
        "description": "获取单个基金的详细信息",
        "params": [
            {
                "name": "fund_code",  # 参数名（后端使用）
                "label": "基金代码",   # 显示标签
                "type": "text",        # 参数类型：text, number, select
                "placeholder": "请输入基金代码，如：000001",
                "required": True,      # 是否必填
                "default": None
            }
        ]
    },
    "batch_update": {
        "enabled": True,
        "description": "批量获取所有基金的详细信息",
        "params": []  # 批量更新时从 batch_source_collection 获取参数
    }
},
```

#### 5.3 多参数接口配置

```python
"fund_hold_example": {
    "display_name": "基金持仓示例",
    "update_description": "获取指定基金在指定季度的持仓信息",
    "single_update": {
        "enabled": True,
        "description": "获取单个基金在指定季度的持仓信息",
        "params": [
            {
                "name": "fund_code",
                "label": "基金代码",
                "type": "text",
                "placeholder": "请输入基金代码，如：000001",
                "required": True
            },
            {
                "name": "date",
                "label": "日期",
                "type": "text",
                "placeholder": "请输入日期，格式：YYYYMMDD，如：20231231",
                "required": True
            }
        ]
    },
    "batch_update": {
        "enabled": True,
        "description": "批量获取所有基金的历史持仓信息",
        "params": [
            {
                "name": "start_year",
                "label": "起始年份",
                "type": "number",
                "placeholder": "请输入起始年份，如：2010",
                "required": False,
                "default": 2010,
                "min": 2000,
                "max": 2100
            },
            {
                "name": "end_year",
                "label": "结束年份",
                "type": "number",
                "placeholder": "请输入结束年份，如：2023",
                "required": False,
                "default": None,
                "min": 2000,
                "max": 2100
            }
        ]
    }
},
```

#### 5.4 参数类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| `text` | 文本输入 | 基金代码、日期字符串 |
| `number` | 数字输入 | 年份、数量 |
| `select` | 下拉选择 | 需要提供 `options` 字段 |

**select 类型示例**:

```python
{
    "name": "fund_type",
    "label": "基金类型",
    "type": "select",
    "required": True,
    "options": [
        {"label": "全部", "value": "全部"},
        {"label": "股票型", "value": "股票型"},
        {"label": "混合型", "value": "混合型"},
    ]
}
```

---

### 步骤 6: （可选）创建前端组件

#### 6.1 自动生成组件

系统会自动为每个集合生成前端组件。如果集合使用默认功能，无需创建自定义组件。

#### 6.2 创建自定义组件（可选）

如果需要自定义功能（如特殊图表、筛选器等），在 `frontend/src/views/Funds/collections/` 目录下创建组件：

**文件命名规范**: `{PascalCase(collection_name)}.vue`

例如: `FundNewExample.vue`

```vue
<template>
  <DefaultCollection>
    <!-- 使用插槽扩展 -->
    <template #charts="{ stats, collectionName }">
      <!-- 自定义图表 -->
      <div class="custom-charts">
        <!-- 你的自定义图表代码 -->
      </div>
    </template>

    <template #extra-filters="{ collectionName }">
      <!-- 自定义筛选器 -->
      <el-form-item label="自定义筛选">
        <el-input v-model="customFilter" placeholder="自定义筛选条件" />
      </el-form-item>
    </template>
  </DefaultCollection>
</template>

<script setup lang="ts">
import DefaultCollection from './DefaultCollection.vue'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const collectionName = route.params.collectionName as string
const customFilter = ref('')

// TODO: 在此添加 fund_new_example 的特殊逻辑
// 例如：自定义图表、筛选器、更新参数等
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
```

---

## 代码示例

### 完整示例：新增一个基金评级数据集合

#### 1. Provider (`fund_rating_example_provider.py`)

```python
"""
基金评级示例-数据提供者
"""
from app.services.data_sources.base_provider import BaseProvider


class FundRatingExampleProvider(BaseProvider):
    """基金评级示例-数据提供者"""
    
    collection_name = "fund_rating_example"
    display_name = "基金评级示例"
    akshare_func = "fund_rating_all_em"  # 假设的 akshare 函数
    unique_keys = ["基金代码", "评级日期"]
    
    collection_description = "基金评级数据，包括评级机构、评级等级等"
    collection_route = "/funds/collections/fund_rating_example"
    collection_order = 103
    
    param_mapping = {
        "date": "date",
        "rating_date": "date",
    }
    
    required_params = ["date"]
    
    add_param_columns = {
        "date": "评级日期",
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金唯一标识"},
        {"name": "评级日期", "type": "string", "description": "评级日期"},
        {"name": "评级机构", "type": "string", "description": "评级机构名称"},
        {"name": "评级等级", "type": "string", "description": "评级等级"},
    ]
```

#### 2. Service (`fund_rating_example_service.py`)

```python
"""
基金评级示例-数据服务
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.fund_rating_example_provider import FundRatingExampleProvider


class FundRatingExampleService(BaseService):
    """基金评级示例-数据服务"""
    
    collection_name = "fund_rating_example"
    provider_class = FundRatingExampleProvider
    
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    
    batch_concurrency = 5
    batch_progress_interval = 20
    
    incremental_check_fields = ["基金代码", "评级日期"]
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """构建批量更新参数"""
        if len(args) >= 1:
            fund_code = args[0]
            # 假设需要当前日期作为评级日期
            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d")
            return {
                "symbol": fund_code,
                "date": date
            }
        return {}
```

#### 3. 元信息配置 (`collection_metadata.py`)

```python
'fund_rating_example': {
    'display_name': '基金评级示例',
    'description': '基金评级数据，包括评级机构、评级等级等',
    'route': '/funds/collections/fund_rating_example',
    'order': 103,
},
```

#### 4. 更新参数配置 (`fund_update_config.py`)

```python
"fund_rating_example": {
    "display_name": "基金评级示例",
    "update_description": "获取基金的评级信息",
    "single_update": {
        "enabled": True,
        "description": "获取指定基金的评级信息",
        "params": [
            {
                "name": "fund_code",
                "label": "基金代码",
                "type": "text",
                "placeholder": "请输入基金代码，如：000001",
                "required": True
            },
            {
                "name": "date",
                "label": "评级日期",
                "type": "text",
                "placeholder": "请输入日期，格式：YYYYMMDD",
                "required": True
            }
        ]
    },
    "batch_update": {
        "enabled": True,
        "description": "批量获取所有基金的评级信息",
        "params": []
    }
},
```

---

## 最佳实践

### 1. 命名规范

- **集合名称**: 使用 `snake_case`，格式：`fund_{功能}_{数据源}`
  - 例如: `fund_name_em`, `fund_etf_spot_ths`
- **Provider 类名**: `{PascalCase(collection_name)}Provider`
  - 例如: `FundNameEmProvider`
- **Service 类名**: `{PascalCase(collection_name)}Service`
  - 例如: `FundNameEmService`

### 2. 唯一键选择

- 选择能够唯一标识一条记录的字段组合
- 优先使用业务主键（如基金代码）
- 时间序列数据需要包含时间字段

### 3. 参数映射

- 支持多种参数名映射到同一个 akshare 参数
- 提供友好的参数名（如 `fund_code` 而不是 `symbol`）
- 保持向后兼容

### 4. 批量更新配置

- 合理设置并发数（`batch_concurrency`），避免过载
- 设置合适的进度更新间隔（`batch_progress_interval`）
- 使用增量更新（`incremental_check_fields`）避免重复数据

### 5. 错误处理

- Provider 中处理数据源异常
- Service 中处理业务逻辑异常
- 使用统一的错误处理机制

### 6. 数据转换

- 在 Provider 的 `transform_data` 方法中进行数据清洗
- 统一字段命名（使用中文）
- 处理缺失值和异常值

### 7. 文档注释

- 为每个类和方法添加详细的文档字符串
- 说明参数含义和返回值
- 提供使用示例

---

## 常见问题

### Q1: 如何测试新创建的 Provider？

```python
# 在 Python 交互环境中测试
from app.services.data_sources.funds.providers.fund_new_example_provider import FundNewExampleProvider

provider = FundNewExampleProvider()
params = {}  # 或 {"symbol": "000001"}
df = provider.fetch_data(params)
print(df.head())
```

### Q2: 如何测试新创建的 Service？

```python
# 在 Python 交互环境中测试
from app.services.data_sources.funds.services.fund_new_example_service import FundNewExampleService
from app.core.database import get_mongo_db

db = get_mongo_db()
service = FundNewExampleService(db)

# 测试单条更新
result = await service.update_single_data("task_id", {"fund_code": "000001"})

# 测试批量更新
result = await service.update_batch_data("task_id", {})
```

### Q3: 前端页面不显示新集合？

1. 检查 `collection_metadata.py` 中是否添加了元信息
2. 检查 `provider_registry.py` 是否能正确注册 Provider
3. 重启后端服务
4. 清除浏览器缓存

### Q4: 批量更新失败？

1. 检查 `batch_source_collection` 是否存在
2. 检查 `batch_source_field` 是否正确
3. 检查 `get_batch_params` 方法是否正确构建参数
4. 查看后端日志获取详细错误信息

### Q5: 数据重复插入？

1. 检查 `unique_keys` 是否正确设置
2. 检查 `incremental_check_fields` 是否与 `unique_keys` 一致
3. 确认 MongoDB 索引是否正确创建

### Q6: 如何添加自定义数据转换？

在 Provider 类中重写 `transform_data` 方法：

```python
def transform_data(self, df, params=None):
    """自定义数据转换"""
    if df is None or df.empty:
        return df
    
    # 添加自定义列
    df["自定义列"] = df["原列"] * 2
    
    # 数据清洗
    df = df.dropna(subset=["重要字段"])
    
    return df
```

### Q7: 如何支持文件上传导入？

如果集合支持文件上传，需要在路由中添加对应的上传接口。参考 `app/routers/funds.py` 中的 `upload_fund_etf_dividend_sina` 函数。

---

## 测试验证

### 1. 单元测试

创建测试文件 `tests/test_fund_new_example.py`:

```python
import pytest
from app.services.data_sources.funds.providers.fund_new_example_provider import FundNewExampleProvider
from app.services.data_sources.funds.services.fund_new_example_service import FundNewExampleService


def test_provider_fetch_data():
    """测试 Provider 数据获取"""
    provider = FundNewExampleProvider()
    df = provider.fetch_data({})
    assert df is not None
    assert not df.empty
    assert "基金代码" in df.columns


@pytest.mark.asyncio
async def test_service_update_single():
    """测试 Service 单条更新"""
    # 实现测试逻辑
    pass


@pytest.mark.asyncio
async def test_service_update_batch():
    """测试 Service 批量更新"""
    # 实现测试逻辑
    pass
```

### 2. 集成测试

1. **测试 API 接口**:
   - 测试获取集合列表接口
   - 测试获取集合数据接口
   - 测试单条更新接口
   - 测试批量更新接口

2. **测试前端页面**:
   - 验证页面可以正常加载
   - 验证数据可以正常显示
   - 验证更新功能可以正常使用

### 3. 数据验证

1. **数据完整性**:
   - 检查必填字段是否有值
   - 检查数据格式是否正确
   - 检查唯一键是否唯一

2. **数据准确性**:
   - 对比 akshare 原始数据
   - 验证数据转换是否正确
   - 验证计算字段是否正确

---

## 总结

新增一个基金数据集合的完整流程：

1. ✅ 确定数据源和接口
2. ✅ 创建 Provider 类
3. ✅ 创建 Service 类
4. ✅ 添加集合元信息
5. ✅ 配置更新参数
6. ✅ （可选）创建前端组件
7. ✅ 测试验证

按照本文档的步骤，你可以快速、规范地新增一个基金数据集合。如有问题，请参考常见问题部分或联系团队。

---

## 附录

### A. 相关文档

- [基金模块优化总结](./fund_optimization_summary.md)
- [基金改进建议](./fund_improvements.md)
- [BaseProvider 文档](../../app/services/data_sources/base_provider.py)
- [BaseService 文档](../../app/services/data_sources/base_service.py)

### B. 工具脚本

- `scripts/generate_fund_collection_components.py` - 自动生成前端组件

### C. 联系方式

如有问题或建议，请联系开发团队。
