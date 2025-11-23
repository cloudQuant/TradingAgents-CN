<template>
  <div class="collection-view">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionInfo?.display_name || collectionName }}
          </h1>
          <p class="page-description">{{ collectionInfo?.description || '' }}</p>
        </div>
        <div class="header-actions">
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
          <el-button :icon="Download" type="primary" @click="showRefreshDialog" :loading="refreshing">更新数据</el-button>
          <el-button :icon="Delete" type="danger" @click="handleClearData" :loading="clearing">清空数据</el-button>
        </div>
      </div>
    </div>

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

      <el-card shadow="hover" class="data-card">
        <template #header>
          <div class="card-header">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span>数据列表</span>
              <el-tag v-if="collectionInfo?.dynamic_columns && items.length > 0" type="info" size="small">
                显示前 {{ fields.length - 1 }} 个货币列
              </el-tag>
            </div>
            <div class="header-actions">
              <el-input
                v-model="filterValue"
                placeholder="搜索货币..."
                style="width: 200px; margin-right: 8px;"
                clearable
                @clear="handleFilter"
                @keyup.enter="handleFilter"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-button size="small" :icon="Search" @click="handleFilter">搜索</el-button>
            </div>
          </div>
        </template>
        
        <el-table
          :data="items"
          v-loading="loading"
          stripe
          border
          style="width: 100%"
          max-height="600"
        >
          <el-table-column
            v-for="field in fields"
            :key="field"
            :prop="field"
            :label="field"
            :width="field === 'date' ? 150 : undefined"
            :min-width="field === 'date' ? undefined : 120"
            :fixed="field === 'date' ? 'left' : false"
            sortable
            show-overflow-tooltip
          >
             <template #default="{ row }">
              <span v-if="typeof row[field] === 'number'">{{ row[field].toFixed(6) }}</span>
              <span v-else>{{ row[field] }}</span>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="refreshDialogVisible"
      title="更新数据"
      width="600px"
      :close-on-click-modal="false"
    >
      <!-- 集合名称 -->
      <el-form label-width="80px">
        <el-form-item label="集合名称">
          <el-input :value="collectionInfo?.display_name || collectionName" disabled />
        </el-form-item>
      </el-form>

      <!-- 文件导入区域 -->
      <el-divider content-position="left">文件导入</el-divider>
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
        accept=".csv,.xlsx"
        drag
      >
        <div class="el-upload__text">拖拽文件到此处或<em style="color: #409eff; cursor: pointer;">点击选择文件</em></div>
      </el-upload>
      <div style="margin-top: 8px; color: #909399; font-size: 12px;">
        支持 CSV 或 Excel 文件，列结构需包含{{ collectionName === 'currency_latest' ? '货币代码、日期、基础货币、比率' : collectionName === 'currency_currencies' ? '货币代码、名称、符号' : '相关字段' }}
      </div>
      <el-button style="margin-top: 12px;" type="primary" @click="handleImport" :loading="refreshing" :disabled="!importFile">导入文件</el-button>

      <!-- 远程同步区域 (从 MongoDB) -->
      <el-divider content-position="left">远程同步</el-divider>
      <el-form label-position="top">
        <el-row :gutter="16">
          <el-col :span="24">
            <el-form-item label="远程 MongoDB 地址">
              <el-input
                v-model="remoteSyncHost"
                placeholder="远程 MongoDB IP 或 URI，例如 192.168.1.10 或 mongodb://user:pwd@host:27017/db"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="数据库类型">
              <el-select v-model="remoteSyncDbType" disabled style="width: 100%">
                <el-option label="MongoDB" value="mongodb" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="批次大小">
              <el-select v-model="remoteSyncBatchSize" style="width: 100%">
                <el-option label="1000" :value="1000" />
                <el-option label="2000" :value="2000" />
                <el-option label="5000" :value="5000" />
                <el-option label="10000" :value="10000" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="远程集合名称">
              <el-input v-model="remoteSyncCollection" :placeholder="`默认 ${collectionName}`" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="远程用户名（可选）">
              <el-input v-model="remoteSyncUsername" placeholder="远程用户名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="24">
            <el-form-item label="认证库（authSource）">
              <el-input v-model="remoteSyncAuthSource" placeholder="例如 admin 或 tradingagents" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="24">
            <el-form-item label="远程密码（可选）">
              <el-input v-model="remoteSyncPassword" type="password" show-password placeholder="远程密码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-button type="primary" @click="handleRemoteSync" :loading="remoteSyncing" :disabled="!remoteSyncHost || remoteSyncing">
          远程同步
        </el-button>
        <div v-if="remoteSyncStats" style="margin-top: 8px; font-size: 12px; color: #606266;">
          最近一次同步：远程共 {{ remoteSyncStats.remote_total }} 条，已写入/更新 {{ remoteSyncStats.synced }} 条
        </div>
      </el-form>

      <!-- 在线更新区域 (从 AKShare API) -->
      <el-divider content-position="left">在线更新</el-divider>
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
          <el-button type="primary" @click="handleSync" :loading="refreshing">单个更新</el-button>
          <el-button 
            v-if="collectionName !== 'currency_currencies'"
            type="success" 
            @click="handleBatchSync" 
            :loading="refreshing"
            style="margin-left: 8px;"
          >
            批量更新
          </el-button>
        </div>
      </el-form>

      <!-- 更新说明 -->
      <div style="margin-top: 24px; background-color: #fdf6ec; padding: 16px; border-radius: 4px;">
        <div style="color: #e6a23c; font-weight: bold; margin-bottom: 8px;">更新说明</div>
        <div style="font-size: 13px; color: #e6a23c; line-height: 1.6;">
          <p style="margin: 0 0 8px 0;"><strong>文件导入：</strong>支持 CSV 或 Excel 文件导入数据。</p>
          <p style="margin: 0 0 8px 0;"><strong>远程同步：</strong>从远程 MongoDB 数据库同步数据到本地。</p>
          <p style="margin: 0 0 8px 0;"><strong>在线更新：</strong>使用 CurrencyScoop API 在线获取最新数据。</p>
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
        <div style="text-align: right;">
          <el-button @click="refreshDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { Box, Refresh, Search, Download, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { currenciesApi } from '@/api/currencies'
