/**
 * 期权模块 Pinia Store
 * 管理期权相关的全局状态
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { optionsApi } from '@/api/options'
import type {
  OptionsCollection,
  CollectionStats,
} from '@/types/options'

export const useOptionsStore = defineStore('options', () => {
  // ==================== 状态 ====================
  
  // 集合列表
  const collections = ref<OptionsCollection[]>([])
  const collectionsLoading = ref(false)
  const collectionsLastFetch = ref<Date | null>(null)
  
  // 集合统计信息缓存
  const collectionStats = ref<Record<string, CollectionStats>>({})
  const statsLoading = ref<Record<string, boolean>>({})
  
  // ==================== Getters ====================
  
  /**
   * 根据名称获取集合信息
   */
  const getCollectionByName = computed(() => {
    return (name: string): OptionsCollection | undefined => {
      return collections.value.find(c => c.name === name)
    }
  })
  
  /**
   * 获取集合的显示名称
   */
  const getCollectionDisplayName = computed(() => {
    return (name: string): string => {
      const collection = getCollectionByName.value(name)
      return collection?.display_name || name
    }
  })
  
  /**
   * 检查集合列表是否需要刷新（超过5分钟）
   */
  const shouldRefreshCollections = computed(() => {
    if (!collectionsLastFetch.value) return true
    const now = new Date()
    const diff = now.getTime() - collectionsLastFetch.value.getTime()
    return diff > 5 * 60 * 1000 // 5分钟
  })
  
  // ==================== Actions ====================
  
  /**
   * 加载集合列表
   */
  async function loadCollections(force = false): Promise<OptionsCollection[]> {
    // 如果已有数据且未过期，且不是强制刷新，直接返回
    if (collections.value.length > 0 && !shouldRefreshCollections.value && !force) {
      return collections.value
    }
    
    collectionsLoading.value = true
    try {
      const res = await optionsApi.getCollections()
      if (res.success && res.data) {
        collections.value = res.data as OptionsCollection[]
        collectionsLastFetch.value = new Date()
      }
    } catch (error) {
      console.error('加载期权集合列表失败:', error)
    } finally {
      collectionsLoading.value = false
    }
    
    return collections.value
  }
  
  /**
   * 加载集合统计信息
   */
  async function loadCollectionStats(
    collectionName: string,
    force = false
  ): Promise<CollectionStats | null> {
    // 如果已有缓存且不是强制刷新，直接返回
    if (collectionStats.value[collectionName] && !force) {
      return collectionStats.value[collectionName]
    }
    
    statsLoading.value[collectionName] = true
    try {
      const res = await optionsApi.getCollectionStats(collectionName)
      if (res.success && res.data) {
        collectionStats.value[collectionName] = res.data as CollectionStats
        return res.data as CollectionStats
      }
    } catch (error) {
      console.error('加载期权统计信息失败:', error)
    } finally {
      statsLoading.value[collectionName] = false
    }
    
    return null
  }
  
  /**
   * 清除集合统计缓存
   */
  function clearCollectionStats(collectionName?: string): void {
    if (collectionName) {
      delete collectionStats.value[collectionName]
      delete statsLoading.value[collectionName]
    } else {
      collectionStats.value = {}
      statsLoading.value = {}
    }
  }
  
  /**
   * 清除所有缓存
   */
  function clearCache(): void {
    collections.value = []
    collectionsLastFetch.value = null
    clearCollectionStats()
  }
  
  return {
    // 状态
    collections,
    collectionsLoading,
    collectionStats,
    statsLoading,
    
    // Getters
    getCollectionByName,
    getCollectionDisplayName,
    shouldRefreshCollections,
    
    // Actions
    loadCollections,
    loadCollectionStats,
    clearCollectionStats,
    clearCache,
  }
})
