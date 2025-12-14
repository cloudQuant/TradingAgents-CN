# 基金集合组件架构说明

## 📁 目录结构

```bash
frontend/src/views/Funds/collections/
├── index.vue                    # 动态加载入口

├── DefaultCollection.vue        # 默认集合组件（通用逻辑）

├── FundNameEm.vue              # 基金基本信息集合组件

├── FundBasicInfo.vue           # 雪球基金基本信息集合组件

├── FundInfoIndexEm.vue         # 指数型基金基本信息集合组件（特殊）

├── FundPurchaseStatus.vue      # 基金申购状态集合组件（特殊）

├── FundEtfSpotThs.vue          # ETF 基金实时行情-同花顺集合组件（特殊）

├── FundLofSpotEm.vue           # LOF 基金实时行情集合组件（特殊）

└── ...                         # 其他集合组件

```bash

## 🏗️ 架构设计

### 1. 动态加载机制 (`index.vue`)

`index.vue` 作为入口文件，根据路由参数 `collectionName` 动态加载对应的集合组件：

- 自动将 `snake_case` 集合名称转换为 `PascalCase` 组件名
- 如果找不到对应组件，使用 `DefaultCollection.vue` 作为后备
- 支持异步组件加载，优化性能

### 2. 默认组件 (`DefaultCollection.vue`)

`DefaultCollection.vue` 包含所有集合的通用功能：

- ✅ 数据加载和分页
- ✅ 排序和过滤
- ✅ 数据导出（CSV/Excel/JSON）
- ✅ API 更新（单条/批量）
- ✅ 文件导入
- ✅ 远程同步
- ✅ 数据清空
- ✅ 基础图表展示（类型分布饼图）

### 3. 特殊集合组件

对于有特殊需求的集合（如自定义图表、筛选器等），可以创建独立组件：

- *特殊集合列表：**
- `fund_purchase_status` - 申购赎回状态图表
- `fund_etf_spot_ths` - 市场分析图表（涨跌分布、TOP10 等）
- `fund_lof_spot_em` - 市场行情图表
- `fund_info_index_em` - 指数型基金筛选器（跟踪标的、跟踪方式、基金公司）

## 📝 如何扩展集合组件

### 方式一：使用 DefaultCollection（推荐）

对于大多数集合，直接使用 `DefaultCollection.vue` 即可：

```vue
<template>
  <DefaultCollection />
</template>

<script setup lang="ts">
import DefaultCollection from './DefaultCollection.vue'
</script>

```bash

### 方式二：扩展 DefaultCollection

如果需要添加自定义逻辑，可以：

1. **使用 Composable**（推荐）

```vue
<template>
  <div class="collection-page">
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :loading="loading"
      @refresh="loadData"
    />

    <!-- 自定义内容 -->
    <div class="custom-section">
      <!-- 你的自定义内容 -->
    </div>

    <!-- 使用 DefaultCollection 的其他部分 -->
    <CollectionDataTable
      :data="items"
      :fields="fields"
      :total="total"
      :loading="loading"
      @search="loadData"
    />
  </div>
</template>

<script setup lang="ts">
import { useFundCollection } from '@/components/collection'
import { CollectionPageHeader, CollectionDataTable } from '@/components/collection'

const {
  collectionName,
  collectionInfo,
  loading,
  items,
  fields,
  total,
  loadData,
} = useFundCollection()
</script>

```bash

1. **直接扩展组件**

```vue
<template>
  <DefaultCollection>
    <!-- 使用插槽扩展 -->
    <template #charts="{ stats, collectionName }">
      <!-- 自定义图表 -->
    </template>

    <template #extra-filters="{ collectionName }">
      <!-- 自定义筛选器 -->
    </template>

    <template #before-table="{ collectionName }">
      <!-- 表格前内容 -->
    </template>
  </DefaultCollection>
</template>

<script setup lang="ts">
import DefaultCollection from './DefaultCollection.vue'
</script>

```bash

### 方式三：完全自定义组件

对于需要完全自定义的集合，可以创建独立组件：

```vue
<template>
  <div class="collection-page">
    <!-- 完全自定义的布局和逻辑 -->
  </div>
</template>

<script setup lang="ts">
import { useFundCollection } from '@/components/collection'
// 使用 composable 获取通用功能
const collection = useFundCollection()
// 添加自定义逻辑
</script>

```bash

