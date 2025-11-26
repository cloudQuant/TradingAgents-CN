<template>
  <div class="collection-page">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :loading="loading"
      :updating="refreshing || batchUpdating"
      :clearing="clearing"
      @show-overview="overviewDialogVisible = true"
      @refresh="loadData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    />

    <div class="content">
      <!-- 时间序列图表 (只在 currency_time_series 集合显示) -->
      <el-card v-if="collectionName === 'currency_time_series' && items.length > 0" shadow="hover" class="chart-card" style="margin-bottom: 16px;">
        <template #header>
          <div class="card-header">
            <span>货币报价时间序列图</span>
            <div style="display: flex; gap: 8px; align-items: center;">
              <span style="font-size: 13px; color: #606266;">选择货币：</span>
              <el-select
                v-model="selectedCurrencies"
                multiple
                collapse-tags
                collapse-tags-tooltip
                :max-collapse-tags="5"
                placeholder="选择货币"
                style="width: 300px;"
                @change="handleCurrencyChange"
              >
                <el-option
                  v-for="currency in currencyOptions"
                  :key="currency"
                  :label="currency"
                  :value="currency"
                />
              </el-select>
              <el-button size="small" @click="resetChart">重置</el-button>
            </div>
          </div>
        </template>
        <div ref="chartRef" style="width: 100%; height: 400px;"></div>
      </el-card>

      <!-- 数据列表 -->
      <CollectionDataTable
        :data="items"
        :fields="currencyFields"
        :total="total"
        :loading="loading"
        :page="page"
        :page-size="pageSize"
        :sortable="true"
        :format-cell-value="formatCurrencyValue"
        :fetch-all-data="fetchAllDataForExport"
        :collection-name="collectionName"
        :show-field-filter="false"
        search-placeholder="搜索货币..."
        v-model:filter-value="filterValue"
        @search="handleFilter"
        @page-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </div>

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

    <!-- API更新对话框 -->
    <el-dialog
      v-model="apiUpdateDialogVisible"
      title="API更新"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form label-position="top">
        <el-form-item label="API Key" required>
          <el-input v-model="apiKey" type="password" show-password placeholder="请输入 CurrencyScoop API Key" />
        </el-form-item>

        <el-row :gutter="16" v-if="collectionName !== 'currency_currencies'">
          <el-col :span="12">
            <el-form-item label="基础货币">
              <el-input v-model="syncBase" placeholder="USD" />
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="collectionName === 'currency_convert'">
            <el-form-item label="目标货币">
              <el-input v-model="syncTo" placeholder="CNY" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="16" v-if="collectionName === 'currency_convert'">
          <el-col :span="12">
            <el-form-item label="数量">
              <el-input v-model="syncAmount" placeholder="10000" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="16" v-if="collectionName === 'currency_history'">
          <el-col :span="12">
            <el-form-item label="日期" required>
              <el-date-picker
                v-model="syncDate"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="16" v-if="collectionName === 'currency_time_series'">
          <el-col :span="24">
            <el-form-item label="日期范围" required>
              <el-date-picker
                v-model="syncDateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                style="width: 100%"
                @change="handleDateRangeChange"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="16" v-if="['currency_latest', 'currency_history', 'currency_time_series'].includes(collectionName)">
          <el-col :span="24">
            <el-form-item label="货币代码（可选）">
              <el-input v-model="syncSymbols" placeholder="为空则获取全部, 或输入如 AUD,CNY (用于单个或指定更新)" />
            </el-form-item>
          </el-col>
        </el-row>

        <div style="margin-top: 16px;">
          <el-button type="primary" @click="handleSync" :loading="refreshing" :disabled="batchUpdating">单个更新</el-button>
          <el-button 
            v-if="collectionName !== 'currency_currencies'"
            type="success" 
            @click="handleBatchSync" 
            :loading="batchUpdating"
            :disabled="refreshing"
            style="margin-left: 8px;"
          >
            批量更新
          </el-button>
        </div>

        <!-- 批量更新进度条 -->
        <div v-if="batchUpdating" style="margin-top: 16px; padding: 16px; background-color: #f5f7fa; border-radius: 4px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: bold; color: #409eff;">批量更新进度</span>
            <span style="font-size: 14px; color: #909399;">{{ progressPercentage }}%</span>
          </div>
          <el-progress 
            :percentage="progressPercentage" 
            :status="progressStatus"
            :stroke-width="15"
          />
          <p style="margin-top: 10px; text-align: center; color: #606266; font-size: 13px;">
            {{ progressMessage }}
          </p>
        </div>
      </el-form>

      <!-- 更新说明 -->
      <div style="margin-top: 24px; background-color: #fdf6ec; padding: 16px; border-radius: 4px;">
        <div style="color: #e6a23c; font-weight: bold; margin-bottom: 8px;">更新说明</div>
        <div style="font-size: 13px; color: #e6a23c; line-height: 1.6;">
          <template v-if="collectionName === 'currency_latest'">
            <p style="margin: 0;">- 单个更新：输入货币代码更新指定货币（逗号分隔可更新多个）<br/>- 批量更新：同时获取 USD 和 CNY 两个基准货币的所有汇率数据</p>
          </template>
          <template v-else-if="collectionName === 'currency_history'">
            <p style="margin: 0;">获取指定日期的历史汇率数据（必须指定日期）。批量更新会自动遍历所有货币。</p>
          </template>
          <template v-else-if="collectionName === 'currency_time_series'">
            <p style="margin: 0;">获取时间范围内的汇率数据（必须指定开始和结束日期）。批量更新会自动遍历所有货币。</p>
          </template>
          <template v-else-if="collectionName === 'currency_currencies'">
            <p style="margin: 0;">获取所有支持的货币基础信息列表（包含10个字段）。</p>
          </template>
          <template v-else-if="collectionName === 'currency_convert'">
            <p style="margin: 0;">获取货币对转换价格。批量更新会刷新已有的转换记录。</p>
          </template>
        </div>
      </div>

      <template #footer>
        <el-button @click="apiUpdateDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :total-count="currencyStats.total_count"
      :field-count="fields.length"
      :latest-update="currencyStats.latest_date"
      :data-source="currentCollectionInfo.dataSource"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
