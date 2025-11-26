<template>
  <el-card shadow="hover" class="data-card">
    <template #header>
      <div class="card-header">
        <div style="display: flex; align-items: center;">
          <span>{{ title || '数据' }}</span>
          
          <!-- 字段说明 Popover -->
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
              <el-table-column prop="type" label="类型" width="120" v-if="showFieldType" />
              <el-table-column prop="description" label="说明" v-if="showFieldDescription" />
              <el-table-column prop="example" label="示例" show-overflow-tooltip>
                <template #default="{ row }">
                  <span v-if="row.example !== null && row.example !== undefined">{{ row.example }}</span>
                  <span v-else class="text-muted">-</span>
                </template>
              </el-table-column>
            </el-table>
          </el-popover>
          
          <!-- 导出按钮 (Excel 图标) -->
          <el-tooltip content="导出数据" placement="top">
            <span class="export-icon" @click="openExportDialog">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8.5 13h2l1.5 3 1.5-3h2l-2.5 4 2.5 4h-2l-1.5-3-1.5 3h-2l2.5-4-2.5-4z"/>
              </svg>
            </span>
          </el-tooltip>
        </div>
        <div class="header-actions">
          <!-- 额外的筛选插槽 -->
          <slot name="extra-filters"></slot>
          
          <!-- 搜索输入框 -->
          <el-input
            v-model="localFilterValue"
            :placeholder="searchPlaceholder"
            style="width: 200px; margin-right: 8px;"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <!-- 搜索字段选择器 -->
          <el-select
            v-if="showFieldFilter"
            v-model="localFilterField"
            placeholder="搜索字段"
            style="width: 150px; margin-right: 8px;"
            clearable
          >
            <el-option
              v-for="field in filterableFields"
              :key="getFieldProp(field)"
              :label="getFieldProp(field)"
              :value="getFieldProp(field)"
            />
          </el-select>
          
          <!-- 搜索按钮 -->
          <el-button size="small" :icon="Search" @click="handleSearch">搜索</el-button>
        </div>
      </div>
    </template>

    <!-- 表格前内容插槽 -->
    <slot name="before-table"></slot>

    <!-- 数据表格 -->
    <el-table
      :data="data"
      v-loading="loading"
      stripe
      border
      :style="{ width: '100%' }"
      :max-height="maxHeight"
      @sort-change="handleSortChange"
    >
      <el-table-column
        v-for="field in displayFields"
        :key="getFieldKey(field)"
        :prop="getFieldProp(field)"
        :label="getFieldLabel(field)"
        :min-width="getFieldMinWidth(field)"
        :width="getFieldWidth(field)"
        :fixed="getFieldFixed(field)"
        show-overflow-tooltip
        :sortable="sortable ? 'custom' : false"
      >
        <template #default="{ row }">
          <slot :name="`column-${getFieldProp(field)}`" :row="row" :field="field">
            <span v-if="row[getFieldProp(field)] !== null && row[getFieldProp(field)] !== undefined">
              {{ formatCellValue(row[getFieldProp(field)], field) }}
            </span>
            <span v-else class="text-muted">-</span>
          </slot>
        </template>
      </el-table-column>
    </el-table>

    <!-- 导出对话框 -->
    <el-dialog v-model="exportDialogVisible" title="导出数据" width="400px">
      <el-form label-width="100px">
        <el-form-item label="文件名">
          <el-input v-model="exportFileName" placeholder="请输入文件名" />
        </el-form-item>
        <el-form-item label="导出格式">
          <el-radio-group v-model="exportFormat">
            <el-radio label="csv">CSV</el-radio>
            <el-radio label="xlsx">Excel (XLSX)</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="导出范围">
          <el-radio-group v-model="exportScope">
            <el-radio label="current">当前页 ({{ data.length }} 条)</el-radio>
            <el-radio label="all">全部数据 ({{ total }} 条)</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="exportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleExport" :loading="exporting">
          {{ exporting ? '导出中...' : '导出' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 分页器 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="localPage"
        v-model:page-size="localPageSize"
        :page-sizes="pageSizes"
        :total="total"
        :layout="paginationLayout"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Search, QuestionFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// Props 定义
export interface FieldDefinition {
  name: string
  type?: string
  description?: string
  example?: any
  width?: number
  minWidth?: number
  fixed?: boolean | 'left' | 'right'
}

const props = withDefaults(defineProps<{
  // 数据相关
  data: any[]
  fields: (FieldDefinition | string)[]
  total: number
  loading?: boolean
  
  // 分页相关
  page?: number
  pageSize?: number
  pageSizes?: number[]
  paginationLayout?: string
  
  // 搜索相关
  filterValue?: string
  filterField?: string
  searchPlaceholder?: string
  showFieldFilter?: boolean
  
  // 显示相关
  title?: string
  maxHeight?: number | string
  sortable?: boolean
  showFieldType?: boolean
  showFieldDescription?: boolean
  
  // 格式化
  numberPrecision?: number
  
  // 导出相关
  fetchAllData?: () => Promise<any[]>  // 获取全部数据的回调函数
  collectionName?: string  // 集合名称，用于导出文件命名
}>(), {
  loading: false,
  page: 1,
  pageSize: 20,
  pageSizes: () => [20, 50, 100, 200],
  paginationLayout: 'total, sizes, prev, pager, next, jumper',
  filterValue: '',
  filterField: '',
  searchPlaceholder: '搜索...',
  showFieldFilter: true,
  title: '数据',
  maxHeight: 600,
  sortable: true,
  showFieldType: true,
  showFieldDescription: false,
  numberPrecision: 6,
})

// Emits 定义
const emit = defineEmits<{
  (e: 'update:page', value: number): void
  (e: 'update:pageSize', value: number): void
  (e: 'update:filterValue', value: string): void
  (e: 'update:filterField', value: string): void
  (e: 'search'): void
  (e: 'page-change', page: number): void
  (e: 'size-change', size: number): void
  (e: 'sort-change', params: { prop: string; order: 'ascending' | 'descending' | null }): void
}>()

// 导出相关状态
const exportDialogVisible = ref(false)
const exportFileName = ref('')
const exportFormat = ref<'csv' | 'xlsx'>('xlsx')
const exportScope = ref<'current' | 'all'>('current')
const exporting = ref(false)

// 生成默认导出文件名
const generateExportFileName = () => {
  const now = new Date()
  const timestamp = now.getFullYear().toString() +
    String(now.getMonth() + 1).padStart(2, '0') +
    String(now.getDate()).padStart(2, '0') + '_' +
    String(now.getHours()).padStart(2, '0') +
    String(now.getMinutes()).padStart(2, '0') +
    String(now.getSeconds()).padStart(2, '0')
  const baseName = props.collectionName || 'data_export'
  return `${baseName}_${timestamp}`
}

// 打开导出对话框时生成文件名
const openExportDialog = () => {
  exportFileName.value = generateExportFileName()
  exportDialogVisible.value = true
}

// 本地状态（双向绑定）
const localPage = ref(props.page)
const localPageSize = ref(props.pageSize)
const localFilterValue = ref(props.filterValue)
const localFilterField = ref(props.filterField)

// 监听 props 变化
watch(() => props.page, (val) => { localPage.value = val })
watch(() => props.pageSize, (val) => { localPageSize.value = val })
watch(() => props.filterValue, (val) => { localFilterValue.value = val })
watch(() => props.filterField, (val) => { localFilterField.value = val })

// 监听本地状态变化，同步到父组件
watch(localPage, (val) => { emit('update:page', val) })
watch(localPageSize, (val) => { emit('update:pageSize', val) })
watch(localFilterValue, (val) => { emit('update:filterValue', val) })
watch(localFilterField, (val) => { emit('update:filterField', val) })

// 计算属性：显示字段
const displayFields = computed(() => props.fields)

// 计算属性：可过滤字段
const filterableFields = computed(() => props.fields)

// 辅助方法：获取字段属性
const getFieldKey = (field: FieldDefinition | string): string => {
  return typeof field === 'string' ? field : field.name
}

const getFieldProp = (field: FieldDefinition | string): string => {
  return typeof field === 'string' ? field : field.name
}

const getFieldLabel = (field: FieldDefinition | string): string => {
  return typeof field === 'string' ? field : field.name
}

const getFieldMinWidth = (field: FieldDefinition | string): number => {
  if (typeof field === 'string') return 120
  return field.minWidth || 120
}

const getFieldWidth = (field: FieldDefinition | string): number | undefined => {
  if (typeof field === 'string') return undefined
  return field.width
}

const getFieldFixed = (field: FieldDefinition | string): boolean | 'left' | 'right' | undefined => {
  if (typeof field === 'string') return undefined
  return field.fixed
}

// 格式化单元格值
const formatCellValue = (value: any, _field?: FieldDefinition | string): string => {
  if (value === null || value === undefined) return '-'
  
  // 数字格式化
  if (typeof value === 'number') {
    // 整数不加小数位
    if (Number.isInteger(value)) {
      return value.toLocaleString()
    }
    // 浮点数保留指定精度
    return value.toFixed(props.numberPrecision)
  }
  
  return String(value)
}

// 事件处理
const handleSearch = () => {
  localPage.value = 1
  emit('search')
}

const handlePageChange = (page: number) => {
  emit('page-change', page)
}

const handleSizeChange = (size: number) => {
  localPage.value = 1
  emit('size-change', size)
}

const handleSortChange = (params: { prop: string; order: 'ascending' | 'descending' | null }) => {
  emit('sort-change', params)
}

// 导出功能
const handleExport = async () => {
  if (!exportFileName.value.trim()) {
    ElMessage.warning('请输入文件名')
    return
  }

  exporting.value = true
  
  try {
    let dataToExport: any[]
    
    // 根据导出范围获取数据
    if (exportScope.value === 'all' && props.fetchAllData) {
      // 导出全部数据
      ElMessage.info('正在获取全部数据，请稍候...')
      dataToExport = await props.fetchAllData()
    } else if (exportScope.value === 'all' && !props.fetchAllData) {
      // 没有提供获取全部数据的方法，使用当前页数据
      ElMessage.warning('未配置全部数据获取方法，将导出当前页数据')
      dataToExport = props.data
    } else {
      // 导出当前页数据
      dataToExport = props.data
    }
    
    if (dataToExport.length === 0) {
      ElMessage.warning('没有数据可导出')
      return
    }

    // 获取字段名列表
    const headers = props.fields.map(f => typeof f === 'string' ? f : f.name)
    
    if (exportFormat.value === 'csv') {
      exportToCSV(dataToExport, headers)
    } else {
      await exportToXLSX(dataToExport, headers)
    }
    
    ElMessage.success(`成功导出 ${dataToExport.length} 条数据`)
    exportDialogVisible.value = false
  } catch (error: any) {
    console.error('导出失败:', error)
    // 确保错误消息是纯字符串，避免 Vue 渲染问题
    const errorMsg = typeof error === 'string' ? error : (error?.message || '未知错误')
    ElMessage.error('导出失败: ' + String(errorMsg))
  } finally {
    exporting.value = false
  }
}

// 导出为 CSV
const exportToCSV = (data: any[], headers: string[]) => {
  // 构建 CSV 内容
  const csvRows: string[] = []
  
  // 添加表头
  csvRows.push(headers.map(h => `"${h}"`).join(','))
  
  // 添加数据行
  for (const row of data) {
    const values = headers.map(header => {
      const value = row[header]
      if (value === null || value === undefined) return ''
      // 处理包含逗号、引号或换行的值
      const strValue = String(value)
      if (strValue.includes(',') || strValue.includes('"') || strValue.includes('\n')) {
        return `"${strValue.replace(/"/g, '""')}"`
      }
      return strValue
    })
    csvRows.push(values.join(','))
  }
  
  const csvContent = '\uFEFF' + csvRows.join('\n') // 添加 BOM 以支持中文
  downloadFile(csvContent, `${exportFileName.value}.csv`, 'text/csv;charset=utf-8')
}

// 导出为 XLSX
const exportToXLSX = async (data: any[], headers: string[]) => {
  try {
    // 动态导入 xlsx 库
    const XLSX = await import('xlsx')
    
    // 确保表头都是有效字符串，避免数字或特殊字符
    const safeHeaders = headers.map((h, i) => {
      const str = String(h || '')
      // 如果表头是空的或者纯数字，添加前缀
      if (!str || /^\d+$/.test(str)) {
        return `col_${i}_${str}`
      }
      return str
    })
    
    // 构建二维数组数据（更稳定）
    const wsData: any[][] = [safeHeaders]
    for (const row of data) {
      const rowData = headers.map(header => {
        const value = row[header]
        if (value === null || value === undefined) return ''
        if (typeof value === 'object') return JSON.stringify(value)
        return value
      })
      wsData.push(rowData)
    }
    
    // 创建工作簿和工作表
    const ws = XLSX.utils.aoa_to_sheet(wsData)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')
    
    // 使用 write 生成 ArrayBuffer，避免 writeFile 的 DOM 操作问题
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
    
    // 手动创建 Blob 并下载
    const blob = new Blob([wbout], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${exportFileName.value}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } catch (error: any) {
    // 如果出错，回退到 CSV
    console.warn('Excel 导出失败，回退到 CSV 格式:', error)
    ElMessage.warning('Excel 导出失败，已自动切换为 CSV 格式')
    exportToCSV(data, headers)
  }
}

// 下载文件
const downloadFile = (content: string, fileName: string, mimeType: string) => {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
</script>

<style lang="scss" scoped>
.data-card {
  margin-top: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.text-muted {
  color: #909399;
}

.export-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-left: 8px;
  padding: 4px;
  cursor: pointer;
  color: #217346; // Excel 绿色
  border-radius: 4px;
  transition: all 0.2s;
  
  &:hover {
    background-color: #e6f4ea;
    color: #1a5d38;
  }
  
  svg {
    display: block;
  }
}
</style>
