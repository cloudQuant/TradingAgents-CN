<template>
  <div class="collections-view">
    <div class="page-header">
      <h1 class="page-title"><el-icon><Box /></el-icon> 外汇数据集合</h1>
      <p class="page-description">管理和查看各类外汇数据集合</p>
    </div>
    <div class="content">
      <el-card shadow="hover" class="search-card">
        <el-input v-model="searchKeyword" placeholder="搜索数据集合..." clearable size="large">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </el-card>
      <div class="collections-grid">
        <el-card v-for="collection in filteredCollections" :key="collection.name" shadow="hover" class="collection-card">
          <template #header>
            <div class="collection-header">
              <el-icon class="collection-icon"><Document /></el-icon>
              <span class="collection-name">{{ collection.display_name }}</span>
            </div>
          </template>
          <div><p class="collection-description">{{ collection.description }}</p></div>
        </el-card>
      </div>
      <el-empty v-if="filteredCollections.length === 0" description="暂无数据集合" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Box, Search, Document } from '@element-plus/icons-vue'
import { currenciesApi } from '@/api/currencies'

const searchKeyword = ref('')
const collections = ref<any[]>([])

const filteredCollections = computed(() => {
  if (!searchKeyword.value) return collections.value
  const keyword = searchKeyword.value.toLowerCase()
  return collections.value.filter(c => 
    c.name.toLowerCase().includes(keyword) || c.display_name.toLowerCase().includes(keyword)
  )
})

onMounted(async () => {
  try {
    const res = await currenciesApi.getCollections()
    if (res.success) collections.value = res.data
  } catch (error) { console.error('加载数据集合失败:', error) }
})
</script>

<style scoped>
.collections-view { padding: 16px; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 28px; font-weight: 600; color: #303133; margin: 0; display: flex; align-items: center; gap: 12px; }
.page-description { font-size: 14px; color: #909399; margin: 8px 0 0 0; }
.content { max-width: 1400px; }
.search-card { margin-bottom: 16px; }
.collections-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.collection-card { cursor: pointer; transition: transform 0.2s; }
.collection-card:hover { transform: translateY(-4px); }
.collection-header { display: flex; align-items: center; gap: 8px; }
.collection-icon { font-size: 20px; color: #409eff; }
.collection-name { font-size: 16px; font-weight: 600; }
.collection-description { font-size: 14px; color: #606266; margin: 0; min-height: 40px; }
</style>