// import { Search, UploadFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { currenciesApi } from '@/api/currencies'
import * as echarts from 'echarts'
import {
  CollectionPageHeader,
  CollectionDataTable,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  type RemoteSyncConfig,
} from '@/components/collection'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)
const collectionInfo = ref<any>(null)

const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const overviewDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)
const apiUpdateDialogVisible = ref(false)
const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

// 批量更新进度相关
const batchUpdating = ref(false)
const progressPercentage = ref(0)
const progressStatus = ref<'' | 'success' | 'warning' | 'exception'>('')
const progressMessage = ref('')
const currentTaskId = ref('')
let batchProgressTimer: ReturnType<typeof setInterval> | null = null

// Chart related
const chartRef = ref<HTMLElement | null>(null)
const chartInstance = ref<echarts.ECharts | null>(null)
const selectedCurrencies = ref<string[]>([])
const hoveredCurrency = ref<string>('') // New: Track hovered currency
const availableCurrencies = computed(() => {
  if (items.value && items.value.length > 0) {
    const firstItem = items.value[0] as any
    return Object.keys(firstItem)
      .filter(key => key !== 'date' && key !== '_id' && key !== 'created_at' && 
                     key !== 'updated_at' && key !== 'source' && key !== 'synced_at')
      .sort()
  }
  return []
})

const currencyOptions = computed(() => {
    return ['全部', ...availableCurrencies.value]
})

const handleCurrencyChange = (val: string[]) => {
    // Logic for "All" option mutual exclusion
    const hasAll = val.includes('全部')
    const lastItem = val[val.length - 1]
    
    if (lastItem === '全部') {
        // User clicked 'All', clear others
        selectedCurrencies.value = ['全部']
    } else if (hasAll && val.length > 1) {
        // User clicked something else while 'All' was selected, remove 'All'
        selectedCurrencies.value = val.filter(v => v !== '全部')
    } else if (val.length === 0) {
        // If cleared (e.g. 'All' removed), default to BTC and ETH
        const defaults = ['BTC', 'ETH'].filter(c => availableCurrencies.value.includes(c))
        if (defaults.length > 0) {
             selectedCurrencies.value = defaults
        } else {
             // If BTC/ETH not available, select first 5
             selectedCurrencies.value = availableCurrencies.value.slice(0, 5)
        }
    }
    
    updateChart()
}
const filterValue = ref('')
const fields = computed(() => {
  // Check if collection has dynamic columns flag
  if (collectionInfo.value?.dynamic_columns || 
      (collectionInfo.value?.fields && collectionInfo.value.fields.length === 0)) {
    // Generate fields from actual data
    if (items.value && items.value.length > 0) {
      const firstItem = items.value[0] as any
      const allKeys = Object.keys(firstItem).filter(key => 
        key !== '_id' && key !== 'created_at' && key !== 'updated_at' && key !== 'source' && key !== 'synced_at'
      )
      // Sort: date first, then alphabetically, limit to first 30 currencies for better UX
      const sortedKeys = allKeys.sort((a, b) => {
        if (a === 'date') return -1
        if (b === 'date') return 1
        return a.localeCompare(b)
      })
      
      // Return date + first 30 currency columns (adjust as needed)
      const dateCol = sortedKeys.find(k => k === 'date')
      const otherCols = sortedKeys.filter(k => k !== 'date').slice(0, 30)
      return dateCol ? [dateCol, ...otherCols] : otherCols
    }
    return ['date']  // Default if no data
  }
  return collectionInfo.value?.fields || []
})

