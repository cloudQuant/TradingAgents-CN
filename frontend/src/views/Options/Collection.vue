<template>
  <div class="collection-page">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionDef?.display_name"
      :description="collectionDef?.description"
      :loading="loading"
      :updating="refreshing"
      :clearing="clearing"
      show-english-name
      @show-overview="overviewDialogVisible = true"
      @refresh="loadData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    >
      <!-- 未找到集合时的返回按钮 -->
      <template v-if="!collectionDef" #extra-actions>
        <el-button @click="goBack" :icon="ArrowLeft">返回列表</el-button>
      </template>
    </CollectionPageHeader>

    <div class="content">
      <!-- 数据表格 -->
      <CollectionDataTable
        :data="rows"
        :fields="fields"
        :total="total"
        :loading="loading"
        :collection-name="collectionName"
        :export-all-data="exportAllData"
        v-model:page="currentPage"
        v-model:page-size="pageSize"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="loadData"
        @refresh="loadData"
        @page-change="loadData"
        @size-change="loadData"
        @sort-change="handleSortChange"
      />
    </div>

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :display-name="collectionDef?.display_name"
      :description="collectionDef?.description"
      :total-count="stats?.total_count"
      :field-count="fields.length"
      :latest-update="stats?.latest_update"
      :data-source="currentCollectionSource"
    />

    <!-- 文件导入对话框 -->
    <FileImportDialog
      ref="fileImportRef"
      v-model:visible="uploadDialogVisible"
      :importing="importing"
      @import="handleImportFile"
    />

    <!-- 远程同步对话框 -->
    <RemoteSyncDialog
      v-model:visible="syncDialogVisible"
      :collection-name="collectionName"
      :syncing="remoteSyncing"
      :sync-result="remoteSyncStats"
      @sync="handleRemoteSync"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { optionsApi } from '@/api/options'
import {
  CollectionDataTable,
  CollectionPageHeader,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  type RemoteSyncConfig,
} from '@/components/collection'

const route = useRoute()
const router = useRouter()

// 基础状态
const collectionName = computed(() => route.params.collectionName as string)
const collectionDef = ref<any>(null)
const rows = ref<any[]>([])
const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const importing = ref(false)
const remoteSyncing = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索和排序
const filterValue = ref('')
const filterField = ref('')
const sortBy = ref<string | null>(null)
const sortDir = ref<'asc' | 'desc'>('desc')

// 数据
const stats = ref<any>({})
const fields = ref<Array<{ name: string; type: string; example: string | null }>>([])

// 对话框状态
const overviewDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)
const fileImportRef = ref()

// 同步结果
const remoteSyncStats = ref<any>(null)

// 数据源映射
const collectionSourceMap: Record<string, string> = {
  option_contract_info_ctp: 'http://openctp.cn/instruments.html',
  option_finance_board: 'http://www.sse.com.cn/assortment/options/price/',
  option_risk_indicator_sse: 'http://www.sse.com.cn/assortment/options/risk/',
  option_current_day_sse: 'https://www.sse.com.cn/assortment/options/disclo/preinfo/',
  option_current_day_szse: 'https://www.sse.org.cn/option/quotation/contract/daycontract/index.html',
  option_daily_stats_sse: 'http://www.sse.com.cn/assortment/options/date/',
  option_daily_stats_szse: 'https://investor.szse.cn/market/option/day/index.html',
  option_cffex_sz50_list_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex',
  option_cffex_hs300_list_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_cffex_zz1000_list_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_cffex_sz50_spot_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex',
  option_cffex_hs300_spot_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_cffex_zz1000_spot_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_cffex_sz50_daily_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex',
  option_cffex_hs300_daily_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_cffex_zz1000_daily_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_list_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_expire_day_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_codes_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_underlying_spot_price_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_greeks_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_minute_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_sse_daily_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
  option_finance_minute_sina: 'https://stock.finance.sina.com.cn/option/quotes.html',
  option_minute_em: 'https://wap.eastmoney.com/quote/stock/151.cu2404P61000.html',
  option_current_em: 'https://quote.eastmoney.com/center/qqsc.html',
  option_lhb_em: 'https://data.eastmoney.com/other/qqlhb.html',
  option_value_analysis_em: 'https://data.eastmoney.com/other/valueAnal.html',
  option_risk_analysis_em: 'https://data.eastmoney.com/other/riskanal.html',
  option_premium_analysis_em: 'https://data.eastmoney.com/other/premium.html',
  option_commodity_contract_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsDP.php',
  option_commodity_contract_table_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsDP.php',
  option_commodity_hist_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsDP.php',
  option_comm_info: 'https://www.9qihuo.com/qiquanshouxufei',
  option_margin: 'https://www.iweiai.com/qiquan/yuanyou',
  option_hist_shfe: 'https://www.shfe.com.cn/reports/tradedata/dailyandweeklydata/',
  option_hist_dce: 'http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html',
  option_hist_czce: 'http://www.czce.com.cn/cn/jysj/mrhq/H770301index_1.htm',
  option_hist_gfex: 'http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml',
  option_vol_gfex: 'http://www.gfex.com.cn/gfex/rihq/hqsj_tjsj.shtml',
  option_czce_hist: 'http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm',
  option_sse_spot_price_sina: 'https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php',
}

