<template>
  <div class="sync-tasks-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>同步任务</h2>
      <el-button @click="loadTasks" :loading="loading">
        <el-icon><Refresh /></el-icon> 刷新
      </el-button>
    </div>

    <!-- 任务列表 -->
    <el-table :data="tasks" v-loading="loading" stripe>
      <el-table-column prop="task_id" label="任务ID" width="280" show-overflow-tooltip />
      <el-table-column prop="direction" label="方向" width="100">
        <template #default="{ row }">
          <el-tag :type="row.direction === 'pull' ? 'primary' : 'success'">
            {{ row.direction === 'pull' ? '拉取' : '推送' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="collection" label="集合" width="180" />
      <el-table-column label="节点" width="150">
        <template #default="{ row }">
          {{ row.direction === 'pull' ? row.source_node : row.target_node }}
        </template>
      </el-table-column>
      <el-table-column prop="strategy" label="策略" width="100">
        <template #default="{ row }">
          {{ row.strategy === 'incremental' ? '增量' : '全量' }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="进度" width="200">
        <template #default="{ row }">
          <el-progress 
            :percentage="getProgress(row)" 
            :status="row.status === 'completed' ? 'success' : row.status === 'failed' ? 'exception' : ''"
            :stroke-width="8"
          />
          <div class="progress-text">
            {{ row.stats.transferred }}/{{ row.stats.total_records }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="统计" width="180">
        <template #default="{ row }">
          <span class="stat-item">插入: {{ row.stats.inserted }}</span>
          <span class="stat-item">更新: {{ row.stats.updated }}</span>
          <span class="stat-item" v-if="row.stats.failed">失败: {{ row.stats.failed }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="started_at" label="开始时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.started_at) }}
        </template>
      </el-table-column>
      <el-table-column label="错误信息" min-width="200">
        <template #default="{ row }">
          <span v-if="row.error_message" class="error-text">{{ row.error_message }}</span>
          <span v-else>-</span>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { getSyncTasks, type SyncTask } from '@/api/sync'

const loading = ref(false)
const tasks = ref<SyncTask[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

let refreshTimer: number | null = null

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const res = await getSyncTasks({
      limit: pageSize.value,
      skip: (currentPage.value - 1) * pageSize.value
    })
    if (res.success && res.data) {
      tasks.value = res.data
      // 假设总数从 data 长度或其他字段获取
      total.value = res.data.length >= pageSize.value ? currentPage.value * pageSize.value + 1 : tasks.value.length
    }
  } catch (e) {
    console.error('加载任务失败:', e)
  } finally {
    loading.value = false
  }
}

// 获取状态类型
const getStatusType = (status: string): 'success' | 'warning' | 'info' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '等待中',
    running: '进行中',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

// 计算进度
const getProgress = (task: SyncTask) => {
  if (!task.stats.total_records) return 0
  return Math.round((task.stats.transferred / task.stats.total_records) * 100)
}

// 格式化日期时间
const formatDateTime = (dateStr?: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 处理分页变化
const handlePageChange = (page: number) => {
  currentPage.value = page
  loadTasks()
}

// 自动刷新运行中的任务
const startAutoRefresh = () => {
  refreshTimer = window.setInterval(() => {
    const hasRunning = tasks.value.some(t => t.status === 'running' || t.status === 'pending')
    if (hasRunning) {
      loadTasks()
    }
  }, 2000)
}

onMounted(() => {
  loadTasks()
  startAutoRefresh()
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.sync-tasks-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.progress-text {
  font-size: 12px;
  color: #909399;
  text-align: center;
}

.stat-item {
  margin-right: 8px;
  font-size: 12px;
}

.error-text {
  color: #f56c6c;
  font-size: 12px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
