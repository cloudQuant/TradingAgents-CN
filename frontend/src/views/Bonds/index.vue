<template>
  <div class="bonds-overview">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Tickets /></el-icon>
            债券分析 · 概览
          </h1>
          <p class="page-description">搜索并浏览各类债券的基础信息，支持多维度筛选和排序</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 数据统计卡片 -->
      <el-row :gutter="16" class="stats-row">
        <el-col :xs="12" :sm="8" :md="6" :lg="4">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="债券总数" :value="stats.total" />
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6" :lg="4">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="可转债" :value="stats.convertible">
              <template #prefix>
                <el-tag type="success" size="small">可转债</el-tag>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6" :lg="4">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="利率债" :value="stats.interest">
              <template #prefix>
                <el-tag type="primary" size="small">利率债</el-tag>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6" :lg="4">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="信用债" :value="stats.credit">
              <template #prefix>
                <el-tag type="warning" size="small">信用债</el-tag>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6" :lg="4">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="可交债" :value="stats.exchangeable">
              <template #prefix>
                <el-tag type="info" size="small">可交债</el-tag>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="8" :md="6" :lg="4">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="当前页" :value="items.length" />
          </el-card>
        </el-col>
      </el-row>

      <!-- 搜索和筛选卡片 -->
      <el-card shadow="hover" class="search-card" style="margin-top: 16px;">
        <template #header>
          <div class="card-header">
            <span>搜索与筛选</span>
            <el-button text type="primary" @click="resetFilters">重置筛选</el-button>
          </div>
        </template>

        <el-form :inline="true" @submit.prevent>
          <el-form-item label="关键词">
            <el-input
              v-model="keyword"
              placeholder="输入代码或名称片段..."
              clearable
              style="width: 280px"
              @keyup.enter="loadBonds"
              @clear="handleKeywordClear"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="债券类别">
            <el-select
              v-model="activeCategory"
              placeholder="选择类别"
              clearable
              style="width: 150px"
              @change="onCategoryChange"
            >
              <el-option label="全部" value="" />
              <el-option label="可转债" value="convertible" />
              <el-option label="利率债" value="interest" />
              <el-option label="信用债" value="credit" />
              <el-option label="可交债" value="exchangeable" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>

          <el-form-item label="交易所">
            <el-select
              v-model="filterExchange"
              placeholder="选择交易所"
              clearable
              style="width: 120px"
              @change="loadBonds"
            >
              <el-option label="全部" value="" />
              <el-option label="上交所" value="SH" />
              <el-option label="深交所" value="SZ" />
            </el-select>
          </el-form-item>

          <el-form-item v-if="activeCategory === 'interest' || activeCategory === 'all'">
            <el-checkbox v-model="onlyNotMatured" @change="loadBonds">仅未到期</el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" :loading="loading" @click="loadBonds" :icon="Search">
              搜索
            </el-button>
            <el-button @click="resetFilters" :icon="Refresh">重置</el-button>
          </el-form-item>
        </el-form>

        <!-- 快速分类标签 -->
        <div class="category-tags" style="margin-top: 12px;">
          <el-tag
            v-for="cat in categoryOptions"
            :key="cat.value"
            :type="cat.value === activeCategory ? 'primary' : undefined"
            :effect="cat.value === activeCategory ? 'dark' : 'plain'"
            class="category-tag"
            @click="quickSelectCategory(cat.value)"
            style="cursor: pointer; margin-right: 8px; margin-bottom: 8px;"
          >
            {{ cat.label }}
            <span v-if="cat.count !== undefined" class="tag-count">({{ cat.count }})</span>
          </el-tag>
        </div>
      </el-card>

      <!-- 数据表格卡片 -->
      <el-card shadow="hover" class="table-card" style="margin-top: 16px;">
        <template #header>
          <div class="card-header">
            <span>债券列表</span>
            <div>
              <el-button text type="primary" @click="loadBonds" :icon="Refresh" :loading="loading">
                刷新
              </el-button>
            </div>
          </div>
        </template>

        <el-table
          :data="items"
          v-loading="loading"
          stripe
          :style="{ width: '100%' }"
          :default-sort="{ prop: sortBy, order: sortDir === 'asc' ? 'ascending' : 'descending' }"
          @sort-change="onSortChange"
          @row-click="handleRowClick"
          highlight-current-row
        >
          <el-table-column type="index" label="序号" width="60" :index="(index) => (page - 1) * pageSize + index + 1" />

          <el-table-column prop="code" label="债券代码" width="140" sortable="custom" fixed="left">
            <template #default="{ row }">
              <el-link type="primary" @click.stop="viewBondDetail(row.code)" :underline="false">
                {{ row.code }}
              </el-link>
            </template>
          </el-table-column>

          <el-table-column prop="name" label="债券名称" min-width="220" sortable="custom" show-overflow-tooltip>
            <template #default="{ row }">
              <span class="bond-name">{{ row.name || '-' }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="exchange" label="交易所" width="100" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.exchange === 'SH'" type="danger" size="small">上交所</el-tag>
              <el-tag v-else-if="row.exchange === 'SZ'" type="success" size="small">深交所</el-tag>
              <span v-else>{{ row.exchange || '-' }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="category" label="类别" width="110" align="center">
            <template #default="{ row }">
              <el-tag :type="categoryTagType(row.category)" size="small">
                {{ categoryLabel(row.category) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="issuer" label="发行人" min-width="180" show-overflow-tooltip>
            <template #default="{ row }">
              <span>{{ row.issuer || '-' }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="list_date" label="上市日期" width="120" sortable="custom" align="center">
            <template #default="{ row }">
              <span>{{ formatDate(row.list_date) || '-' }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="maturity_date" label="到期日" width="120" sortable="custom" align="center">
            <template #default="{ row }">
              <span :class="getMaturityDateClass(row.maturity_date)">
                {{ formatDate(row.maturity_date) || '-' }}
              </span>
            </template>
          </el-table-column>

          <el-table-column prop="days_to_maturity" label="剩余天数" width="110" sortable="custom" align="center">
            <template #default="{ row }">
              <el-tag :type="getDaysToMaturityTagType(row.maturity_date)" size="small">
                {{ formatDaysToMaturity(row.maturity_date) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="coupon_rate" label="息票率" width="100" sortable="custom" align="right">
            <template #default="{ row }">
              <span class="coupon-rate">{{ formatCoupon(row.coupon_rate) || '-' }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="120" fixed="right" align="center">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click.stop="viewBondDetail(row.code)">
                详情
              </el-button>
              <el-button link type="primary" size="small" @click.stop="viewBondHistory(row.code)">
                历史
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="table-pagination">
          <el-pagination
            background
            layout="total, sizes, prev, pager, next, jumper"
            :current-page="page"
            :page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            @current-change="onPageChange"
            @size-change="onPageSizeChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 债券详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`债券详情 - ${selectedBondCode}`"
      width="800px"
      destroy-on-close
    >
      <div v-if="bondDetailLoading" style="text-align: center; padding: 40px;">
        <el-icon class="is-loading" style="font-size: 32px;"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
      <div v-else-if="bondDetail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="债券代码">{{ bondDetail.code || '-' }}</el-descriptions-item>
          <el-descriptions-item label="债券名称">{{ bondDetail.name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="交易所">
            <el-tag v-if="bondDetail.exchange === 'SH'" type="danger" size="small">上交所</el-tag>
            <el-tag v-else-if="bondDetail.exchange === 'SZ'" type="success" size="small">深交所</el-tag>
            <span v-else>{{ bondDetail.exchange || '-' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="类别">
            <el-tag :type="categoryTagType(bondDetail.category)" size="small">
              {{ categoryLabel(bondDetail.category) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="发行人">{{ bondDetail.issuer || '-' }}</el-descriptions-item>
          <el-descriptions-item label="息票率">{{ formatCoupon(bondDetail.coupon_rate) || '-' }}</el-descriptions-item>
          <el-descriptions-item label="上市日期">{{ formatDate(bondDetail.list_date) || '-' }}</el-descriptions-item>
          <el-descriptions-item label="到期日">
            <span :class="getMaturityDateClass(bondDetail.maturity_date)">
              {{ formatDate(bondDetail.maturity_date) || '-' }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="剩余天数" :span="2">
            <el-tag :type="getDaysToMaturityTagType(bondDetail.maturity_date)" size="small">
              {{ formatDaysToMaturity(bondDetail.maturity_date) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据来源" :span="2">{{ bondDetail.source || 'AKShare' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <div v-else style="text-align: center; padding: 40px; color: #909399;">
        <el-icon style="font-size: 48px;"><Warning /></el-icon>
        <p>未找到债券详情</p>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="viewBondHistory(selectedBondCode)">查看历史数据</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Tickets, Search, Refresh, Loading, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { bondsApi, type BondItem } from '@/api/bonds'

const router = useRouter()

// 数据状态
const keyword = ref('')
const loading = ref(false)
const items = ref<BondItem[]>([])
const activeCategory = ref<'interest' | 'credit' | 'convertible' | 'exchangeable' | 'other' | 'all'>('convertible')
const filterExchange = ref('')
const onlyNotMatured = ref(false)
const page = ref(1)
const pageSize = ref(20)
const sortBy = ref<'code' | 'name' | 'maturity_date' | 'list_date' | 'coupon_rate'>('code')
const sortDir = ref<'asc' | 'desc'>('asc')
const total = ref(0)

// 统计数据
const stats = ref({
  total: 0,
  convertible: 0,
  interest: 0,
  credit: 0,
  exchangeable: 0,
  other: 0
})

// 详情对话框
const detailDialogVisible = ref(false)
const selectedBondCode = ref('')
const bondDetail = ref<BondItem | null>(null)
const bondDetailLoading = ref(false)

// 分类选项
const categoryOptions = computed(() => [
  { label: '全部', value: 'all', count: stats.value.total },
  { label: '可转债', value: 'convertible', count: stats.value.convertible },
  { label: '利率债', value: 'interest', count: stats.value.interest },
  { label: '信用债', value: 'credit', count: stats.value.credit },
  { label: '可交债', value: 'exchangeable', count: stats.value.exchangeable },
  { label: '其他', value: 'other', count: stats.value.other }
])

// 加载债券数据
const loadBonds = async () => {
  try {
    loading.value = true
    // 处理category参数：空字符串表示全部，需要特殊处理
    let categoryParam: string | undefined = undefined
    if (activeCategory.value && activeCategory.value !== 'all') {
      categoryParam = activeCategory.value
    }
    
    const res = await bondsApi.list({
      q: keyword.value || undefined,
      category: categoryParam,
      exchange: filterExchange.value || undefined,
      only_not_matured: onlyNotMatured.value,
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value,
      sort_dir: sortDir.value
    })

    if (res.success) {
      const dataItems = res.data?.items || []
      const dataTotal = res.data?.total || 0

      if (Array.isArray(dataItems)) {
        items.value = dataItems
        total.value = dataTotal
        console.log('债券数据加载成功:', {
          count: dataItems.length,
          total: dataTotal,
          category: activeCategory.value
        })

        // 延迟加载统计数据（避免阻塞主查询）
        if (page.value === 1) {
          setTimeout(() => {
            loadStats()
          }, 500)
        }
      } else {
        console.error('返回的数据格式不正确:', res.data)
        items.value = []
        total.value = 0
        ElMessage.error('数据格式错误')
      }
    } else {
      console.error('加载失败:', res.message)
      ElMessage.error(res.message || '加载失败')
      items.value = []
      total.value = 0
    }
  } catch (e: any) {
    console.error('请求异常:', e)
    // 显示详细的错误信息
    const errorMessage = e?.response?.data?.detail || e?.response?.data?.error?.message || e?.message || '请求失败'
    ElMessage.error(`请求失败: ${errorMessage}`)
    console.error('详细错误信息:', {
      message: e?.message,
      response: e?.response,
      responseData: e?.response?.data,
      status: e?.response?.status
    })
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 加载统计数据（延迟加载，避免影响主查询性能）
const loadStats = async () => {
  try {
    // 只在首次加载或数据为空时加载统计数据
    if (stats.value.total > 0 && items.value.length > 0) {
      return
    }

    // 加载各类别的统计数据（使用较小的page_size以减少数据传输）
    const categories = ['convertible', 'interest', 'credit', 'exchangeable', 'other']
    const statsPromises = categories.map(async (cat) => {
      try {
        const res = await bondsApi.list({ category: cat, page: 1, page_size: 1 })
        return { category: cat, total: res.success ? (res.data?.total || 0) : 0 }
      } catch {
        return { category: cat, total: 0 }
      }
    })

    // 加载总数
    let totalCount = 0
    try {
      const totalRes = await bondsApi.list({ page: 1, page_size: 1 })
      totalCount = totalRes.success ? (totalRes.data?.total || 0) : 0
    } catch {
      totalCount = 0
    }

    const categoryStats = await Promise.all(statsPromises)
    stats.value = {
      total: totalCount,
      convertible: categoryStats.find(s => s.category === 'convertible')?.total || 0,
      interest: categoryStats.find(s => s.category === 'interest')?.total || 0,
      credit: categoryStats.find(s => s.category === 'credit')?.total || 0,
      exchangeable: categoryStats.find(s => s.category === 'exchangeable')?.total || 0,
      other: categoryStats.find(s => s.category === 'other')?.total || 0
    }
  } catch (e) {
    console.error('加载统计数据失败:', e)
  }
}

// 快速选择分类
const quickSelectCategory = (category: string) => {
  activeCategory.value = category as any
  if (category === 'all') {
    onlyNotMatured.value = false
  } else if (category === 'interest') {
    onlyNotMatured.value = true
  } else {
    onlyNotMatured.value = false
  }
  page.value = 1
  loadBonds()
}

// 重置筛选
const resetFilters = () => {
  keyword.value = ''
  activeCategory.value = 'convertible'
  filterExchange.value = ''
  onlyNotMatured.value = false
  page.value = 1
  sortBy.value = 'code'
  sortDir.value = 'asc'
  loadBonds()
}

// 关键词清除
const handleKeywordClear = () => {
  page.value = 1
  loadBonds()
}

// 分类切换
const onCategoryChange = () => {
  if (activeCategory.value !== 'interest') {
    onlyNotMatured.value = false
  } else {
    onlyNotMatured.value = true
  }
  page.value = 1
  sortBy.value = 'code'
  sortDir.value = 'asc'
  loadBonds()
}

// 分类标签
const categoryLabel = (cat?: string) => {
  switch ((cat || '').toLowerCase()) {
    case 'interest': return '利率债'
    case 'credit': return '信用债'
    case 'convertible': return '可转债'
    case 'exchangeable': return '可交债'
    default: return '其他'
  }
}

const categoryTagType = (cat?: string) => {
  switch ((cat || '').toLowerCase()) {
    case 'interest': return 'primary'
    case 'credit': return 'warning'
    case 'convertible': return 'success'
    case 'exchangeable': return 'info'
    default: return 'info'
  }
}

// 分页
const onPageChange = (p: number) => {
  page.value = p
  loadBonds()
}

const onPageSizeChange = (ps: number) => {
  pageSize.value = ps
  page.value = 1
  loadBonds()
}

// 排序
const onSortChange = (opt: { column: any; prop: string; order: 'ascending' | 'descending' | null }) => {
  if (!opt || !opt.prop || !opt.order) {
    sortBy.value = 'code'
    sortDir.value = 'asc'
  } else {
    const allowedSortFields: Array<'code' | 'name' | 'maturity_date' | 'list_date' | 'coupon_rate'> = [
      'code',
      'name',
      'maturity_date',
      'list_date',
      'coupon_rate'
    ]
    if (allowedSortFields.includes(opt.prop as any)) {
      sortBy.value = opt.prop as 'code' | 'name' | 'maturity_date' | 'list_date' | 'coupon_rate'
      sortDir.value = opt.order === 'ascending' ? 'asc' : 'desc'
    } else {
      sortBy.value = 'code'
      sortDir.value = 'asc'
    }
  }
  page.value = 1
  loadBonds()
}

// 格式化函数
const formatCoupon = (val: any) => {
  if (val === null || val === undefined || val === '') return ''
  const num = Number(val)
  if (Number.isNaN(num)) return String(val)
  return `${num.toFixed(2)}%`
}

const formatDate = (d: any) => {
  if (!d) return ''
  try {
    if (typeof d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(d)) {
      return d
    }
    const t = new Date(d)
    if (Number.isNaN(t.getTime())) {
      if (typeof d === 'string') {
        const cleaned = d.replace(/[年月日]/g, '-').replace(/\./g, '-')
        const parsed = new Date(cleaned)
        if (!Number.isNaN(parsed.getTime())) {
          return parsed.toISOString().slice(0, 10)
        }
      }
      return String(d)
    }
    return t.toISOString().slice(0, 10)
  } catch {
    return String(d)
  }
}

const formatDaysToMaturity = (d: any) => {
  if (!d) return '-'
  try {
    const endDate = new Date(d + 'T00:00:00')
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const diff = Math.ceil((endDate.getTime() - today.getTime()) / (24 * 3600 * 1000))

    if (isNaN(diff)) return '-'

    if (diff < 0) {
      return `已过期 ${Math.abs(diff)} 天`
    } else if (diff === 0) {
      return '今日到期'
    } else if (diff <= 30) {
      return `剩余 ${diff} 天`
    } else if (diff <= 365) {
      return `剩余 ${Math.floor(diff / 30)} 个月`
    } else {
      return `剩余 ${Math.floor(diff / 365)} 年`
    }
  } catch {
    return '-'
  }
}

const getDaysToMaturityTagType = (d: any) => {
  if (!d) return 'info'
  try {
    const endDate = new Date(d + 'T00:00:00')
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const diff = Math.ceil((endDate.getTime() - today.getTime()) / (24 * 3600 * 1000))

    if (isNaN(diff)) return 'info'
    if (diff < 0) return 'danger'
    if (diff <= 30) return 'warning'
    if (diff <= 365) return 'info'
    return 'success'
  } catch {
    return 'info'
  }
}

const getMaturityDateClass = (d: any): string => {
  if (!d) return ''
  try {
    const endDate = new Date(d + 'T00:00:00')
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const diff = Math.ceil((endDate.getTime() - today.getTime()) / (24 * 3600 * 1000))

    if (isNaN(diff)) return ''
    if (diff < 0) return 'maturity-expired'
    if (diff <= 30) return 'maturity-soon'
    return ''
  } catch {
    return ''
  }
}

// 行点击
const handleRowClick = (row: BondItem) => {
  viewBondDetail(row.code)
}

// 查看债券详情
const viewBondDetail = async (code: string) => {
  selectedBondCode.value = code
  detailDialogVisible.value = true
  bondDetailLoading.value = true
  bondDetail.value = null

  try {
    const res = await bondsApi.getInfo(code)
    if (res.success && res.data) {
      bondDetail.value = res.data
    } else {
      // 如果API没有返回详情，从当前列表中查找
      const found = items.value.find(item => item.code === code)
      if (found) {
        bondDetail.value = found
      }
    }
  } catch (e) {
    console.error('加载债券详情失败:', e)
    // 从当前列表中查找
    const found = items.value.find(item => item.code === code)
    if (found) {
      bondDetail.value = found
    }
  } finally {
    bondDetailLoading.value = false
  }
}

// 查看历史数据
const viewBondHistory = (code: string) => {
  detailDialogVisible.value = false
  router.push({
    name: 'BondHistory',
    params: { code },
    query: { code }
  }).catch(() => {
    // 如果路由不存在，显示提示
    ElMessage.info('历史数据功能开发中，敬请期待')
  })
}

onMounted(() => {
  loadBonds()
})
</script>

<style lang="scss" scoped>
@use '@/styles/overview.scss' as *;
</style>
