# 香港基金历史数据前端展示说明

## 功能概述

为 `fund_hk_hist_em` 集合创建了自定义前端页面，支持按数据类型（历史净值明细/分红送配详情）筛选和展示数据。

## 实现方式

### 1. 自定义组件

创建了 `frontend/src/views/Funds/collections/FundHkHistEm.vue` 组件，在默认集合组件的基础上添加了数据类型筛选功能。

### 2. 数据类型标签页

在数据表格上方添加了一个标签页组件，包含三个选项：

- **全部数据**：显示所有数据（净值数据 + 分红数据）
- **历史净值明细**：只显示 `symbol="历史净值明细"` 的数据
- **分红送配详情**：只显示 `symbol="分红送配详情"` 的数据

每个标签页显示对应数据类型的数量（通过 Badge 组件展示）。

### 3. 筛选逻辑

当用户切换标签页时：

```typescript
const handleDataTypeChange = (tabName: string) => {
  if (tabName === 'all') {
    // 显示全部数据，清除 symbol 筛选
    filterField.value = ''
    filterValue.value = ''
  } else {
    // 按 symbol 筛选
    filterField.value = 'symbol'
    filterValue.value = tabName
  }
  // 重置到第一页并重新加载数据
  page.value = 1
  loadData()
}
```

### 4. 统计数据展示

组件会加载各类型数据的统计数量：

- `allDataCount`：全部数据总数
- `netValueCount`：历史净值明细数据总数
- `dividendCount`：分红送配详情数据总数

这些统计数据通过调用后端 API 获取，并在标签页的 Badge 中显示。

## 使用方式

### 用户操作流程

1. **访问集合页面**：打开 `http://localhost:3000/funds/collections/fund_hk_hist_em`

2. **选择数据类型**：
   - 点击"全部数据"标签：查看所有数据
   - 点击"历史净值明细"标签：只查看净值数据
   - 点击"分红送配详情"标签：只查看分红数据

3. **查看数据**：数据表格会根据选择的标签自动筛选并显示对应类型的数据

4. **其他功能**：仍然可以使用搜索、排序、分页等标准功能

## 技术实现

### 组件结构

```vue
<template>
  <!-- 页面头部 -->
  <CollectionPageHeader ... />
  
  <div class="content">
    <!-- 数据类型筛选标签页 -->
    <el-card>
      <el-tabs v-model="activeDataType" @tab-change="handleDataTypeChange">
        <el-tab-pane label="全部数据" name="all" />
        <el-tab-pane label="历史净值明细" name="历史净值明细" />
        <el-tab-pane label="分红送配详情" name="分红送配详情" />
      </el-tabs>
    </el-card>
    
    <!-- 数据表格 -->
    <CollectionDataTable ... />
  </div>
</template>
```

### 关键代码

1. **数据类型状态管理**：
   ```typescript
   const activeDataType = ref<string>('all')
   ```

2. **筛选条件更新**：
   ```typescript
   const handleDataTypeChange = (tabName: string) => {
     if (tabName === 'all') {
       filterField.value = ''
       filterValue.value = ''
     } else {
       filterField.value = 'symbol'
       filterValue.value = tabName
     }
     page.value = 1
     loadData()
   }
   ```

3. **统计数据加载**：
   ```typescript
   const loadStats = async () => {
     // 获取各类型数据的统计数量
     // 用于在标签页 Badge 中显示
   }
   ```

## 数据展示效果

### 全部数据视图
- 显示所有记录，包括净值数据和分红数据
- 可以通过 `symbol` 列区分数据类型

### 历史净值明细视图
- 只显示 `symbol="历史净值明细"` 的记录
- 包含字段：净值日期、单位净值、日增长值、日增长率等

### 分红送配详情视图
- 只显示 `symbol="分红送配详情"` 的记录
- 包含字段：权益登记日、除息日期、分红金额等

## 优势

1. **清晰的数据分类**：用户可以快速切换查看不同类型的数据
2. **直观的数量展示**：每个标签页显示对应数据类型的数量
3. **保持原有功能**：搜索、排序、分页等功能仍然可用
4. **响应式设计**：使用 Element Plus 组件，界面美观且易用

## 后续优化建议

1. **添加图表展示**：可以为净值数据添加趋势图
2. **添加导出功能**：支持按数据类型导出数据
3. **添加日期范围筛选**：支持按日期范围筛选数据
4. **添加基金代码筛选**：支持按基金代码筛选数据