// 为 CollectionDataTable 提供字段定义（带 fixed 属性）
const currencyFields = computed(() => {
  return fields.value.map((field: string) => ({
    name: field,
    fixed: field === 'date' ? 'left' as const : undefined,
    width: field === 'date' ? 150 : undefined,
  }))
})

// 格式化货币值（数字保留6位小数）
const formatCurrencyValue = (value: any) => {
  if (typeof value === 'number') {
    return value.toFixed(6)
  }
  return value
}

// Sync params
const syncBase = ref('USD')
const syncSymbols = ref('')
const apiKey = ref('')
const fileImportRef = ref()
const importing = ref(false)
const syncDate = ref('')
const syncDateRange = ref([])
const syncStartDate = ref('')
const syncEndDate = ref('')
const syncTo = ref('CNY')
const syncAmount = ref('10000')

// Remote sync params (MongoDB)
const remoteSyncing = ref(false)
const remoteSyncStats = ref<any>(null)

const handleDateRangeChange = (val: any) => {
    if (val && val.length === 2) {
        syncStartDate.value = val[0]
        syncEndDate.value = val[1]
    } else {
        syncStartDate.value = ''
        syncEndDate.value = ''
    }
}

const loadData = async () => {
  loading.value = true
  try {
    // Load collection info first if not loaded
    if (!collectionInfo.value) {
        const collections = await currenciesApi.getCollections()
        collectionInfo.value = collections.data.find((c: any) => c.name === collectionName.value)
    }

    const res = await currenciesApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      q: filterValue.value
    })
    if (res.success) {
      items.value = res.data.items
      total.value = res.data.total
      
      // Initialize chart for time series collection
      if (collectionName.value === 'currency_time_series' && items.value.length > 0) {
        await nextTick()
        initChart()
      }
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const initChart = () => {
  if (!chartRef.value) return
  
  // Dispose existing chart
  if (chartInstance.value) {
    chartInstance.value.dispose()
  }
  
  // Initialize chart
  chartInstance.value = echarts.init(chartRef.value)
  
  // Add event listeners for hover effects
  chartInstance.value.on('mouseover', (params: any) => {
    if (params.componentType === 'series') {
        hoveredCurrency.value = params.seriesName
    }
  })
  
  chartInstance.value.on('mouseout', () => {
    hoveredCurrency.value = ''
  })

  // Set default selected currencies (All available currencies)
  if (availableCurrencies.value.length > 0) {
    // Select 'All' by default
    selectedCurrencies.value = ['全部']
  }
  
  updateChart()
}

// Watch for hover changes to update title
watch(hoveredCurrency, (newVal) => {
  if (chartInstance.value) {
    chartInstance.value.setOption({
      title: {
        text: newVal ? `当前选中: ${newVal}` : '货币价格涨跌幅 (%)',
        subtext: newVal ? '已高亮显示' : '以第一个日期价格为基准',
        textStyle: {
            color: newVal ? '#409EFF' : '#303133',
            fontSize: newVal ? 20 : 18
        }
      }
    })
  }
})

const updateChart = () => {
  if (!chartInstance.value || items.value.length === 0) return
  
  // Sort items by date
  const sortedItems = [...items.value].sort((a: any, b: any) => {
    return new Date(a.date).getTime() - new Date(b.date).getTime()
  })
  
  // Extract dates for X axis
  const dates = sortedItems.map((item: any) => item.date)
  
  // Prepare series data
  const series: any[] = []
  
  // Determine currencies to show
  let currenciesToShow: string[] = []
  if (selectedCurrencies.value.includes('全部')) {
    currenciesToShow = availableCurrencies.value
  } else {
    currenciesToShow = selectedCurrencies.value
  }
  
  // If too many currencies selected, use simpler chart settings for performance
  const isHeavyData = currenciesToShow.length > 50;

  currenciesToShow.forEach(currency => {
    const data: number[] = []
    let baseValue: number | null = null
    let hasValidData = false
    
    sortedItems.forEach((item: any) => {
      const value = item[currency]
      if (value !== undefined && value !== null && typeof value === 'number') {
        if (!hasValidData) {
            // First valid data point becomes baseline
            baseValue = value
            hasValidData = true
            data.push(0) 
        } else if (baseValue !== null && baseValue !== 0) {
          // Calculate percentage change from baseline
          const percentChange = ((value - baseValue) / baseValue) * 100
          data.push(percentChange)
        } else {
          data.push(0)
        }
      } else {
        // If missing data, use previous value or 0
        data.push(data.length > 0 ? data[data.length - 1] : 0)
      }
    })
    
    series.push({
      name: currency,
      type: 'line',
      data: data,
      smooth: false, // Disable smooth for better performance
      showSymbol: !isHeavyData, // Hide symbols if too many lines
      symbol: 'circle',
      symbolSize: 6, // Larger symbol for easier interaction
      sampling: 'lttb', // Downsample data for performance
      lineStyle: {
        width: 2, // Thicker line for easier hovering
        opacity: 0.6
      },
      emphasis: {
        focus: 'series', // Highlight series on hover
        blurScope: 'coordinateSystem', // Blur other series
        lineStyle: {
            width: 5, // Even thicker when highlighted
            opacity: 1,
            shadowBlur: 10,
            shadowColor: 'rgba(0,0,0,0.5)'
        },
        itemStyle: {
            scale: 1.5 // Enlarge symbol
        },
        z: 10 // Bring to front
      },
      triggerLineEvent: true // Enable line hover events
    })
  })
  
  const option = {
    animation: !isHeavyData, // Disable animation for large datasets
    title: {
      text: hoveredCurrency.value ? `当前选中: ${hoveredCurrency.value}` : '货币价格涨跌幅 (%)',
      subtext: hoveredCurrency.value ? '已高亮显示' : '以第一个日期价格为基准',
      left: 'center',
      textStyle: {
        color: hoveredCurrency.value ? '#409EFF' : '#303133',
        fontSize: hoveredCurrency.value ? 20 : 18
      }
    },
    tooltip: {
      trigger: 'axis',
      enterable: true, // Allow mouse to enter tooltip
      confine: true, // Keep tooltip within chart
      order: 'valueDesc', // Sort tooltip items by value
      formatter: (params: any) => {
        if (!Array.isArray(params)) {
            return '';
        }
        
        let result = params[0].axisValue + '<br/>'
        
        // If a currency is hovered, prioritize showing it
        if (hoveredCurrency.value) {
            const hoveredParam = params.find((p: any) => p.seriesName === hoveredCurrency.value)
            if (hoveredParam) {
                 const sign = hoveredParam.value >= 0 ? '+' : ''
                 result += `<div style="font-weight:bold; color:#409EFF; margin-bottom:6px; padding:4px; background:rgba(64,158,255,0.1); border-radius:4px;">
                    ${hoveredParam.marker} ${hoveredParam.seriesName}: ${sign}${hoveredParam.value.toFixed(2)}%
                 </div>`
            }
        }

        // Only show top 20 items in tooltip to avoid overflow
        const sortedParams = [...params].sort((a, b) => b.value - a.value);
        const displayParams = sortedParams.slice(0, 20);
        
        let count = 0;
        displayParams.forEach((param: any) => {
          // Skip the hovered currency if we already showed it at top
          if (param.seriesName === hoveredCurrency.value) return
          
          const sign = param.value >= 0 ? '+' : ''
          const color = param.color
          result += `<div style="margin-bottom:2px;">
            <span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:${color};"></span>
            <span style="display:inline-block;width:50px;">${param.seriesName}</span>
            <span style="font-weight:bold;">${sign}${param.value.toFixed(2)}%</span>
          </div>`
          count++;
        })
        
        if (params.length > 20) {
            result += `<div style="margin-top:4px;color:#909399;font-size:12px;">... (还有 ${params.length - count - (hoveredCurrency.value ? 1 : 0)} 个)</div>`
        }
        return result
      }
    },
    legend: {
      data: currenciesToShow,
      top: 40,
      type: 'scroll', // Scrollable legend
      width: '80%'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: 100,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '涨跌幅 (%)',
      axisLabel: {
        formatter: '{value}%'
      },
      scale: true // Focus on the data range
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        start: 0,
        end: 100
      }
    ],
    series: series
  }
  
  chartInstance.value.setOption(option, true) // true = not merge, completely replace
}

