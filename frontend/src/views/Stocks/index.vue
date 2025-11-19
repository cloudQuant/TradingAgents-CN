<template>
  <div class="stocks-overview">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><TrendCharts /></el-icon>
            股票投研 · 概览
          </h1>
          <p class="page-description">查看股票市场概况，浏览热门股票和实时行情</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 数据统计卡片 -->
      <el-row :gutter="16" class="stats-row">
        <el-col :xs="12" :sm="8" :md="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="A股总数" :value="stats.total">
              <template #prefix>
                <el-icon color="#409EFF"><TrendCharts /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="沪市" :value="stats.sh">
              <template #prefix>
                <el-tag type="success" size="small">SH</el-tag>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="深市" :value="stats.sz">
              <template #prefix>
                <el-tag type="primary" size="small">SZ</el-tag>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="数据更新" value="实时">
              <template #prefix>
                <el-icon color="#67C23A"><CircleCheck /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
      </el-row>

      <!-- 快速导航 -->
      <el-card shadow="hover" class="nav-card" style="margin-top: 16px;">
        <template #header>
          <div class="card-header">
            <span>快速导航</span>
          </div>
        </template>
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12" :md="6">
            <el-card shadow="hover" class="feature-card" @click="navigateTo('/stocks/collections')">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40"><DataAnalysis /></el-icon>
                <h3>数据集合</h3>
                <p>查看6个股票数据集合</p>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-card shadow="hover" class="feature-card" @click="navigateTo('/analysis/single')">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40"><Document /></el-icon>
                <h3>单股分析</h3>
                <p>分析单只股票</p>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-card shadow="hover" class="feature-card" @click="navigateTo('/analysis/batch')">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40"><Grid /></el-icon>
                <h3>批量分析</h3>
                <p>批量分析多只股票</p>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-card shadow="hover" class="feature-card" @click="navigateTo('/screening')">
              <div class="feature-content">
                <el-icon class="feature-icon" size="40"><Search /></el-icon>
                <h3>股票筛选</h3>
                <p>多维度筛选股票</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
      
      <!-- 市场行情一览 -->
      <el-card shadow="hover" class="quotes-card">
        <template #header>
          <div class="card-header">
            <span>市场行情一览</span>
            <div class="quotes-toolbar">
              <el-input
                v-model="keyword"
                placeholder="按代码或名称搜索"
                size="small"
                clearable
                @keyup.enter="handleSearch"
                style="width: 220px;"
              />
              <el-button
                type="primary"
                size="small"
                style="margin-left: 8px;"
                @click="handleSearch"
              >
                查询
              </el-button>
            </div>
          </div>
        </template>

        <el-table
          :data="quotes"
          :loading="loading"
          size="small"
          stripe
          style="width: 100%"
          :default-sort="{ prop: 'amount', order: 'descending' }"
          @sort-change="handleSortChange"
        >
          <el-table-column
            prop="code"
            label="代码"
            width="120"
            sortable="custom"
          >
            <template #default="{ row }">
              <el-link type="primary" @click="navigateTo(`/stocks/${row.code}`)">
                {{ row.code }}
              </el-link>
            </template>
          </el-table-column>

          <el-table-column
            prop="name"
            label="名称"
            min-width="140"
            sortable="custom"
          >
            <template #default="{ row }">
              <el-link type="primary" @click="navigateTo(`/stocks/${row.code}`)">
                {{ row.name }}
              </el-link>
            </template>
          </el-table-column>

          <el-table-column
            prop="latest_price"
            label="最新价"
            width="100"
            sortable="custom"
          >
            <template #default="{ row }">
              {{ typeof row.latest_price === 'number' ? row.latest_price.toFixed(2) : '-' }}
            </template>
          </el-table-column>

          <el-table-column
            prop="pct_chg"
            label="涨跌幅(%)"
            width="110"
            sortable="custom"
          >
            <template #default="{ row }">
              <span :class="pctClass(row.pct_chg ?? 0)">
                {{ typeof row.pct_chg === 'number' ? row.pct_chg.toFixed(2) : '-' }}
              </span>
            </template>
          </el-table-column>

          <el-table-column
            prop="volume"
            label="成交量"
            width="140"
            sortable="custom"
          >
            <template #default="{ row }">
              {{ formatAmount(row.volume) }}
            </template>
          </el-table-column>

          <el-table-column
            prop="amount"
            label="成交额"
            width="140"
            sortable="custom"
          >
            <template #default="{ row }">
              {{ formatAmount(row.amount) }}
            </template>
          </el-table-column>
        </el-table>

        <div class="quotes-pagination">
          <el-pagination
            background
            layout="prev, pager, next, total"
            :current-page="page"
            :page-size="pageSize"
            :total="total"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>

      <!-- 说明文档 -->
      <el-card shadow="hover" class="info-card" style="margin-top: 16px;">
        <template #header>
          <div class="card-header">
            <span>功能说明</span>
          </div>
        </template>
        <div class="info-content">
          <h3>📊 股票投研功能</h3>
          <ul>
            <li><strong>数据集合</strong>：查看6个核心数据集合（基础信息、实时行情、财务数据、历史K线等）</li>
            <li><strong>单股分析</strong>：深度分析单只股票的基本面和技术面</li>
            <li><strong>批量分析</strong>：同时分析多只股票，进行对比</li>
            <li><strong>股票筛选</strong>：使用多个条件筛选符合要求的股票</li>
            <li><strong>分析报告</strong>：查看历史分析报告</li>
          </ul>

          <h3 style="margin-top: 20px;">💡 使用提示</h3>
          <ul>
            <li>点击上方快速导航卡片可直接进入对应功能</li>
            <li>支持A股、港股、美股的数据查询和分析</li>
            <li>数据来源包括Tushare、AKShare、BaoStock等</li>
          </ul>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { TrendCharts, CircleCheck, DataAnalysis, Document, Grid, Search } from '@element-plus/icons-vue'
