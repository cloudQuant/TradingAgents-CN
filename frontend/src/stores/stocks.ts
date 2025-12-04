/**
 * 股票模块状态管理
 *
 * 使用Pinia管理股票数据集合的状态
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { stocksApi } from '@/api/stocks'
import type { CollectionInfo, CollectionStatsResponse } from '@/api/stocks'

export const useStockStore = defineStore('stocks', () => {
  // ==================== 状态 ====================

  // 集合列表
  const collections = ref<CollectionInfo[]>([])
  const collectionsLoading = ref(false)
  const collectionsLastFetch = ref<Date | null>(null)

  // 集合统计信息缓存
  const collectionStats = ref<Record<string, CollectionStatsResponse>>({})
  const statsLoading = ref<Record<string, boolean>>({})

  // ==================== Getters ====================

  /**
   * 根据名称获取集合
   */
  const getCollectionByName = computed(() => {
    return (name: string) => collections.value.find((c) => c.name === name)
  })

  /**
   * 获取集合显示名称
   */
  const getCollectionDisplayName = computed(() => {
    return (name: string) => {
      const collection = collections.value.find((c) => c.name === name)
      return collection?.display_name || name
    }
  })

  /**
   * 按类别分组的集合
   */
  const collectionsByCategory = computed(() => {
    const groups: Record<string, CollectionInfo[]> = {}
    for (const collection of collections.value) {
      const category = collection.category || '默认'
      if (!groups[category]) {
        groups[category] = []
      }
      groups[category].push(collection)
    }
    return groups
  })

  // ==================== Actions ====================

  /**
   * 加载集合列表
   */
  async function loadCollections(force = false) {
    // 如果不是强制刷新，且缓存未过期（5分钟），则使用缓存
    if (
      !force &&
      collections.value.length > 0 &&
      collectionsLastFetch.value &&
      Date.now() - collectionsLastFetch.value.getTime() < 5 * 60 * 1000
    ) {
      return collections.value
    }

    collectionsLoading.value = true
    try {
      const response = await stocksApi.getCollections()
      if (response.success && response.data) {
        collections.value = response.data
        collectionsLastFetch.value = new Date()
      }
      return collections.value
    } catch (error) {
      console.error('加载股票集合列表失败:', error)
      throw error
    } finally {
      collectionsLoading.value = false
    }
  }

  /**
   * 加载集合统计信息
   */
  async function loadCollectionStats(collectionName: string, force = false) {
    // 如果不是强制刷新，且已有缓存，则使用缓存
    if (!force && collectionStats.value[collectionName]) {
      return collectionStats.value[collectionName]
    }

    statsLoading.value[collectionName] = true
    try {
      const response = await stocksApi.getCollectionStats(collectionName)
      if (response.success && response.data) {
        collectionStats.value[collectionName] = response.data
      }
      return collectionStats.value[collectionName]
    } catch (error) {
      console.error(`加载股票集合 ${collectionName} 统计信息失败:`, error)
      throw error
    } finally {
      statsLoading.value[collectionName] = false
    }
  }

  /**
   * 清除集合统计缓存
   */
  function clearCollectionStats(collectionName?: string) {
    if (collectionName) {
      delete collectionStats.value[collectionName]
    } else {
      collectionStats.value = {}
    }
  }

  /**
   * 清除所有缓存
   */
  function clearCache() {
    collections.value = []
    collectionsLastFetch.value = null
    collectionStats.value = {}
  }

  return {
    // 状态
    collections,
    collectionsLoading,
    collectionsLastFetch,
    collectionStats,
    statsLoading,

    // Getters
    getCollectionByName,
    getCollectionDisplayName,
    collectionsByCategory,

    // Actions
    loadCollections,
    loadCollectionStats,
    clearCollectionStats,
    clearCache,
  }
})