const resetChart = () => {
  // Reset to All
  selectedCurrencies.value = ['全部']
  updateChart()
}

// 处理更新数据下拉菜单命令
const handleUpdateCommand = async (command: string) => {
  if (command === 'api') {
    // 清空表单数据
    syncSymbols.value = ''
    syncDate.value = ''
    syncDateRange.value = []
    syncStartDate.value = ''
    syncEndDate.value = ''
    
    // 加载默认 API Key
    try {
      const configRes = await currenciesApi.getConfig()
      if (configRes.success && configRes.data.default_api_key) {
        apiKey.value = configRes.data.default_api_key
      } else {
        apiKey.value = ''
      }
    } catch (error) {
      console.error('Failed to load config:', error)
      apiKey.value = ''
    }
    
    apiUpdateDialogVisible.value = true
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

const handleFilter = () => {
  page.value = 1
  loadData()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  page.value = 1
  loadData()
}

const handlePageChange = (val: number) => {
  page.value = val
  loadData()
}

// 获取全部数据用于导出（分页获取）
const fetchAllDataForExport = async (): Promise<any[]> => {
  const allData: any[] = []
  const batchSize = 500 // 后端限制最大 500
  let currentPage = 1
  let hasMore = true
  
  while (hasMore) {
    const res = await currenciesApi.getCollectionData(collectionName.value, {
      page: currentPage,
      page_size: batchSize,
      filter_value: filterValue.value || undefined,
    })
    
    if (!res.success) {
      throw new Error(res.message || '获取数据失败')
    }
    
    const items = res.data?.items || []
    allData.push(...items)
    
    const totalItems = res.data?.total || 0
    hasMore = allData.length < totalItems && items.length === batchSize
    currentPage++
    
    if (currentPage > 1000) break
  }
  
  return allData
}

const handleSync = async () => {
    if (!apiKey.value) {
        ElMessage.warning('请输入 API Key')
        return
    }
    
    refreshing.value = true
    try {
        let res;
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.syncCurrencyLatest({
                base: syncBase.value,
                symbols: syncSymbols.value,
                api_key: apiKey.value
            })
        } else if (collectionName.value === 'currency_history') {
            if (!syncDate.value) {
                 ElMessage.warning('请输入日期')
                 refreshing.value = false
                 return
            }
            res = await currenciesApi.syncCurrencyHistory({
                base: syncBase.value,
                date: syncDate.value,
                symbols: syncSymbols.value,
                api_key: apiKey.value
            })
        } else if (collectionName.value === 'currency_time_series') {
            if (!syncStartDate.value || !syncEndDate.value) {
                 ElMessage.warning('请输入开始和结束日期')
                 refreshing.value = false
                 return
            }
            res = await currenciesApi.syncCurrencyTimeSeries({
                base: syncBase.value,
                start_date: syncStartDate.value,
                end_date: syncEndDate.value,
                symbols: syncSymbols.value,
                api_key: apiKey.value
            })
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.syncCurrencyCurrencies({
                c_type: 'fiat',
                api_key: apiKey.value
            })
        } else if (collectionName.value === 'currency_convert') {
            // 单个转换使用统一刷新 API
            res = await currenciesApi.refreshCollectionData(collectionName.value, {
                base: syncBase.value,
                to: syncTo.value,
                amount: syncAmount.value,
                api_key: apiKey.value
            })
        }

        if (res && res.success) {
            ElMessage.success(res.message)
            apiUpdateDialogVisible.value = false
            loadData()
        } else {
            ElMessage.error(res?.message || '同步失败')
        }
    } catch (error) {
        ElMessage.error('同步失败')
    } finally {
        refreshing.value = false
    }
}

const handleBatchSync = async () => {
    if (!apiKey.value) {
        ElMessage.warning('请输入 API Key')
        return
    }
    
    // 验证必填参数
    if (collectionName.value === 'currency_history' && !syncDate.value) {
        ElMessage.warning('请输入日期')
        return
    }
    if (collectionName.value === 'currency_time_series' && (!syncStartDate.value || !syncEndDate.value)) {
        ElMessage.warning('请输入开始和结束日期')
        return
    }
    
    // 初始化进度状态
    batchUpdating.value = true
    progressPercentage.value = 0
    progressStatus.value = ''
    progressMessage.value = '正在创建批量更新任务...'
    
    try {
        // 构建参数
        const params: any = {
            update_type: 'batch',
            api_key: apiKey.value,
            base: syncBase.value
        }
        
        if (collectionName.value === 'currency_history') {
            params.date = syncDate.value
        } else if (collectionName.value === 'currency_time_series') {
            params.start_date = syncStartDate.value
            params.end_date = syncEndDate.value
        } else if (collectionName.value === 'currency_convert') {
            params.to = syncTo.value
            params.amount = syncAmount.value
        }
        
        // 调用统一刷新 API
        const res = await currenciesApi.refreshCollectionData(collectionName.value, params)
        
        if (res.success && res.data?.task_id) {
            currentTaskId.value = res.data.task_id
            progressMessage.value = '任务已创建，正在执行...'
            pollBatchTaskStatus()
        } else {
            progressStatus.value = 'exception'
            progressMessage.value = res.message || '创建任务失败'
            batchUpdating.value = false
        }
    } catch (error) {
        console.error('Batch sync error:', error)
        progressStatus.value = 'exception'
        progressMessage.value = '批量更新失败'
        batchUpdating.value = false
    }
}

// 轮询任务状态
const pollBatchTaskStatus = () => {
    if (batchProgressTimer) {
        clearInterval(batchProgressTimer)
    }
    
    batchProgressTimer = setInterval(async () => {
        try {
            const res = await currenciesApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
            
            if (res.success && res.data) {
                const task = res.data
                
                // 更新进度
                if (task.progress !== undefined && task.total !== undefined && task.total > 0) {
                    progressPercentage.value = Math.round((task.progress / task.total) * 100)
                }
                progressMessage.value = task.message || '正在批量更新...'
                
                // 完成
                if (task.status === 'success') {
                    if (batchProgressTimer) clearInterval(batchProgressTimer)
                    progressStatus.value = 'success'
                    progressPercentage.value = 100
                    progressMessage.value = task.message || '批量更新完成'
                    ElMessage.success(task.message || '批量更新完成')
                    await loadData()
                    setTimeout(() => {
                        batchUpdating.value = false
                    }, 2000)
                    
                } else if (task.status === 'failed') {
                    if (batchProgressTimer) clearInterval(batchProgressTimer)
                    progressStatus.value = 'exception'
                    progressMessage.value = task.message || '批量更新失败'
                    ElMessage.error(task.message || '批量更新失败')
                    batchUpdating.value = false
                }
            }
        } catch (error) {
            console.error('Poll task status error:', error)
        }
    }, 1000)
}

// 文件导入处理（使用共享组件）
const handleImportFile = async (files: File[]) => {
    if (!files.length) return
    importing.value = true
    try {
        let res;
        const file = files[0]
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.uploadCurrencyLatest(file)
        } else if (collectionName.value === 'currency_history') {
            res = await currenciesApi.uploadCurrencyHistory(file)
        } else if (collectionName.value === 'currency_time_series') {
            res = await currenciesApi.uploadCurrencyTimeSeries(file)
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.uploadCurrencyCurrencies(file)
        }
        
        if (res && res.success) {
            ElMessage.success(res.message)
            fileImportRef.value?.clearFiles()
            uploadDialogVisible.value = false
            loadData()
        } else {
            ElMessage.error(res?.message || '导入失败')
        }
    } catch (error) {
        ElMessage.error('导入失败')
    } finally {
        importing.value = false
    }
}

