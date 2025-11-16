<template>
  <div class="collections-view">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            期货数据集合
          </h1>
          <p class="page-description">管理和查看各类期货数据集合</p>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 搜索框 -->
      <el-card shadow="hover" class="search-card">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索数据集合..."
          clearable
          size="large"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </el-card>

      <!-- 集合列表 -->
      <div class="collections-grid">
        <el-card
          v-for="collection in filteredCollections"
          :key="collection.name"
          shadow="hover"
          class="collection-card"
          @click="goToCollection(collection.name)"
        >
          <template #header>
            <div class="collection-header">
              <el-icon class="collection-icon"><Document /></el-icon>
              <span class="collection-name">{{ collection.display_name }}</span>
            </div>
          </template>
          <div class="collection-body">
            <p class="collection-description">{{ collection.description }}</p>
            <div class="collection-fields">
              <el-tag
                v-for="field in collection.fields.slice(0, 4)"
                :key="field"
                size="small"
                style="margin-right: 4px; margin-bottom: 4px;"
              >
                {{ field }}
              </el-tag>
              <el-tag v-if="collection.fields.length > 4" size="small">
                +{{ collection.fields.length - 4 }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 空状态 -->
      <el-empty
        v-if="filteredCollections.length === 0"
        description="暂无数据集合"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Box, Search, Document } from '@element-plus/icons-vue'
import { futuresApi } from '@/api/futures'
import { ElMessage } from 'element-plus'

const router = useRouter()
const searchKeyword = ref('')
const collections = ref<any[]>([])
const loading = ref(false)

const filteredCollections = computed(() => {
  if (!searchKeyword.value) {
    return collections.value
  }
  const keyword = searchKeyword.value.toLowerCase()
  return collections.value.filter(
    (c) =>
      c.name.toLowerCase().includes(keyword) ||
      c.display_name.toLowerCase().includes(keyword) ||
      c.description.toLowerCase().includes(keyword)
  )
})

const loadCollections = async () => {
  loading.value = true
  try {
    const res = await futuresApi.getCollections()
    if (res.success) {
      collections.value = res.data
    } else {
      ElMessage.error(res.error || '加载数据集合失败')
    }
  } catch (error: any) {
    console.error('加载数据集合失败:', error)
    ElMessage.error(error.message || '加载数据集合失败')
  } finally {
    loading.value = false
  }
}

const goToCollection = (collectionName: string) => {
  router.push(`/futures/collections/${collectionName}`)
}

onMounted(() => {
  loadCollections()
})
</script>

<style scoped>
.collections-view {
  padding: 16px;
}

.page-header {
  margin-bottom: 24px;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 32px;
  color: #409eff;
}

.page-description {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.content {
  max-width: 1400px;
}

.search-card {
  margin-bottom: 16px;
}

.collections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.collection-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.collection-card:hover {
  transform: translateY(-4px);
}

.collection-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.collection-icon {
  font-size: 20px;
  color: #409eff;
}

.collection-name {
  font-size: 16px;
  font-weight: 600;
}

.collection-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.collection-description {
  font-size: 14px;
  color: #606266;
  margin: 0;
  min-height: 40px;
}

.collection-fields {
  display: flex;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .collections-grid {
    grid-template-columns: 1fr;
  }
}
</style>
