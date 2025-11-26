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
              <div class="chart-title">{{ collectionName === 'fund_purchase_status' ? '基金类型分布' : '基金类型分布' }}</div>
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
        
        <!-- 基金申购状态专用Tab -->
        <el-tab-pane label="申购赎回状态" v-if="collectionName === 'fund_purchase_status'">
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">申购状态分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="purchaseStatusPieOption"
                  :option="purchaseStatusPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无申购状态数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">赎回状态分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="redeemStatusPieOption"
                  :option="redeemStatusPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无赎回状态数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- ETF实时行情专用Tab -->
        <el-tab-pane label="市场概况" v-if="collectionName === 'fund_etf_spot_em'">
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="24">
              <el-row :gutter="24">
                <el-col :span="6">
                  <div class="stat-card rise">
                    <div class="stat-label">上涨</div>
                    <div class="stat-value">{{ stats?.rise_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card fall">
                    <div class="stat-label">下跌</div>
                    <div class="stat-value">{{ stats?.fall_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card flat">
                    <div class="stat-label">平盘</div>
                    <div class="stat-value">{{ stats?.flat_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-label">总计</div>
                    <div class="stat-value">{{ stats?.total_count || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">涨跌分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="etfRiseFallPieOption"
                  :option="etfRiseFallPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">成交额TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="etfVolumeBarOption"
                  :option="etfVolumeBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- 同花顺ETF实时行情专用Tab -->
        <el-tab-pane label="市场分析" v-if="collectionName === 'fund_etf_spot_ths'">
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="24">
              <el-row :gutter="24">
                <el-col :span="6">
                  <div class="stat-card rise">
                    <div class="stat-label">上涨</div>
                    <div class="stat-value">{{ stats?.rise_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card fall">
                    <div class="stat-label">下跌</div>
                    <div class="stat-value">{{ stats?.fall_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card flat">
                    <div class="stat-label">平盘</div>
                    <div class="stat-value">{{ stats?.flat_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-label">总计</div>
                    <div class="stat-value">{{ stats?.total_count || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="12">
              <div class="chart-title">涨跌分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsRiseFallPieOption"
                  :option="thsRiseFallPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">基金类型分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsTypePieOption"
                  :option="thsTypePieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">涨幅TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsGainersBarOption"
                  :option="thsGainersBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">跌幅TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsLosersBarOption"
                  :option="thsLosersBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- LOF基金实时行情专用Tab -->
        <el-tab-pane label="市场行情" v-if="collectionName === 'fund_lof_spot_em'">
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="24">
              <el-row :gutter="24">
                <el-col :span="6">
                  <div class="stat-card rise">
                    <div class="stat-label">上涨</div>
                    <div class="stat-value">{{ stats?.rise_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card fall">
                    <div class="stat-label">下跌</div>
                    <div class="stat-value">{{ stats?.fall_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card flat">
                    <div class="stat-label">平盘</div>
                    <div class="stat-value">{{ stats?.flat_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-label">总计</div>
                    <div class="stat-value">{{ stats?.total_count || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="12">
              <div class="chart-title">涨跌分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofRiseFallPieOption"
                  :option="lofRiseFallPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">成交额TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofVolumeBarOption"
                  :option="lofVolumeBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">涨幅TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofGainersBarOption"
                  :option="lofGainersBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">市值分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofMarketCapPieOption"
                  :option="lofMarketCapPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
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
        :page="page"
        :page-size="pageSize"
        :sortable="true"
        :fetch-all-data="fetchAllDataForExport"
        :collection-name="collectionName"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="loadData"
        @page-change="loadData"
        @size-change="loadData"
        @sort-change="handleSortChange"
      >
        <!-- 额外筛选器 -->
        <template #extra-filters>
          <el-select
            v-if="collectionName === 'fund_info_index_em'"
            v-model="filterCompany"
            placeholder="基金公司"
            style="width: 150px; margin-right: 8px;"
            clearable
            filterable
            @change="handleFilterChange('company', $event)"
          >
            <el-option label="全部基金公司" value="全部" />
            <el-option v-for="company in companyOptions" :key="company" :label="company" :value="company" />
          </el-select>
        </template>

        <!-- 指数型基金筛选栏 (表格前内容) -->
        <template #before-table v-if="collectionName === 'fund_info_index_em'">
          <div class="filter-section">
            <div class="filter-row">
              <span class="filter-label">跟踪标的：</span>
              <div class="filter-options">
                <span 
                  v-for="opt in targetOptions" 
                  :key="opt" 
                  class="filter-option" 
                  :class="{ active: filterTarget === opt }"
                  @click="handleFilterChange('target', opt)"
                >
                  {{ opt }}
                </span>
              </div>
            </div>
            <div class="filter-row" style="margin-top: 10px;">
              <span class="filter-label">跟踪方式：</span>
              <div class="filter-options">
                <span 
                  v-for="opt in methodOptions" 
                  :key="opt" 
                  class="filter-option" 
                  :class="{ active: filterMethod === opt }"
                  @click="handleFilterChange('method', opt)"
                >
                  {{ opt }}
                </span>
              </div>
            </div>
            <el-divider style="margin: 15px 0;" />
          </div>
        </template>
      </CollectionDataTable>
    </div>

    <!-- API更新对话框（动态配置版） -->
    <el-dialog
      v-model="apiRefreshDialogVisible"
      title="API更新"
      width="650px"
      :close-on-click-modal="false"
      @open="loadUpdateConfig"
    >
      <el-form label-width="100px" v-loading="!updateConfig">
        <!-- 集合名称 -->
        <el-form-item label="集合名称">
          <el-input :value="updateConfig?.display_name || collectionName" disabled />
        </el-form-item>

        <!-- 单条更新区域 -->
        <template v-if="updateConfig?.single_update?.enabled">
          <el-card shadow="never" style="margin-bottom: 16px;">
            <template #header>
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600;">更新</span>
              </div>
            </template>
            <div v-if="updateConfig.single_update.description" style="color: #909399; font-size: 12px; margin-bottom: 12px;">
              {{ updateConfig.single_update.description }}
            </div>
            <!-- 动态参数 -->
            <el-row :gutter="16" v-if="updateConfig.single_update.params?.length">
              <el-col 
                v-for="param in updateConfig.single_update.params" 
                :key="param.name"
                :span="updateConfig.single_update.params.length === 1 ? 24 : 12"
              >
                <el-form-item :label="param.label" :required="param.required">
                  <!-- 文本输入 -->
                  <el-input
                    v-if="param.type === 'text'"
                    v-model="singleUpdateParams[param.name]"
                    :placeholder="param.placeholder"
                    clearable
                  />
                  <!-- 数字输入 -->
                  <el-input-number
                    v-else-if="param.type === 'number'"
                    v-model="singleUpdateParams[param.name]"
                    :min="param.min"
                    :max="param.max"
                    :step="param.step"
                    style="width: 100%"
                  />
                  <!-- 下拉选择 -->
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
            <div v-else style="color: #909399; font-size: 13px; margin-bottom: 12px;">
              无需参数，直接点击更新
            </div>
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

        <!-- 批量更新区域 -->
        <template v-if="updateConfig?.batch_update?.enabled">
          <el-card shadow="never" style="margin-bottom: 16px;">
            <template #header>
              <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600;">批量更新</span>
              </div>
            </template>
            <div v-if="updateConfig.batch_update.description" style="color: #909399; font-size: 12px; margin-bottom: 12px;">
              {{ updateConfig.batch_update.description }}
            </div>
            <!-- 动态参数 -->
            <el-row :gutter="16" v-if="updateConfig.batch_update.params?.length">
              <el-col 
                v-for="param in updateConfig.batch_update.params" 
                :key="param.name"
                :span="updateConfig.batch_update.params.length === 1 ? 24 : 12"
              >
                <el-form-item :label="param.label" :required="param.required">
                  <!-- 文本输入 -->
                  <el-input
                    v-if="param.type === 'text'"
                    v-model="batchUpdateParams[param.name]"
                    :placeholder="param.placeholder"
                    clearable
                  />
                  <!-- 数字输入 -->
                  <el-input-number
                    v-else-if="param.type === 'number'"
                    v-model="batchUpdateParams[param.name]"
                    :min="param.min"
                    :max="param.max"
                    :step="param.step"
                    style="width: 100%"
                  />
                  <!-- 下拉选择 -->
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
            <div v-else style="color: #909399; font-size: 13px; margin-bottom: 12px;">
              无需参数，直接点击批量更新
            </div>
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

        <!-- 进度显示 -->
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
        
        <!-- 更新说明 -->
        <el-alert
          v-if="updateConfig?.update_description"
          title="更新说明"
          type="warning"
          :closable="false"
          style="margin-top: 16px;"
        >
          <template #default>
            <div style="font-size: 12px; line-height: 1.6;">
              {{ updateConfig.update_description }}
            </div>
          </template>
        </el-alert>
      </el-form>
      
      <template #footer>
        <el-button @click="apiRefreshDialogVisible = false">
          关闭
        </el-button>
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
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
// import { Search, QuestionFilled } from '@element-plus/icons-vue'
import {
  CollectionPageHeader,
  CollectionDataTable,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  type RemoteSyncConfig,
} from '@/components/collection'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fundsApi } from '@/api/funds'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
// import dayjs from 'dayjs'

use([CanvasRenderer, PieChart, GridComponent, TooltipComponent, LegendComponent])

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)

// 数据状态
const loading = ref(false)
const items = ref<any[]>([])
const fields = ref<Array<{ name: string; type: string; example: string | null }>>([])
const page = ref(1)
const pageSize = ref(50)
const total = ref(0)

// 过滤条件
const filterField = ref('')
const filterValue = ref('')

// 指数型基金筛选
const filterTarget = ref('全部')
const filterMethod = ref('全部')
const targetOptions = [
  '全部', '沪深指数', '行业主题', '大盘指数', '中盘指数', '小盘指数', '股票指数', '债券指数'
]
const methodOptions = [
  '全部', '被动指数型', '增强指数型'
]
// const filterAbnormal = ref(true) // 已移除
const filterCompany = ref('全部')
const companyOptions = ref<string[]>([])

const loadCompanies = async () => {
  try {
    const res = await fundsApi.getFundCompanies()
    if (res.success && res.data) {
      companyOptions.value = res.data
    }
  } catch (e) {
    console.error('加载基金公司列表失败:', e)
  }
}

const handleFilterChange = (type: 'target' | 'method' | 'company', value: string) => {
  if (type === 'target') {
    filterTarget.value = value
  } else if (type === 'method') {
    filterMethod.value = value
  } else if (type === 'company') {
    filterCompany.value = value
  }
  page.value = 1 // 重置页码
  loadData()
}

// 排序条件
const sortBy = ref('')
const sortDir = ref<'asc' | 'desc'>('desc')

// 统计数据
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)

// 是否有图表数据
const hasCharts = computed(() => {
  // fund_purchase_status 有申购赎回状态图表
  if (collectionName.value === 'fund_purchase_status') {
    return stats.value && (stats.value.purchase_status_stats || stats.value.redeem_status_stats)
  }
  // fund_etf_spot_em 有涨跌分布和成交额TOP图表
  if (collectionName.value === 'fund_etf_spot_em') {
    return stats.value && stats.value.total_count > 0
  }
  // fund_etf_spot_ths 有涨跌分布、基金类型、涨跌幅TOP、申赎状态图表
  if (collectionName.value === 'fund_etf_spot_ths') {
    return stats.value && stats.value.total_count > 0
  }
  // fund_lof_spot_em 有涨跌分布、成交额TOP、涨跌幅TOP、市值分布图表
  if (collectionName.value === 'fund_lof_spot_em') {
    return stats.value && stats.value.total_count > 0
  }
  // fund_spot_sina 有涨跌分布、基金类型、成交额TOP、涨跌幅TOP图表
  if (collectionName.value === 'fund_spot_sina') {
    return stats.value && stats.value.total_count > 0
  }
  // 其他集合有type_stats图表
  return stats.value && stats.value.type_stats && stats.value.type_stats.length > 0
})

// 颜色池
const colorPalette = [
  '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
  '#36CBCB', '#975FE4', '#F2637B', '#FAD337', '#4DCB73'
]

// 基金类型分布数据 - Progress Bar
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

// 申购状态饼图配置
const purchaseStatusPieOption = computed(() => {
  if (!stats.value || !stats.value.purchase_status_stats) return null
  
  const chartData = stats.value.purchase_status_stats.map((item: any, index: number) => ({
    name: item.status || '未知',
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
        name: '申购状态',
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

// 赎回状态饼图配置
const redeemStatusPieOption = computed(() => {
  if (!stats.value || !stats.value.redeem_status_stats) return null
  
  const chartData = stats.value.redeem_status_stats.map((item: any, index: number) => ({
    name: item.status || '未知',
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
        name: '赎回状态',
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

// ETF涨跌分布饼图配置
const etfRiseFallPieOption = computed(() => {
  if (!stats.value || stats.value.total_count === 0) return null
  
  const chartData = [
    {
      name: '上涨',
      value: stats.value.rise_count || 0,
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '下跌',
      value: stats.value.fall_count || 0,
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '平盘',
      value: stats.value.flat_count || 0,
      itemStyle: { color: '#909399' }
    }
  ]
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '涨跌分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
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
        data: chartData
      }
    ]
  }
})

// ETF成交额TOP10柱状图配置
const etfVolumeBarOption = computed(() => {
  if (!stats.value || !stats.value.top_volume || stats.value.top_volume.length === 0) return null
  
  const names = stats.value.top_volume.map((item: any) => item.name || item.code)
  const volumes = stats.value.top_volume.map((item: any) => (item.volume / 100000000).toFixed(2)) // 转换为亿元
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>成交额: ${item.value}亿元`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '成交额(亿元)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 8 ? value.substring(0, 8) + '...' : value
        }
      }
    },
    series: [
      {
        name: '成交额',
        type: 'bar',
        data: volumes,
        itemStyle: {
          color: '#409EFF',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}亿'
        }
      }
    ]
  }
})

// 同花顺ETF涨跌分布饼图配置
const thsRiseFallPieOption = computed(() => {
  if (!stats.value || stats.value.total_count === 0) return null
  
  const chartData = [
    {
      name: '上涨',
      value: stats.value.rise_count || 0,
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '下跌',
      value: stats.value.fall_count || 0,
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '平盘',
      value: stats.value.flat_count || 0,
      itemStyle: { color: '#909399' }
    }
  ]
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '涨跌分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
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
        data: chartData
      }
    ]
  }
})

// 同花顺ETF基金类型分布饼图配置
const thsTypePieOption = computed(() => {
  if (!stats.value || !stats.value.type_stats || stats.value.type_stats.length === 0) return null
  
  const chartData = stats.value.type_stats.map((item: any, index: number) => ({
    name: item.type || '未知',
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
        data: chartData
      }
    ]
  }
})

// 同花顺ETF涨幅TOP10柱状图配置
const thsGainersBarOption = computed(() => {
  if (!stats.value || !stats.value.top_gainers || stats.value.top_gainers.length === 0) return null
  
  const names = stats.value.top_gainers.map((item: any) => item.name || item.code)
  const rates = stats.value.top_gainers.map((item: any) => item.rate)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>涨幅: ${item.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '涨幅(%)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 8 ? value.substring(0, 8) + '...' : value
        }
      }
    },
    series: [
      {
        name: '涨幅',
        type: 'bar',
        data: rates,
        itemStyle: {
          color: '#F56C6C',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }
})

// 同花顺ETF跌幅TOP10柱状图配置
const thsLosersBarOption = computed(() => {
  if (!stats.value || !stats.value.top_losers || stats.value.top_losers.length === 0) return null
  
  const names = stats.value.top_losers.map((item: any) => item.name || item.code)
  const rates = stats.value.top_losers.map((item: any) => item.rate)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>跌幅: ${item.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '跌幅(%)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 8 ? value.substring(0, 8) + '...' : value
        }
      }
    },
    series: [
      {
        name: '跌幅',
        type: 'bar',
        data: rates,
        itemStyle: {
          color: '#67C23A',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }
})

// LOF基金涨跌分布饼图配置
const lofRiseFallPieOption = computed(() => {
  if (!stats.value || stats.value.total_count === 0) return null
  
  const chartData = [
    {
      name: '上涨',
      value: stats.value.rise_count || 0,
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '下跌',
      value: stats.value.fall_count || 0,
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '平盘',
      value: stats.value.flat_count || 0,
      itemStyle: { color: '#909399' }
    }
  ]
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '涨跌分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
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
        data: chartData
      }
    ]
  }
})

// LOF基金成交额TOP10柱状图配置
const lofVolumeBarOption = computed(() => {
  if (!stats.value || !stats.value.top_volume || stats.value.top_volume.length === 0) return null
  
  const names = stats.value.top_volume.map((item: any) => item.name || item.code)
  const amounts = stats.value.top_volume.map((item: any) => (item.amount / 100000000).toFixed(2))
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>成交额: ${item.value}亿`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '成交额(亿)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 10 ? value.substring(0, 10) + '...' : value
        }
      }
    },
    series: [
      {
        name: '成交额',
        type: 'bar',
        data: amounts,
        itemStyle: {
          color: '#409EFF',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}亿'
        }
      }
    ]
  }
})

// LOF基金涨幅TOP10柱状图配置
const lofGainersBarOption = computed(() => {
  if (!stats.value || !stats.value.top_gainers || stats.value.top_gainers.length === 0) return null
  
  const names = stats.value.top_gainers.map((item: any) => item.name || item.code)
  const rates = stats.value.top_gainers.map((item: any) => item.rate)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>涨幅: ${item.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '涨幅(%)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 10 ? value.substring(0, 10) + '...' : value
        }
      }
    },
    series: [
      {
        name: '涨幅',
        type: 'bar',
        data: rates,
        itemStyle: {
          color: '#F56C6C',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }
})

// LOF基金市值分布饼图配置
const lofMarketCapPieOption = computed(() => {
  if (!stats.value || !stats.value.market_cap_stats || stats.value.market_cap_stats.length === 0) return null
  
  const chartData = stats.value.market_cap_stats.map((item: any, index: number) => ({
    name: item.range || '未知',
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
      left: 'left'
    },
    series: [
      {
        name: '市值分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
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
        data: chartData
      }
    ]
  }
})

// 更新数据相关 - 三个独立对话框
const apiRefreshDialogVisible = ref(false)  // API更新对话框
const fileImportDialogVisible = ref(false)  // 文件导入对话框
const remoteSyncDialogVisible = ref(false)  // 远程同步对话框
const refreshing = ref(false)
const currentTaskId = ref('')
const progressPercentage = ref(0)
const progressStatus = ref<'success' | 'exception' | 'warning' | ''>('')
const progressMessage = ref('')
let progressTimer: NodeJS.Timeout | null = null

// 更新配置（从后端获取）
const updateConfig = ref<any>(null)
const singleUpdateParams = ref<Record<string, any>>({})
const batchUpdateParams = ref<Record<string, any>>({})
const singleUpdating = ref(false)
const batchUpdating = ref(false)

// 批量更新配置（兼容旧代码）
const batchSize = ref(50)
const concurrency = ref(3)
const delay = ref(0.1)
const singleFundCode = ref('')
const singleYear = ref('')
const batchYear = ref('')  // fund_portfolio_hold_em 的批量更新年份参数
const singleDate = ref('')  // fund_individual_detail_hold_xq 的日期参数
const fundValueSymbol = ref('全部')  // fund_value_estimation_em 的基金类型参数

// 指数型基金更新参数
const indexSymbol = ref('全部')

// 新浪基金类型选择
const selectedFundType = ref('全部')
const indexIndicator = ref('全部')
// ETF/LOF分时行情参数 - 单个更新
const singleSymbol = ref('')
const singlePeriod = ref('5')
const singleAdjust = ref('hfq')

// ETF/LOF分时行情参数 - 批量更新
const batchPeriod = ref('5')
const batchAdjust = ref('hfq')
const batchConcurrency = ref(5)

// 文件导入相关
const fileImportRef = ref()
const importing = ref(false)

// 远程同步相关
const remoteSyncing = ref(false)
const remoteSyncStats = ref<any>(null)

// 清空数据相关
const clearing = ref(false)

// 数据概览对话框
const overviewDialogVisible = ref(false)

// 集合固定信息映射
const collectionStaticInfo: Record<string, any> = {
  fund_name_em: {
    name: 'fund_name_em',
    displayName: '基金基本信息',
    fieldCount: 5,
    dataSource: 'http://fund.eastmoney.com/fund.html'
  },
  fund_basic_info: {
    name: 'fund_basic_info',
    displayName: '雪球基金基本信息',
    fieldCount: 10,
    dataSource: 'https://xueqiu.com/'
  },
  fund_info_index_em: {
    name: 'fund_info_index_em',
    displayName: '指数型基金基本信息',
    fieldCount: 18,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_purchase_status: {
    name: 'fund_purchase_status',
    displayName: '基金申购状态',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_spot_em: {
    name: 'fund_etf_spot_em',
    displayName: 'ETF基金实时行情-东财',
    fieldCount: 37,
    dataSource: 'https://quote.eastmoney.com/center/gridlist.html#fund_etf'
  },
  fund_etf_spot_ths: {
    name: 'fund_etf_spot_ths',
    displayName: 'ETF基金实时行情-同花顺',
    fieldCount: 15,
    dataSource: 'http://q.10jqka.com.cn/'
  },
  fund_lof_spot_em: {
    name: 'fund_lof_spot_em',
    displayName: 'LOF基金实时行情-东财',
    fieldCount: 15,
    dataSource: 'https://quote.eastmoney.com/center/gridlist.html#fund_lof'
  },
  fund_spot_sina: {
    name: 'fund_spot_sina',
    displayName: '基金实时行情-新浪',
    fieldCount: 15,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_etf_hist_min_em: {
    name: 'fund_etf_hist_min_em',
    displayName: 'ETF基金分时行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/sz159707.html'
  },
  fund_lof_hist_min_em: {
    name: 'fund_lof_hist_min_em',
    displayName: 'LOF基金分时行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_etf_hist_em: {
    name: 'fund_etf_hist_em',
    displayName: 'ETF基金历史行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_lof_hist_em: {
    name: 'fund_lof_hist_em',
    displayName: 'LOF基金历史行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_hist_sina: {
    name: 'fund_hist_sina',
    displayName: '基金历史行情-新浪',
    fieldCount: 7,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_open_fund_daily_em: {
    name: 'fund_open_fund_daily_em',
    displayName: '开放式基金实时行情-东方财富',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1'
  },
  fund_open_fund_info_em: {
    name: 'fund_open_fund_info_em',
    displayName: '开放式基金历史行情-东方财富',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_money_fund_daily_em: {
    name: 'fund_money_fund_daily_em',
    displayName: '货币型基金实时行情-东方财富',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_money_fund_info_em: {
    name: 'fund_money_fund_info_em',
    displayName: '货币型基金历史行情-东方财富',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_financial_fund_daily_em: {
    name: 'fund_financial_fund_daily_em',
    displayName: '理财型基金实时行情-东方财富',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_financial_fund_info_em: {
    name: 'fund_financial_fund_info_em',
    displayName: '理财型基金历史行情-东方财富',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_graded_fund_daily_em: {
    name: 'fund_graded_fund_daily_em',
    displayName: '分级基金实时数据-东方财富',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_fund_daily_em: {
    name: 'fund_etf_fund_daily_em',
    displayName: '场内交易基金实时数据-东方财富',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_graded_fund_info_em: {
    name: 'fund_graded_fund_info_em',
    displayName: '分级基金历史数据-东方财富',
    fieldCount: 8,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_hk_hist_em: {
    name: 'fund_hk_hist_em',
    displayName: '香港基金-历史数据',
    fieldCount: 13,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_fund_info_em: {
    name: 'fund_etf_fund_info_em',
    displayName: '场内交易基金-历史行情',
    fieldCount: 8,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_dividend_sina: {
    name: 'fund_etf_dividend_sina',
    displayName: '基金累计分红-新浪',
    fieldCount: 6,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_fh_em: {
    name: 'fund_fh_em',
    displayName: '基金分红-东财',
    fieldCount: 8,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_cf_em: {
    name: 'fund_cf_em',
    displayName: '基金拆分-东方财富',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_fh_rank_em: {
    name: 'fund_fh_rank_em',
    displayName: '基金分红排行-东方财富',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_open_fund_rank_em: {
    name: 'fund_open_fund_rank_em',
    displayName: '开放式基金排行-东方财富',
    fieldCount: 22,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_exchange_rank_em: {
    name: 'fund_exchange_rank_em',
    displayName: '场内交易基金排行-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_money_rank_em: {
    name: 'fund_money_rank_em',
    displayName: '货币型基金排行-东财',
    fieldCount: 23,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_lcx_rank_em: {
    name: 'fund_lcx_rank_em',
    displayName: '理财基金排行-东财',
    fieldCount: 22,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_hk_rank_em: {
    name: 'fund_hk_rank_em',
    displayName: '香港基金排行-东财',
    fieldCount: 23,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_individual_achievement_xq: {
    name: 'fund_individual_achievement_xq',
    displayName: '基金业绩-雪球',
    fieldCount: 12,
    dataSource: 'https://xueqiu.com/'
  },
  fund_value_estimation_em: {
    name: 'fund_value_estimation_em',
    displayName: '净值估算-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_individual_analysis_xq: {
    name: 'fund_individual_analysis_xq',
    displayName: '基金数据分析-雪球',
    fieldCount: 11,
    dataSource: 'https://xueqiu.com/'
  },
  fund_individual_profit_probability_xq: {
    name: 'fund_individual_profit_probability_xq',
    displayName: '基金盈利概率-雪球',
    fieldCount: 9,
    dataSource: 'https://xueqiu.com/'
  },
  fund_individual_detail_hold_xq: {
    name: 'fund_individual_detail_hold_xq',
    displayName: '基金持仓资产比例-雪球',
    fieldCount: 11,
    dataSource: 'https://xueqiu.com/'
  },
  fund_overview_em: {
    name: 'fund_overview_em',
    displayName: '基金基本概况-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_fee_em: {
    name: 'fund_fee_em',
    displayName: '基金交易费率-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_individual_detail_info_xq: {
    name: 'fund_individual_detail_info_xq',
    displayName: '基金交易规则-雪球',
    fieldCount: 14,
    dataSource: 'https://xueqiu.com/'
  },
  fund_portfolio_hold_em: {
    name: 'fund_portfolio_hold_em',
    displayName: '基金持仓-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_portfolio_bond_hold_em: {
    name: 'fund_portfolio_bond_hold_em',
    displayName: '债券持仓-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_portfolio_industry_allocation_em: {
    name: 'fund_portfolio_industry_allocation_em',
    displayName: '行业配置-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_portfolio_change_em: {
    name: 'fund_portfolio_change_em',
    displayName: '重大变动-东财',
    fieldCount: 16,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_all_em: {
    name: 'fund_rating_all_em',
    displayName: '基金评级总汇-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_sh_em: {
    name: 'fund_rating_sh_em',
    displayName: '上海证券评级-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_zs_em: {
    name: 'fund_rating_zs_em',
    displayName: '招商证券评级-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_ja_em: {
    name: 'fund_rating_ja_em',
    displayName: '济安金信评级-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_manager_em: {
    name: 'fund_manager_em',
    displayName: '基金经理-东财',
    fieldCount: 13,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_new_found_em: {
    name: 'fund_new_found_em',
    displayName: '新发基金-东财',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_scale_open_sina: {
    name: 'fund_scale_open_sina',
    displayName: '开放式基金规模-新浪',
    fieldCount: 12,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_scale_close_sina: {
    name: 'fund_scale_close_sina',
    displayName: '封闭式基金规模-新浪',
    fieldCount: 12,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_scale_structured_sina: {
    name: 'fund_scale_structured_sina',
    displayName: '分级子基金规模-新浪',
    fieldCount: 12,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_aum_em: {
    name: 'fund_aum_em',
    displayName: '基金规模详情-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_aum_trend_em: {
    name: 'fund_aum_trend_em',
    displayName: '基金规模走势-东财',
    fieldCount: 11,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_aum_hist_em: {
    name: 'fund_aum_hist_em',
    displayName: '基金公司历年管理规模-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  reits_realtime_em: {
    name: 'reits_realtime_em',
    displayName: 'REITs实时行情-东财',
    fieldCount: 17,
    dataSource: 'https://quote.eastmoney.com/'
  },
  reits_hist_em: {
    name: 'reits_hist_em',
    displayName: 'REITs历史行情-东财',
    fieldCount: 12,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_report_stock_cninfo: {
    name: 'fund_report_stock_cninfo',
    displayName: '基金重仓股-巨潮',
    fieldCount: 15,
    dataSource: 'http://www.cninfo.com.cn/'
  },
  fund_report_industry_allocation_cninfo: {
    name: 'fund_report_industry_allocation_cninfo',
    displayName: '基金行业配置-巨潮',
    fieldCount: 15,
    dataSource: 'http://www.cninfo.com.cn/'
  },
  fund_report_asset_allocation_cninfo: {
    name: 'fund_report_asset_allocation_cninfo',
    displayName: '基金资产配置-巨潮',
    fieldCount: 13,
    dataSource: 'http://www.cninfo.com.cn/'
  },
  fund_scale_change_em: {
    name: 'fund_scale_change_em',
    displayName: '规模变动-东财',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_hold_structure_em: {
    name: 'fund_hold_structure_em',
    displayName: '持有人结构-东财',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_stock_position_lg: {
    name: 'fund_stock_position_lg',
    displayName: '股票型基金仓位-乐咕乐股',
    fieldCount: 5,
    dataSource: 'https://www.legulegu.com/'
  },
  fund_balance_position_lg: {
    name: 'fund_balance_position_lg',
    displayName: '平衡混合型基金仓位-乐咕乐股',
    fieldCount: 5,
    dataSource: 'https://www.legulegu.com/'
  },
  fund_linghuo_position_lg: {
    name: 'fund_linghuo_position_lg',
    displayName: '灵活配置型基金仓位-乐咕乐股',
    fieldCount: 5,
    dataSource: 'https://www.legulegu.com/'
  },
  fund_announcement_dividend_em: {
    name: 'fund_announcement_dividend_em',
    displayName: '基金公告分红配送-东财',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_announcement_report_em: {
    name: 'fund_announcement_report_em',
    displayName: '基金公告定期报告-东财',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_announcement_personnel_em: {
    name: 'fund_announcement_personnel_em',
    displayName: '基金公告人事调整-东财',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  }
}

// 获取当前集合的固定信息
const currentCollectionInfo = computed(() => {
  return collectionStaticInfo[collectionName.value] || {
    name: collectionName.value,
    displayName: collectionInfo.value?.display_name || collectionName.value,
    fieldCount: fields.value.length,
    dataSource: '暂无'
  }
})

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载集合信息
    const collectionsRes = await fundsApi.getCollections()
    if (collectionsRes.success && collectionsRes.data) {
      collectionInfo.value = collectionsRes.data.find((c: any) => c.name === collectionName.value)
    }

    // 加载统计数据
    const statsRes = await fundsApi.getCollectionStats(collectionName.value)
    if (statsRes.success && statsRes.data) {
      stats.value = statsRes.data
    }

    // 加载数据
    const dataRes = await fundsApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
      tracking_target: collectionName.value === 'fund_info_index_em' ? filterTarget.value : undefined,
      tracking_method: collectionName.value === 'fund_info_index_em' ? filterMethod.value : undefined,
      fund_company: collectionName.value === 'fund_info_index_em' ? filterCompany.value : undefined,
    })
    
    if (dataRes.success && dataRes.data) {
      items.value = dataRes.data.items || []
      
      // 调整字段顺序：将系统字段移到最后
      const allFields = dataRes.data.fields || []
      const metaFields = ['code', 'endpoint', 'source', 'updated_at']
      const mainFields = allFields.filter((f: any) => !metaFields.includes(f.name))
      const metaFieldsData = allFields.filter((f: any) => metaFields.includes(f.name))
      fields.value = [...mainFields, ...metaFieldsData]
      
      total.value = dataRes.data.total || 0
    } else {
      ElMessage.error('加载数据失败')
    }
  } catch (error: any) {
    console.error('加载数据失败:', error)
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 排序处理
const handleSortChange = ({ prop, order }: any) => {
  if (!order) {
    sortBy.value = ''
    sortDir.value = 'desc'
  } else {
    sortBy.value = prop
    sortDir.value = order === 'ascending' ? 'asc' : 'desc'
  }
  loadData()
}

// 获取全部数据用于导出（分页获取）
const fetchAllDataForExport = async (): Promise<any[]> => {
  const allData: any[] = []
  const batchSize = 500 // 后端限制最大 500
  let currentPage = 1
  let hasMore = true
  
  while (hasMore) {
    const res = await fundsApi.getCollectionData(collectionName.value, {
      page: currentPage,
      page_size: batchSize,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    
    if (!res.success) {
      throw new Error(res.message || '获取数据失败')
    }
    
    const items = res.data?.items || []
    allData.push(...items)
    
    // 检查是否还有更多数据
    const totalItems = res.data?.total || 0
    hasMore = allData.length < totalItems && items.length === batchSize
    currentPage++
    
    // 安全限制，防止无限循环
    if (currentPage > 1000) break
  }
  
  return allData
}

// 处理下拉菜单命令
const handleUpdateCommand = (command: string) => {
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = ''
  
  switch(command) {
    case 'api':
      apiRefreshDialogVisible.value = true
      break
    case 'file':
      fileImportDialogVisible.value = true
      break
    case 'remote':
      remoteSyncDialogVisible.value = true
      break
  }
}

// 更新数据（旧版，保留供参考）
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const refreshData = async (mode: string = 'batch') => {
  // 支持的自动更新集合列表
  const supportedCollections = [
    'fund_name_em', 'fund_basic_info', 'fund_info_index_em', 'fund_purchase_status',
    'fund_etf_spot_em', 'fund_etf_spot_ths', 'fund_lof_spot_em', 'fund_spot_sina',
    'fund_etf_hist_min_em', 'fund_etf_hist_em', 'fund_lof_hist_em', 'fund_hist_sina',
    'fund_open_fund_daily_em', 'fund_open_fund_info_em', 'fund_money_fund_daily_em',
    'fund_money_fund_info_em', 'fund_financial_fund_daily_em', 'fund_financial_fund_info_em',
    'fund_graded_fund_daily_em', 'fund_etf_fund_daily_em', 'fund_etf_fund_info_em',
    'fund_etf_dividend_sina', 'fund_fh_em', 'fund_cf_em', 'fund_fh_rank_em',
    'fund_open_fund_rank_em', 'fund_exchange_rank_em', 'fund_money_rank_em', 'fund_hk_rank_em',
    'fund_individual_achievement_xq', 'fund_value_estimation_em', 'fund_individual_analysis_xq',
    'fund_individual_profit_probability_xq', 'fund_individual_detail_hold_xq', 'fund_overview_em',
    'fund_portfolio_hold_em', 'fund_portfolio_bond_hold_em', 'fund_portfolio_change_em'
  ]
  if (!supportedCollections.includes(collectionName.value)) {
    ElMessage.warning('该集合暂不支持自动更新')
    return
  }

  // 智能判断模式：如果输入了单个代码，自动使用single模式（仅针对按基金代码的集合）
  let actualMode = mode
  if (mode === 'batch') {
    // 对于支持单个更新的集合，如果输入了单个代码，自动切换为single模式
    const singleUpdateCollections = [
      'fund_open_fund_info_em', 'fund_money_fund_info_em', 'fund_financial_fund_info_em',
      'fund_etf_fund_info_em', 'fund_etf_dividend_sina', 'fund_individual_achievement_xq',
      'fund_individual_analysis_xq', 'fund_individual_profit_probability_xq',
      'fund_individual_detail_hold_xq', 'fund_overview_em',
      'fund_portfolio_hold_em', 'fund_portfolio_bond_hold_em', 'fund_portfolio_change_em'
    ]
    
    // fund_individual_detail_hold_xq 需要同时检查基金代码和日期
    if (collectionName.value === 'fund_individual_detail_hold_xq') {
      if (singleFundCode.value && singleDate.value) {
        actualMode = 'single'
      }
    } else if (collectionName.value === 'fund_portfolio_bond_hold_em' || collectionName.value === 'fund_portfolio_change_em') {
      // 持仓 / 债券持仓 / 重大变动 需要同时检查基金代码和年份才是单个更新
      if (singleFundCode.value && singleYear.value) {
        actualMode = 'single'
      }
      // 如果只有年份，保持批量更新模式
    } else if (singleUpdateCollections.includes(collectionName.value) && singleFundCode.value) {
      actualMode = 'single'
    }
  }

  refreshing.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  
  try {
    // 构建参数
    const params: any = {}
    
    // ETF/LOF分时行情的参数处理
    if (collectionName.value === 'fund_etf_hist_min_em' || collectionName.value === 'fund_lof_hist_min_em') {
      if (actualMode === 'single') {
        // 单个更新模式
        if (!singleSymbol.value) {
          ElMessage.warning('请输入基金代码')
          refreshing.value = false
          return
        }
        params.symbol = singleSymbol.value
        params.period = singlePeriod.value
        params.adjust = singleAdjust.value
      } else {
        // 批量更新模式
        params.period = batchPeriod.value
        params.adjust = batchAdjust.value
        params.concurrency = batchConcurrency.value
      }
    }
    if (collectionName.value === 'fund_basic_info') {
      if (actualMode === 'single' && singleFundCode.value) {
        params.fund_code = singleFundCode.value
      } else {
        params.batch_size = batchSize.value
        params.concurrency = concurrency.value
        params.delay = delay.value
      }
    } else if (collectionName.value === 'fund_info_index_em') {
      params.symbol = indexSymbol.value || '全部'
      params.indicator = indexIndicator.value || '全部'
    } else if (collectionName.value === 'fund_spot_sina') {
      params.symbol = selectedFundType.value || '全部'
    } else if (collectionName.value === 'fund_open_fund_info_em') {
      if (actualMode === 'single' && singleFundCode.value) {
        params.fund_code = singleFundCode.value
      } else {
        // 批量更新模式
        params.concurrency = concurrency.value
      }
    } else if (collectionName.value === 'fund_money_fund_info_em') {
      if (actualMode === 'single' && singleFundCode.value) {
        params.symbol = singleFundCode.value
      } else {
        // 批量更新模式
        params.concurrency = concurrency.value
      }
    } else if (collectionName.value === 'fund_financial_fund_info_em') {
      if (actualMode === 'single' && singleFundCode.value) {
        params.symbol = singleFundCode.value
      } else {
        // 批量更新模式
        params.concurrency = concurrency.value
      }
    } else if (collectionName.value === 'fund_etf_fund_info_em') {
      if (actualMode === 'single' && singleFundCode.value) {
        params.symbol = singleFundCode.value
      } else {
        // 批量更新模式
        params.concurrency = concurrency.value
      }
    } else if (collectionName.value === 'fund_etf_dividend_sina') {
      if (actualMode === 'single' && singleFundCode.value) {
        // 单个更新：传入 symbol（如 sh510050）到后端的 fund_code 参数
        params.fund_code = singleFundCode.value
        params.batch_update = false
      } else {
        // 批量更新模式：从 fund_name_em 获取代码列表
        params.batch_update = true
        params.batch_size = batchSize.value
        params.concurrency = concurrency.value
      }
    } else if (collectionName.value === 'fund_individual_achievement_xq') {
      if (actualMode === 'single' && singleFundCode.value) {
        // 单个更新：传入基金代码到后端的 fund_code 参数
        params.fund_code = singleFundCode.value
      } else {
        // 批量更新模式：从 fund_basic_info 获取代码列表，并发更新
        params.batch = true
        params.limit = batchSize.value
        params.concurrency = concurrency.value
      }
    } else if (String(collectionName.value) === 'fund_value_estimation_em') {
      // 净值估算：传入基金类型参数
      params.symbol = fundValueSymbol.value
    } else if (String(collectionName.value) === 'fund_individual_analysis_xq') {
      if (actualMode === 'single' && singleFundCode.value) {
        // 单个更新：传入基金代码到后端的 fund_code 参数
        params.fund_code = singleFundCode.value
      } else {
        // 批量更新模式：从 fund_name_em 获取代码列表，并发更新
        params.batch = true
        params.limit = batchSize.value
        params.concurrency = concurrency.value
      }
    } else if (String(collectionName.value) === 'fund_individual_profit_probability_xq') {
      if (actualMode === 'single' && singleFundCode.value) {
        // 单个更新：传入基金代码到后端的 fund_code 参数
        params.fund_code = singleFundCode.value
      } else {
        // 批量更新模式：从 fund_name_em 获取代码列表，并发更新
        params.batch = true
        params.limit = batchSize.value
        params.concurrency = concurrency.value
      }
    } else if (String(collectionName.value) === 'fund_individual_detail_hold_xq') {
      if (actualMode === 'single') {
        // 单个更新：传入基金代码(symbol)和日期(date)参数
        if (!singleFundCode.value) {
          ElMessage.warning('请输入基金代码')
          refreshing.value = false
          return
        }
        if (!singleDate.value) {
          ElMessage.warning('请输入季度末日期（如 2024-09-30）')
          refreshing.value = false
          return
        }
        params.symbol = singleFundCode.value
        params.date = singleDate.value
      } else {
        // 批量更新模式：从 fund_name_em 获取代码列表，自动遍历所有季度末日期
        params.batch = true
        params.limit = batchSize.value
        params.concurrency = concurrency.value
      }
    } else if (String(collectionName.value) === 'fund_overview_em') {
      if (actualMode === 'single' && singleFundCode.value) {
        // 单个更新：传入基金代码到后端的 fund_code 参数
        params.fund_code = singleFundCode.value
      } else {
        // 批量更新模式：从 fund_name_em 获取代码列表，并发更新
        params.batch = true
        params.limit = batchSize.value
        params.concurrency = concurrency.value
      }
    } else if (String(collectionName.value) === 'fund_portfolio_hold_em') {
      console.log('fund_portfolio_hold_em - actualMode:', actualMode, 'mode:', mode)
      console.log('singleFundCode:', singleFundCode.value, 'singleYear:', singleYear.value, 'batchYear:', batchYear.value)
      
      if (actualMode === 'single') {
        // 单个更新：必须提供基金代码和年份
        if (!singleFundCode.value) {
          ElMessage.warning('请输入基金代码')
          refreshing.value = false
          return
        }
        if (!singleYear.value) {
          ElMessage.warning('请输入查询年份（如 2024）')
          refreshing.value = false
          return
        }
        params.fund_code = singleFundCode.value
        params.year = singleYear.value
        console.log('设置单个更新参数:', params)
      } else {
        // 批量更新模式：从 fund_name_em 获取所有代码，遍历年份
        params.batch = true
        params.concurrency = concurrency.value
        // year 参数可选，为空时更新2010-今年所有年份
        if (batchYear.value) {
          params.year = batchYear.value
        }
        console.log('设置批量更新参数:', params)
      }
    } else if (String(collectionName.value) === 'fund_portfolio_bond_hold_em') {
      console.log('fund_portfolio_bond_hold_em - actualMode:', actualMode, 'mode:', mode)
      console.log('singleFundCode:', singleFundCode.value, 'singleYear:', singleYear.value, 'batchYear:', batchYear.value)
      
      if (actualMode === 'single') {
        // 单个更新：必须提供基金代码和年份
        if (!singleFundCode.value) {
          ElMessage.warning('请输入基金代码')
          refreshing.value = false
          return
        }
        if (!singleYear.value) {
          ElMessage.warning('请输入查询年份（如 2024）')
          refreshing.value = false
          return
        }
        params.fund_code = singleFundCode.value
        params.year = singleYear.value
        console.log('设置单个更新参数:', params)
      } else {
        // 批量更新模式：从 fund_name_em 获取所有代码，遍历年份
        params.batch = true
        params.concurrency = concurrency.value
        // year 参数可选，为空时更新2010-今年所有年份
        if (batchYear.value) {
          params.year = batchYear.value
        }
        console.log('设置批量更新参数:', params)
      }
    } else if (collectionName.value === 'fund_portfolio_change_em') {
      console.log('fund_portfolio_change_em - actualMode:', actualMode, 'mode:', mode)
      console.log('singleFundCode:', singleFundCode.value, 'singleYear:', singleYear.value, 'batchYear:', batchYear.value)
      
      if (actualMode === 'single') {
        // 单个更新：必须提供基金代码和年份
        if (!singleFundCode.value) {
          ElMessage.warning('请输入基金代码')
          refreshing.value = false
          return
        }
        if (!singleYear.value) {
          ElMessage.warning('请输入查询年份（如 2024）')
          refreshing.value = false
          return
        }
        params.fund_code = singleFundCode.value
        params.date = singleYear.value
        console.log('设置单个更新参数:', params)
      } else {
        // 批量更新模式：从 fund_name_em 获取所有代码，按年份增量更新
        if (!batchYear.value) {
          ElMessage.warning('请输入批量更新年份（如 2024）')
          refreshing.value = false
          return
        }
        params.batch = true
        params.concurrency = concurrency.value
        params.date = batchYear.value
        console.log('设置批量更新参数:', params)
      }
    } else if (collectionName.value === 'fund_fh_em') {
      if (mode === 'single') {
        // 单年更新：传入 year 参数
        if (!singleYear.value) {
          ElMessage.warning('请输入年份')
          refreshing.value = false
          return
        }
        params.year = singleYear.value
        params.batch_update = false
      } else {
        // 批量更新：1999-2025 年，前端允许配置并发数
        params.batch_update = true
        params.start_year = 1999
        params.end_year = 2025
        params.concurrency = concurrency.value
      }
    } else if (collectionName.value === 'fund_cf_em') {
      if (mode === 'single') {
        // 单年更新：传入 year 参数
        if (!singleYear.value) {
          ElMessage.warning('请输入年份')
          refreshing.value = false
          return
        }
        params.year = singleYear.value
        params.batch_update = false
      } else {
        // 批量更新：2005-当前年份，前端固定起始年份，结束年份取当前年，允许配置并发数
        const currentYear = new Date().getFullYear()
        params.batch_update = true
        params.start_year = 2005
        params.end_year = currentYear
        params.concurrency = concurrency.value
      }
    }
    
    const res = await fundsApi.refreshCollectionData(collectionName.value, params)
    
    if (res.success && res.data?.task_id) {
      currentTaskId.value = res.data.task_id
      progressMessage.value = '任务已创建，正在更新数据...'
      
      // 开始轮询任务状态
      await pollTaskStatus()
    } else {
      throw new Error(res.data?.message || '创建任务失败')
    }
  } catch (e: any) {
    console.error('更新数据失败:', e)
    ElMessage.error(e.message || '更新数据失败')
    progressStatus.value = 'exception'
    refreshing.value = false
  }
}

// 轮询任务状态
const pollTaskStatus = async () => {
  let pollCount = 0
  const maxPollCount = 300 // 最多轮询5分钟（300秒）
  
  progressTimer = setInterval(async () => {
    try {
      pollCount++
      
      // 超时检查
      if (pollCount > maxPollCount) {
        if (progressTimer) {
          clearInterval(progressTimer)
          progressTimer = null
        }
        progressStatus.value = 'warning'
        progressMessage.value = '任务超时，请刷新页面查看结果'
        ElMessage.warning('任务执行时间过长，请刷新页面查看结果')
        refreshing.value = false
        return
      }
      
      const res = await fundsApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
      
      if (res.success && res.data) {
        const task = res.data
        
        // 更新进度
        if (task.progress !== undefined && task.total !== undefined) {
          progressPercentage.value = Math.round((task.progress / task.total) * 100)
        }
        progressMessage.value = task.message || ''
        
        // 检查是否完成
        if (task.status === 'success') {
          progressStatus.value = 'success'
          progressPercentage.value = 100
          
          let message = task.message || '数据更新成功'
          if (task.result && task.result.saved !== undefined) {
            message = `成功更新 ${task.result.saved} 条数据`
          }
          
          progressMessage.value = message + ' - 正在刷新数据...'
          
          // 清除轮询定时器
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          
          // 刷新页面数据
          await loadData()
          
          // 数据刷新完成后更新提示信息，但不关闭对话框
          progressMessage.value = message + ' - 数据已刷新，请手动关闭对话框'
          ElMessage.success(message)
          refreshing.value = false
          
        } else if (task.status === 'failed') {
          progressStatus.value = 'exception'
          ElMessage.error(task.error || '数据更新失败')
          
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          refreshing.value = false
        }
      }
    } catch (e) {
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
      progressStatus.value = 'exception'
      progressMessage.value = '查询任务状态失败'
      refreshing.value = false
    }
  }, 1000)
}

// 取消刷新
const cancelRefresh = () => {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
  apiRefreshDialogVisible.value = false
  refreshing.value = false
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = ''
}

// 文件导入处理（使用共享组件）
const handleImportFile = async (files: File[]) => {
  if (!files.length) return
  
  importing.value = true
  
  try {
    const res = await fundsApi.uploadData(collectionName.value, files[0])
    
    if (res.success) {
      ElMessage.success(res.data?.message || '导入成功')
      fileImportRef.value?.clearFiles()
      fileImportDialogVisible.value = false
      loadData()
    } else {
      ElMessage.error(res.message || '导入失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

// 远程同步处理（使用共享组件）
const handleRemoteSync = async (config: RemoteSyncConfig) => {
  remoteSyncing.value = true
  remoteSyncStats.value = null

  try {
    const res = await fundsApi.syncData(collectionName.value, {
      host: config.host,
      username: config.username,
      password: config.password,
      authSource: config.authSource,
      collection: config.collection || collectionName.value,
      batch_size: config.batchSize
    })

    if (res.success) {
      remoteSyncStats.value = res.data
      ElMessage.success(res.data?.message || '同步成功')
      loadData()
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '同步失败')
  } finally {
    remoteSyncing.value = false
  }
}

// ========== 动态更新配置相关函数 ==========

// 加载更新配置
const loadUpdateConfig = async () => {
  try {
    updateConfig.value = null
    singleUpdateParams.value = {}
    batchUpdateParams.value = {}
    
    const res = await fundsApi.getCollectionUpdateConfig(collectionName.value)
    if (res.success && res.data) {
      updateConfig.value = res.data
      
      // 初始化单条更新参数默认值
      if (res.data.single_update?.params) {
        for (const param of res.data.single_update.params) {
          if (param.default !== undefined) {
            singleUpdateParams.value[param.name] = param.default
          }
        }
      }
      
      // 初始化批量更新参数默认值
      if (res.data.batch_update?.params) {
        for (const param of res.data.batch_update.params) {
          if (param.default !== undefined) {
            batchUpdateParams.value[param.name] = param.default
          }
        }
      }
    }
  } catch (error: any) {
    console.error('加载更新配置失败:', error)
    ElMessage.error('加载更新配置失败')
  }
}

// 计算是否可以单条更新（所有必填参数都已填写）
const canSingleUpdate = computed(() => {
  if (!updateConfig.value?.single_update?.enabled) return false
  const params = updateConfig.value.single_update.params || []
  for (const param of params) {
    if (param.required && !singleUpdateParams.value[param.name]) {
      return false
    }
  }
  return true
})

// 计算是否可以批量更新（所有必填参数都已填写）
const canBatchUpdate = computed(() => {
  if (!updateConfig.value?.batch_update?.enabled) return false
  const params = updateConfig.value.batch_update.params || []
  for (const param of params) {
    if (param.required && !batchUpdateParams.value[param.name]) {
      return false
    }
  }
  return true
})

// 处理单条更新
const handleSingleUpdate = async () => {
  if (!canSingleUpdate.value) return
  
  singleUpdating.value = true
  progressPercentage.value = 0
  progressMessage.value = '正在执行单条更新...'
  
  try {
    const res = await fundsApi.refreshCollectionData(collectionName.value, {
      update_type: 'single',
      ...singleUpdateParams.value
    })
    
    if (res.success) {
      progressPercentage.value = 100
      progressStatus.value = 'success'
      progressMessage.value = res.data?.message || '单条更新完成'
      ElMessage.success('单条更新成功')
      await loadData()
    } else {
      progressStatus.value = 'exception'
      progressMessage.value = res.message || '更新失败'
      ElMessage.error(res.message || '单条更新失败')
    }
  } catch (error: any) {
    progressStatus.value = 'exception'
    progressMessage.value = error.message || '更新失败'
    ElMessage.error(error.message || '单条更新失败')
  } finally {
    singleUpdating.value = false
  }
}

// 批量更新任务轮询定时器
let batchProgressTimer: ReturnType<typeof setInterval> | null = null

// 轮询批量更新任务状态
const pollBatchTaskStatus = async () => {
  let pollCount = 0
  const maxPollCount = 1800 // 最多轮询30分钟（批量更新可能需要更长时间）
  
  batchProgressTimer = setInterval(async () => {
    try {
      pollCount++
      
      // 超时检查
      if (pollCount > maxPollCount) {
        if (batchProgressTimer) {
          clearInterval(batchProgressTimer)
          batchProgressTimer = null
        }
        progressStatus.value = 'warning'
        progressMessage.value = '任务超时，请刷新页面查看结果'
        ElMessage.warning('任务执行时间过长，请刷新页面查看结果')
        batchUpdating.value = false
        return
      }
      
      const res = await fundsApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
      
      if (res.success && res.data) {
        const task = res.data
        
        // 更新进度
        if (task.progress !== undefined && task.total !== undefined) {
          progressPercentage.value = Math.round((task.progress / task.total) * 100)
        }
        progressMessage.value = task.message || '正在批量更新...'
        
        // 检查是否完成
        if (task.status === 'success' || task.status === 'completed') {
          progressStatus.value = 'success'
          progressPercentage.value = 100
          
          let message = task.message || '批量更新完成'
          if (task.result) {
            if (task.result.inserted !== undefined) {
              message = `批量更新完成，成功插入/更新 ${task.result.inserted} 条数据`
            } else if (task.result.saved !== undefined) {
              message = `批量更新完成，成功保存 ${task.result.saved} 条数据`
            }
          }
          
          progressMessage.value = message
          
          // 清除轮询定时器
          if (batchProgressTimer) {
            clearInterval(batchProgressTimer)
            batchProgressTimer = null
          }
          
          // 刷新页面数据
          await loadData()
          
          ElMessage.success(message)
          batchUpdating.value = false
          
        } else if (task.status === 'failed') {
          progressStatus.value = 'exception'
          progressMessage.value = task.error || task.message || '批量更新失败'
          ElMessage.error(task.error || '批量更新失败')
          
          if (batchProgressTimer) {
            clearInterval(batchProgressTimer)
            batchProgressTimer = null
          }
          batchUpdating.value = false
        }
      }
    } catch (e: any) {
      console.error('轮询批量更新状态失败:', e)
      // 不立即停止轮询，可能是网络抖动
      if (pollCount > 5) {
        if (batchProgressTimer) {
          clearInterval(batchProgressTimer)
          batchProgressTimer = null
        }
        progressStatus.value = 'exception'
        progressMessage.value = '查询任务状态失败'
        batchUpdating.value = false
      }
    }
  }, 1000)
}

// 处理批量更新
const handleBatchUpdate = async () => {
  if (!canBatchUpdate.value) return
  
  batchUpdating.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = '正在创建批量更新任务...'
  
  try {
    const res = await fundsApi.refreshCollectionData(collectionName.value, {
      update_type: 'batch',
      ...batchUpdateParams.value
    })
    
    if (res.success) {
      // 如果返回了任务ID，启动进度轮询
      if (res.data?.task_id) {
        currentTaskId.value = res.data.task_id
        progressMessage.value = '任务已创建，正在批量更新数据...'
        pollBatchTaskStatus()
      } else {
        progressPercentage.value = 100
        progressStatus.value = 'success'
        progressMessage.value = res.data?.message || '批量更新完成'
        ElMessage.success('批量更新成功')
        await loadData()
        batchUpdating.value = false
      }
    } else {
      progressStatus.value = 'exception'
      progressMessage.value = res.message || '更新失败'
      ElMessage.error(res.message || '批量更新失败')
      batchUpdating.value = false
    }
  } catch (error: any) {
    progressStatus.value = 'exception'
    progressMessage.value = error.message || '更新失败'
    ElMessage.error(error.message || '批量更新失败')
    batchUpdating.value = false
  }
}

// 处理清空数据
const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(
      `确认要清空 "${collectionInfo.value?.display_name || collectionName.value}" 集合的所有数据吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确认清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    clearing.value = true
    try {
      const res = await fundsApi.clearCollectionData(collectionName.value)
      if (res.success) {
        ElMessage.success(`成功清空 ${res.data?.deleted_count || 0} 条数据`)
        await loadData()
      } else {
        ElMessage.error(res.message || '清空数据失败')
      }
    } catch (error: any) {
      ElMessage.error(error.message || '清空数据失败')
    } finally {
      clearing.value = false
    }
  } catch (error) {
    // 用户取消
  }
}

onMounted(() => {
  if (collectionName.value === 'fund_info_index_em') {
    loadCompanies()
  }
  loadData()
})

onUnmounted(() => {
  if (progressTimer) {
    clearInterval(progressTimer)
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>