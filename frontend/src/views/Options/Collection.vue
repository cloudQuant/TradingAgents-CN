<template>
  <div class="collection-page">
    <!-- Header -->
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
          <el-button :icon="Box" @click="showOverviewDialog">数据概览</el-button>
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
          <el-dropdown @command="handleUpdateCommand">
            <el-button :icon="Download" type="primary" :loading="refreshing">
              更新数据<el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="api">API更新</el-dropdown-item>
                <el-dropdown-item command="file">文件导入</el-dropdown-item>
                <el-dropdown-item command="sync">远程同步</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-button :icon="Delete" type="danger" @click="clearData" :loading="clearing">清空数据</el-button>
        </div>
      </div>
      <!-- Error State -->
      <div class="header-content" v-else>
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            未知集合
          </h1>
          <p class="page-description">集合名称：{{ collectionName }}</p>
        </div>
        <div class="header-actions">
          <el-button @click="goBack" icon="ArrowLeft">返回列表</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- Data Table -->
      <el-card shadow="hover" class="data-card">
        <template #header>
          <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center;">
              <span>数据</span>
              <el-popover
                placement="right"
                title="字段说明"
                :width="600"
                trigger="hover"
                v-if="fields && fields.length > 0"
              >
                <template #reference>
                  <el-icon style="margin-left: 8px; cursor: pointer; color: #909399;"><QuestionFilled /></el-icon>
                </template>
                <el-table :data="fields" stripe border size="small" :style="{ width: '100%' }">
                  <el-table-column prop="name" label="字段名" width="200" />
                  <el-table-column prop="type" label="类型" width="120" />
                  <el-table-column prop="example" label="示例" show-overflow-tooltip>
                    <template #default="{ row }">
                      <span v-if="row.example" class="example-text">{{ row.example }}</span>
                      <span v-else class="text-muted">-</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-popover>
            </div>
            <div class="card-actions">
              <el-input
                v-model="filterValue"
                placeholder="搜索..."
                style="width: 200px; margin-right: 8px;"
                clearable
                @clear="loadData"
                @keyup.enter="loadData"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-select
                v-model="filterField"
                placeholder="搜索字段"
                style="width: 150px; margin-right: 8px;"
                clearable
              >
                <el-option
                  v-for="field in fields"
                  :key="field.name"
                  :label="field.name"
                  :value="field.name"
                />
              </el-select>
              <el-button size="small" :icon="Search" @click="loadData">搜索</el-button>
              <el-button size="small" @click="loadData" icon="Refresh" style="margin-left: 8px;">刷新列表</el-button>
            </div>
          </div>
        </template>

        <el-table
          :data="rows"
          v-loading="loading"
          stripe
          border
          :style="{ width: '100%' }"
          max-height="600"
          @sort-change="handleSortChange"
        >
          <el-table-column
            v-for="field in displayFields"
            :key="field"
            :prop="field"
            :label="field"
            min-width="120"
            show-overflow-tooltip
            sortable="custom"
          >
            <template #default="{ row }">
              <span v-if="row[field] !== null && row[field] !== undefined">
                {{ row[field] }}
              </span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadData"
            @current-change="loadData"
          />
        </div>
      </el-card>
    </div>

    <!-- 文件导入对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="文件导入"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        multiple
        :on-change="handleImportFileChange"
        :on-remove="handleImportFileRemove"
        accept=".csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        drag
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击选择文件</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 CSV 或 Excel 文件，文件结构需与集合字段一致
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleImportFile"
          :loading="importing"
          :disabled="!importFiles.length || importing"
        >
          导入
        </el-button>
      </template>
    </el-dialog>

    <!-- 远程同步对话框 -->
    <el-dialog
      v-model="syncDialogVisible"
      title="远程同步"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form label-width="120px">
        <el-form-item label="远程主机">
          <el-input
            v-model="remoteSyncHost"
            placeholder="IP地址或URI，例如 192.168.1.10 或 mongodb://user:pwd@host:27017/db"
          />
        </el-form-item>
        <el-form-item label="数据库类型">
          <el-select v-model="remoteSyncDbType" disabled style="width: 100%">
            <el-option label="MongoDB" value="mongodb" />
          </el-select>
        </el-form-item>
        <el-form-item label="批次大小">
          <el-select v-model="remoteSyncBatchSize" style="width: 100%">
            <el-option label="1000" :value="1000" />
            <el-option label="2000" :value="2000" />
            <el-option label="5000" :value="5000" />
            <el-option label="10000" :value="10000" />
          </el-select>
        </el-form-item>
        <el-form-item label="远程集合名">
          <el-input
            v-model="remoteSyncCollection"
            :placeholder="`默认使用当前集合名: ${collectionName}`"
          />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input
            v-model="remoteSyncUsername"
            placeholder="可选"
          />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="remoteSyncPassword"
            type="password"
            placeholder="可选"
            show-password
          />
        </el-form-item>
        <el-form-item label="认证数据库">
          <el-input
            v-model="remoteSyncAuthSource"
            placeholder="通常为 admin"
          />
        </el-form-item>
      </el-form>

      <el-alert
        v-if="remoteSyncStats"
        :title="`同步完成: ${remoteSyncStats.synced_count}/${remoteSyncStats.remote_total} 条`"
        type="success"
        style="margin-top: 16px"
        show-icon
      />

      <template #footer>
        <el-button @click="syncDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleRemoteSync"
          :loading="remoteSyncing"
        >
          开始同步
        </el-button>
      </template>
    </el-dialog>

    <!-- 数据概览对话框 -->
    <el-dialog
      v-model="overviewDialogVisible"
      title="数据概览"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="集合名称">
          {{ collectionName }}
        </el-descriptions-item>
        <el-descriptions-item label="显示名称">
          {{ collectionDef?.display_name || collectionName }}
        </el-descriptions-item>
        <el-descriptions-item label="数据总数">
          {{ stats?.total_count || 0 }} 条
        </el-descriptions-item>
        <el-descriptions-item label="字段数量">
          {{ (collectionDef?.fields && collectionDef?.fields.length) || 0 }} 个
        </el-descriptions-item>
        <el-descriptions-item label="最后更新" :span="2">
          {{ stats?.latest_update ? formatTime(stats.latest_update) : '暂无数据' }}
        </el-descriptions-item>
        <el-descriptions-item label="数据来源" :span="2">
          <template v-if="currentCollectionSource">
            <el-link :href="currentCollectionSource" target="_blank" type="primary">
              {{ currentCollectionSource }}
            </el-link>
          </template>
          <template v-else>
            暂无
          </template>
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ collectionDef?.description || `数据集合：${collectionName}` }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="overviewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Box, ArrowLeft, Refresh, Delete, Download, QuestionFilled, Search, ArrowDown, UploadFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { optionsApi } from '@/api/options'

