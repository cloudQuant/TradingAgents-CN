<template>
  <div class="collection-page">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :loading="loading"
      :updating="refreshing || importing || remoteSyncing"
      :clearing="clearing"
      @show-overview="overviewDialogVisible = true"
      @refresh="loadData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    />

    <div class="content">
      <!-- 数据类型筛选标签页 -->
      <!-- 注意：分红送配详情接口暂时有问题，已禁用，目前只显示历史净值明细数据 -->
      <el-card shadow="hover" style="margin-bottom: 16px;">
        <el-tabs v-model="activeDataType" @tab-change="handleDataTypeChange">
          <el-tab-pane label="全部数据" name="all">
            <template #label>
              <span>全部数据 <el-badge :value="allDataCount" class="item" /></span>
            </template>
          </el-tab-pane>
          <el-tab-pane label="历史净值明细" name="历史净值明细">
            <template #label>
              <span>历史净值明细 <el-badge :value="netValueCount" class="item" /></span>
            </template>
          </el-tab-pane>
          <!-- 分红送配详情标签页已暂时禁用 -->
        </el-tabs>
      </el-card>

      <!-- 数据列表 -->
      <CollectionDataTable
        :data="items"
        :fields="fields"
        :total="total"
        :loading="loading"
        :page="page"
        :page-size="pageSize"
        :sortable="true"
        :collection-name="collectionName"
        :export-all-data="exportAllData"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="loadData"
        @page-change="loadData"
        @size-change="loadData"
        @sort-change="handleSortChange"
      />
    </div>

    <!-- API更新对话框 -->
    <el-dialog
      v-model="apiRefreshDialogVisible"
      title="API更新"
      width="650px"
      :close-on-click-modal="false"
      @open="loadUpdateConfig"
    >
      <el-form label-width="100px" v-loading="!updateConfig">
        <el-form-item label="集合名称">
          <el-input :value="updateConfig?.display_name || collectionName" disabled />
        </el-form-item>

        <template v-if="updateConfig?.single_update?.enabled">
          <el-card shadow="never" style="margin-bottom: 16px;">
            <template #header>
              <span style="font-weight: 600;">单条更新</span>
            </template>
            <div v-if="updateConfig.single_update.description" style="color: #909399; font-size: 12px; margin-bottom: 12px;">
              {{ updateConfig.single_update.description }}
            </div>
            <el-row :gutter="16" v-if="updateConfig.single_update.params?.length">
              <el-col 
                v-for="param in updateConfig.single_update.params" 
                :key="param.name"
                :span="updateConfig.single_update.params.length === 1 ? 24 : 12"
              >
                <el-form-item :label="param.label" :required="param.required">
                  <el-input
                    v-if="param.type === 'text'"
                    v-model="singleUpdateParams[param.name]"
                    :placeholder="param.placeholder"
                    clearable
                  />
                  <el-input-number
                    v-else-if="param.type === 'number'"
                    v-model="singleUpdateParams[param.name]"
                    :min="param.min"
                    :max="param.max"
                    :step="param.step"
                    style="width: 100%"
                  />
                  <el-select
                    v-else-if="param.type === 'select'"
                    v-model="singleUpdateParams[param.name]"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="opt in param.options"
                      :key="opt.value"
                      :label="opt.label"
                      :value="opt.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-button
              type="primary"
              @click="handleSingleUpdate"
              :loading="singleUpdating"
              :disabled="!canSingleUpdate || singleUpdating || batchUpdating"
              style="width: 100%;"
            >
              更新
            </el-button>
          </el-card>
        </template>

        <template v-if="updateConfig?.batch_update?.enabled">
          <el-card shadow="never" style="margin-bottom: 16px;">
            <template #header>
              <span style="font-weight: 600;">批量更新</span>
            </template>
            <div v-if="updateConfig.batch_update.description" style="color: #909399; font-size: 12px; margin-bottom: 12px;">
              {{ updateConfig.batch_update.description }}
            </div>
            <!-- 更新方式选择 -->
            <el-form-item label="更新方式" style="margin-bottom: 16px;">
              <el-radio-group v-model="updateMode">
                <el-radio label="incremental">增量更新</el-radio>
                <el-radio label="full">全量更新</el-radio>
              </el-radio-group>
              <div style="color: #909399; font-size: 12px; margin-top: 4px;">
                <span v-if="updateMode === 'incremental'">增量更新：只更新新增或变更的数据</span>
                <span v-else style="color: #E6A23C;">全量更新：先清除所有数据，然后重新获取全部数据</span>
              </div>
            </el-form-item>
            
            <el-row :gutter="16" v-if="updateConfig.batch_update.params?.length">
              <el-col 
                v-for="param in updateConfig.batch_update.params" 
                :key="param.name"
                :span="updateConfig.batch_update.params.length === 1 ? 24 : 12"
              >
                <el-form-item :label="param.label" :required="param.required">
                  <el-input
                    v-if="param.type === 'text'"
                    v-model="batchUpdateParams[param.name]"
                    :placeholder="param.placeholder"
                    clearable
                  />
                  <el-input-number
                    v-else-if="param.type === 'number'"
                    v-model="batchUpdateParams[param.name]"
                    :min="param.min"
                    :max="param.max"
                    :step="param.step"
                    style="width: 100%"
                  />
                  <el-select
                    v-else-if="param.type === 'select'"
                    v-model="batchUpdateParams[param.name]"
                    style="width: 100%"
                  >
                    <el-option
                      v-for="opt in param.options"
                      :key="opt.value"
                      :label="opt.label"
                      :value="opt.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-button
              type="primary"
              @click="handleBatchUpdate"
              :loading="batchUpdating"
              :disabled="!canBatchUpdate || singleUpdating || batchUpdating"
              style="width: 100%;"
            >
              批量更新
            </el-button>
          </el-card>
        </template>

        <div v-if="singleUpdating || batchUpdating" style="margin-top: 16px;">
          <el-progress 
            :percentage="progressPercentage" 
            :status="progressStatus"
            :stroke-width="15"
          />
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">
            {{ progressMessage }}
          </p>
        </div>
      </el-form>
      
      <template #footer>
        <el-button @click="apiRefreshDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 文件导入对话框 -->
    <FileImportDialog
      ref="fileImportRef"
      v-model:visible="fileImportDialogVisible"
      :importing="importing"
      @import="handleImportFile"
    />

    <!-- 远程同步对话框 -->
    <RemoteSyncDialog
      v-model:visible="remoteSyncDialogVisible"
      :collection-name="collectionName"
      :syncing="remoteSyncing"
      :sync-result="remoteSyncStats"
      @sync="handleRemoteSync"
    />

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :total-count="stats?.total_count"
      :field-count="fields.length"
      :latest-update="stats?.latest_date || stats?.latest_time"
      :data-source="currentCollectionInfo.dataSource"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import {
  CollectionPageHeader,
  CollectionDataTable,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  useFundCollection,
} from '@/components/collection'
import { useFundStore } from '@/stores/funds'
import { fundsApi } from '@/api/funds'