// 远程同步处理（使用共享组件）
const handleRemoteSync = async (config: RemoteSyncConfig) => {
    remoteSyncing.value = true
    remoteSyncStats.value = null
    
    try {
        let res
        const collection = config.collection || collectionName.value
        
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.remoteSyncCurrencyLatest({
                remote_host: config.host,
                remote_collection: collection,
                remote_username: config.username,
                remote_password: config.password,
                remote_auth_source: config.authSource,
                batch_size: config.batchSize
            })
        } else if (collectionName.value === 'currency_history') {
            res = await currenciesApi.remoteSyncCurrencyHistory({
                remote_host: config.host,
                remote_collection: collection,
                remote_username: config.username,
                remote_password: config.password,
                remote_auth_source: config.authSource,
                batch_size: config.batchSize
            })
        } else if (collectionName.value === 'currency_time_series') {
            res = await currenciesApi.remoteSyncCurrencyTimeSeries({
                remote_host: config.host,
                remote_collection: collection,
                remote_username: config.username,
                remote_password: config.password,
                remote_auth_source: config.authSource,
                batch_size: config.batchSize
            })
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.remoteSyncCurrencyCurrencies({
                remote_host: config.host,
                remote_collection: collection,
                remote_username: config.username,
                remote_password: config.password,
                remote_auth_source: config.authSource,
                batch_size: config.batchSize
            })
        }

        if (res && res.success) {
            ElMessage.success(res.message || '同步成功')
            remoteSyncStats.value = res.data
            loadData()
        } else {
            ElMessage.error(res?.message || '同步失败')
        }
    } catch (error) {
        ElMessage.error('同步失败')
    } finally {
        remoteSyncing.value = false
    }
}

