<template>
  <div class="collections-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            股票数据集合
          </h1>
          <p class="page-description">
            查看和管理所有股票相关的数据集合，快速访问各类数据源
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
import { Box, Search } from '@element-plus/icons-vue'
import { ApiClient } from '@/api/request'

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
    const res = await ApiClient.get('/api/stocks/collections')
    // ApiClient返回 ApiResponse，所以访问 res.data
    if (Array.isArray(res.data)) {
      collections.value = res.data
    } else if (Array.isArray(res)) {
      // 兼容：如果直接返回数组
      collections.value = res
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
    name: 'StocksCollectionDetail',
    params: { collectionName },
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

<style lang="scss" scoped>
@use '@/styles/collections.scss' as *;
</style>
