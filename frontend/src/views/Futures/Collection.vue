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
          <el-button :icon="Box" @click="showOverviewDialog">数据概览</el-button>
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
          <el-dropdown @command="handleUpdateCommand">
            <el-button :icon="Download" type="primary" :loading="refreshing">
              更新数据<el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="api">API更新</el-dropdown-item>
                <el-dropdown-item command="file">文件导入</el-dropdown-item>
                <el-dropdown-item command="sync">远程同步</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-button :icon="Delete" type="danger" @click="handleClearData" :loading="clearing">清空数据</el-button>
        </div>
      </div>
    </div>

    <div class="content">
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
            <div style="display: flex; align-items: center;">
              <span>数据列表</span>
              <el-popover
                placement="right"
                title="字段说明"
                :width="600"
                trigger="hover"
                v-if="fields && fields.length > 0"
              >
                <template #reference>
                  <el-icon style="margin-left: 8px; cursor: pointer; color: #909399;"><QuestionFilled /></el-icon>
                </template>
                <el-table :data="fields" stripe border size="small" style="width: 100%">
                  <el-table-column prop="name" label="字段名" width="200" />
                  <el-table-column prop="type" label="类型" width="120" />
                  <el-table-column prop="example" label="示例" show-overflow-tooltip>
                    <template #default="{ row }">
                      <span v-if="row.example" class="example-text">{{ row.example }}</span>
                      <span v-else class="text-muted">-</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-popover>
            </div>
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
            v-for="field in displayColumns"
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

    <!-- 文件导入对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="文件导入"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        multiple
        :on-change="handleImportFileChange"
        :on-remove="handleImportFileRemove"
        accept=".csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        drag
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击选择文件</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 CSV 或 Excel 文件，文件结构需与集合字段一致
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleImportFile"
          :loading="importing"
          :disabled="!importFiles.length || importing"
        >
          导入
        </el-button>
      </template>
    </el-dialog>

    <!-- 远程同步对话框 -->
    <el-dialog
      v-model="syncDialogVisible"
      title="远程同步"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form label-width="120px">
        <el-form-item label="远程主机">
          <el-input
            v-model="remoteSyncHost"
            placeholder="IP地址或URI，例如 192.168.1.10 或 mongodb://user:pwd@host:27017/db"
          />
        </el-form-item>
        <el-form-item label="数据库类型">
          <el-select v-model="remoteSyncDbType" disabled style="width: 100%">
            <el-option label="MongoDB" value="mongodb" />
          </el-select>
        </el-form-item>
        <el-form-item label="批次大小">
          <el-select v-model="remoteSyncBatchSize" style="width: 100%">
            <el-option label="1000" :value="1000" />
            <el-option label="2000" :value="2000" />
            <el-option label="5000" :value="5000" />
            <el-option label="10000" :value="10000" />
          </el-select>
        </el-form-item>
        <el-form-item label="远程集合名">
          <el-input
            v-model="remoteSyncCollection"
            :placeholder="`默认使用当前集合名: ${collectionName}`"
          />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input
            v-model="remoteSyncUsername"
            placeholder="可选"
          />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="remoteSyncPassword"
            type="password"
            placeholder="可选"
            show-password
          />
        </el-form-item>
        <el-form-item label="认证数据库">
          <el-input
            v-model="remoteSyncAuthSource"
            placeholder="通常为 admin"
          />
        </el-form-item>
      </el-form>

      <el-alert
        v-if="remoteSyncStats"
        :title="`同步完成: ${remoteSyncStats.synced_count}/${remoteSyncStats.total_count} 条`"
        type="success"
        style="margin-top: 16px"
        show-icon
      />

      <template #footer>
        <el-button @click="syncDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleRemoteSync"
          :loading="remoteSyncing"
        >
          开始同步
        </el-button>
      </template>
    </el-dialog>

    <!-- 数据概览对话框 -->
    <el-dialog
      v-model="overviewDialogVisible"
      title="数据概览"
      width="600px"
      :close-on-click-modal="false"
    >
      <div style="padding: 10px;">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="集合名称" label-align="right">
            {{ currentCollectionInfo.name }}
          </el-descriptions-item>
          <el-descriptions-item label="显示名称" label-align="right">
            {{ currentCollectionInfo.displayName }}
          </el-descriptions-item>
          <el-descriptions-item label="数据总数" label-align="right">
            {{ formatNumber(stats?.total_count || 0) }} 条
          </el-descriptions-item>
          <el-descriptions-item label="字段数量" label-align="right">
            {{ currentCollectionInfo.fieldCount }} 个
          </el-descriptions-item>
          <el-descriptions-item label="最后更新" label-align="right" :span="2">
            {{ stats?.latest_date || stats?.latest_time || '暂无数据' }}
          </el-descriptions-item>
          <el-descriptions-item label="数据来源" label-align="right" :span="2">
            <el-link :href="currentCollectionInfo.dataSource" target="_blank" type="primary" v-if="currentCollectionInfo.dataSource !== '暂无'">
              {{ currentCollectionInfo.dataSource }}
            </el-link>
            <span v-else>{{ currentCollectionInfo.dataSource }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="描述" label-align="right" :span="2">
            {{ collectionInfo?.description || `数据集合：${collectionName}` }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="overviewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Box, Refresh, Download, Delete, Search, QuestionFilled, ArrowDown, UploadFilled } from '@element-plus/icons-vue'
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
const fields = ref<any[]>([])
const overviewDialogVisible = ref(false)
const currentCollectionInfo = ref<any>({
  name: '',
  displayName: '',
  fieldCount: 0,
  dataSource: '暂无',
})

// 筛选
const filterValue = ref('')
const filterField = ref('')

// 更新数据对话框
const refreshDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)
const symbol = ref('')
const market = ref('CF')
const adjust = ref('0')

// 文件导入相关
const uploadRef = ref()
const importFiles = ref<any[]>([])
const importing = ref(false)

// 远程同步相关
const remoteSyncHost = ref('')
const remoteSyncDbType = ref('mongodb')
const remoteSyncBatchSize = ref(1000)
const remoteSyncCollection = ref('')
const remoteSyncUsername = ref('')
const remoteSyncPassword = ref('')
const remoteSyncAuthSource = ref('admin')
const remoteSyncing = ref(false)
const remoteSyncStats = ref<any>(null)

// 计算显示的字段
const displayFields = computed(() => {
  if (tableData.value.length === 0) return []
  const firstRow = tableData.value[0]
  return Object.keys(firstRow).filter(key => key !== '_id')
})

const displayColumns = computed(() => {
  if (fields.value && fields.value.length > 0) {
    return fields.value.map((f: any) => f.name)
  }
  return displayFields.value
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

const formatNumber = (value: number) => {
  if (!value) return '0'
  return value.toLocaleString()
}

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
      fields.value = res.data.fields || []
      
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

const showOverviewDialog = () => {
  const info = collectionInfo.value || {}
  const name = info.name || collectionName.value
  const displayName = info.display_name || collectionName.value
  const fieldCount = Array.isArray(info.fields) ? info.fields.length : (fields.value?.length || 0)
  const dataSource = info.data_source || info.source || '暂无'
  currentCollectionInfo.value = {
    name,
    displayName,
    fieldCount,
    dataSource,
  }
  overviewDialogVisible.value = true
}

// 显示更新对话框
const showRefreshDialog = () => {
  refreshDialogVisible.value = true
}

// 处理更新数据下拉菜单命令
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    refreshDialogVisible.value = true
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

// 文件导入处理
const handleImportFileChange = (file: any) => {
  importFiles.value = [file]
}

const handleImportFileRemove = () => {
  importFiles.value = []
}

const handleImportFile = async () => {
  if (!importFiles.value.length) return
  
  importing.value = true
  const file = importFiles.value[0].raw
  
  try {
    const res = await futuresApi.uploadData(collectionName.value, file)
    
    if (res.success) {
      ElMessage.success(res.message || '导入成功')
      if (uploadRef.value) uploadRef.value.clearFiles()
      importFiles.value = []
      uploadDialogVisible.value = false
      await loadStats()
      await loadData()
    } else {
      ElMessage.error(res.message || '导入失败')
    }
  } catch (error: any) {
    console.error('导入失败:', error)
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

// 远程同步处理
const handleRemoteSync = async () => {
  if (!remoteSyncHost.value) {
    ElMessage.warning('请输入远程主机地址')
    return
  }

  remoteSyncing.value = true
  remoteSyncStats.value = null

  try {
    const config = {
      host: remoteSyncHost.value,
      username: remoteSyncUsername.value,
      password: remoteSyncPassword.value,
      authSource: remoteSyncAuthSource.value,
      collection: remoteSyncCollection.value || collectionName.value,
      batch_size: remoteSyncBatchSize.value
    }

    const res = await futuresApi.syncData(collectionName.value, config)

    if (res.success) {
      remoteSyncStats.value = res.data
      ElMessage.success(res.message || '同步成功')
      await loadStats()
      await loadData()
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (error: any) {
    console.error('同步失败:', error)
    ElMessage.error(error.message || '同步失败')
  } finally {
    remoteSyncing.value = false
  }
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