import { stocksApi } from '@/api/stocks'

const router = useRouter()

interface StockQuoteRow {
  code: string
  name?: string
  latest_price?: number
  pct_chg?: number
  volume?: number
  amount?: number
}

const stats = ref({
  total: 5000,
  sh: 2100,
  sz: 2900,
})

const quotes = ref<StockQuoteRow[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const keyword = ref('')
const sortBy = ref<string | undefined>('amount')
const sortDir = ref<'asc' | 'desc' | ''>('desc')

const navigateTo = (path: string) => {
  router.push(path)
}

const formatAmount = (value: number) => {
  if (value == null || isNaN(value)) return '-'
  if (value >= 1e8) return (value / 1e8).toFixed(2) + '亿'
  if (value >= 1e4) return (value / 1e4).toFixed(2) + '万'
  return value.toString()
}

const pctClass = (value: number) => {
  if (value > 0) return 'pct-positive'
  if (value < 0) return 'pct-negative'
  return 'pct-neutral'
}

const loadQuotes = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value || undefined,
    }

    if (sortBy.value) {
      params.sort_by = sortBy.value
      params.sort_dir = sortDir.value || 'desc'
    }

    const res = await stocksApi.getQuotesOverview(params)
    const data = res.data
    quotes.value = data.items || []
    total.value = data.total || 0
    page.value = data.page || page.value
    pageSize.value = data.page_size || pageSize.value
  } catch (error) {
    console.error('加载市场行情失败', error)
    ElMessage.error('加载市场行情失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  loadQuotes()
}

const handlePageChange = (newPage: number) => {
  page.value = newPage
  loadQuotes()
}

const handleSortChange = (sort: { prop: string; order: 'ascending' | 'descending' | null }) => {
  // 代码 / 名称：前端本地排序（只对当前页）
  if (sort.prop === 'code' || sort.prop === 'name') {
    if (!sort.order) {
      // 清除排序时，回到默认后端排序
      sortBy.value = 'amount'
      sortDir.value = 'desc'
      page.value = 1
      loadQuotes()
      return
    }

    const factor = sort.order === 'ascending' ? 1 : -1
    const prop = sort.prop as 'code' | 'name'
    quotes.value = [...quotes.value].sort((a, b) => {
      const va = (a[prop] || '') as string
      const vb = (b[prop] || '') as string
      return va.localeCompare(vb, 'zh-Hans-CN') * factor
    })
    return
  }

  // 数值字段：后端排序
  if (!sort.order) {
    // 如果清除排序，则回到默认：按成交额降序
    sortBy.value = 'amount'
    sortDir.value = 'desc'
  } else {
    let backendField = 'amount'
    if (sort.prop === 'latest_price') {
      backendField = 'close'
    } else if (sort.prop === 'pct_chg') {
      backendField = 'pct_chg'
    } else if (sort.prop === 'volume') {
      backendField = 'volume'
    } else if (sort.prop === 'amount') {
      backendField = 'amount'
    }
    sortBy.value = backendField
    sortDir.value = sort.order === 'ascending' ? 'asc' : 'desc'
  }

  // 排序变化时回到第一页并重新请求
  page.value = 1
  loadQuotes()
}

onMounted(() => {
  loadQuotes()
})
</script>

<style scoped>
.stocks-overview {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 32px;
  color: #409EFF;
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
  cursor: default;
}

.stat-card:hover {
  transform: translateY(-2px);
  transition: all 0.3s;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.quotes-toolbar {
  display: flex;
  align-items: center;
}

.nav-card {
  margin-top: 16px;
}

.quotes-card {
  margin-top: 16px;
}

.quotes-pagination {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.feature-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.feature-content {
  text-align: center;
  padding: 20px 10px;
}

.feature-icon {
  color: #409EFF;
  margin-bottom: 12px;
}

.feature-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 8px 0;
}

.feature-content p {
  font-size: 13px;
  color: #909399;
  margin: 0;
}

.info-card {
  margin-top: 16px;
}

.info-content {
  line-height: 1.8;
}

.info-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.info-content ul {
  padding-left: 20px;
  margin: 8px 0;
}

.info-content li {
  margin-bottom: 8px;
  color: #606266;
}

.pct-positive {
  color: #f56c6c;
}

.pct-negative {
  color: #67c23a;
}

.pct-neutral {
  color: #606266;
}
</style>