const currentCollectionSource = computed(() => collectionSourceMap[collectionName.value] || '')

// 加载集合信息
const loadCollectionInfo = async () => {
  try {
    const res = await optionsApi.getCollections()
    if (res.success) {
      const found = res.data.find((c: any) => c.name === collectionName.value)
      if (found) {
        collectionDef.value = found
      }
    }
  } catch (e) {
    console.error(e)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await optionsApi.getCollectionData(collectionName.value, {
      page: currentPage.value,
      page_size: pageSize.value,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    if (res.success) {
      rows.value = res.data.items
      total.value = res.data.total
      currentPage.value = res.data.page
      pageSize.value = res.data.page_size
      fields.value = res.data.fields || []
    } else {
      ElMessage.error(res.message || '加载数据失败')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 加载统计数据
const loadStats = async () => {
  try {
    const res = await optionsApi.getCollectionStats(collectionName.value)
    if (res?.success) {
      stats.value = res.data || {}
    }
  } catch (e) {
    console.error('加载统计数据失败:', e)
  }
}

// 处理更新命令
const handleUpdateCommand = async (command: string) => {
  if (command === 'api') {
    refreshing.value = true
    try {
      const res = await optionsApi.refreshCollection(collectionName.value)
      if (res.success) {
        ElMessage.success(res.message || '更新任务已提交')
        setTimeout(loadData, 2000)
      } else {
        ElMessage.error(res.message || '更新失败')
      }
    } catch (e: any) {
      ElMessage.error(e.message || '更新失败')
    } finally {
      refreshing.value = false
    }
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

// 处理清空数据
const handleClearData = async () => {
  clearing.value = true
  try {
    const res = await optionsApi.clearCollection(collectionName.value)
    if (res.success) {
      ElMessage.success(res.message || '数据已清空')
      loadData()
    } else {
      ElMessage.error(res.message || '清空失败')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '清空失败')
  } finally {
    clearing.value = false
  }
}

// 处理排序
const handleSortChange = (params: { prop: string; order: 'ascending' | 'descending' | null }) => {
  const { prop, order } = params
  if (!prop || !order) {
    sortBy.value = null
    sortDir.value = 'desc'
  } else {
    sortBy.value = prop
    sortDir.value = order === 'ascending' ? 'asc' : 'desc'
  }
  loadData()
}

// 处理文件导入
const handleImportFile = async (files: File[]) => {
  if (!files.length) return

  importing.value = true
  try {
    const res = await optionsApi.uploadData(collectionName.value, files[0])
    if (res.success) {
      ElMessage.success((res.data as any)?.message || '导入成功')
      fileImportRef.value?.clearFiles()
      uploadDialogVisible.value = false
      await loadData()
    } else {
      ElMessage.error((res as any).error || '导入失败')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '导入失败')
  } finally {
    importing.value = false
  }
}

// 处理远程同步
const handleRemoteSync = async (config: RemoteSyncConfig) => {
  remoteSyncing.value = true
  remoteSyncStats.value = null

  try {
    const res = await optionsApi.syncData(collectionName.value, {
      host: config.host,
      username: config.username,
      password: config.password,
      authSource: config.authSource,
      collection: config.collection || collectionName.value,
      batch_size: config.batchSize,
    })

    if (res.success) {
      remoteSyncStats.value = res.data
      ElMessage.success((res.data as any)?.message || '同步成功')
      await loadData()
    } else {
      ElMessage.error((res as any).error || '同步失败')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '同步失败')
  } finally {
    remoteSyncing.value = false
  }
}

// 返回列表
const goBack = () => {
  router.push('/options/collections')
}

// 后端全量导出
const exportAllData = async ({ fileName, format }: { fileName: string; format: 'csv' | 'xlsx' | 'json' }) => {
  try {
    const blob = await optionsApi.exportCollectionData(collectionName.value, {
      file_format: format,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    downloadBlob(blob, buildExportFileName(fileName, format))
  } catch (error: any) {
    console.error('导出全部数据失败:', error)
    ElMessage.error(error?.message || '导出失败')
    throw error
  }
}

const buildExportFileName = (baseName: string, format: 'csv' | 'xlsx' | 'json'): string => {
  const normalized = baseName.replace(/\.(csv|xlsx|json)$/i, '')
  return `${normalized}.${format === 'xlsx' ? 'xlsx' : format}`
}

const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

onMounted(async () => {
  await loadCollectionInfo()
  if (collectionDef.value) {
    await loadData()
    await loadStats()
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
