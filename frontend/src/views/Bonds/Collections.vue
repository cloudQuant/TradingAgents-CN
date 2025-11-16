<template>
  <div class="collections-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            数据集合
          </h1>
          <p class="page-description">
            查看和管理所有债券相关的数据集合，快速访问各类数据源
          </p>
        </div>
        <div class="header-stats">
          <el-statistic title="集合总数" :value="collections.length" />
        </div>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="hover">
      <el-row :gutter="16" align="middle">
        <el-col :span="12">
          <el-input
            v-model="searchText"
            placeholder="搜索集合名称或描述..."
            clearable
            size="large"
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="12">
          <div class="filter-info">
            <span class="collections-count">
              共 {{ filteredCollections.length }} 个集合
            </span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 数据集合列表 -->
    <el-card shadow="hover" class="collections-card">
      <div class="collections-list" v-loading="collectionsLoading">
        <el-empty
          v-if="filteredCollections.length === 0 && !collectionsLoading"
          description="暂无匹配的数据集合"
        />
        <el-row v-else :gutter="16">
          <el-col
            v-for="collection in filteredCollections"
            :key="collection.name"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-tooltip
              :content="collection.description"
              placement="top"
              effect="dark"
            >
              <div
                class="collection-item"
                @click="viewCollection(collection.name)"
              >
                <div class="collection-icon">
                  <el-icon><Box /></el-icon>
                </div>
                <div class="collection-info">
                  <div class="collection-name">{{ collection.display_name }}</div>
                  <div class="collection-desc">{{ collection.description }}</div>
                  <div class="collection-fields">
                    <el-tag
                      v-for="(field, idx) in collection.fields.slice(0, 3)"
                      :key="idx"
                      size="small"
                      type="info"
                      effect="plain"
                    >
                      {{ field }}
                    </el-tag>
                    <span v-if="collection.fields.length > 3" class="more-fields">
                      +{{ collection.fields.length - 3 }}
                    </span>
                  </div>
                </div>
              </div>
            </el-tooltip>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { bondsApi } from '@/api/bonds'
import { ElMessage } from 'element-plus'
import { Box, Search } from '@element-plus/icons-vue'

const router = useRouter()

// 数据集合
const collections = ref<Array<{
  name: string
  display_name: string
  description: string
  route: string
  fields: string[]
}>>([])

const collectionsLoading = ref(false)
const searchText = ref('')

// 过滤后的集合列表
const filteredCollections = computed(() => {
  if (!searchText.value) {
    return collections.value
  }
  
  const searchLower = searchText.value.toLowerCase()
  return collections.value.filter(collection => {
    return collection.display_name.toLowerCase().includes(searchLower) ||
           collection.description.toLowerCase().includes(searchLower) ||
           collection.name.toLowerCase().includes(searchLower)
  })
})

// 加载数据集合列表
const loadCollections = async () => {
  collectionsLoading.value = true
  try {
    const res = await bondsApi.getCollections()
    if (res.success && res.data) {
      collections.value = res.data
    } else {
      ElMessage.error('加载数据集合失败')
    }
  } catch (e) {
    console.error('加载数据集合失败:', e)
    ElMessage.error('加载数据集合失败')
  } finally {
    collectionsLoading.value = false
  }
}

// 查看集合详情
const viewCollection = (collectionName: string) => {
  router.push({
    name: 'BondCollection',
    params: { collectionName }
  })
}

// 搜索处理
const handleSearch = () => {
  // 搜索逻辑已由computed处理
}

onMounted(() => {
  loadCollections()
})
</script>

<style scoped lang="scss">
.collections-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 24px;
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  }
  
  .title-section {
    flex: 1;
  }
  
  .page-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 28px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: white;
    
    .title-icon {
      font-size: 32px;
    }
  }
  
  .page-description {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
  }
  
  .header-stats {
    :deep(.el-statistic__head) {
      color: rgba(255, 255, 255, 0.8);
      font-size: 14px;
    }
    
    :deep(.el-statistic__content) {
      color: white;
      font-size: 32px;
      font-weight: 700;
    }
  }
}

.search-card {
  margin-bottom: 20px;
  
  .filter-info {
    text-align: right;
    
    .collections-count {
      font-size: 14px;
      color: #909399;
      font-weight: 500;
    }
  }
}

.collections-card {
  .collections-list {
    min-height: 400px;
  }
  
  .el-row {
    margin-left: -8px !important;
    margin-right: -8px !important;
  }
  
  .el-col {
    padding-left: 8px !important;
    padding-right: 8px !important;
    margin-bottom: 16px;
  }
}

.collection-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  background: #fff;
  
  &:hover {
    border-color: #409eff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
}

.collection-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
  
  .el-icon {
    font-size: 20px;
  }
}

.collection-info {
  flex: 1;
  min-width: 0;
}

.collection-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.collection-desc {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.collection-fields {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  
  .el-tag {
    margin: 0;
  }
  
  .more-fields {
    font-size: 12px;
    color: #909399;
    margin-left: 4px;
  }
}

@media (max-width: 768px) {
  .page-header {
    .header-content {
      flex-direction: column;
      gap: 16px;
    }
    
    .header-stats {
      width: 100%;
    }
  }
}
</style>
