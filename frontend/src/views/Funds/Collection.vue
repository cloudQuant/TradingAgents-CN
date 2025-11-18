<template>
  <div class="fund-collection-detail">
    <!-- 头部信息 -->
    <el-card class="header-card">
      <div class="header-content">
        <div class="collection-info">
          <h2>{{ collectionInfo?.display_name || collectionName }}</h2>
          <p class="description">{{ collectionInfo?.description }}</p>
          <div class="stats" v-if="stats">
            <el-tag type="success">总数据量: {{ stats.total_count }}</el-tag>
          </div>
        </div>
        <div class="action-buttons">
          <el-button @click="loadData" :icon="Refresh" :loading="loading">
            刷新
          </el-button>
          <el-button type="primary" @click="handleRefreshData" :icon="Download">
            更新数据
          </el-button>
          <el-button type="danger" @click="handleClearData" :icon="Delete" :loading="clearing">
            清空数据
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <!-- 过滤和排序 -->
      <div class="table-controls">
        <div class="filter-controls">
          <el-input
            v-model="filterField"
            placeholder="过滤字段"
            style="width: 150px; margin-right: 8px;"
            clearable
          />
          <el-input
            v-model="filterValue"
            placeholder="过滤值"
            style="width: 200px; margin-right: 8px;"
            clearable
          />
          <el-button @click="loadData" type="primary" :icon="Search">搜索</el-button>
        </div>
        <div class="sort-controls">
          <span style="margin-right: 8px;">排序:</span>
          <el-select v-model="sortBy" placeholder="排序字段" style="width: 150px; margin-right: 8px;" clearable>
            <el-option
              v-for="field in fields"
              :key="field.name"
              :label="field.name"
              :value="field.name"
            />
          </el-select>
          <el-select v-model="sortDir" style="width: 100px;">
            <el-option label="降序" value="desc" />
            <el-option label="升序" value="asc" />
          </el-select>
        </div>
      </div>

      <!-- 字段信息 -->
      <el-collapse v-if="fields.length > 0" style="margin-bottom: 16px;">
        <el-collapse-item title="字段信息" name="fields">
          <el-table :data="fields" border size="small">
            <el-table-column prop="name" label="字段名" width="200" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column prop="example" label="示例值" />
          </el-table>
        </el-collapse-item>
      </el-collapse>

      <!-- 数据表格 -->
      <el-table
        :data="items"
        border
        v-loading="loading"
        style="width: 100%"
        max-height="600"
      >
        <el-table-column
          v-for="field in fields"
          :key="field.name"
          :prop="field.name"
          :label="field.name"
          :width="getColumnWidth(field.name)"
          show-overflow-tooltip
        />
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :page-sizes="[20, 50, 100, 200]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadData"
        @current-change="loadData"
        style="margin-top: 16px; justify-content: flex-end;"
      />
    </el-card>

    <!-- 基金类型分布图表 -->
    <el-card class="chart-card" v-if="stats && stats.type_stats && stats.type_stats.length > 0">
      <template #header>
        <div class="card-header">
          <span style="font-weight: 600; font-size: 16px;">基金类型分布</span>
        </div>
      </template>
      <v-chart :option="chartOption" style="height: 400px;" />
    </el-card>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="refreshDialogVisible"
      title="更新数据"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form label-width="100px">
        <!-- 进度显示 -->
        <div v-if="refreshing" style="margin-top: 20px;">
          <el-progress 
            :percentage="progressPercentage" 
            :status="progressStatus"
            :stroke-width="15"
          />
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">
            {{ progressMessage }}
          </p>
        </div>
        
        <el-alert
          title="更新说明"
          type="warning"
          :closable="false"
          style="margin-bottom: 16px;"
        >
          <template #default>
            <div style="font-size: 12px; line-height: 1.6;">
              <p v-if="collectionName === 'fund_name_em'">将从东方财富网获取所有基金的基本信息数据</p>
              <p v-else-if="collectionName === 'fund_basic_info'">将从东方财富网获取所有基金的基本信息数据（使用fund_name_em接口）</p>
              <p v-else>该集合暂不支持自动更新，如需更新请联系管理员</p>
            </div>
          </template>
        </el-alert>
      </el-form>
      
      <template #footer>
        <el-button @click="cancelRefresh" :disabled="refreshing && progressPercentage < 10">
          {{ refreshing ? '取消' : '关闭' }}
        </el-button>
        <el-button 
          type="primary" 
          @click="refreshData" 
          :loading="refreshing"
          :disabled="refreshing"
        >
          {{ refreshing ? '更新中...' : '开始更新' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Refresh, Search, Download, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fundsApi } from '@/api/funds'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent])

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