const handleClearData = async () => {
    try {
        await ElMessageBox.confirm(
            '确定要清空当前数据集合的所有数据吗？此操作不可恢复！',
            '清空数据确认',
            {
                type: 'warning',
                confirmButtonText: '确定',
                cancelButtonText: '取消'
            }
        )
    } catch {
        return
    }

    clearing.value = true
    try {
        let res;
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.clearCurrencyLatest()
        } else if (collectionName.value === 'currency_history') {
            res = await currenciesApi.clearCurrencyHistory()
        } else if (collectionName.value === 'currency_time_series') {
            res = await currenciesApi.clearCurrencyTimeSeries()
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.clearCurrencyCurrencies()
        } else if (collectionName.value === 'currency_convert') {
            // 使用通用清空 API (如果后端支持)
            res = { success: false, message: '暂不支持清空此集合' }
        }
        
        if (res && res.success) {
            ElMessage.success(res.message || '清空成功')
            loadData()
        } else {
            ElMessage.error(res?.message || '清空失败')
        }
    } catch (error) {
        ElMessage.error('清空失败')
    } finally {
        clearing.value = false
    }
}

const currencyCollectionStaticInfo: Record<string, { dataSource: string }> = {
  currency_latest: {
    dataSource: 'https://currencyscoop.com/'
  },
  currency_history: {
    dataSource: 'https://currencyscoop.com/'
  },
  currency_time_series: {
    dataSource: 'https://currencyscoop.com/'
  },
  currency_currencies: {
    dataSource: 'https://currencyscoop.com/'
  },
  currency_convert: {
    dataSource: 'https://currencyscoop.com/'
  }
}

