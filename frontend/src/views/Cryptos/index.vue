<template>
  <div class="cryptos-overview">
    <div class="page-header">
      <h1 class="page-title"><el-icon><TrendCharts /></el-icon> 数字货币投研 · 概览</h1>
      <p class="page-description">数字货币投研概览，提供数字货币数据的综合视图和分析工具</p>
    </div>
    <div class="content">
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12" :md="8">
          <el-card shadow="hover"><el-statistic title="数字货币总数" :value="stats.total_cryptos || 0" /></el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-card shadow="hover"><el-statistic title="数据集合" :value="collections.length" /></el-card>
        </el-col>
      </el-row>
      <el-card shadow="hover" style="margin-top: 16px;">
        <template #header><div>快速导航</div></template>
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="8">
            <el-button type="primary" size="large" style="width: 100%" @click="$router.push('/cryptos/collections')">
              <el-icon><Box /></el-icon><span style="margin-left: 8px">数据集合</span>
            </el-button>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" style="margin-top: 8px">
            <el-button type="success" size="large" style="width: 100%" @click="$router.push('/cryptos/analysis')">
              <el-icon><DataAnalysis /></el-icon><span style="margin-left: 8px">数字货币分析</span>
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
import { cryptosApi } from '@/api/cryptos'

const stats = ref<any>({})
const collections = ref<any[]>([])

onMounted(async () => {
  try {
    const overviewRes = await cryptosApi.getOverview()
    if (overviewRes.success) stats.value = overviewRes.data
    const collectionsRes = await cryptosApi.getCollections()
    if (collectionsRes.success) collections.value = collectionsRes.data
  } catch (error) { console.error('加载数据失败:', error) }
})
</script>

<style scoped>
.cryptos-overview { padding: 16px; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 600; color: #303133; margin: 0; display: flex; align-items: center; gap: 12px; }
.page-description { font-size: 14px; color: #909399; margin: 8px 0 0 0; }
.content { max-width: 1400px; }
</style>
