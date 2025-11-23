<template>
  <div class="collection-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionInfo?.display_name || collectionName }}
          </h1>
          <p class="page-description">{{ collectionInfo?.description || '' }}</p>
        </div>
        <div class="header-actions">
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
          <el-button :icon="Download" type="primary" @click="showRefreshDialog" :loading="refreshing">更新数据</el-button>
          <el-button :icon="Delete" type="danger" @click="handleClearData" :loading="clearing">清空数据</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 统计数据卡片 -->
      <el-card shadow="hover" class="stats-card" v-if="stats">
        <template #header>
          <div class="card-header">
            <span>数据概览</span>
            <el-tag size="small" type="info" effect="plain">更新于: {{ new Date().toLocaleString() }}</el-tag>
          </div>
        </template>
        <el-row :gutter="24">
          <el-col :span="24">
            <div class="stat-metric-group">
              <div class="stat-metric-item">
                <div class="metric-label">总记录数</div>
                <div class="metric-value-large">{{ stats.total_count?.toLocaleString() || 0 }}</div>
                <div class="metric-sub">条数据记录</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 实时行情图表 (仅futures_zh_spot显示) -->
      <el-card shadow="hover" class="chart-card" v-if="collectionName === 'futures_zh_spot' && chartData.length > 0">
        <template #header>
          <span>价格走势</span>
        </template>
        <v-chart
          :option="priceChartOption"
          :autoresize="true"
          style="height: 300px; width: 100%"
        />
      </el-card>

      <!-- 数据列表 -->
      <el-card shadow="hover" class="data-card">
        <template #header>
          <div class="card-header">
            <span>数据列表</span>
            <div class="header-actions">
              <el-input
                v-model="filterValue"
                placeholder="搜索..."
                style="width: 200px; margin-right: 8px;"
                clearable
                @clear="handleFilter"
                @keyup.enter="handleFilter"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </div>
        </template>

        <el-table
          :data="tableData"
          stripe
          border
          v-loading="loading"
          style="width: 100%"
          height="500"
        >
          <el-table-column
            v-for="field in displayFields"
            :key="field"
            :prop="field"
            :label="field"
            :min-width="120"
            show-overflow-tooltip
          >
            <template #default="{ row }">
              <span v-if="row[field] !== null && row[field] !== undefined">{{ row[field] }}</span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="refreshDialogVisible"
      title="更新数据"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form label-width="100px">
        <el-form-item label="集合名称">
          <el-input :value="collectionInfo?.display_name || collectionName" disabled />
        </el-form-item>

        <!-- futures_zh_spot 特定参数 -->
        <template v-if="collectionName === 'futures_zh_spot'">
          <el-form-item label="市场类型">
            <el-select v-model="market" style="width: 100%">
              <el-option label="商品期货 (CF)" value="CF" />
              <el-option label="金融期货 (FF)" value="FF" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="数据详细度">
            <el-select v-model="adjust" style="width: 100%">
              <el-option label="基本数据" value="0" />
              <el-option label="包含交易所信息" value="1" />
            </el-select>
          </el-form-item>

          <el-form-item label="合约代码">
            <el-input
              v-model="symbol"
              placeholder="可选，留空获取所有合约"
            />
          </el-form-item>
        </template>

        <!-- 通用symbol参数 -->
        <el-form-item v-else label="参数">
          <el-input
            v-model="symbol"
            placeholder="请输入参数（如合约代码、日期等）"
          />
        </el-form-item>

        <!-- 进度显示 -->
        <div v-if="refreshing" style="margin-top: 20px;">
          <el-progress
            :percentage="100"
            status="success"
            :indeterminate="true"
            :stroke-width="15"
          />
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">
            数据更新中，请稍候...
          </p>
        </div>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="refreshDialogVisible = false" :disabled="refreshing">取消</el-button>
          <el-button type="primary" @click="handleRefresh" :loading="refreshing">
            开始更新
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Box, Refresh, Download, Delete, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { futuresApi } from '@/api/futures'
import VChart from 'vue-echarts'

const route = useRoute()
const collectionName = ref(route.params.collectionName as string)

// 数据状态
const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const tableData = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(50)
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)
const chartData = ref<any[]>([])

// 筛选
const filterValue = ref('')
const filterField = ref('')

