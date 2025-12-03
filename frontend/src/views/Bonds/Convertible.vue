<template>
  <div class="convertible-bonds-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><TrendCharts /></el-icon>
          可转债比价分析
        </h1>
        <p class="page-description">实时可转债数据、转股价值分析、套利机会扫描</p>
      </div>
      <div class="header-actions">
        <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
        <el-button :icon="Download" type="primary" @click="syncData" :loading="syncing">同步数据</el-button>
      </div>
    </div>

    <!-- 筛选工具栏 -->
    <el-card shadow="hover" class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="转股溢价率">
          <el-slider
            v-model="premiumRange"
            range
            :min="-50"
            :max="200"
            :step="5"
            :marks="{ 0: '0%', 50: '50%', 100: '100%' }"
            style="width: 200px"
            @change="handleFilter"
          />
        </el-form-item>
        <el-form-item label="搜索">
          <el-input
            v-model="filterForm.keyword"
            placeholder="代码/名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleFilter"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 统计数据卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="可转债总数" :value="stats.total">
            <template #prefix>
              <el-icon style="color: #409eff"><Document /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="低溢价机会" :value="stats.lowPremiumCount">
            <template #prefix>
              <el-icon style="color: #67c23a"><Opportunity /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="强赎预警" :value="stats.redeemAlertCount">
            <template #prefix>
              <el-icon style="color: #f56c6c"><Warning /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="平均溢价率" :value="stats.avgPremium" :precision="2" suffix="%">
            <template #prefix>
              <el-icon style="color: #e6a23c"><DataAnalysis /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- 可转债比价表 -->
    <el-card shadow="hover" class="table-card">
      <template #header>
        <div class="card-header">
          <span>可转债比价表</span>
          <el-tag type="info" size="small">更新于: {{ lastUpdateTime }}</el-tag>
        </div>
      </template>

      <el-table
        :data="bonds"
        v-loading="loading"
        stripe
        border
        :style="{ width: '100%' }"
        @sort-change="handleSortChange"
        @row-click="handleRowClick"
        highlight-current-row
      >
        <el-table-column type="index" label="序号" width="60" />

        <el-table-column prop="code" label="转债代码" width="110" sortable="custom" fixed="left">
          <template #default="{ row }">
            <el-link type="primary" @click.stop="viewDetail(row.code)">
              {{ row.code }}
            </el-link>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="转债名称" width="140" sortable="custom" show-overflow-tooltip />

        <el-table-column prop="price" label="转债价格" width="100" sortable="custom" align="right">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_pct)">
              {{ row.price?.toFixed(2) || '-' }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="change_pct" label="涨跌幅" width="90" sortable="custom" align="right">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_pct)">
              {{ formatChangePercent(row.change_pct) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="stock_code" label="正股代码" width="110">
          <template #default="{ row }">
            <el-link type="primary">{{ row.stock_code }}</el-link>
          </template>
        </el-table-column>

        <el-table-column prop="stock_price" label="正股价格" width="100" align="right">
          <template #default="{ row }">
            {{ row.stock_price?.toFixed(2) || '-' }}
          </template>
        </el-table-column>

        <el-table-column prop="convert_price" label="转股价" width="90" sortable="custom" align="right">
          <template #default="{ row }">
            {{ row.convert_price?.toFixed(2) || '-' }}
          </template>
        </el-table-column>

        <el-table-column prop="convert_value" label="转股价值" width="100" sortable="custom" align="right">
          <template #default="{ row }">
            {{ row.convert_value?.toFixed(2) || '-' }}
          </template>
        </el-table-column>

        <el-table-column prop="convert_premium_rate" label="转股溢价率" width="120" sortable="custom" align="right">
          <template #default="{ row }">
            <el-tag :type="getPremiumTagType(row.convert_premium_rate)" size="small">
              {{ row.convert_premium_rate?.toFixed(2) || '-' }}%
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="pure_debt_value" label="纯债价值" width="100" sortable="custom" align="right">
          <template #default="{ row }">
            {{ row.pure_debt_value?.toFixed(2) || '-' }}
          </template>
        </el-table-column>

        <el-table-column prop="pure_debt_premium_rate" label="纯债溢价率" width="120" sortable="custom" align="right">
          <template #default="{ row }">
            {{ row.pure_debt_premium_rate?.toFixed(2) || '-' }}%
          </template>
        </el-table-column>

        <el-table-column label="操作" width="160" fixed="right" align="center">
          <template #default="{ row }">
            <el-button size="small" @click.stop="viewAnalysis(row.code)" link>价值分析</el-button>
            <el-button size="small" @click.stop="viewDetail(row.code)" link>详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :page-sizes="[20, 50, 100, 200]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 价值分析对话框 -->
    <el-dialog
      v-model="analysisDialogVisible"
      :title="`${currentBondCode} 价值分析`"
      width="90%"
      top="5vh"
      :close-on-click-modal="false"
    >
      <div v-loading="analysisLoading">
        <div v-if="analysisData.length > 0" class="analysis-content">
          <div id="valueChart" style="width: 100%; height: 400px"></div>
        </div>
        <el-empty v-else description="暂无价值分析数据" />
      </div>
      <template #footer>
        <el-button @click="analysisDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="syncAnalysisData">同步数据</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  TrendCharts, Refresh, Download, Search, Document, 
  Opportunity, Warning, DataAnalysis 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { bondsApi } from '@/api/bonds'
import * as echarts from 'echarts'

const router = useRouter()

// 数据状态
const loading = ref(false)
const syncing = ref(false)
const bonds = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(50)
const lastUpdateTime = ref('')

// 筛选条件
const filterForm = reactive({
  keyword: ''
})
const premiumRange = ref<[number, number]>([0, 100])

// 排序
const sortBy = ref('')
const sortDir = ref<'asc' | 'desc'>('asc')

// 统计数据
const stats = computed(() => {
  const filtered = bonds.value
  return {
    total: filtered.length,
    lowPremiumCount: filtered.filter(b => (b.convert_premium_rate || 0) < 10).length,
    redeemAlertCount: filtered.filter(b => 
      b.stock_price && b.redeem_trigger_price && 
      b.stock_price >= b.redeem_trigger_price
    ).length,
    avgPremium: filtered.length > 0 
      ? filtered.reduce((sum, b) => sum + (b.convert_premium_rate || 0), 0) / filtered.length 
      : 0
  }
})

// 价值分析对话框
const analysisDialogVisible = ref(false)
const analysisLoading = ref(false)
const currentBondCode = ref('')
const analysisData = ref<any[]>([])

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params: any = {
      page: page.value,
      page_size: pageSize.value
    }
    
    if (sortBy.value) {
      params.sort_by = sortBy.value
      params.sort_dir = sortDir.value
    }
    
    if (premiumRange.value) {
      params.min_premium = premiumRange.value[0]
      params.max_premium = premiumRange.value[1]
    }
    
    const res = await bondsApi.getConvertibleComparison(params)
    
    if (res.success && res.data) {
      bonds.value = res.data.items || []
      total.value = res.data.total || 0
      
      // 如果有关键词过滤，前端再筛选一次
      if (filterForm.keyword) {
        bonds.value = bonds.value.filter(b => 
          b.code.includes(filterForm.keyword) || 
          b.name.includes(filterForm.keyword)
        )
        total.value = bonds.value.length
      }
      
      lastUpdateTime.value = new Date().toLocaleString()
    }
  } catch (e: any) {
    console.error('加载可转债数据失败:', e)
    ElMessage.error('加载数据失败: ' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 同步数据
const syncData = async () => {
  syncing.value = true
  try {
    const res = await bondsApi.syncConvertibleComparison()
    if (res.success) {
      ElMessage.success(res.data?.message || '同步成功')
      await loadData()
    }
  } catch (e: any) {
    console.error('同步数据失败:', e)
    ElMessage.error('同步失败: ' + (e.message || '未知错误'))
  } finally {
    syncing.value = false
  }
}

// 筛选处理
const handleFilter = () => {
  page.value = 1
  loadData()
}

const resetFilter = () => {
  filterForm.keyword = ''
  premiumRange.value = [0, 100]
  sortBy.value = ''
  sortDir.value = 'asc'
  page.value = 1
  loadData()
}

// 排序处理
const handleSortChange = ({ prop, order }: any) => {
  if (order === null) {
    sortBy.value = ''
    sortDir.value = 'asc'
  } else {
    sortBy.value = prop
    sortDir.value = order === 'ascending' ? 'asc' : 'desc'
  }
  page.value = 1
  loadData()
}

// 分页处理
const handleSizeChange = () => {
  page.value = 1
  loadData()
}

const handlePageChange = () => {
  loadData()
}

// 行点击
const handleRowClick = (row: any) => {
  console.log('点击行:', row)
}

// 查看详情
const viewDetail = (code: string) => {
  router.push({ name: 'BondDetail', params: { code } })
}

// 查看价值分析
const viewAnalysis = async (code: string) => {
  currentBondCode.value = code
  analysisDialogVisible.value = true
  analysisLoading.value = true
  
  try {
    const res = await bondsApi.getConvertibleValueAnalysis(code)
    if (res.success && res.data) {
      analysisData.value = res.data.data || []
      
      // 渲染图表
      if (analysisData.value.length > 0) {
        setTimeout(() => {
          renderChart()
        }, 100)
      }
    }
  } catch (e: any) {
    console.error('加载价值分析失败:', e)
    ElMessage.error('加载失败: ' + (e.message || '未知错误'))
  } finally {
    analysisLoading.value = false
  }
}

// 同步价值分析数据
const syncAnalysisData = async () => {
  analysisLoading.value = true
  try {
    const res = await bondsApi.syncConvertibleValueAnalysis(currentBondCode.value)
    if (res.success) {
      ElMessage.success(res.data?.message || '同步成功')
      // 重新加载数据
      await viewAnalysis(currentBondCode.value)
    }
  } catch (e: any) {
    ElMessage.error('同步失败: ' + (e.message || '未知错误'))
  } finally {
    analysisLoading.value = false
  }
}

// 渲染价值分析图表
const renderChart = () => {
  const chartDom = document.getElementById('valueChart')
  if (!chartDom) return
  
  const myChart = echarts.init(chartDom)
  
  const dates = analysisData.value.map(d => d.date)
  const closePrices = analysisData.value.map(d => d.close_price)
  const pureDebtValues = analysisData.value.map(d => d.pure_debt_value)
  const convertValues = analysisData.value.map(d => d.convert_value)
  const convertPremiums = analysisData.value.map(d => d.convert_premium_rate)
  
  const option = {
    title: {
      text: '可转债价值分析'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['转债价格', '纯债价值', '转股价值', '转股溢价率']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: [
      {
        type: 'value',
        name: '价格(元)',
        position: 'left'
      },
      {
        type: 'value',
        name: '溢价率(%)',
        position: 'right'
      }
    ],
    series: [
      {
        name: '转债价格',
        type: 'line',
        data: closePrices,
        yAxisIndex: 0
      },
      {
        name: '纯债价值',
        type: 'line',
        data: pureDebtValues,
        yAxisIndex: 0
      },
      {
        name: '转股价值',
        type: 'line',
        data: convertValues,
        yAxisIndex: 0
      },
      {
        name: '转股溢价率',
        type: 'line',
        data: convertPremiums,
        yAxisIndex: 1
      }
    ]
  }
  
  myChart.setOption(option)
}

// 工具函数
const getPriceClass = (changePct: number | undefined) => {
  if (!changePct) return ''
  return changePct > 0 ? 'price-up' : changePct < 0 ? 'price-down' : ''
}

const formatChangePercent = (value: number | undefined) => {
  if (value === undefined || value === null) return '-'
  const sign = value > 0 ? '+' : ''
  return `${sign}${value.toFixed(2)}%`
}

type TagType = 'primary' | 'success' | 'warning' | 'info' | 'danger'
const getPremiumTagType = (premium: number | undefined): TagType => {
  if (premium === undefined || premium === null) return 'info'
  if (premium < 0) return 'success'
  if (premium < 10) return 'success'
  if (premium < 30) return 'info'
  if (premium < 50) return 'warning'
  return 'danger'
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.convertible-bonds-view {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.page-description {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.filter-card {
  margin-bottom: 16px;
}

.stats-row {
  margin-bottom: 16px;
}

.stat-card {
  text-align: center;
}

.table-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.price-up {
  color: #f56c6c;
}

.price-down {
  color: #67c23a;
}

.analysis-content {
  padding: 16px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
  }
}
</style>
