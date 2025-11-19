<template>
  <div class="collection-page">
    <!-- 顶部信息区域 -->
    <div class="page-header">
      <div class="header-content" v-if="collectionDef">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionDef.display_name }}
            <span class="collection-name-en">({{ collectionName }})</span>
          </h1>
          <p class="page-description">{{ collectionDef.description }}</p>
        </div>
        <div class="header-actions">
          <el-button @click="goBack" icon="ArrowLeft" round>返回数据集合列表</el-button>
        </div>
      </div>
      <div class="header-content" v-else>
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            未找到数据集合
          </h1>
          <p class="page-description">集合名称：{{ collectionName }}</p>
        </div>
        <div class="header-actions">
          <el-button @click="goBack" icon="ArrowLeft" round>返回数据集合列表</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <el-empty
        v-if="!collectionDef"
        description="未找到对应的数据集合定义"
      />

      <template v-else>
        <!-- 字段说明 -->
        <el-card shadow="hover" class="fields-card">
          <template #header>
            <div class="card-header">
              <span>字段说明</span>
            </div>
          </template>

          <el-table :data="fieldRows" size="small" style="width: 100%">
            <el-table-column prop="name" label="字段名" width="180" />
            <el-table-column prop="description" label="说明" />
            <el-table-column prop="example" label="示例值" width="200">
              <template #default="{ row }">
                <span v-if="row.example !== null && row.example !== undefined">{{ row.example }}</span>
                <span v-else class="example-placeholder">-</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 数据表格 -->
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <span>数据预览</span>
              <div class="card-actions">
                <el-button size="small" @click="refreshData">刷新</el-button>
              </div>
            </div>
          </template>

          <el-table
            :data="rows"
            size="small"
            stripe
            v-loading="loading"
            style="width: 100%"
          >
            <el-table-column
              v-for="field in collectionDef.fields"
              :key="field"
              :prop="field"
              :label="field"
              :min-width="120"
            />
          </el-table>

          <div class="pagination-wrapper">
            <el-pagination
              background
              layout="prev, pager, next, jumper"
              :total="total"
              :page-size="pageSize"
              :current-page="currentPage"
              @current-change="handlePageChange"
            />
          </div>
        </el-card>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Box } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { stocksApi } from '@/api/stocks'

const route = useRoute()
const router = useRouter()

const collectionName = computed(() => (route.params.collectionName as string) || '')

interface CollectionDefinition {
  display_name: string
  description: string
  fields: string[]
}

interface FieldRow {
  name: string
  description: string
  example: any
}

// 集合定义：与后端 /api/stocks/collections 中的字段保持一致
const collectionDefinitions: Record<string, CollectionDefinition> = {
  stock_basic_info: {
    display_name: '股票基础信息',
    description: '股票的基础信息，包括代码、名称、行业、市场、总市值、流通市值等',
    fields: ['code', 'name', 'industry', 'market', 'list_date', 'total_mv', 'circ_mv', 'pe', 'pb'],
  },
  market_quotes: {
    display_name: '实时行情数据',
    description: '股票的实时行情数据，包括最新价、涨跌幅、成交量、成交额等',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'pct_chg', 'turnover_rate'],
  },
  stock_financial_data: {
    display_name: '财务数据',
    description: '股票的财务数据，包括营业收入、净利润、ROE、负债率等财务指标',
    fields: ['code', 'report_period', 'revenue', 'net_profit', 'roe', 'debt_to_assets', 'eps'],
  },
  stock_daily: {
    display_name: '日线行情',
    description: '股票的日线历史行情数据，包括开盘价、最高价、最低价、收盘价、成交量等',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'],
  },
  stock_weekly: {
    display_name: '周线行情',
    description: '股票的周线历史行情数据',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'],
  },
  stock_monthly: {
    display_name: '月线行情',
    description: '股票的月线历史行情数据',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'],
  },
}

const collectionDef = computed<CollectionDefinition | null>(() => {
  const name = collectionName.value
  return collectionDefinitions[name] || null
})

const fieldRows = computed<FieldRow[]>(() => {
  if (!collectionDef.value) return []
  return collectionDef.value.fields.map((name) => ({
    name,
    description: '',
    example: null,
  }))
})

const rows = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadCollectionPage = async () => {
  const name = collectionName.value
  if (!name) return

  try {
    const res = await stocksApi.getStockCollectionData(name, {
      page: currentPage.value,
      page_size: pageSize.value,
    })
    const data = res.data
    rows.value = data.items || []
    total.value = data.total ?? 0
    currentPage.value = data.page ?? currentPage.value
    pageSize.value = data.page_size ?? pageSize.value
  } catch (error) {
    console.error('加载集合数据失败', error)
    ElMessage.error('加载集合数据失败')
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    // 当前版本使用本地Mock数据，后续可替换为真实API调用
    await loadCollectionPage()
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  refreshData()
}

const goBack = () => {
  router.push('/stocks/collections')
}

onMounted(() => {
  if (!collectionDef.value) {
    ElMessage.warning('未找到对应的数据集合定义')
    return
  }
  refreshData()
})
</script>

<style scoped lang="scss">
.collection-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 24px;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 24px;
    background: linear-gradient(135deg, #409eff 0%, #3a8ee6 100%);
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 20px rgba(64, 158, 255, 0.4);
  }

  .title-section {
    flex: 1;
  }

  .page-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 26px;
    font-weight: 600;
    margin: 0 0 8px 0;

    .title-icon {
      font-size: 32px;
    }

    .collection-name-en {
      font-size: 16px;
      opacity: 0.9;
    }
  }

  .page-description {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
  }

  .header-actions {
    display: flex;
    align-items: center;
  }
}

.content {
  margin-top: 8px;
}

.fields-card {
  margin-bottom: 16px;
}

.data-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.pagination-wrapper {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.example-placeholder {
  color: #c0c4cc;
}

@media (max-width: 768px) {
  .page-header {
    .header-content {
      flex-direction: column;
      gap: 16px;
    }

    .header-actions {
      width: 100%;
      justify-content: flex-end;
    }
  }
}
</style>
