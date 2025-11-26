<template>
  <el-dialog
    :model-value="visible"
    title="远程同步"
    width="600px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form label-width="120px">
      <el-form-item label="远程主机">
        <el-input
          v-model="localConfig.host"
          placeholder="IP地址或URI，例如 192.168.1.10 或 mongodb://user:pwd@host:27017/db"
        />
      </el-form-item>
      <el-form-item label="数据库类型">
        <el-select v-model="localConfig.dbType" disabled style="width: 100%">
          <el-option label="MongoDB" value="mongodb" />
        </el-select>
      </el-form-item>
      <el-form-item label="批次大小">
        <el-select v-model="localConfig.batchSize" style="width: 100%">
          <el-option label="1000" :value="1000" />
          <el-option label="2000" :value="2000" />
          <el-option label="5000" :value="5000" />
          <el-option label="10000" :value="10000" />
        </el-select>
      </el-form-item>
      <el-form-item label="远程集合名">
        <el-input
          v-model="localConfig.collection"
          :placeholder="`默认使用当前集合名: ${collectionName}`"
        />
      </el-form-item>
      <el-form-item label="用户名">
        <el-input
          v-model="localConfig.username"
          placeholder="可选"
        />
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="localConfig.password"
          type="password"
          placeholder="可选"
          show-password
        />
      </el-form-item>
      <el-form-item label="认证数据库">
        <el-input
          v-model="localConfig.authSource"
          placeholder="通常为 admin"
        />
      </el-form-item>
    </el-form>

    <!-- 同步结果显示 -->
    <el-alert
      v-if="syncResult"
      :title="syncResultTitle"
      :type="syncResult.success ? 'success' : 'error'"
      style="margin-top: 16px"
      show-icon
    />
    
    <!-- 额外配置插槽 -->
    <slot name="extra-config"></slot>

    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button
        type="primary"
        @click="handleSync"
        :loading="syncing"
        :disabled="!localConfig.host"
      >
        开始同步
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'

export interface RemoteSyncConfig {
  host: string
  dbType: string
  batchSize: number
  collection: string
  username: string
  password: string
  authSource: string
}

export interface SyncResult {
  success: boolean
  synced_count?: number
  total_count?: number
  remote_total?: number
  synced?: number
  message?: string
  error?: string
}

const props = withDefaults(defineProps<{
  visible: boolean
  collectionName: string
  syncing?: boolean
  syncResult?: SyncResult | null
  initialConfig?: Partial<RemoteSyncConfig>
}>(), {
  syncing: false,
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'sync', config: RemoteSyncConfig): void
}>()

// 本地配置
const localConfig = reactive<RemoteSyncConfig>({
  host: '',
  dbType: 'mongodb',
  batchSize: 1000,
  collection: '',
  username: '',
  password: '',
  authSource: 'admin',
})

// 监听初始配置
watch(() => props.initialConfig, (newConfig) => {
  if (newConfig) {
    Object.assign(localConfig, newConfig)
  }
}, { immediate: true })

// 监听可见性变化，重置结果
watch(() => props.visible, (newVal) => {
  if (newVal && props.initialConfig) {
    Object.assign(localConfig, props.initialConfig)
  }
})

// 同步结果标题
const syncResultTitle = computed(() => {
  if (!props.syncResult) return ''
  if (props.syncResult.success) {
    const synced = props.syncResult.synced_count || props.syncResult.synced || 0
    const total = props.syncResult.total_count || props.syncResult.remote_total || 0
    return `同步完成: ${synced}/${total} 条`
  }
  return props.syncResult.error || props.syncResult.message || '同步失败'
})

const handleSync = () => {
  const config = { ...localConfig }
  if (!config.collection) {
    config.collection = props.collectionName
  }
  emit('sync', config)
}
</script>
