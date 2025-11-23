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
      <el-row :gutter="16" style="margin-top: 16px;">
        <!-- 快速导航 -->
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover" style="height: 100%;">
            <template #header><div>快速导航</div></template>
            <el-row :gutter="16">
              <el-col :xs="24" style="margin-bottom: 16px;">
                <el-button type="primary" size="large" style="width: 100%" @click="$router.push('/currencies/collections')">
                  <el-icon><Box /></el-icon><span style="margin-left: 8px">数据集合</span>
                </el-button>
              </el-col>
              <el-col :xs="24">
                <el-button type="success" size="large" style="width: 100%" @click="$router.push('/currencies/analysis')">
                  <el-icon><DataAnalysis /></el-icon><span style="margin-left: 8px">外汇分析</span>
                </el-button>
              </el-col>
            </el-row>
          </el-card>
        </el-col>

        <!-- 货币转换器 -->
        <el-col :xs="24" :sm="12">
          <el-card shadow="hover" v-loading="converting">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>货币转换计算器</span>
                <el-button type="primary" size="small" @click="handleConvert">转换</el-button>
              </div>
            </template>
            
            <el-form label-position="top">
              <el-row :gutter="12">
                <el-col :span="12">
                  <el-form-item label="基础货币 (From)">
                    <el-input v-model="convertForm.base" placeholder="USD" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="目标货币 (To)">
                    <el-input v-model="convertForm.to" placeholder="CNY" />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="数量">
                <el-input v-model="convertForm.amount" placeholder="10000" type="number" />
              </el-form-item>
              
              <el-form-item label="API Key">
                <el-input v-model="convertForm.apiKey" type="password" show-password placeholder="CurrencyScoop API Key" />
              </el-form-item>
              
              <div v-if="convertResult" style="margin-top: 16px; padding: 16px; background-color: #f5f7fa; border-radius: 4px;">
                <div style="font-size: 14px; color: #909399;">转换结果</div>
                <div style="font-size: 24px; font-weight: bold; color: #67c23a; margin-top: 8px;">
                  {{ Number(convertResult.value).toLocaleString() }} {{ convertResult.to }}
                </div>
                <div style="font-size: 12px; color: #909399; margin-top: 4px;">
                  1 {{ convertResult.base }} = {{ (convertResult.value / convertResult.amount).toFixed(6) }} {{ convertResult.to }}
                </div>
                <div style="font-size: 12px; color: #c0c4cc; margin-top: 4px;">
                  更新时间: {{ convertResult.date }}
                </div>
              </div>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { TrendCharts, Box, DataAnalysis } from '@element-plus/icons-vue'
import { currenciesApi } from '@/api/currencies'
import { ElMessage } from 'element-plus'

const stats = ref<any>({})
const collections = ref<any[]>([])
const converting = ref(false)

const convertForm = reactive({
    base: 'USD',
    to: 'CNY',
    amount: '10000',
    apiKey: ''
})
const convertResult = ref<any>(null)

const handleConvert = async () => {
    if (!convertForm.apiKey) {
        ElMessage.warning('请输入 API Key')
        return
    }
    
    converting.value = true
    try {
        const res = await currenciesApi.convertCurrencyTool({
            base: convertForm.base,
            to: convertForm.to,
            amount: convertForm.amount,
            api_key: convertForm.apiKey
        })
        
        if (res.success) {
            convertResult.value = res.data
        } else {
            ElMessage.error(res.message || '转换失败')
        }
    } catch (error) {
        ElMessage.error('转换请求失败')
    } finally {
        converting.value = false
    }
}

onMounted(async () => {
  try {
    const overviewRes = await currenciesApi.getOverview()
    if (overviewRes.success) stats.value = overviewRes.data
    const collectionsRes = await currenciesApi.getCollections()
    if (collectionsRes.success) collections.value = collectionsRes.data
    
    // Load default config
    const configRes = await currenciesApi.getConfig()
    if (configRes.success && configRes.data.default_api_key) {
        convertForm.apiKey = configRes.data.default_api_key
    }
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