// 排序条件
const sortBy = ref('')
const sortDir = ref<'asc' | 'desc'>('desc')

// 统计数据
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)

// 饼图配置
const chartOption = computed(() => {
  if (!stats.value || !stats.value.type_stats) {
    console.log('⚠️ 无法生成饼图配置，统计数据不完整:', stats.value)
    return {}
  }
  
  const chartData = stats.value.type_stats.map((item: any) => ({
    name: item.type || '未分类',
    value: item.count
  }))
  
  console.log('✅ 饼图数据准备完成:', chartData)
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll',
      pageIconSize: 12,
      pageTextStyle: {
        color: '#666'
      }
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
          show: true,
          formatter: '{b}: {d}%'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: chartData
      }
    ]
  }
})

// 更新数据相关
const refreshDialogVisible = ref(false)
const refreshing = ref(false)
const currentTaskId = ref('')
const progressPercentage = ref(0)
const progressStatus = ref<'success' | 'exception' | 'warning' | ''>('')
const progressMessage = ref('')
let progressTimer: NodeJS.Timeout | null = null

// 清空数据相关
const clearing = ref(false)

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
      console.log('📊 统计数据加载成功:', stats.value)
      if (stats.value.type_stats) {
        console.log('📈 基金类型统计:', stats.value.type_stats)
      }
    }

    // 加载数据
    const dataRes = await fundsApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
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

// 获取列宽
const getColumnWidth = (fieldName: string): number => {
  if (fieldName.includes('代码') || fieldName.includes('code')) return 120
  if (fieldName.includes('类型') || fieldName.includes('type')) return 100
  if (fieldName.includes('简称') || fieldName.includes('name')) return 200
  if (fieldName.includes('全称')) return 300
  return undefined as any
}

// 处理更新数据
const handleRefreshData = () => {
  refreshDialogVisible.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = ''
}

// 更新数据
const refreshData = async () => {
  // 支持fund_name_em和fund_basic_info集合的更新
  const supportedCollections = ['fund_name_em', 'fund_basic_info']
  if (!supportedCollections.includes(collectionName.value)) {
    ElMessage.warning('该集合暂不支持自动更新')
    return
  }

  refreshing.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  
  try {
    // 创建任务
    const res = await fundsApi.refreshCollectionData(collectionName.value, {})
    
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
    let errorMessage = '更新数据失败'
    if (e.response?.data?.detail) {
      errorMessage = e.response.data.detail
    } else if (e.response?.data?.error) {
      errorMessage = e.response.data.error  
    } else if (e.message) {
      errorMessage = e.message
    }
    ElMessage.error(errorMessage)
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
        console.warn('任务状态轮询超时，停止轮询')
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
          console.log('✅ 任务完成，准备关闭对话框', task)
          progressStatus.value = 'success'
          progressPercentage.value = 100
          
          let message = task.message || '数据更新成功'
          if (task.result && task.result.saved !== undefined) {
            message = `成功更新 ${task.result.saved} 条数据`
          }
          
          progressMessage.value = message
          ElMessage.success(message)
          
          // 清除轮询定时器
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          
          // 刷新页面数据
          await loadData()
          
          // 延迟1.5秒后关闭对话框
          setTimeout(() => {
            console.log('🔒 关闭更新对话框')
            refreshDialogVisible.value = false
            refreshing.value = false
            progressPercentage.value = 0
            progressStatus.value = ''
            progressMessage.value = ''
          }, 1500)
          
        } else if (task.status === 'failed') {
          progressStatus.value = 'exception'
          ElMessage.error(task.error || '数据更新失败')
          
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          refreshing.value = false
        }
        // 如果是 running 或 pending，继续轮询
      } else {
        console.warn('获取任务状态失败，响应:', res)
      }
    } catch (e) {
      console.error('查询任务状态失败:', e)
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
      progressStatus.value = 'exception'
      progressMessage.value = '查询任务状态失败'
      ElMessage.error('查询任务状态失败，请重试')
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
  refreshDialogVisible.value = false
  refreshing.value = false
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = ''
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
      console.error('清空数据失败:', error)
      ElMessage.error(error.message || '清空数据失败')
    } finally {
      clearing.value = false
    }
  } catch (error) {
    // 用户取消
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.fund-collection-detail {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.collection-info h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #303133;
}

.collection-info .description {
  margin: 0 0 12px 0;
  color: #606266;
  font-size: 14px;
}

.stats {
  display: flex;
  gap: 12px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.table-card {
  background: #fff;
}

.chart-card {
  margin-top: 20px;
  background: #fff;
}

.table-controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.filter-controls,
.sort-controls {
  display: flex;
  align-items: center;
}

.sort-controls span {
  color: #606266;
  font-size: 14px;
}
</style>
