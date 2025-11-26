<template>
  <el-dialog
    :model-value="visible"
    title="数据概览"
    width="600px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <div style="padding: 10px;">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="集合名称" label-align="right">
          {{ collectionName }}
        </el-descriptions-item>
        <el-descriptions-item label="显示名称" label-align="right">
          {{ displayName || collectionName }}
        </el-descriptions-item>
        <el-descriptions-item label="数据总数" label-align="right">
          {{ formatNumber(totalCount) }} 条
        </el-descriptions-item>
        <el-descriptions-item label="字段数量" label-align="right">
          {{ fieldCount }} 个
        </el-descriptions-item>
        <el-descriptions-item label="最后更新" label-align="right" :span="2">
          {{ latestUpdate ? formatTime(latestUpdate) : '暂无数据' }}
        </el-descriptions-item>
        <el-descriptions-item label="数据来源" label-align="right" :span="2">
          <el-link 
            v-if="dataSource && dataSource !== '暂无'" 
            :href="dataSource" 
            target="_blank" 
            type="primary"
          >
            {{ dataSource }}
          </el-link>
          <span v-else>{{ dataSource || '暂无' }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="描述" label-align="right" :span="2">
          {{ description || `数据集合：${collectionName}` }}
        </el-descriptions-item>
        
        <!-- 额外统计信息插槽 -->
        <slot name="extra-stats"></slot>
      </el-descriptions>
      
      <!-- 额外内容插槽 -->
      <slot name="extra-content"></slot>
    </div>
    <template #footer>
      <el-button @click="$emit('update:visible', false)">关闭</el-button>
      <slot name="extra-footer-buttons"></slot>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  visible: boolean
  collectionName: string
  displayName?: string
  description?: string
  totalCount?: number
  fieldCount?: number
  latestUpdate?: string | Date
  dataSource?: string
}>(), {
  totalCount: 0,
  fieldCount: 0,
})

defineEmits<{
  (e: 'update:visible', value: boolean): void
}>()

// 格式化数字
const formatNumber = (num: number | undefined): string => {
  if (num === undefined || num === null) return '0'
  return num.toLocaleString()
}

// 格式化时间
const formatTime = (value: string | Date | undefined): string => {
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
</script>
