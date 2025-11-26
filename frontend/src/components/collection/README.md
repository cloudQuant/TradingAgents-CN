# 数据集合共享组件

这些组件用于各个模块（Stocks、Bonds、Funds、Options、Currencies、Futures）的数据集合详情页面，提供统一的数据表格展示、页面头部、对话框等功能。

## 组件列表

| 组件 | 功能 | 文件 |
|------|------|------|
| `CollectionDataTable` | 数据表格（搜索、分页、排序） | `CollectionDataTable.vue` |
| `CollectionPageHeader` | 页面头部（标题、操作按钮） | `CollectionPageHeader.vue` |
| `CollectionOverviewDialog` | 数据概览对话框 | `CollectionOverviewDialog.vue` |
| `FileImportDialog` | 文件导入对话框 | `FileImportDialog.vue` |
| `RemoteSyncDialog` | 远程同步对话框 | `RemoteSyncDialog.vue` |

## 使用示例

### 基础用法

```vue
<template>
  <div class="collection-view">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :loading="loading"
      :updating="refreshing"
      :clearing="clearing"
      @show-overview="overviewDialogVisible = true"
      @refresh="loadData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    />

    <div class="content">
      <!-- 数据表格 -->
      <CollectionDataTable
        :data="items"
        :fields="fields"
        :total="total"
        :loading="loading"
        v-model:page="page"
        v-model:page-size="pageSize"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="loadData"
        @refresh="loadData"
        @page-change="loadData"
        @size-change="loadData"
        @sort-change="handleSortChange"
      />
    </div>

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :total-count="stats?.total_count"
      :field-count="fields.length"
      :latest-update="stats?.latest_update"
      :data-source="dataSourceUrl"
    />

    <!-- 文件导入对话框 -->
    <FileImportDialog
      v-model:visible="uploadDialogVisible"
      :importing="importing"
      @import="handleImport"
    />

    <!-- 远程同步对话框 -->
    <RemoteSyncDialog
      v-model:visible="syncDialogVisible"
      :collection-name="collectionName"
      :syncing="remoteSyncing"
      :sync-result="remoteSyncResult"
      @sync="handleRemoteSync"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  CollectionDataTable,
  CollectionPageHeader,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
} from '@/components/collection'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)

// 状态
const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const importing = ref(false)
const remoteSyncing = ref(false)

// 数据
const items = ref([])
const fields = ref([])
const total = ref(0)
const stats = ref({})
const collectionInfo = ref(null)

// 分页
const page = ref(1)
const pageSize = ref(20)

// 搜索
const filterValue = ref('')
const filterField = ref('')

// 对话框
const overviewDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)

// 同步结果
const remoteSyncResult = ref(null)

// 数据源URL
const dataSourceUrl = computed(() => {
  // 根据集合名返回对应的数据源URL
  return ''
})

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // API调用...
  } finally {
    loading.value = false
  }
}

// 处理更新命令
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    // 显示API更新对话框
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

// 处理清空数据
const handleClearData = async () => {
  clearing.value = true
  try {
    // API调用...
  } finally {
    clearing.value = false
  }
}

// 处理排序变化
const handleSortChange = (params: { prop: string; order: 'ascending' | 'descending' | null }) => {
  // 更新排序参数并重新加载数据
  loadData()
}

// 处理文件导入
const handleImport = async (files: File[]) => {
  importing.value = true
  try {
    // API调用...
  } finally {
    importing.value = false
  }
}

// 处理远程同步
const handleRemoteSync = async (config: any) => {
  remoteSyncing.value = true
  remoteSyncResult.value = null
  try {
    // API调用...
  } finally {
    remoteSyncing.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
```

### 自定义列渲染

```vue
<CollectionDataTable
  :data="items"
  :fields="fields"
  :total="total"
  :loading="loading"
  @search="loadData"
>
  <!-- 自定义 "涨跌幅" 列的渲染 -->
  <template #column-涨跌幅="{ row }">
    <span :style="{ color: row.涨跌幅 > 0 ? '#f56c6c' : '#67c23a' }">
      {{ row.涨跌幅 > 0 ? '+' : '' }}{{ row.涨跌幅?.toFixed(2) }}%
    </span>
  </template>
  
  <!-- 额外的筛选器 -->
  <template #extra-filters>
    <el-select v-model="filterType" placeholder="类型" clearable>
      <el-option label="全部" value="" />
      <el-option label="上涨" value="rise" />
      <el-option label="下跌" value="fall" />
    </el-select>
  </template>
</CollectionDataTable>
```

### 扩展数据概览

```vue
<CollectionOverviewDialog
  v-model:visible="overviewDialogVisible"
  :collection-name="collectionName"
  :total-count="stats?.total_count"
>
  <!-- 额外的统计信息 -->
  <template #extra-stats>
    <el-descriptions-item label="上涨数量">
      {{ stats?.rise_count || 0 }}
    </el-descriptions-item>
    <el-descriptions-item label="下跌数量">
      {{ stats?.fall_count || 0 }}
    </el-descriptions-item>
  </template>
  
  <!-- 额外的内容 -->
  <template #extra-content>
    <div style="margin-top: 16px;">
      <h4>数据分布图表</h4>
      <!-- 图表组件 -->
    </div>
  </template>
</CollectionOverviewDialog>
```

## Props 说明

### CollectionDataTable

| Prop | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data` | `any[]` | 必填 | 表格数据 |
| `fields` | `(FieldDefinition \| string)[]` | 必填 | 字段定义 |
| `total` | `number` | 必填 | 数据总数 |
| `loading` | `boolean` | `false` | 加载状态 |
| `page` | `number` | `1` | 当前页码 |
| `pageSize` | `number` | `20` | 每页条数 |
| `filterValue` | `string` | `''` | 搜索值 |
| `filterField` | `string` | `''` | 搜索字段 |
| `sortable` | `boolean` | `true` | 是否支持排序 |
| `maxHeight` | `number \| string` | `600` | 表格最大高度 |

### CollectionPageHeader

| Prop | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `collectionName` | `string` | 必填 | 集合名称 |
| `displayName` | `string` | - | 显示名称 |
| `description` | `string` | - | 描述 |
| `loading` | `boolean` | `false` | 刷新按钮加载状态 |
| `updating` | `boolean` | `false` | 更新按钮加载状态 |
| `clearing` | `boolean` | `false` | 清空按钮加载状态 |
| `showOverviewButton` | `boolean` | `true` | 是否显示概览按钮 |
| `showUpdateDropdown` | `boolean` | `true` | 是否显示更新下拉菜单 |
| `showClearButton` | `boolean` | `true` | 是否显示清空按钮 |

## 迁移指南

将现有的 Collection.vue 迁移到使用共享组件：

1. 导入共享组件
2. 替换模板中的对应部分
3. 保留特定模块的自定义逻辑（如可视化图表、特殊的API更新对话框等）

共享组件通过插槽机制支持扩展，可以在不修改组件源码的情况下添加自定义功能。
