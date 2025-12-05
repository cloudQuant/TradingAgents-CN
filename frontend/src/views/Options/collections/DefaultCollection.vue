<template>
  <div class="collection-page">
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :loading="loading"
      :updating="refreshing || importing || remoteSyncing"
      :clearing="clearing"
      @show-overview="overviewDialogVisible = true"
      @refresh="loadData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    />

    <div class="content">
      <CollectionDataTable
        :data="items"
        :fields="fields"
        :total="total"
        :loading="loading"
        v-model:page="page"
        v-model:page-size="pageSize"
        :sortable="true"
        :collection-name="collectionName"
        :export-all-data="exportAllData"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="loadData"
        @page-change="() => loadData()"
        @size-change="() => loadData()"
        @sort-change="handleSortChange"
      />
    </div>

    <el-dialog v-model="apiRefreshDialogVisible" title="API更新" width="650px" :close-on-click-modal="false" @open="loadUpdateConfig">
      <el-form label-width="100px" v-loading="!updateConfig">
        <el-form-item label="集合名称">
          <el-input :value="updateConfig?.display_name || collectionName" disabled />
        </el-form-item>
        <el-form-item label="更新说明" v-if="updateConfig?.update_description">
          <div style="color: #606266; font-size: 13px;">{{ updateConfig.update_description }}</div>
        </el-form-item>

        <template v-if="updateConfig?.single_update?.enabled">
          <el-card shadow="never" style="margin-bottom: 16px;">
            <template #header><span style="font-weight: 600;">更新</span></template>
            <div v-if="updateConfig.single_update.description" style="color: #909399; font-size: 12px; margin-bottom: 12px;">{{ updateConfig.single_update.description }}</div>
            <el-row :gutter="16" v-if="updateConfig.single_update.params?.length">
              <el-col v-for="param in updateConfig.single_update.params" :key="param.name" :span="updateConfig.single_update.params.length === 1 ? 24 : 12">
                <el-form-item :label="param.label" :required="param.required">
                  <el-input v-if="param.type === 'text'" v-model="singleUpdateParams[param.name]" :placeholder="param.placeholder" clearable />
                  <el-input-number v-else-if="param.type === 'number'" v-model="singleUpdateParams[param.name]" :min="param.min" :max="param.max" :step="param.step" style="width: 100%" />
                  <el-select v-else-if="param.type === 'select'" v-model="singleUpdateParams[param.name]" style="width: 100%">
                    <el-option v-for="(opt, idx) in param.options" :key="idx" :label="opt.label" :value="opt.value" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-button type="primary" @click="handleSingleUpdate" :loading="singleUpdating" :disabled="!canSingleUpdate || singleUpdating || batchUpdating" style="width: 100%;">更新</el-button>
          </el-card>
        </template>

        <template v-if="updateConfig?.batch_update?.enabled">
          <el-card shadow="never" style="margin-bottom: 16px;">
            <template #header><span style="font-weight: 600;">批量更新</span></template>
            <div v-if="updateConfig.batch_update.description" style="color: #909399; font-size: 12px; margin-bottom: 12px;">{{ updateConfig.batch_update.description }}</div>
            <el-form-item label="更新方式" style="margin-bottom: 16px;">
              <el-radio-group v-model="updateMode">
                <el-radio label="incremental">增量更新</el-radio>
                <el-radio label="full">全量更新</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-row :gutter="16" v-if="updateConfig.batch_update.params?.length">
              <el-col v-for="param in updateConfig.batch_update.params" :key="param.name" :span="updateConfig.batch_update.params.length === 1 ? 24 : 12">
                <el-form-item :label="param.label" :required="param.required">
                  <el-input v-if="param.type === 'text'" v-model="batchUpdateParams[param.name]" :placeholder="param.placeholder" clearable />
                  <el-input-number v-else-if="param.type === 'number'" v-model="batchUpdateParams[param.name]" :min="param.min" :max="param.max" :step="param.step" style="width: 100%" />
                  <el-select v-else-if="param.type === 'select'" v-model="batchUpdateParams[param.name]" style="width: 100%">
                    <el-option v-for="(opt, idx) in param.options" :key="idx" :label="opt.label" :value="opt.value" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-button type="primary" @click="handleBatchUpdate" :loading="batchUpdating" :disabled="!canBatchUpdate || singleUpdating || batchUpdating" style="width: 100%;">批量更新</el-button>
          </el-card>
        </template>

        <div v-if="singleUpdating || batchUpdating" style="margin-top: 16px;">
          <el-progress :percentage="progressPercentage" :status="progressStatus" :stroke-width="15" />
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">{{ progressMessage }}</p>
        </div>
      </el-form>
      <template #footer><el-button @click="apiRefreshDialogVisible = false">关闭</el-button></template>
    </el-dialog>

    <FileImportDialog ref="fileImportRef" v-model:visible="fileImportDialogVisible" :importing="importing" @import="handleImportFile" />
    <RemoteSyncDialog v-model:visible="remoteSyncDialogVisible" :collection-name="collectionName" :syncing="remoteSyncing" :sync-result="remoteSyncStats" @sync="handleRemoteSync" />
    <CollectionOverviewDialog v-model:visible="overviewDialogVisible" :collection-name="collectionName" :display-name="collectionInfo?.display_name" :description="collectionInfo?.description" :total-count="stats?.total_count" :field-count="fields.length" :latest-update="stats?.latest_date" :data-source="currentCollectionInfo.dataSource" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { CollectionPageHeader, CollectionDataTable, CollectionOverviewDialog, FileImportDialog, RemoteSyncDialog, useOptionsCollection } from '@/components/collection'
import { useOptionsStore } from '@/stores/options'

const {
  collectionName, loading, items, fields, page, pageSize, total, filterField, filterValue,
  sortBy: _sortBy, sortDir: _sortDir, stats, collectionInfo, apiRefreshDialogVisible,
  fileImportDialogVisible, remoteSyncDialogVisible, overviewDialogVisible, updateConfig,
  singleUpdateParams, batchUpdateParams, updateMode, singleUpdating, batchUpdating,
  canSingleUpdate, canBatchUpdate, progressPercentage, progressStatus, progressMessage,
  refreshing, importing, remoteSyncing, clearing, fileImportRef, remoteSyncStats,
  currentCollectionInfo, loadData, handleSortChange, exportAllData, handleUpdateCommand,
  loadUpdateConfig, handleSingleUpdate, handleBatchUpdate, handleImportFile, handleRemoteSync,
  handleClearData, cleanup,
} = useOptionsCollection()

const optionsStore = useOptionsStore()

onMounted(() => { optionsStore.loadCollections(); loadData() })
onUnmounted(() => { cleanup() })
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
