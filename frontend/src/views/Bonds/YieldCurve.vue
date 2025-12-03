<template>
  <div class="bonds-yield-curve">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><TrendCharts /></el-icon>
            债券 · 收益率曲线
          </h1>
          <p class="page-description">查询与可视化国债收益率曲线（多期限点）</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 查询条件卡片 -->
      <el-card shadow="hover" class="query-card">
        <template #header>
          <div class="card-header">
            <h3>查询条件</h3>
          </div>
        </template>

        <el-form :inline="true" @submit.prevent>
          <el-form-item label="开始日期">
            <el-date-picker
              v-model="start"
              type="date"
              value-format="YYYY-MM-DD"
              placeholder="开始日期"
              style="width: 200px;"
            />
          </el-form-item>
          <el-form-item label="结束日期">
            <el-date-picker
              v-model="end"
              type="date"
              value-format="YYYY-MM-DD"
              placeholder="结束日期"
              style="width: 200px;"
            />
          </el-form-item>
          <el-form-item label="曲线名称">
            <el-select
              v-model="selectedCurveName"
              placeholder="全部曲线"
              clearable
              filterable
              style="width: 250px;"
            >
              <el-option
                v-for="curve in availableCurveNames"
                :key="curve"
                :label="curve"
                :value="curve"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" :icon="Search" @click="fetchCurve">
              查询
            </el-button>
            <el-button :loading="syncing" :icon="Refresh" @click="syncCurve">
              同步入库
            </el-button>
            <el-button :icon="Download" @click="exportData">导出数据</el-button>
          </el-form-item>
        </el-form>

        <el-alert v-if="message" :title="message" type="info" show-icon :closable="false" style="margin-top: 8px;" />
      </el-card>

      <!-- 统计数据卡片 -->
      <el-card shadow="hover" class="stats-card" v-if="statistics">
        <el-row :gutter="16">
          <el-col :xs="12" :sm="8" :md="6" :lg="4">
            <el-statistic title="总记录数" :value="statistics.total_records">
              <template #prefix>
                <el-icon><Document /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4">
            <el-statistic title="日期范围">
              <template #prefix>
                <el-icon><Calendar /></el-icon>
              </template>
              <template #default>
                <span>{{ dateRangeText }}</span>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4">
            <el-statistic title="曲线数量" :value="statistics.curve_names.length">
              <template #prefix>
                <el-icon><DataLine /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4">
            <el-statistic title="期限数量" :value="statistics.tenors.length">
              <template #prefix>
                <el-icon><Grid /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="8" v-if="statistics.curve_names.length > 0">
            <div class="curve-names">
              <span class="label">可用曲线：</span>
              <el-tag
                v-for="curve in statistics.curve_names"
                :key="curve"
                size="small"
                style="margin-right: 8px; margin-bottom: 4px; cursor: pointer;"
                :type="selectedCurveName === curve ? 'primary' : 'info'"
                @click="selectedCurveName = curve"
              >
                {{ curve }}
              </el-tag>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 图表卡片 -->
      <el-card shadow="hover" class="chart-card" v-if="chartData && Object.keys(chartData).length > 0">
        <template #header>
          <div class="card-header">
            <h3>收益率曲线图表</h3>
            <div class="chart-controls">
              <el-radio-group v-model="chartType" size="small">
                <el-radio-button value="line">折线图</el-radio-button>
                <el-radio-button value="surface">3D曲面</el-radio-button>
              </el-radio-group>
              <el-select
                v-model="selectedDate"
                placeholder="选择日期"
                clearable
                style="width: 150px; margin-left: 12px;"
                @change="updateChart"
              >
                <el-option
                  v-for="date in sortedDates"
                  :key="date"
                  :label="date"
                  :value="date"
                />
              </el-select>
            </div>
          </div>
        </template>

        <div class="chart-container" v-loading="loading">
          <v-chart
            v-if="chartOption"
            :option="chartOption"
            :autoresize="true"
            style="height: 500px; width: 100%;"
            class="yield-curve-chart"
          />
          <el-empty v-else description="暂无图表数据" />
        </div>
      </el-card>

      <!-- 数据表格卡片 -->
      <el-card shadow="hover" class="table-card" v-if="records && records.length > 0">
        <template #header>
          <div class="card-header">
            <h3>数据列表</h3>
            <div class="table-controls">
              <el-input
                v-model="tableFilter"
                placeholder="搜索..."
                style="width: 200px;"
                clearable
                @input="handleTableFilter"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </div>
        </template>

        <el-table
          :data="paginatedRecords"
          v-loading="loading"
          stripe
          border
          :style="{ width: '100%' }"
          max-height="600"
        >
          <el-table-column prop="date" label="日期" width="120" sortable />
          <el-table-column prop="curve_name" label="曲线名称" width="200" show-overflow-tooltip />
          <el-table-column prop="tenor" label="期限" width="120" sortable />
          <el-table-column prop="yield" label="收益率(%)" width="120" sortable>
            <template #default="{ row }">
              <span :class="getYieldClass(row.yield)">
                {{ formatYield(row.yield) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="yield_type" label="收益率类型" width="150" />
        </el-table>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="tablePage"
            v-model:page-size="tablePageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="filteredRecords.length"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleTableSizeChange"
            @current-change="handleTablePageChange"
          />
        </div>
      </el-card>

      <!-- 空状态 -->
      <el-card shadow="hover" v-if="!loading && (!records || records.length === 0)">
        <el-empty description="暂无数据，请点击查询按钮获取数据" />
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { TrendCharts, Search, Refresh, Download, Document, Calendar, DataLine, Grid } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, HeatmapChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  VisualMapComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { bondsApi } from '@/api/bonds'
import dayjs from 'dayjs'

// 注册ECharts组件
use([
  CanvasRenderer,
  LineChart,
  HeatmapChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  VisualMapComponent
])

// 数据状态
const start = ref<string | undefined>(undefined)
const end = ref<string | undefined>(undefined)
const selectedCurveName = ref<string | undefined>(undefined)
const loading = ref(false)
const syncing = ref(false)
const message = ref('')

// 数据
const records = ref<Array<{
  date: string
  tenor: string
  yield: number
  curve_name?: string
  yield_type?: string
}>>([])
const chartData = ref<Record<string, Record<string, Record<string, number>>>>({})
const statistics = ref<{
  total_records: number
  curve_names: string[]
  tenors: string[]
  date_range: {
    start: string | null
    end: string | null
    count: number
  }
} | null>(null)

// 图表配置
const chartType = ref<'line' | 'surface'>('line')
const selectedDate = ref<string | undefined>(undefined)
const chartOption = ref<any>(null)

// 表格配置
const tableFilter = ref('')
const tablePage = ref(1)
const tablePageSize = ref(50)

// 计算属性
const availableCurveNames = computed(() => {
  return statistics.value?.curve_names || []
})

const sortedDates = computed(() => {
  if (!chartData.value) return []
  return Object.keys(chartData.value).sort()
})

const dateRangeText = computed(() => {
  if (!statistics.value?.date_range) return '-'
  const { start: s, end: e, count } = statistics.value.date_range
  if (!s || !e) return '-'
  return `${s} 至 ${e} (${count}天)`
})

const filteredRecords = computed(() => {
  let result = records.value

  // 应用搜索过滤
  if (tableFilter.value) {
    const filter = tableFilter.value.toLowerCase()
    result = result.filter(r => {
      return (
        r.date?.toLowerCase().includes(filter) ||
        r.curve_name?.toLowerCase().includes(filter) ||
        r.tenor?.toLowerCase().includes(filter) ||
        r.yield_type?.toLowerCase().includes(filter)
      )
    })
  }

  // 应用曲线名称过滤
  if (selectedCurveName.value) {
    result = result.filter(r => r.curve_name === selectedCurveName.value)
  }

  return result
})

const paginatedRecords = computed(() => {
  const start = (tablePage.value - 1) * tablePageSize.value
  const end = start + tablePageSize.value
  return filteredRecords.value.slice(start, end)
})

// 方法
const fetchCurve = async () => {
  try {
    loading.value = true
    message.value = ''
    records.value = []
    chartData.value = {}
    statistics.value = null
    chartOption.value = null

    const res = await bondsApi.getYieldCurve(start.value, end.value, selectedCurveName.value, 'json')
    
    if (res.success && res.data) {
      if (res.data.records && res.data.records.length > 0) {
        records.value = res.data.records
        chartData.value = res.data.chart_data || {}
        statistics.value = res.data.statistics || null
        
        // 自动选择最新日期
        if (sortedDates.value.length > 0 && !selectedDate.value) {
          selectedDate.value = sortedDates.value[sortedDates.value.length - 1]
        }
        
        updateChart()
        ElMessage.success(`查询成功，共 ${records.value.length} 条记录`)
      } else {
        message.value = '无返回数据'
      }
    } else {
      ElMessage.error(res.message || '查询失败')
    }
  } catch (e: any) {
    console.error(e)
    ElMessage.error('请求失败: ' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const syncCurve = async () => {
  try {
    syncing.value = true
    const res = await bondsApi.syncYieldCurve(start.value, end.value)
    if (res.success) {
      ElMessage.success(`同步完成：saved=${(res.data as any)?.saved ?? '-'} rows=${(res.data as any)?.rows ?? '-'}`)
      // 同步后自动刷新数据
      await fetchCurve()
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (e: any) {
    console.error(e)
    ElMessage.error('请求失败: ' + (e.message || '未知错误'))
  } finally {
    syncing.value = false
  }
}

const updateChart = () => {
  if (!chartData.value || Object.keys(chartData.value).length === 0) {
    chartOption.value = null
    return
  }

  if (chartType.value === 'line') {
    updateLineChart()
  } else {
    updateSurfaceChart()
  }
}

const updateLineChart = () => {
  if (!selectedDate.value || !chartData.value[selectedDate.value]) {
    // 如果没有选择日期，显示所有日期的数据
    const allDates = sortedDates.value
    if (allDates.length === 0) {
      chartOption.value = null
      return
    }

    // 获取所有期限
    const allTenors = new Set<string>()
    allDates.forEach(date => {
      Object.values(chartData.value[date] || {}).forEach(curve => {
        Object.keys(curve).forEach(tenor => allTenors.add(tenor))
      })
    })
    const sortedTenors = Array.from(allTenors).sort((a, b) => {
      const aNum = parseFloat(a) || 0
      const bNum = parseFloat(b) || 0
      return aNum - bNum
    })

    // 为每个曲线创建系列
    const curves = new Set<string>()
    allDates.forEach(date => {
      Object.keys(chartData.value[date] || {}).forEach(curve => curves.add(curve))
    })

    const series = Array.from(curves).map(curveName => {
      const data = sortedTenors.map(tenor => {
        // 找到该期限的最新数据
        for (let i = allDates.length - 1; i >= 0; i--) {
          const date = allDates[i]
          const yieldVal = chartData.value[date]?.[curveName]?.[tenor]
          if (yieldVal !== undefined) {
            return yieldVal
          }
        }
        return null
      }).filter(v => v !== null)

      return {
        name: curveName,
        type: 'line',
        smooth: true,
        data: data,
        symbol: 'circle',
        symbolSize: 6
      }
    })

    chartOption.value = {
      title: {
        text: '收益率曲线',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          let result = `期限: ${params[0].axisValue}<br/>`
          params.forEach((param: any) => {
            result += `${param.seriesName}: ${formatYield(param.value)}%<br/>`
          })
          return result
        }
      },
      legend: {
        data: Array.from(curves),
        top: 30
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: sortedTenors,
        name: '期限',
        nameLocation: 'middle',
        nameGap: 30
      },
      yAxis: {
        type: 'value',
        name: '收益率(%)',
        nameLocation: 'middle',
        nameGap: 50
      },
      dataZoom: [
        {
          type: 'slider',
          xAxisIndex: 0,
          start: 0,
          end: 100
        },
        {
          type: 'inside',
          xAxisIndex: 0
        }
      ],
      series: series
    }
  } else {
    // 显示选定日期的数据
    const dateData = chartData.value[selectedDate.value]
    const curves = Object.keys(dateData)
    const tenors = new Set<string>()
    curves.forEach(curve => {
      Object.keys(dateData[curve]).forEach(tenor => tenors.add(tenor))
    })
    const sortedTenors = Array.from(tenors).sort((a, b) => {
      const aNum = parseFloat(a) || 0
      const bNum = parseFloat(b) || 0
      return aNum - bNum
    })

    const series = curves.map(curveName => ({
      name: curveName,
      type: 'line',
      smooth: true,
      data: sortedTenors.map(tenor => dateData[curveName][tenor] || null),
      symbol: 'circle',
      symbolSize: 6
    }))

    chartOption.value = {
      title: {
        text: `收益率曲线 - ${selectedDate.value}`,
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          let result = `期限: ${params[0].axisValue}<br/>`
          params.forEach((param: any) => {
            result += `${param.seriesName}: ${formatYield(param.value)}%<br/>`
          })
          return result
        }
      },
      legend: {
        data: curves,
        top: 30
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: sortedTenors,
        name: '期限',
        nameLocation: 'middle',
        nameGap: 30
      },
      yAxis: {
        type: 'value',
        name: '收益率(%)',
        nameLocation: 'middle',
        nameGap: 50
      },
      dataZoom: [
        {
          type: 'slider',
          xAxisIndex: 0,
          start: 0,
          end: 100
        },
        {
          type: 'inside',
          xAxisIndex: 0
        }
      ],
      series: series
    }
  }
}

const updateSurfaceChart = () => {
  // 3D曲面图实现（简化版，使用热力图）
  const allDates = sortedDates.value
  if (allDates.length === 0) return

  const allTenors = new Set<string>()
  allDates.forEach(date => {
    Object.values(chartData.value[date] || {}).forEach(curve => {
      Object.keys(curve).forEach(tenor => allTenors.add(tenor))
    })
  })
  const sortedTenors = Array.from(allTenors).sort((a, b) => {
    const aNum = parseFloat(a) || 0
    const bNum = parseFloat(b) || 0
    return aNum - bNum
  })

  // 获取第一个曲线（或选定的曲线）
  const curveName = selectedCurveName.value || statistics.value?.curve_names[0] || 'default'
  
  const data: number[][] = []
  allDates.forEach((date, dateIdx) => {
    sortedTenors.forEach((tenor, tenorIdx) => {
      const yieldVal = chartData.value[date]?.[curveName]?.[tenor]
      if (yieldVal !== undefined) {
        data.push([tenorIdx, dateIdx, yieldVal])
      }
    })
  })

  chartOption.value = {
    title: {
      text: '收益率曲线热力图',
      left: 'center'
    },
    tooltip: {
      position: 'top',
      formatter: (params: any) => {
        const dateIdx = params.data[1]
        const tenorIdx = params.data[0]
        return `日期: ${allDates[dateIdx]}<br/>期限: ${sortedTenors[tenorIdx]}<br/>收益率: ${formatYield(params.data[2])}%`
      }
    },
    grid: {
      height: '50%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: sortedTenors,
      splitArea: {
        show: true
      },
      name: '期限'
    },
    yAxis: {
      type: 'category',
      data: allDates,
      splitArea: {
        show: true
      },
      name: '日期'
    },
    visualMap: {
      min: Math.min(...data.map(d => d[2])),
      max: Math.max(...data.map(d => d[2])),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffcc', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      }
    },
    series: [
      {
        name: '收益率',
        type: 'heatmap',
        data: data,
        label: {
          show: false
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
}

const formatYield = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return '-'
  return value.toFixed(4)
}

const getYieldClass = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return ''
  // 可以根据收益率高低添加不同的样式类
  return ''
}

const handleTableFilter = () => {
  tablePage.value = 1
}

const handleTableSizeChange = (size: number) => {
  tablePageSize.value = size
  tablePage.value = 1
}

const handleTablePageChange = (page: number) => {
  tablePage.value = page
}

const exportData = () => {
  if (!records.value || records.value.length === 0) {
    ElMessage.warning('没有数据可导出')
    return
  }

  // 转换为CSV格式
  const headers = ['日期', '曲线名称', '期限', '收益率(%)', '收益率类型']
  const rows = records.value.map(r => [
    r.date,
    r.curve_name || '',
    r.tenor,
    r.yield,
    r.yield_type || ''
  ])

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n')

  // 创建下载链接
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `收益率曲线_${dayjs().format('YYYY-MM-DD_HH-mm-ss')}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  ElMessage.success('导出成功')
}

// 监听图表类型和日期变化
watch([chartType, selectedDate], () => {
  if (chartData.value && Object.keys(chartData.value).length > 0) {
    updateChart()
  }
})

// 初始化：设置默认日期范围（最近30天）
onMounted(() => {
  const today = dayjs()
  end.value = today.format('YYYY-MM-DD')
  start.value = today.subtract(30, 'day').format('YYYY-MM-DD')
})
</script>

<style scoped>
.bonds-yield-curve {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.page-description {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
}

.query-card,
.stats-card,
.chart-card,
.table-card {
  margin-bottom: 16px;
}

.stats-card :deep(.el-card__body) {
  padding: 20px;
}

.curve-names {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.curve-names .label {
  font-size: 14px;
  color: #606266;
  margin-right: 8px;
}

.chart-container {
  min-height: 500px;
}

.chart-controls {
  display: flex;
  align-items: center;
}

.table-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .chart-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