import * as echarts from 'echarts'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)
const collectionInfo = ref<any>(null)

const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const refreshDialogVisible = ref(false)
const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

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

// Sync params
const activeTab = ref('sync')
const syncBase = ref('USD')
const syncSymbols = ref('')
const apiKey = ref('')
const importFile = ref<File | null>(null)
const syncDate = ref('')
const syncDateRange = ref([])
const syncStartDate = ref('')
const syncEndDate = ref('')
const syncTo = ref('CNY')
const syncAmount = ref('10000')

// Remote sync params (MongoDB)
const remoteSyncing = ref(false)
const remoteSyncHost = ref('')
const remoteSyncDbType = ref('mongodb')
const remoteSyncBatchSize = ref(1000)
const remoteSyncCollection = ref('')
const remoteSyncUsername = ref('')
const remoteSyncPassword = ref('')
const remoteSyncAuthSource = ref('admin')
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
    
    sortedItems.forEach((item: any, index: number) => {
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

const showRefreshDialog = async () => {
  activeTab.value = 'sync'
  syncSymbols.value = ''
  syncDate.value = ''
  syncDateRange.value = []
  syncStartDate.value = ''
  syncEndDate.value = ''
  
  // Load default API key from backend config
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
  
  refreshDialogVisible.value = true
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

        if (res && res.success) {
            ElMessage.success(res.message)
            refreshDialogVisible.value = false
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
    
    refreshing.value = true
    try {
        let res
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.batchSyncCurrencyLatest({
                api_key: apiKey.value
            })
        } else if (collectionName.value === 'currency_history') {
            if (!syncDate.value) {
                 ElMessage.warning('请输入日期')
                 refreshing.value = false
                 return
            }
            res = await currenciesApi.batchSyncCurrencyHistory({
                base: syncBase.value,
                date: syncDate.value,
                api_key: apiKey.value
            })
        } else if (collectionName.value === 'currency_time_series') {
            if (!syncStartDate.value || !syncEndDate.value) {
                 ElMessage.warning('请输入开始和结束日期')
                 refreshing.value = false
                 return
            }
            res = await currenciesApi.batchSyncCurrencyTimeSeries({
                base: syncBase.value,
                start_date: syncStartDate.value,
                end_date: syncEndDate.value,
                api_key: apiKey.value
            })

        if (res && res.success) {
            ElMessage.success(res.message)
            refreshDialogVisible.value = false
            loadData()
        } else {
            ElMessage.error(res?.message || '批量更新失败')
        }
    } catch (error) {
        ElMessage.error('批量更新失败')
    } finally {
        refreshing.value = false
    }
}

const handleImport = async () => {
    if (!importFile.value) return
    refreshing.value = true
    try {
        let res;
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.uploadCurrencyLatest(importFile.value)
        } else if (collectionName.value === 'currency_history') {
            res = await currenciesApi.uploadCurrencyHistory(importFile.value)
        } else if (collectionName.value === 'currency_time_series') {
            res = await currenciesApi.uploadCurrencyTimeSeries(importFile.value)
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.uploadCurrencyCurrencies(importFile.value)
        }
        
         if (res && res.success) {
            ElMessage.success(res.message)
            refreshDialogVisible.value = false
            loadData()
        } else {
            ElMessage.error(res?.message || '导入失败')
        }
    } catch (error) {
         ElMessage.error('导入失败')
    } finally {
        refreshing.value = false
    }
}

const handleFileChange = (file: any) => {
    importFile.value = (file && (file.raw || file)) || null
}

const handleRemoteSync = async () => {
    if (!remoteSyncHost.value) {
        ElMessage.warning('请输入远程 MongoDB 地址')
        return
    }
    
    remoteSyncing.value = true
    try {
        let res
        const collection = remoteSyncCollection.value || collectionName.value
        
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.remoteSyncCurrencyLatest({
                remote_host: remoteSyncHost.value,
                remote_collection: collection,
                remote_username: remoteSyncUsername.value,
                remote_password: remoteSyncPassword.value,
                remote_auth_source: remoteSyncAuthSource.value,
                batch_size: remoteSyncBatchSize.value
            })
        } else if (collectionName.value === 'currency_history') {
            res = await currenciesApi.remoteSyncCurrencyHistory({
                remote_host: remoteSyncHost.value,
                remote_collection: collection,
                remote_username: remoteSyncUsername.value,
                remote_password: remoteSyncPassword.value,
                remote_auth_source: remoteSyncAuthSource.value,
                batch_size: remoteSyncBatchSize.value
            })
        } else if (collectionName.value === 'currency_time_series') {
            res = await currenciesApi.remoteSyncCurrencyTimeSeries({
                remote_host: remoteSyncHost.value,
                remote_collection: collection,
                remote_username: remoteSyncUsername.value,
                remote_password: remoteSyncPassword.value,
                remote_auth_source: remoteSyncAuthSource.value,
                batch_size: remoteSyncBatchSize.value
            })
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.remoteSyncCurrencyCurrencies({
                remote_host: remoteSyncHost.value,
                remote_collection: collection,
                remote_username: remoteSyncUsername.value,
                remote_password: remoteSyncPassword.value,
                remote_auth_source: remoteSyncAuthSource.value,
                batch_size: remoteSyncBatchSize.value
            })
        }

        if (res && res.success) {
            ElMessage.success(res.message || '远程同步成功')
            remoteSyncStats.value = res.data
            loadData()
        } else {
            ElMessage.error(res?.message || '远程同步失败')
        }
    } catch (error) {
        ElMessage.error('远程同步失败')
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
        let res
        if (collectionName.value === 'currency_latest') {
            res = await currenciesApi.clearCurrencyLatest()
        } else if (collectionName.value === 'currency_history') {
            res = await currenciesApi.clearCurrencyHistory()
        } else if (collectionName.value === 'currency_time_series') {
            res = await currenciesApi.clearCurrencyTimeSeries()
        } else if (collectionName.value === 'currency_currencies') {
            res = await currenciesApi.clearCurrencyCurrencies()
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

onMounted(() => {
  loadData()
  
  // Add resize listener for chart
  const handleResize = () => {
    if (chartInstance.value) {
      chartInstance.value.resize()
    }
  }
  
  window.addEventListener('resize', handleResize)
  
  // Cleanup on unmount
  return () => {
    window.removeEventListener('resize', handleResize)
    if (chartInstance.value) {
      chartInstance.value.dispose()
    }
  }
})
</script>

<style scoped>
.collection-view { padding: 16px; }
.page-header { margin-bottom: 24px; }
.header-content { display: flex; justify-content: space-between; align-items: flex-start; }
.page-title { font-size: 24px; display: flex; align-items: center; gap: 10px; margin: 0; }
.page-description { color: #909399; margin: 5px 0 0 0; }
.content { max-width: 1400px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.pagination-wrapper { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
