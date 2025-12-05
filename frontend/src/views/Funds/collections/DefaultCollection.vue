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
      <!-- 可视化分析 Tabs -->
      <el-tabs type="border-card" class="analysis-tabs" v-if="hasCharts">
        <el-tab-pane label="结构分布分析">
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">基金类型分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="typePieOption"
                  :option="typePieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无类型数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="stat-distribution-group" style="border-left: none; padding-left: 0; height: 100%; display: flex; flex-direction: column;">
                <div class="chart-title" style="margin-bottom: 12px; text-align: left;">主要构成</div>
                <div class="distribution-list" v-if="categoryDistribution.length > 0" style="max-height: 320px; overflow-y: auto; padding-right: 8px;">
                  <div v-for="item in categoryDistribution" :key="item.category" class="distribution-item">
                    <div class="dist-info">
                      <span class="dist-name">{{ item.category }}</span>
                      <span class="dist-count">{{ item.count?.toLocaleString() }} ({{ item.percentage }}%)</span>
                    </div>
                    <el-progress 
                      :percentage="Number(item.percentage)" 
                      :show-text="false" 
                      :stroke-width="6" 
                      :color="item.color"
                    />
                  </div>
                </div>
                <div v-else class="text-muted" style="text-align: center; margin-top: 20px;">暂无分类数据</div>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>

      <!-- 数据列表 -->
      <CollectionDataTable
        :data="items"
        :fields="fields"
        :total="total"
        :loading="loading"
        v-model:page="page"
        v-model:page-size="pageSize"
        :sortable="true"
        :collection-name="collectionName"
        :export-all-data="exportAllData"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="loadData"
        @page-change="() => loadData()"
        @size-change="() => loadData()"
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
              <span style="font-weight: 600;">更新</span>
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
                      v-for="(opt, optIdx) in param.options"
                      :key="`${param.name}-opt-${optIdx}`"
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
                      v-for="(opt, optIdx) in param.options"
                      :key="`${param.name}-opt-${optIdx}`"
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
import { onMounted, onUnmounted, computed } from 'vue'
// useRoute available for subcomponents
import {
  CollectionPageHeader,
  CollectionDataTable,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  useFundCollection,
} from '@/components/collection'
// ElMessage available for future use
import { useFundStore } from '@/stores/funds'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, PieChart, GridComponent, TooltipComponent, LegendComponent])

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
  sortBy: _sortBy,
  sortDir: _sortDir,
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

// 是否有图表数据
const hasCharts = computed(() => {
  return stats.value?.type_stats && stats.value.type_stats.length > 0
})

// 颜色池
const colorPalette = [
  '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
  '#36CBCB', '#975FE4', '#F2637B', '#FAD337', '#4DCB73'
]

// 基金类型分布数据
const categoryDistribution = computed(() => {
  if (!stats.value || !stats.value.type_stats) return []
  
  const total = stats.value.type_stats.reduce((sum: number, item: any) => sum + item.count, 0)
  
  return stats.value.type_stats.map((item: any, index: number) => ({
    category: item.type || '未分类',
    count: item.count,
    percentage: ((item.count / total) * 100).toFixed(1),
    color: colorPalette[index % colorPalette.length]
  })).sort((a: any, b: any) => b.count - a.count)
})

// 饼图配置
const typePieOption = computed(() => {
  if (!stats.value || !stats.value.type_stats) return null
  
  const chartData = stats.value.type_stats.map((item: any, index: number) => ({
    name: item.type || '未分类',
    value: item.count,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll'
    },
    series: [
      {
        name: '基金类型',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: chartData
      }
    ]
  }
})

// 所有状态和方法都从 composable 获取，无需重复定义

onMounted(() => {
  // 加载集合列表到 store
  fundStore.loadCollections()
  loadData()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