// 使用 composable 和 store
const {
  collectionName,
  loading,
  items,
  fields,
  page,
  pageSize,
  total,
  filterField,
  filterValue,
  sortBy,
  sortDir,
  stats,
  collectionInfo,
  apiRefreshDialogVisible,
  fileImportDialogVisible,
  remoteSyncDialogVisible,
  overviewDialogVisible,
  updateConfig,
  singleUpdateParams,
  batchUpdateParams,
  updateMode,
  singleUpdating,
  batchUpdating,
  canSingleUpdate,
  canBatchUpdate,
  progressPercentage,
  progressStatus,
  progressMessage,
  refreshing,
  importing,
  remoteSyncing,
  clearing,
  fileImportRef,
  remoteSyncStats,
  currentCollectionInfo,
  loadData,
  handleSortChange,
  exportAllData,
  handleUpdateCommand,
  loadUpdateConfig,
  handleSingleUpdate,
  handleBatchUpdate,
  handleImportFile,
  handleRemoteSync,
  handleClearData,
  cleanup,
} = useFundCollection()

const fundStore = useFundStore()

// 数据类型筛选
const activeDataType = ref<string>('all')

// 统计数据（用于显示各类型数据数量）
const allDataCount = ref(0)
const netValueCount = ref(0)
// const dividendCount = ref(0)  // 分红送配详情接口暂时有问题，已禁用

// 监听数据类型变化，更新筛选条件
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

// 加载统计数据（用于显示各类型数据数量）
const loadStats = async () => {
  try {
    // 获取全部数据统计
    const allRes = await fundsApi.getCollectionStats(collectionName.value)
    if (allRes.success && allRes.data) {
      allDataCount.value = allRes.data.total_count || 0
    }

    // 获取历史净值明细统计
    const netValueRes = await fundsApi.getCollectionData(collectionName.value, {
      page: 1,
      page_size: 1,
      filter_field: 'symbol',
      filter_value: '历史净值明细',
    })
    if (netValueRes.success && netValueRes.data) {
      netValueCount.value = netValueRes.data.total || 0
    }

    // 分红送配详情接口暂时有问题，已禁用
    // const dividendRes = await fundsApi.getCollectionData(collectionName.value, {
    //   page: 1,
    //   page_size: 1,
    //   filter_field: 'symbol',
    //   filter_value: '分红送配详情',
    // })
    // if (dividendRes.success && dividendRes.data) {
    //   dividendCount.value = dividendRes.data.total || 0
    // }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 监听数据加载完成，更新统计数据
watch([items, total], () => {
  // 当数据加载完成时，可以更新统计数据
  // 这里可以根据实际需求决定是否需要实时更新
}, { immediate: false })

onMounted(() => {
  // 加载集合列表到 store
  fundStore.loadCollections()
  loadData()
  loadStats()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;

:deep(.el-badge) {
  margin-left: 8px;
}

:deep(.el-tabs__item) {
  font-size: 14px;
}
</style>
