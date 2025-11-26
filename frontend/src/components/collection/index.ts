/**
 * 数据集合共享组件
 * 
 * 这些组件用于各个模块（Stocks、Bonds、Funds、Options、Currencies、Futures）的数据集合详情页面
 * 提供统一的数据表格展示、页面头部、对话框等功能
 */

export { default as CollectionDataTable } from './CollectionDataTable.vue'
export { default as CollectionPageHeader } from './CollectionPageHeader.vue'
export { default as CollectionOverviewDialog } from './CollectionOverviewDialog.vue'
export { default as FileImportDialog } from './FileImportDialog.vue'
export { default as RemoteSyncDialog } from './RemoteSyncDialog.vue'

// 类型导出
export type { FieldDefinition } from './CollectionDataTable.vue'
export type { RemoteSyncConfig, SyncResult } from './RemoteSyncDialog.vue'
