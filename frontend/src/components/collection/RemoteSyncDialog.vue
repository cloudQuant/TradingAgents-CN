<template>
  <el-dialog
    :model-value="visible"
    title="远程同步"
    width="700px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <!-- 同步模式选择 -->
    <el-tabs v-model="syncMode" type="border-card">
      <!-- 节点同步模式 -->
      <el-tab-pane label="节点同步" name="node">
        <el-form label-width="120px">
          <el-form-item label="同步方向">
            <el-radio-group v-model="nodeConfig.direction">
              <el-radio-button value="pull">
                <el-icon><Download /></el-icon> 从远程拉取（Pull）
              </el-radio-button>
              <el-radio-button value="push">
                <el-icon><Upload /></el-icon> 推送到远程（Push）
              </el-radio-button>
              <el-radio-button value="sync">
                <el-icon><Connection /></el-icon> 双向同步（Sync）
              </el-radio-button>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item :label="nodeConfig.direction === 'pull' ? '源节点' : '目标节点'">
            <el-select 
              v-model="nodeConfig.nodeId" 
              style="width: 100%"
              placeholder="请选择同步节点"
              :loading="loadingNodes"
            >
              <el-option
                v-for="node in nodes"
                :key="node.node_id"
                :label="`${node.name} (${node.url})`"
                :value="node.node_id"
              >
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <span>{{ node.name }}</span>
                  <el-tag size="small" :type="node.status === 'active' ? 'success' : 'info'">
                    {{ node.status === 'active' ? '在线' : '离线' }}
                  </el-tag>
                </div>
              </el-option>
            </el-select>
            <div style="margin-top: 8px;">
              <el-button size="small" @click="loadNodes" :loading="loadingNodes">
                <el-icon><Refresh /></el-icon> 刷新节点
              </el-button>
              <el-button size="small" type="primary" link @click="showNodeManager">
                <el-icon><Setting /></el-icon> 管理节点
              </el-button>
            </div>
          </el-form-item>
          
          <el-form-item label="同步策略">
            <el-radio-group v-model="nodeConfig.strategy">
              <el-radio value="incremental">增量同步</el-radio>
              <el-radio value="full">全量同步</el-radio>
            </el-radio-group>
            <div class="form-tip">
              <span v-if="nodeConfig.strategy === 'incremental'">只同步新增或更新的数据</span>
              <span v-else>同步全部数据（可能较慢）</span>
            </div>
          </el-form-item>
        </el-form>
        
        <!-- 节点同步进度 -->
        <div v-if="currentTask" class="sync-progress">
          <el-divider>同步进度</el-divider>
          <div class="progress-info">
            <p><strong>任务ID:</strong> {{ currentTask.task_id }}</p>
            <p><strong>状态:</strong> 
              <el-tag :type="getStatusType(currentTask.status)">{{ getStatusText(currentTask.status) }}</el-tag>
            </p>
            <el-progress 
              :percentage="getProgress(currentTask)" 
              :status="currentTask.status === 'completed' ? 'success' : currentTask.status === 'failed' ? 'exception' : ''"
            />
            <p class="progress-stats">
              已传输: {{ currentTask.stats.transferred }} / {{ currentTask.stats.total_records }} 条 |
              插入: {{ currentTask.stats.inserted }} | 更新: {{ currentTask.stats.updated }}
            </p>
          </div>
        </div>
      </el-tab-pane>
      
      <!-- 直连模式（保留原有功能） -->
      <el-tab-pane label="直连同步" name="direct">
        <el-form label-width="120px">
          <el-form-item label="远程主机">
            <el-input
              v-model="localConfig.host"
              placeholder="IP地址或URI，例如 192.168.1.10 或 mongodb://user:pwd@host:27017/db"
            />
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
            <el-input v-model="localConfig.username" placeholder="可选" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="localConfig.password" type="password" placeholder="可选" show-password />
          </el-form-item>
          <el-form-item label="认证数据库">
            <el-input v-model="localConfig.authSource" placeholder="通常为 admin" />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

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
        :disabled="!canSync"
      >
        <template v-if="syncMode === 'node'">
          {{
            nodeConfig.direction === 'pull'
              ? '开始从远程拉取（Pull）'
              : nodeConfig.direction === 'push'
                ? '开始推送到远程（Push）'
                : '开始双向同步（Sync）'
          }}
        </template>
        <template v-else>
          开始直连同步
        </template>
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { Download, Upload, Refresh, Setting } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { 
  getSyncNodes, 
  pullData, 
  pushData, 
  getSyncTask,
  type SyncNode,
  type SyncTask
} from '@/api/sync'

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
  (e: 'nodeSync', task: SyncTask): void
}>()

// 同步模式
const syncMode = ref<'node' | 'direct'>('node')

// 节点同步配置
const nodeConfig = reactive({
  direction: 'pull' as 'pull' | 'push' | 'sync',
  nodeId: '',
  strategy: 'incremental' as 'incremental' | 'full'
})