## 🔧 Composable API

`useFundCollection` 提供了所有通用功能：

### 状态

```typescript
{
  collectionName: ComputedRef<string>
  loading: Ref<boolean>
  items: Ref<any[]>
  fields: Ref<Array<{name: string, type: string, example: string | null}>>

  page: Ref<number>
  pageSize: Ref<number>
  total: Ref<number>
  stats: Ref<any>
  collectionInfo: Ref<any>
  // ... 更多状态
}

```bash

### 方法

```typescript
{
  loadData(extraParams?: Record<string, any>): Promise<void>
  handleSortChange({ prop, order }): void
  exportAllData({ fileName, format }, extraParams?): Promise<void>
  handleUpdateCommand(command: string): void
  handleSingleUpdate(): Promise<void>
  handleBatchUpdate(): Promise<void>
  handleImportFile(files: File[]): Promise<void>
  handleRemoteSync(config: RemoteSyncConfig): Promise<void>
  handleClearData(): Promise<void>
  cleanup(): void
}

```bash

## 📋 最佳实践

1. **优先使用 DefaultCollection**
   - 大多数集合可以直接使用，无需额外代码

1. **使用 Composable 共享逻辑**
   - 避免重复代码
   - 保持一致性

1. **按需扩展**
   - 只在需要特殊功能时创建自定义组件
   - 尽量复用现有组件和逻辑

1. **命名规范**
   - 组件文件：`PascalCase.vue`（如 `FundNameEm.vue`）
   - 集合名称：`snake_case`（如 `fund_name_em`）

1. **组件注册**
   - 在 `index.vue` 中自动注册
   - 使用动态导入优化性能

## 🚀 示例：创建特殊集合组件

以 `fund_info_index_em` 为例，需要添加筛选器：

```vue
<template>
  <div class="collection-page">
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :loading="loading"
      @refresh="loadData"
    />

    <div class="content">
      <CollectionDataTable
        :data="items"
        :fields="fields"
        :total="total"
        :loading="loading"
        @search="handleSearch"
      >
        <!-- 自定义筛选器 -->
        <template #extra-filters>
          <el-select
            v-model="filterCompany"
            placeholder="基金公司"
            @change="handleFilterChange"
          >
            <el-option
              v-for="company in companyOptions"
              :key="company"
              :label="company"
              :value="company"
            />
          </el-select>
        </template>

        <!-- 表格前筛选栏 -->
        <template #before-table>
          <div class="filter-section">
            <div class="filter-row">
              <span class="filter-label">跟踪标的：</span>
              <div class="filter-options">
                <span
                  v-for="opt in targetOptions"
                  :key="opt"
                  class="filter-option"
                  :class="{ active: filterTarget === opt }"
                  @click="filterTarget = opt; handleSearch()"
                >
                  {{ opt }}
                </span>
              </div>
            </div>
          </div>
        </template>
      </CollectionDataTable>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useFundCollection } from '@/components/collection'
import { CollectionPageHeader, CollectionDataTable } from '@/components/collection'
import { fundsApi } from '@/api/funds'

const {
  collectionName,
  collectionInfo,
  loading,
  items,
  fields,
  total,
  loadData,
} = useFundCollection()

// 自定义筛选器
const filterCompany = ref('全部')
const filterTarget = ref('全部')
const companyOptions = ref<string[]>([])
const targetOptions = ref<string[]>(['全部'])

const loadCompanies = async () => {
  const res = await fundsApi.getFundCompanies()
  if (res.success && res.data) {
    companyOptions.value = res.data
  }
}

const handleFilterChange = () => {
  loadData({
    fund_company: filterCompany.value !== '全部' ? filterCompany.value : undefined,
    tracking_target: filterTarget.value !== '全部' ? filterTarget.value : undefined,
  })
}

const handleSearch = () => {
  handleFilterChange()
}

onMounted(() => {
  loadCompanies()
  loadData()
})
</script>

```bash

## 📚 相关文件

- `frontend/src/components/collection/useFundCollection.ts` - 通用逻辑 Composable
- `frontend/src/components/collection/` - 集合相关组件
- `app/services/data_sources/funds/providers/` - 后端 Provider
- `app/services/data_sources/funds/services/` - 后端 Service
