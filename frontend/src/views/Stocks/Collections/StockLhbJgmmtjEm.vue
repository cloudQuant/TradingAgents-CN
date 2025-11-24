<template>
  <div class="stock_lhb_jgmmtj_em-container">
    <el-card class="header-card">
      <h2>机构买卖每日统计</h2>
    </el-card>

    <el-card class="overview-card">
      <h3>数据概览</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{ overview.total_count || 0 }}</div>
            <div class="stat-label">总记录数</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{ formatDate(overview.last_updated) }}</div>
            <div class="stat-label">最后更新</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="actions-card">
      <el-button type="primary" @click="refreshData" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
      <el-button type="danger" @click="clearData" :loading="loading">
        <el-icon><Delete /></el-icon>
        清空数据
      </el-button>
    </el-card>

    <el-card class="table-card">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column 
          v-for="col in columns" 
          :key="col.prop"
          :prop="col.prop" 
          :label="col.label"
          :width="col.width"
        />
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const API_BASE = '/api/stocks/collections/stock_lhb_jgmmtj_em'

const loading = ref(false)
const overview = ref({})
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const columns = computed(() => {
  if (tableData.value.length === 0) return []
  const firstRow = tableData.value[0]
  return Object.keys(firstRow)
    .filter(key => key !== '_id')
    .map(key => ({
      prop: key,
      label: key,
      width: 150
    }))
})

const loadOverview = async () => {
  try {
    const response = await axios.get(`${API_BASE}/overview`)
    overview.value = response.data
  } catch (error) {
    console.error('Failed to load overview:', error)
  }
}

const loadData = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await axios.get(API_BASE, {
      params: { skip, limit: pageSize.value }
    })
    tableData.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    const response = await axios.post(`${API_BASE}/refresh`)
    if (response.data.success) {
      ElMessage.success(`数据刷新成功！插入: ${response.data.inserted}`)
      await loadOverview()
      await loadData()
    }
  } catch (error) {
    ElMessage.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

const clearData = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有数据吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    const response = await axios.delete(`${API_BASE}/clear`)
    
    if (response.data.success) {
      ElMessage.success(`已删除 ${response.data.deleted} 条记录`)
      await loadOverview()
      await loadData()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空数据失败')
    }
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadData()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadOverview()
  loadData()
})
</script>

<style scoped>
.stock_lhb_jgmmtj_em-container {
  padding: 20px;
}

.header-card, .overview-card, .actions-card, .table-card {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}
</style>
