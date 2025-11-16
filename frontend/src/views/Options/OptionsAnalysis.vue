<template>
  <div class="options-analysis">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><DataAnalysis /></el-icon>
            期权分析
          </h1>
          <p class="page-description">对期权合约进行深入分析</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 搜索框 -->
      <el-card shadow="hover" class="search-card">
        <el-form :inline="true" @submit.prevent="searchOptions">
          <el-form-item label="期权代码/名称">
            <el-input
              v-model="searchKeyword"
              placeholder="输入期权代码或名称..."
              clearable
              style="width: 300px"
              @keyup.enter="searchOptions"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchOptions" :loading="searching">
              搜索
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 搜索结果 -->
      <el-card v-if="searchResults.length > 0" shadow="hover" class="results-card">
        <template #header>
          <div class="card-header">搜索结果</div>
        </template>
        <el-table :data="searchResults" stripe @row-click="selectOption">
          <el-table-column prop="code" label="代码" width="150" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="option_type" label="类型" width="80" />
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click.stop="selectOption(row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 期权详情 -->
      <el-card v-if="selectedOption" shadow="hover" class="details-card">
        <template #header>
          <div class="card-header">
            {{ selectedOption.code }} - {{ selectedOption.name }}
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="期权代码">
            {{ selectedOption.code }}
          </el-descriptions-item>
          <el-descriptions-item label="期权名称">
            {{ selectedOption.name }}
          </el-descriptions-item>
          <el-descriptions-item label="标的资产">
            {{ selectedOption.underlying || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="行权价">
            {{ selectedOption.strike_price || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="期权类型">
            {{ selectedOption.option_type || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="到期日">
            {{ selectedOption.expiry_date || '-' }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 行情数据 -->
        <div v-if="quotes.length > 0" style="margin-top: 24px;">
          <h3>最近行情数据</h3>
          <el-table :data="quotes.slice(0, 10)" stripe>
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="open" label="开盘价" />
            <el-table-column prop="high" label="最高价" />
            <el-table-column prop="low" label="最低价" />
            <el-table-column prop="close" label="收盘价" />
            <el-table-column prop="volume" label="成交量" />
          </el-table>
        </div>

        <!-- 希腊值数据 -->
        <div v-if="greeks.length > 0" style="margin-top: 24px;">
          <h3>希腊字母指标</h3>
          <el-table :data="greeks.slice(0, 10)" stripe>
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="delta" label="Delta" />
            <el-table-column prop="gamma" label="Gamma" />
            <el-table-column prop="theta" label="Theta" />
            <el-table-column prop="vega" label="Vega" />
            <el-table-column prop="rho" label="Rho" />
          </el-table>
        </div>

        <!-- 开发中提示 -->
        <el-alert
          type="info"
          :closable="false"
          style="margin-top: 16px;"
          title="功能开发中"
          description="更多分析功能正在开发中，敬请期待..."
        />
      </el-card>

      <!-- 空状态 -->
      <el-empty
        v-if="!selectedOption && searchResults.length === 0 && !searching"
        description="请搜索期权合约开始分析"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { DataAnalysis, Search } from '@element-plus/icons-vue'
import { optionsApi } from '@/api/options'
import { ElMessage } from 'element-plus'

const searchKeyword = ref('')
const searching = ref(false)
const searchResults = ref<any[]>([])
const selectedOption = ref<any>(null)
const quotes = ref<any[]>([])
const greeks = ref<any[]>([])

const searchOptions = async () => {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  searching.value = true
  try {
    const res = await optionsApi.searchOptions(searchKeyword.value)
    if (res.success) {
      searchResults.value = res.data
      if (res.data.length === 0) {
        ElMessage.info('未找到匹配的期权合约')
      }
    } else {
      ElMessage.error(res.error || '搜索失败')
    }
  } catch (error: any) {
    console.error('搜索期权失败:', error)
    ElMessage.error(error.message || '搜索失败')
  } finally {
    searching.value = false
  }
}

const selectOption = async (option: any) => {
  selectedOption.value = option
  quotes.value = []
  greeks.value = []

  try {
    const res = await optionsApi.getOptionAnalysis(option.code)
    if (res.success) {
      if (res.data.basic_info) {
        selectedOption.value = res.data.basic_info
      }
      if (res.data.quotes) {
        quotes.value = res.data.quotes
      }
      if (res.data.greeks) {
        greeks.value = res.data.greeks
      }
    }
  } catch (error: any) {
    console.error('获取期权分析失败:', error)
    ElMessage.error(error.message || '获取期权分析失败')
  }
}
</script>

<style scoped>
.options-analysis {
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

.content {
  max-width: 1400px;
}

.search-card,
.results-card,
.details-card {
  margin-bottom: 16px;
}

.card-header {
  font-weight: 600;
  font-size: 16px;
}

h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
}
</style>
