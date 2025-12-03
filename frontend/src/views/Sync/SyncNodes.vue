<template>
  <div class="sync-nodes-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>同步节点管理</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon> 添加节点
      </el-button>
    </div>

    <!-- 节点列表 -->
    <el-table :data="nodes" v-loading="loading" stripe>
      <el-table-column prop="node_id" label="节点ID" width="120" />
      <el-table-column prop="name" label="名称" width="150" />
      <el-table-column prop="url" label="地址" min-width="200" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '在线' : '离线' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
      <el-table-column prop="last_sync_at" label="上次同步" width="180">
        <template #default="{ row }">
          {{ row.last_sync_at ? formatDateTime(row.last_sync_at) : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="testNode(row)" :loading="testingNode === row.node_id">
            测试连接
          </el-button>
          <el-button size="small" type="primary" @click="editNode(row)">
            编辑
          </el-button>
          <el-button size="small" type="danger" @click="confirmDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑节点对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingNode ? '编辑节点' : '添加节点'"
      width="500px"
    >
      <el-form :model="nodeForm" label-width="100px">
        <el-form-item label="节点ID" v-if="!editingNode">
          <el-input v-model="nodeForm.node_id" placeholder="留空自动生成" />
        </el-form-item>
        <el-form-item label="名称" required>
          <el-input v-model="nodeForm.name" placeholder="例如: 主服务器" />
        </el-form-item>
        <el-form-item label="地址" required>
          <el-input v-model="nodeForm.url" placeholder="例如: https://api.example.com" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="nodeForm.api_key" type="password" show-password placeholder="可选，用于认证" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="nodeForm.description" type="textarea" :rows="2" placeholder="节点描述" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch 
            v-model="nodeForm.status" 
            active-value="active" 
            inactive-value="inactive"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveNode" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getSyncNodes,
  createSyncNode,
  updateSyncNode,
  deleteSyncNode,
  testSyncNode,
  type SyncNode
} from '@/api/sync'

const loading = ref(false)
const nodes = ref<SyncNode[]>([])
const dialogVisible = ref(false)
const editingNode = ref<SyncNode | null>(null)
const saving = ref(false)
const testingNode = ref('')

const nodeForm = reactive({
  node_id: '',
  name: '',
  url: '',
  api_key: '',
  description: '',
  status: 'active' as 'active' | 'inactive'
})

// 加载节点列表
const loadNodes = async () => {
  loading.value = true
  try {
    const res = await getSyncNodes()
    if (res.success && res.data) {
      nodes.value = res.data
    }
  } catch (e) {
    console.error('加载节点失败:', e)
  } finally {
    loading.value = false
  }
}

// 显示添加对话框
const showAddDialog = () => {
  editingNode.value = null
  Object.assign(nodeForm, {
    node_id: '',
    name: '',
    url: '',
    api_key: '',
    description: '',
    status: 'active'
  })
  dialogVisible.value = true
}

// 编辑节点
const editNode = (node: SyncNode) => {
  editingNode.value = node
  Object.assign(nodeForm, {
    node_id: node.node_id,
    name: node.name,
    url: node.url,
    api_key: '',
    description: node.description || '',
    status: node.status
  })
  dialogVisible.value = true
}

// 保存节点
const saveNode = async () => {
  if (!nodeForm.name || !nodeForm.url) {
    ElMessage.warning('请填写名称和地址')
    return
  }
  
  saving.value = true
  try {
    let res
    if (editingNode.value) {
      res = await updateSyncNode(editingNode.value.node_id, nodeForm)
    } else {
      res = await createSyncNode(nodeForm)
    }
    
    if (res.success) {
      ElMessage.success(editingNode.value ? '节点已更新' : '节点已添加')
      dialogVisible.value = false
      loadNodes()
    } else {
      ElMessage.error((res as any).error || '保存失败')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 测试节点连接
const testNode = async (node: SyncNode) => {
  testingNode.value = node.node_id
  try {
    const res = await testSyncNode(node.node_id)
    if (res.success && res.data) {
      if (res.data.success) {
        ElMessage.success(`连接成功！延迟: ${res.data.latency_ms}ms`)
      } else {
        ElMessage.error(res.data.error || '连接失败')
      }
    }
  } catch (e: any) {
    ElMessage.error(e.message || '测试失败')
  } finally {
    testingNode.value = ''
  }
}

// 确认删除
const confirmDelete = async (node: SyncNode) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除节点 "${node.name}" 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    
    const res = await deleteSyncNode(node.node_id)
    if (res.success) {
      ElMessage.success('节点已删除')
      loadNodes()
    } else {
      ElMessage.error((res as any).error || '删除失败')
    }
  } catch (e) {
    // 用户取消
  }
}

// 格式化日期时间
const formatDateTime = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadNodes()
})
</script>

<style scoped>
.sync-nodes-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}
</style>