const route = useRoute()
const router = useRouter()

const collectionName = computed(() => route.params.collectionName as string)
const collectionDef = ref<any>(null)
const rows = ref<any[]>([])
const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const stats = ref<any>({})
const overviewDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)
const uploadRef = ref()
const importFiles = ref<any[]>([])
const importing = ref(false)
const remoteSyncHost = ref('')
const remoteSyncDbType = ref('mongodb')
const remoteSyncCollection = ref('')
const remoteSyncUsername = ref('')
const remoteSyncPassword = ref('')
const remoteSyncAuthSource = ref('admin')
const remoteSyncBatchSize = ref(1000)
const remoteSyncing = ref(false)
const remoteSyncStats = ref<any>(null)
const fields = ref<Array<{ name: string; type: string; example: string | null }>>([])
const filterValue = ref('')
const filterField = ref('')
const sortBy = ref<string | null>(null)
const sortDir = ref<'asc' | 'desc'>('desc')

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

const displayFields = computed(() => {
    if (fields.value && fields.value.length > 0) {
        return fields.value.map((f) => f.name)
    }
    if (!collectionDef.value) return []
    return collectionDef.value.fields || []
})

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

const loadData = async () => {
    loading.value = true
    try {
        const res = await optionsApi.getCollectionData(collectionName.value, {
            page: currentPage.value,
            page_size: pageSize.value,
            sort_by: sortBy.value || undefined,
            sort_dir: sortDir.value,
            filter_field: filterField.value || undefined,
            filter_value: filterValue.value || undefined
        })
        if (res.success) {
            rows.value = res.data.items
            total.value = res.data.total
            currentPage.value = res.data.page
            pageSize.value = res.data.page_size
            fields.value = res.data.fields || []
        } else {
            ElMessage.error(res.error || '加载数据失败')
        }
    } catch (e: any) {
        ElMessage.error(e.message || '加载数据失败')
    } finally {
        loading.value = false
    }
}

