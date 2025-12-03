<template>
  <div class="fund-analysis">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><DataAnalysis /></el-icon>
            基金分析
          </h1>
          <p class="page-description">对单只基金进行深入分析</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 搜索框 -->
      <el-card shadow="hover" class="search-card">
        <el-form :inline="true" @submit.prevent="searchFund">
          <el-form-item label="基金代码/名称">
            <el-input
              v-model="searchKeyword"
              placeholder="输入基金代码或名称..."
              clearable
              style="width: 300px"
              @keyup.enter="searchFund"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchFund" :loading="searching">
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
        <el-table :data="searchResults" stripe @row-click="selectFund">
          <el-table-column prop="code" label="代码" width="120" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="type" label="类型" width="120" />
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click.stop="selectFund(row)">
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 基金详情 -->
      <el-card v-if="selectedFund" shadow="hover" class="details-card">
        <template #header>
          <div class="card-header">
            {{ selectedFund.code }} - {{ selectedFund.name }}
          </div>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="基金代码">
            {{ selectedFund.code }}
          </el-descriptions-item>
          <el-descriptions-item label="基金名称">
            {{ selectedFund.name }}
          </el-descriptions-item>
          <el-descriptions-item label="基金类型">
            {{ selectedFund.type || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="基金规模">
            {{ selectedFund.size || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="基金经理">
            {{ selectedFund.manager || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="成立日期">
            {{ selectedFund.establish_date || '-' }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 净值数据 -->
        <div v-if="netValues.length > 0" style="margin-top: 24px;">
          <h3>最近净值数据</h3>
          <el-table :data="netValues.slice(0, 10)" stripe>
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="net_value" label="单位净值" />
            <el-table-column prop="accumulated_value" label="累计净值" />
            <el-table-column prop="growth_rate" label="增长率" />
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
        v-if="!selectedFund && searchResults.length === 0 && !searching"
        description="请搜索基金开始分析"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { DataAnalysis, Search } from '@element-plus/icons-vue'
import { fundsApi } from '@/api/funds'
import { ElMessage } from 'element-plus'

const searchKeyword = ref('')
const searching = ref(false)
const searchResults = ref<any[]>([])
const selectedFund = ref<any>(null)
const netValues = ref<any[]>([])

const searchFund = async () => {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  searching.value = true
  try {
    const res = await fundsApi.searchFunds(searchKeyword.value)
    if (res.success) {
      searchResults.value = res.data
      if (res.data.length === 0) {
        ElMessage.info('未找到匹配的基金')
      }
    } else {
      ElMessage.error(res.message || '搜索失败')
    }
  } catch (error: any) {
    console.error('搜索基金失败:', error)
    ElMessage.error(error.message || '搜索失败')
  } finally {
    searching.value = false
  }
}

const selectFund = async (fund: any) => {
  selectedFund.value = fund
  netValues.value = []

  try {
    const res = await fundsApi.getFundAnalysis(fund.code)
    if (res.success) {
      if (res.data.basic_info) {
        selectedFund.value = res.data.basic_info
      }
      if (res.data.net_values) {
        netValues.value = res.data.net_values
      }
    }
  } catch (error: any) {
    console.error('获取基金分析失败:', error)
    ElMessage.error(error.message || '获取基金分析失败')
  }
}
</script>

<style scoped>
.fund-analysis {
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
