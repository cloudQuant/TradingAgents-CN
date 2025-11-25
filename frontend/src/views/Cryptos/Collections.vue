<template>
  <div class="collections-view">
    <div class="page-header">
      <h1 class="page-title"><el-icon><Box /></el-icon> 数字货币数据集合</h1>
      <p class="page-description">管理和查看各类数字货币数据集合</p>
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
import { cryptosApi } from '@/api/cryptos'

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
    const res = await cryptosApi.getCollections()
    if (res.success) collections.value = res.data
  } catch (error) { console.error('加载数据集合失败:', error) }
})
</script>

<style lang="scss" scoped>
@use '@/styles/collections.scss' as *;
</style>
