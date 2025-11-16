<template>
  <div class="currencies-overview">
    <div class="page-header">
      <h1 class="page-title"><el-icon><TrendCharts /></el-icon> 外汇投研 · 概览</h1>
      <p class="page-description">外汇投研概览，提供外汇数据的综合视图和分析工具</p>
    </div>
    <div class="content">
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12" :md="8">
          <el-card shadow="hover"><el-statistic title="外汇货币对总数" :value="stats.total_pairs || 0" /></el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-card shadow="hover"><el-statistic title="数据集合" :value="collections.length" /></el-card>
        </el-col>
      </el-row>
      <el-card shadow="hover" style="margin-top: 16px;">
        <template #header><div>快速导航</div></template>
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="8">
            <el-button type="primary" size="large" style="width: 100%" @click="$router.push('/currencies/collections')">
              <el-icon><Box /></el-icon><span style="margin-left: 8px">数据集合</span>
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" style="margin-top: 8px">
            <el-button type="success" size="large" style="width: 100%" @click="$router.push('/currencies/analysis')">
              <el-icon><DataAnalysis /></el-icon><span style="margin-left: 8px">外汇分析</span>
            </el-button>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { TrendCharts, Box, DataAnalysis } from '@element-plus/icons-vue'
import { currenciesApi } from '@/api/currencies'

const stats = ref<any>({})
const collections = ref<any[]>([])

onMounted(async () => {
  try {
    const overviewRes = await currenciesApi.getOverview()
    if (overviewRes.success) stats.value = overviewRes.data
    const collectionsRes = await currenciesApi.getCollections()
    if (collectionsRes.success) collections.value = collectionsRes.data
  } catch (error) { console.error('加载数据失败:', error) }
})
</script>

<style scoped>
.currencies-overview { padding: 16px; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 600; color: #303133; margin: 0; display: flex; align-items: center; gap: 12px; }
.page-description { font-size: 14px; color: #909399; margin: 8px 0 0 0; }
.content { max-width: 1400px; }
</style>
