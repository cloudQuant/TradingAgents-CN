<template>
  <div class="options-overview">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><TrendCharts /></el-icon>
            期权投研 · 概览
          </h1>
          <p class="page-description">期权投研概览，提供期权数据的综合视图和分析工具</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 数据统计卡片 -->
      <el-row :gutter="16" class="stats-row">
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="期权合约总数" :value="stats.total_contracts || 0" />
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8" :lg="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="数据集合" :value="collections.length" />
          </el-card>
        </el-col>
      </el-row>

      <!-- 快速导航 -->
      <el-card shadow="hover" style="margin-top: 16px;">
        <template #header>
          <div class="card-header">快速导航</div>
        </template>
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="8">
            <el-button
              type="primary"
              size="large"
              style="width: 100%"
              @click="$router.push('/options/collections')"
            >
              <el-icon><Box /></el-icon>
              <span style="margin-left: 8px;">数据集合</span>
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" style="margin-top: 8px">
            <el-button
              type="success"
              size="large"
              style="width: 100%"
              @click="$router.push('/options/analysis')"
            >
              <el-icon><DataAnalysis /></el-icon>
              <span style="margin-left: 8px;">期权分析</span>
            </el-button>
          </el-col>
        </el-row>
      </el-card>

      <!-- 功能说明 -->
      <el-card shadow="hover" style="margin-top: 16px;">
        <template #header>
          <div class="card-header">功能说明</div>
        </template>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="数据集合">
            查看和管理各类期权数据集合，包括基础信息、日行情、希腊值等
          </el-descriptions-item>
          <el-descriptions-item label="期权分析">
            对期权合约进行深入分析，包括价格走势、希腊字母指标等
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag type="info">功能开发中</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { TrendCharts, Box, DataAnalysis } from '@element-plus/icons-vue'
import { optionsApi } from '@/api/options'
import { ElMessage } from 'element-plus'

const stats = ref<any>({})
const collections = ref<any[]>([])
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    // 加载概览数据
    const overviewRes = await optionsApi.getOverview()
    if (overviewRes.success) {
      stats.value = overviewRes.data
    }

    // 加载集合列表
    const collectionsRes = await optionsApi.getCollections()
    if (collectionsRes.success) {
      collections.value = collectionsRes.data
    }
  } catch (error: any) {
    console.error('加载数据失败:', error)
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.options-overview {
  padding: 16px;
}

.page-header {
  margin-bottom: 24px;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 32px;
  color: #409eff;
}

.page-description {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.stats-row {
  margin-bottom: 16px;
}

.stat-card {
  text-align: center;
  margin-bottom: 16px;
}

.card-header {
  font-weight: 600;
  font-size: 16px;
}

.content {
  max-width: 1400px;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 24px;
  }
}
</style>
