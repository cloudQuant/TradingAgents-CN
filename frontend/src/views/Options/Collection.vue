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
          <el-button @click="goBack" icon="ArrowLeft" round>返回列表</el-button>
          <el-button type="danger" @click="clearData" :loading="clearing" icon="Delete" round>清空数据</el-button>
          <el-button type="primary" @click="refreshData" :loading="refreshing" icon="Refresh" round>更新数据</el-button>
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
          <el-button @click="goBack" icon="ArrowLeft" round>返回列表</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- Fields Info -->
       <el-card shadow="hover" class="fields-card" v-if="collectionDef">
          <template #header>
            <div class="card-header">
              <span>字段说明</span>
            </div>
          </template>
          <div class="fields-list">
             <el-tag v-for="field in displayFields" :key="field" class="field-tag">{{ field }}</el-tag>
          </div>
       </el-card>

      <!-- Data Table -->
      <el-card shadow="hover" class="data-card" style="margin-top: 20px;">
        <template #header>
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
              <span>数据预览</span>
              <div class="card-actions">
                <el-button size="small" @click="loadData" icon="Refresh">刷新列表</el-button>
              </div>
            </div>
        </template>
        
        <el-table :data="rows" v-loading="loading" stripe style="width: 100%">
             <el-table-column v-for="field in displayFields" :key="field" :prop="field" :label="field" min-width="120" show-overflow-tooltip />
        </el-table>
        
        <div class="pagination-wrapper">
            <el-pagination
              background
              layout="prev, pager, next, jumper, total"
              :total="total"
              :page-size="pageSize"
              :current-page="currentPage"
              @current-change="handlePageChange"
            />
        </div>
      </el-card>
    </div>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="updateDialogVisible"
      title="更新数据"
      width="500px"
      @close="closeUpdateDialog"
    >
      <el-form label-width="100px">
        <el-form-item label="更新方式">
          <el-radio-group v-model="updateMethod">
            <el-radio label="file">文件导入</el-radio>
            <el-radio label="remote">远程同步</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item v-if="updateMethod === 'file'" label="选择文件">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 CSV, JSON 格式的文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <el-form-item v-if="updateMethod === 'remote'" label="远程源">
          <el-input v-model="remoteSource" placeholder="请输入远程数据源URL" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeUpdateDialog">关闭</el-button>
          <el-button type="primary" @click="startUpdate" :loading="updating">
            开始更新
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 数据概览对话框 -->
    <el-dialog
      v-model="overviewDialogVisible"
      title="数据概览"
      width="80%"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="集合名称">{{ collectionName }}</el-descriptions-item>
        <el-descriptions-item label="显示名称">{{ collectionDef?.display_name }}</el-descriptions-item>
        <el-descriptions-item label="数据总数">{{ stats.total_count || 0 }} 条</el-descriptions-item>
        <el-descriptions-item label="最后更新">
          {{ stats.latest_update ? formatTime(stats.latest_update) : '暂无数据' }}
        </el-descriptions-item>
        <el-descriptions-item label="字段数量">{{ collectionDef?.fields.length || 0 }} 个</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ collectionDef?.description }}
        </el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <el-button type="primary" @click="overviewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Box, ArrowLeft, Refresh, Delete, Document, Upload, UploadFilled } from '@element-plus/icons-vue'
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

const displayFields = computed(() => {
    if (!collectionDef.value) return []
    // Show all fields
    return collectionDef.value.fields
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
            page_size: pageSize.value
        })
        if (res.success) {
            rows.value = res.data.items
            total.value = res.data.total
            currentPage.value = res.data.page
            pageSize.value = res.data.page_size
        } else {
            ElMessage.error(res.error || '加载数据失败')
        }
    } catch (e: any) {
        ElMessage.error(e.message || '加载数据失败')
    } finally {
        loading.value = false
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

const handlePageChange = (page: number) => {
    currentPage.value = page
    loadData()
}

const goBack = () => {
    router.push('/options/collections')
}

onMounted(async () => {
    await loadCollectionInfo()
    if (collectionDef.value) {
        loadData()
    }
})
</script>

<style scoped>
.collection-page {
  padding: 20px;
}
.page-header {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 10px 0;
}
.title-icon {
  color: #409eff;
}
.collection-name-en {
  font-size: 0.8em;
  color: #909399;
  font-weight: normal;
}
.page-description {
  color: #606266;
  margin: 0;
}
.header-actions {
    display: flex;
    gap: 10px;
}
.fields-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.pagination-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}
</style>