// 更新数据对话框
const refreshDialogVisible = ref(false)
const symbol = ref('')
const market = ref('CF')
const adjust = ref('0')

// 计算显示的字段
const displayFields = computed(() => {
  if (tableData.value.length === 0) return []
  const firstRow = tableData.value[0]
  return Object.keys(firstRow).filter(key => key !== '_id')
})

// 价格图表配置
const priceChartOption = computed(() => {
  if (chartData.value.length === 0) return null
  
  const symbols = chartData.value.map(item => item.symbol)
  const prices = chartData.value.map(item => item.current_price)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: symbols,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '价格'
    },
    series: [{
      data: prices,
      type: 'bar',
      itemStyle: {
        color: '#409EFF'
      }
    }]
  }
})

// 加载集合信息
const loadCollectionInfo = async () => {
  try {
    const res = await futuresApi.getCollections()
    if (res.success) {
      collectionInfo.value = res.data.find((c: any) => c.name === collectionName.value)
    }
  } catch (error) {
    console.error('加载集合信息失败:', error)
  }
}

// 加载统计数据
const loadStats = async () => {
  try {
    const res = await futuresApi.getCollectionStats(collectionName.value)
    if (res.success) {
      stats.value = res.data
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await futuresApi.getCollectionData(collectionName.value, {
      page: currentPage.value,
      page_size: pageSize.value,
      filter_field: filterField.value,
      filter_value: filterValue.value
    })
    
    if (res.success) {
      tableData.value = res.data.items || []
      total.value = res.data.total || 0
      
      // 为图表准备数据（取前20条）
      if (collectionName.value === 'futures_zh_spot') {
        chartData.value = (res.data.items || []).slice(0, 20)
      }
    } else {
      ElMessage.error(res.error || '加载数据失败')
    }
  } catch (error: any) {
    console.error('加载数据失败:', error)
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 显示更新对话框
const showRefreshDialog = () => {
  refreshDialogVisible.value = true
}

// 更新数据
const handleRefresh = async () => {
  refreshing.value = true
  try {
    const params: any = {}
    if (symbol.value) params.symbol = symbol.value
    
    if (collectionName.value === 'futures_zh_spot') {
      params.market = market.value
      params.adjust = adjust.value
    }
    
    const res = await futuresApi.updateCollection(collectionName.value, params)
    
    if (res.success) {
      ElMessage.success('更新任务已提交，请稍后刷新查看数据')
      refreshDialogVisible.value = false
      
      // 5秒后自动刷新数据
      setTimeout(() => {
        loadData()
        loadStats()
      }, 5000)
    } else {
      ElMessage.error(res.error || '更新失败')
    }
  } catch (error: any) {
    console.error('更新失败:', error)
    ElMessage.error(error.message || '更新失败')
  } finally {
    refreshing.value = false
  }
}

// 清空数据
const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有数据吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    clearing.value = true
    const res = await futuresApi.clearCollection(collectionName.value)
    
    if (res.success) {
      ElMessage.success('数据已清空')
      loadData()
      loadStats()
    } else {
      ElMessage.error(res.error || '清空失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空数据失败:', error)
      ElMessage.error(error.message || '清空失败')
    }
  } finally {
    clearing.value = false
  }
}

// 筛选
const handleFilter = () => {
  currentPage.value = 1
  loadData()
}

// 分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  loadData()
}

const handlePageChange = (val: number) => {
  currentPage.value = val
  loadData()
}

// 监听路由变化
watch(() => route.params.collectionName, (newVal) => {
  if (newVal) {
    collectionName.value = newVal as string
    currentPage.value = 1
    loadCollectionInfo()
    loadStats()
    loadData()
  }
})

// 初始化
onMounted(() => {
  loadCollectionInfo()
  loadStats()
  loadData()
})
</script>

<style scoped>
.collection-view {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title-section {
  flex: 1;
}

.page-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 28px;
  color: #409EFF;
}

.page-description {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-card, .chart-card, .data-card {
  background: white;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.stat-metric-group {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20px;
}

.stat-metric-item {
  text-align: center;
}

.metric-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.metric-value-large {
  font-size: 32px;
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 4px;
}

.metric-sub {
  font-size: 12px;
  color: #C0C4CC;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.text-muted {
  color: #C0C4CC;
}
</style>