// 节点列表
const nodes = ref<SyncNode[]>([])
const loadingNodes = ref(false)

// 当前任务
const currentTask = ref<SyncTask | null>(null)
let taskPollTimer: number | null = null

// 直连配置
const localConfig = reactive<RemoteSyncConfig>({
  host: '',
  dbType: 'mongodb',
  batchSize: 1000,
  collection: '',
  username: '',
  password: '',
  authSource: 'admin',
})

// 是否可以同步
const canSync = computed(() => {
  if (syncMode.value === 'node') {
    return !!nodeConfig.nodeId
  }
  return !!localConfig.host
})

// 加载节点列表
const loadNodes = async () => {
  loadingNodes.value = true
  try {
    const res = await getSyncNodes()
    if (res.success && res.data) {
      nodes.value = res.data.filter(n => n.status === 'active')
    }
  } catch (e) {
    console.error('加载节点失败:', e)
  } finally {
    loadingNodes.value = false
  }
}

// 显示节点管理
const showNodeManager = () => {
  window.open('/sync/nodes', '_blank')
}

// 获取任务状态类型
const getStatusType = (status: string): 'success' | 'warning' | 'info' | 'danger' => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

// 获取任务状态文本
const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '等待中',
    running: '进行中',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

// 计算进度
const getProgress = (task: SyncTask) => {
  if (!task.stats.total_records) return 0
  return Math.round((task.stats.transferred / task.stats.total_records) * 100)
}

// 轮询任务状态
const pollTaskStatus = async (taskId: string) => {
  try {
    const res = await getSyncTask(taskId)
    if (res.success && res.data) {
      currentTask.value = res.data
      if (res.data.status === 'running' || res.data.status === 'pending') {
        taskPollTimer = window.setTimeout(() => pollTaskStatus(taskId), 1000)
      } else {
        if (res.data.status === 'completed') {
          ElMessage.success('同步完成')
        } else if (res.data.status === 'failed') {
          ElMessage.error(res.data.error_message || '同步失败')
        }
      }
    }
  } catch (e) {
    console.error('查询任务状态失败:', e)
  }
}

// 处理同步
const handleSync = async () => {
  if (syncMode.value === 'node') {
    // 节点同步模式
    try {
      let res
      if (nodeConfig.direction === 'pull') {
        res = await pullData({
          source_node: nodeConfig.nodeId,
          collection: props.collectionName,
          strategy: nodeConfig.strategy
        })
      } else if (nodeConfig.direction === 'push') {
        res = await pushData({
          target_node: nodeConfig.nodeId,
          collection: props.collectionName,
          strategy: nodeConfig.strategy
        })
      } else {
        // 双向同步：先从远程拉取，再推送到远程
        const pullRes = await pullData({
          source_node: nodeConfig.nodeId,
          collection: props.collectionName,
          strategy: nodeConfig.strategy
        })

        if (!pullRes.success || !pullRes.data) {
          ElMessage.error(pullRes.error || '启动拉取任务失败')
          return
        }

        const pushRes = await pushData({
          target_node: nodeConfig.nodeId,
          collection: props.collectionName,
          strategy: nodeConfig.strategy
        })

        if (!pushRes.success || !pushRes.data) {
          ElMessage.error(pushRes.error || '启动推送任务失败')
          return
        }

        // 使用最后一个任务作为当前跟踪的任务
        res = pushRes
      }
      
      if (res.success && res.data) {
        currentTask.value = res.data
        ElMessage.info(
          nodeConfig.direction === 'sync'
            ? '双向同步任务已启动'
            : '同步任务已启动'
        )
        emit('nodeSync', res.data)
        // 开始轮询状态
        pollTaskStatus(res.data.task_id)
      } else {
        ElMessage.error(res.error || '启动同步失败')
      }
    } catch (e: any) {
      ElMessage.error(e.message || '同步失败')
    }
  } else {
    // 直连模式
    const config = { ...localConfig }
    if (!config.collection) {
      config.collection = props.collectionName
    }
    emit('sync', config)
  }
}

// 监听初始配置
watch(() => props.initialConfig, (newConfig) => {
  if (newConfig) {
    Object.assign(localConfig, newConfig)
  }
}, { immediate: true })

// 监听可见性变化
watch(() => props.visible, (newVal) => {
  if (newVal) {
    loadNodes()
    if (props.initialConfig) {
      Object.assign(localConfig, props.initialConfig)
    }
  } else {
    // 关闭时清理
    if (taskPollTimer) {
      clearTimeout(taskPollTimer)
      taskPollTimer = null
    }
    currentTask.value = null
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

onMounted(() => {
  if (props.visible) {
    loadNodes()
  }
})
</script>

<style scoped>
.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.sync-progress {
  margin-top: 16px;
}

.progress-info p {
  margin: 8px 0;
}

.progress-stats {
  font-size: 12px;
  color: #606266;
}
</style>
