<template>
  <div class="currencies-analysis">
    <div class="page-header">
      <h1 class="page-title"><el-icon><DataAnalysis /></el-icon> 外汇分析</h1>
      <p class="page-description">对外汇货币对进行深入分析</p>
    </div>
    <div class="content">
      <el-card shadow="hover">
        <el-form :inline="true" @submit.prevent="searchCurrencies">
          <el-form-item label="货币对">
            <el-input v-model="searchKeyword" placeholder="输入货币对..." clearable style="width: 300px" @keyup.enter="searchCurrencies">
              <template #prefix><el-icon><Search /></el-icon></template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchCurrencies" :loading="searching">搜索</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      <el-alert type="info" :closable="false" style="margin-top: 16px" title="功能开发中" description="外汇分析功能正在开发中，敬请期待..." />
      <el-empty v-if="!searching" description="请搜索货币对开始分析" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { DataAnalysis, Search } from '@element-plus/icons-vue'
import { currenciesApi } from '@/api/currencies'

const searchKeyword = ref('')
const searching = ref(false)

const searchCurrencies = async () => {
  if (!searchKeyword.value.trim()) return
  searching.value = true
  try {
    const res = await currenciesApi.searchCurrencies(searchKeyword.value)
    console.log('搜索结果:', res)
  } catch (error) { console.error('搜索失败:', error) }
  finally { searching.value = false }
}
</script>

<style scoped>
.currencies-analysis { padding: 16px; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 600; color: #303133; margin: 0; display: flex; align-items: center; gap: 12px; }
.page-description { font-size: 14px; color: #909399; margin: 8px 0 0 0; }
.content { max-width: 1400px; }
</style>
