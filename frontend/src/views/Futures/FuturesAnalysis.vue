<template>
  <div class="futures-analysis">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><DataAnalysis /></el-icon>
            期货分析
          </h1>
          <p class="page-description">对期货合约进行深入分析</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 搜索框 -->
      <el-card shadow="hover" class="search-card">
        <el-form :inline="true" @submit.prevent="searchFutures">
          <el-form-item label="期货代码/名称">
            <el-input
              v-model="searchKeyword"
              placeholder="输入期货代码或名称..."
              clearable
              style="width: 300px"
              @keyup.enter="searchFutures"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchFutures" :loading="searching">
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
        <el-table :data="searchResults" stripe @row-click="selectFutures">
          <el-table-column prop="code" label="代码" width="120" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="exchange" label="交易所" width="100" />
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click.stop="selectFutures(row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 期货详情 -->
      <el-card v-if="selectedFutures" shadow="hover" class="details-card">
        <template #header>
          <div class="card-header">
            {{ selectedFutures.code }} - {{ selectedFutures.name }}
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="期货代码">
            {{ selectedFutures.code }}
          </el-descriptions-item>
          <el-descriptions-item label="期货名称">
            {{ selectedFutures.name }}
          </el-descriptions-item>
          <el-descriptions-item label="交易所">
            {{ selectedFutures.exchange || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="标的资产">
            {{ selectedFutures.underlying_asset || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="合约规格">
            {{ selectedFutures.contract_size || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="交割月份">
            {{ selectedFutures.delivery_month || '-' }}
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
        v-if="!selectedFutures && searchResults.length === 0 && !searching"
        description="请搜索期货合约开始分析"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { DataAnalysis, Search } from '@element-plus/icons-vue'
import { futuresApi } from '@/api/futures'
import { ElMessage } from 'element-plus'

const searchKeyword = ref('')
const searching = ref(false)
const searchResults = ref<any[]>([])
const selectedFutures = ref<any>(null)
const quotes = ref<any[]>([])

const searchFutures = async () => {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  searching.value = true
  try {
    const res = await futuresApi.searchFutures(searchKeyword.value)
    if (res.success) {
      searchResults.value = res.data
      if (res.data.length === 0) {
        ElMessage.info('未找到匹配的期货合约')
      }
    } else {
      ElMessage.error(res.error || '搜索失败')
    }
  } catch (error: any) {
    console.error('搜索期货失败:', error)
    ElMessage.error(error.message || '搜索失败')
  } finally {
    searching.value = false
  }
}

const selectFutures = async (futures: any) => {
  selectedFutures.value = futures
  quotes.value = []

  try {
    const res = await futuresApi.getFuturesAnalysis(futures.code)
    if (res.success) {
      if (res.data.basic_info) {
        selectedFutures.value = res.data.basic_info
      }
      if (res.data.quotes) {
        quotes.value = res.data.quotes
      }
    }
  } catch (error: any) {
    console.error('获取期货分析失败:', error)
    ElMessage.error(error.message || '获取期货分析失败')
  }
}
</script>

<style scoped>
.futures-analysis {
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