const loadStats = async () => {
    try {
        const res = await optionsApi.getCollectionStats(collectionName.value)
        if (res && res.success) {
            stats.value = res.data || {}
        }
    } catch (e) {
        // ignore stats error to avoid影响主流程
        console.error('加载统计数据失败:', e)
    }
}

const refreshData = async () => {
    refreshing.value = true
    try {
        const res = await optionsApi.refreshCollection(collectionName.value)
        if (res.success) {
            ElMessage.success(res.message || '更新任务已提交')
            // Wait a bit and reload data
            setTimeout(loadData, 2000)
        } else {
            ElMessage.error(res.error || '更新失败')
        }
    } catch (e: any) {
        ElMessage.error(e.message || '更新失败')
    } finally {
        refreshing.value = false
    }
}

const clearData = async () => {
    try {
        await ElMessageBox.confirm('确定要清空该集合的所有数据吗？', '警告', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })
        
        clearing.value = true
        const res = await optionsApi.clearCollection(collectionName.value)
        if (res.success) {
            ElMessage.success(res.message || '数据已清空')
            loadData()
        } else {
            ElMessage.error(res.error || '清空失败')
        }
    } catch (e) {
        // Cancelled or error
    } finally {
        clearing.value = false
    }
}

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

const handlePageChange = (page: number) => {
    currentPage.value = page
    loadData()
}

const goBack = () => {
    router.push('/options/collections')
}

const showOverviewDialog = () => {
    overviewDialogVisible.value = true
}

// 处理更新数据下拉菜单命令
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    refreshData()
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

const formatTime = (value: any): string => {
    if (!value) return ''
    try {
        const date = new Date(value)
        if (isNaN(date.getTime())) {
            return String(value)
        }
        return date.toLocaleString('zh-CN')
    } catch {
        return String(value)
    }
}

const handleImportFileChange = (file: any, fileList: any[]) => {
    if (!file) return
    importFiles.value = fileList.slice(-1)
}

const handleImportFileRemove = () => {
    importFiles.value = []
}

const handleImportFile = async () => {
    if (!importFiles.value.length) return

    importing.value = true
    const file = importFiles.value[0].raw as File

    try {
        const res = await optionsApi.uploadData(collectionName.value, file)

        if (res.success) {
            ElMessage.success((res.data as any)?.message || '导入成功')
            if (uploadRef.value) uploadRef.value.clearFiles()
            importFiles.value = []
            uploadDialogVisible.value = false
            await loadData()
        } else {
            const anyRes = res as any
            ElMessage.error(anyRes.error || anyRes.message || '导入失败')
        }
    } catch (e: any) {
        ElMessage.error(e.message || '导入失败')
    } finally {
        importing.value = false
    }
}

const handleRemoteSync = async () => {
    if (!remoteSyncHost.value) {
        ElMessage.warning('请输入远程主机地址')
        return
    }

    remoteSyncing.value = true
    remoteSyncStats.value = null

    try {
        const config = {
            host: remoteSyncHost.value,
            username: remoteSyncUsername.value,
            password: remoteSyncPassword.value,
            authSource: remoteSyncAuthSource.value,
            collection: remoteSyncCollection.value || collectionName.value,
            batch_size: remoteSyncBatchSize.value
        }

        const res = await optionsApi.syncData(collectionName.value, config)

        if (res.success) {
            remoteSyncStats.value = res.data
            ElMessage.success((res.data as any)?.message || '同步成功')
            await loadData()
        } else {
            const anyRes = res as any
            ElMessage.error(anyRes.error || anyRes.message || '同步失败')
        }
    } catch (e: any) {
        ElMessage.error(e.message || '同步失败')
    } finally {
        remoteSyncing.value = false
    }
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