const currentCollectionInfo = computed(() => {
  const fieldCount = Array.isArray(fields.value) ? (fields.value as any[]).length : 0
  const staticInfo = currencyCollectionStaticInfo[collectionName.value] || { dataSource: '暂无' }
  return {
    name: collectionName.value,
    displayName: collectionInfo.value?.display_name || collectionName.value,
    fieldCount,
    dataSource: staticInfo.dataSource
  }
})

const currencyStats = computed(() => {
  const result: { total_count: number; latest_date: string } = {
    total_count: total.value || 0,
    latest_date: ''
  }

  if (!items.value || items.value.length === 0) {
    return result
  }

  const rows = items.value as any[]
  let dateField = ''

  if (collectionName.value === 'currency_currencies') {
    if ('updated_at' in rows[0]) {
      dateField = 'updated_at'
    }
  } else {
    if ('date' in rows[0]) {
      dateField = 'date'
    }
  }

  if (dateField) {
    const dates = rows
      .map((row: any) => row[dateField])
      .filter((v: any) => typeof v === 'string' && v.length > 0)
    if (dates.length > 0) {
      dates.sort()
      result.latest_date = dates[dates.length - 1]
    }
  }

  return result
})

onMounted(() => {
  loadData()
  
  const handleResize = () => {
    if (chartInstance.value) {
      chartInstance.value.resize()
    }
  }
  
  window.addEventListener('resize', handleResize)
  
  return () => {
    window.removeEventListener('resize', handleResize)
    if (chartInstance.value) {
      chartInstance.value.dispose()
    }
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
