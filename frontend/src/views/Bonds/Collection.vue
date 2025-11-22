<template>
  <div class="collection-view">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionInfo?.display_name || collectionName }}
          </h1>
          <p class="page-description">{{ collectionInfo?.description || '' }}</p>
        </div>
        <div class="header-actions">
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
          <el-button :icon="Download" type="primary" @click="showRefreshDialog" :loading="refreshing">更新数据</el-button>
          <el-button :icon="Delete" type="danger" @click="handleClearData" :loading="clearing">清空数据</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 统计数据卡片 -->
      <el-card shadow="hover" class="stats-card" v-if="stats">
        <template #header>
          <div class="card-header">数据统计</div>
        </template>
        <el-row :gutter="16">
          <el-col :xs="12" :sm="8" :md="6" :lg="4">
            <el-statistic title="总记录数" :value="stats.total_count">
              <template #prefix>
                <el-icon><Document /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4" v-if="stats.earliest_date">
            <el-statistic title="最早日期" :value="stats.earliest_date">
              <template #prefix>
                <el-icon><Calendar /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4" v-if="stats.latest_date">
            <el-statistic title="最新日期" :value="stats.latest_date">
              <template #prefix>
                <el-icon><Calendar /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="12" v-if="stats.category_stats && stats.category_stats.length > 0">
            <div class="category-stats">
              <span class="stats-label">类别分布：</span>
              <el-tag
                v-for="cat in stats.category_stats"
                :key="cat.category"
                size="small"
                style="margin-right: 8px; margin-bottom: 4px;"
              >
                {{ cat.category }}: {{ cat.count }}
              </el-tag>
            </div>
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="12" v-if="stats.exchange_stats && stats.exchange_stats.length > 0">
            <div class="exchange-stats">
              <span class="stats-label">交易所分布：</span>
              <el-tag
                v-for="ex in stats.exchange_stats"
                :key="ex.exchange"
                size="small"
                style="margin-right: 8px; margin-bottom: 4px;"
              >
                {{ ex.exchange }}: {{ ex.count }}
              </el-tag>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 字段说明 -->
      <el-card shadow="hover" class="fields-card" v-if="fields && fields.length > 0">
        <template #header>
          <div class="card-header">字段说明</div>
        </template>
        <el-table :data="fields" stripe border size="small" style="width: 100%">
          <el-table-column prop="name" label="字段名" width="200" />
          <el-table-column prop="type" label="类型" width="120" />
          <el-table-column prop="example" label="示例" show-overflow-tooltip>
            <template #default="{ row }">
              <span v-if="row.example" class="example-text">{{ row.example }}</span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 数据列表 -->
      <el-card shadow="hover" class="data-card">
        <template #header>
          <div class="card-header">
            <span>数据列表</span>
            <div class="header-actions">
              <el-input
                v-model="filterValue"
                placeholder="搜索..."
                style="width: 200px; margin-right: 8px;"
                clearable
                @clear="handleFilter"
                @keyup.enter="handleFilter"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-select
                v-model="filterField"
                placeholder="搜索字段"
                style="width: 150px; margin-right: 8px;"
                clearable
              >
                <el-option
                  v-for="field in fields"
                  :key="field.name"
                  :label="field.name"
                  :value="field.name"
                />
              </el-select>
              <el-button size="small" :icon="Search" @click="handleFilter">搜索</el-button>
            </div>
          </div>
        </template>
        
        <el-table
          :data="items"
          v-loading="loading"
          stripe
          border
          style="width: 100%"
          max-height="600"
          @sort-change="handleSortChange"
        >
          <el-table-column
            v-for="field in fields"
            :key="field.name"
            :prop="field.name"
            :label="field.name"
            :min-width="120"
            show-overflow-tooltip
            sortable="custom"
          >
            <template #default="{ row }">
              <span v-if="row[field.name] !== null && row[field.name] !== undefined">
                {{ formatValue(row[field.name]) }}
              </span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>

      <!-- 年度发行量柱状图，仅 bond_info_cm 显示 -->
      <el-card
        v-if="collectionName === 'bond_info_cm' && issuanceChartOption"
        shadow="hover"
        class="issuance-card"
      >
        <template #header>
          <div class="card-header">
            <span>年度债券发行量</span>
            <small class="text-muted">数据来源：bond_info_cm · 发行日期</small>
          </div>
        </template>
        <div class="chart-wrapper">
          <v-chart
            :option="issuanceChartOption"
            :autoresize="true"
            style="height: 360px; width: 100%"
            v-loading="issuanceLoading"
          />
        </div>
      </el-card>

      <!-- 债券类型与最新债项评级分布饼图，仅 bond_info_cm 显示 -->
      <el-card
        v-if="collectionName === 'bond_info_cm' && (bondTypePieOption || gradePieOption)"
        shadow="hover"
        class="distribution-card"
      >
        <template #header>
          <div class="card-header">
            <span>债券类型与评级分布</span>
          </div>
        </template>
        <div class="distribution-row">
          <div class="chart-wrapper-small" v-if="bondTypePieOption">
            <v-chart
              :option="bondTypePieOption"
              :autoresize="true"
              style="height: 320px; width: 100%"
            />
          </div>
          <div class="chart-wrapper-small" v-if="gradePieOption">
            <v-chart
              :option="gradePieOption"
              :autoresize="true"
              style="height: 320px; width: 100%"
            />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="refreshDialogVisible"
      title="更新数据"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form label-width="100px">
        <el-form-item label="集合名称">
          <el-input :value="collectionInfo?.display_name || collectionName" disabled />
        </el-form-item>
        
        <el-alert
          v-if="needsDateRange"
          title="此集合需要指定日期范围"
          type="info"
          :closable="false"
          style="margin-bottom: 16px;"
        />
        
        <el-alert
          v-if="needsSingleDate"
          title="此集合需要指定单个日期"
          type="info"
          :closable="false"
          style="margin-bottom: 16px;"
        />
        
        <!-- 进度显示 -->
        <div v-if="refreshing" style="margin-top: 20px;">
          <el-progress 
            :percentage="progressPercentage" 
            :status="progressStatus"
            :stroke-width="15"
          />
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">
            {{ progressMessage }}
          </p>
        </div>
        
        <!-- 批量更新进度显示 -->
        <div v-if="batchRefreshing" style="margin-top: 20px;">
          <el-alert
            title="批量更新进行中"
            type="info"
            :closable="false"
            style="margin-bottom: 16px;"
          >
            <template #default>
              <div style="font-size: 12px;">
                正在使用 {{ sanitizedBatchConcurrency }} 个并发线程，任务启动前延迟 {{ sanitizedBatchDelaySeconds }} 秒，请耐心等待...
              </div>
            </template>
          </el-alert>
          <el-progress 
            :percentage="Math.round((batchProgress.completed / batchProgress.total) * 100)" 
            :status="batchProgress.failed > 0 ? 'warning' : ''"
            :stroke-width="15"
          >
            <template #default="{ percentage }">
              <span style="font-size: 14px;">{{ percentage }}%</span>
            </template>
          </el-progress>
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">
            已完成: {{ batchProgress.completed }} / {{ batchProgress.total }} 个年份
            <span v-if="batchProgress.failed > 0" style="color: #E6A23C;">（失败: {{ batchProgress.failed }}）</span>
          </p>
        </div>
        
        <el-form-item v-if="needsDateRange" label="开始日期">
          <el-date-picker
            v-model="refreshStartDate"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item v-if="collectionName === 'bond_info_cm' || collectionName === 'bond_basic_info'" label="文件导入">
          <div style="width: 100%">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              multiple
              :on-change="handleImportFileChange"
              :on-remove="handleImportFileRemove"
              accept=".csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              drag
            >
              <div class="el-upload__text">
                拖拽文件到此处或<em>点击选择文件</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  <span v-if="collectionName === 'bond_info_cm'">支持 CSV 或 Excel 文件，列结构需与债券信息查询结果一致</span>
                  <span v-else-if="collectionName === 'bond_basic_info'">支持 CSV 或 Excel 文件，列结构需包含债券代码、债券简称等字段</span>
                </div>
              </template>
            </el-upload>
            <el-button
              style="margin-top: 8px;"
              size="small"
              type="primary"
              @click="handleImportFile"
              :loading="importing"
              :disabled="!importFiles.length || importing"
            >
              导入文件
            </el-button>
          </div>
        </el-form-item>

        <el-form-item v-if="collectionName === 'bond_info_cm' || collectionName === 'bond_basic_info'" label="远程同步">
          <div style="width: 100%">
            <el-row :gutter="8">
              <el-col :span="24">
                <el-input
                  v-model="remoteSyncHost"
                  placeholder="远程 MongoDB IP 或 URI，例如 192.168.1.10 或 mongodb://user:pwd@host:27017/db"
                />
              </el-col>
              <el-col :span="12" style="margin-top: 8px;">
                <el-select v-model="remoteSyncDbType" disabled style="width: 100%">
                  <el-option label="MongoDB" value="mongodb" />
                </el-select>
              </el-col>
              <el-col :span="12" style="margin-top: 8px;">
                <el-select v-model="remoteSyncBatchSize" style="width: 100%">
                  <el-option label="1000" :value="1000" />
                  <el-option label="2000" :value="2000" />
                  <el-option label="5000" :value="5000" />
                  <el-option label="10000" :value="10000" />
                </el-select>
              </el-col>
            </el-row>
            <el-row :gutter="8" style="margin-top: 8px;">
              <el-col :span="12">
                <el-input
                  v-model="remoteSyncCollection"
                  :placeholder="collectionName === 'bond_info_cm' ? '远程集合名称，默认 bond_info_cm' : '远程集合名称，默认 bond_basic_info'"
                />
              </el-col>
              <el-col :span="12">
                <el-input
                  v-model="remoteSyncUsername"
                  placeholder="远程用户名（可选）"
                />
              </el-col>
            </el-row>
            <el-row :gutter="8" style="margin-top: 8px;">
              <el-col :span="24">
                <el-input
                  v-model="remoteSyncAuthSource"
                  placeholder="认证库（authSource），通常为创建该用户时所在的数据库，例如 admin 或 tradingagents"
                />
              </el-col>
            </el-row>
            <el-row :gutter="8" style="margin-top: 8px;">
              <el-col :span="24">
                <el-input
                  v-model="remoteSyncPassword"
                  type="password"
                  show-password
                  placeholder="远程密码（可选）"
                />
              </el-col>
            </el-row>
            <el-button
              style="margin-top: 8px;"
              size="small"
              type="primary"
              @click="handleRemoteSync"
              :loading="remoteSyncing"
              :disabled="!remoteSyncHost || remoteSyncing"
            >
              远程同步
            </el-button>
            <div
              v-if="remoteSyncStats"
              style="margin-top: 4px; font-size: 12px; color: #606266;"
            >
              最近一次同步：远程共 {{ remoteSyncStats.remote_total }} 条，已写入/更新
              {{ remoteSyncStats.synced }} 条
            </div>
          </div>
        </el-form-item>
        
        <el-form-item v-if="needsDateRange" label="结束日期">
          <el-date-picker
            v-model="refreshEndDate"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item v-if="needsSingleDate" label="指定日期">
          <el-date-picker
            v-model="refreshStartDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <!-- bond_basic_info 批量更新和增量更新参数 -->
        <template v-if="collectionName === 'bond_basic_info'">
          <section class="batch-config-section">
            <div class="batch-config-header">
              <div>
                <p class="batch-config-title">债券基础信息更新</p>
                <p class="batch-config-subtitle">基于bond_info_cm数据，批量或增量更新债券详细信息</p>
              </div>
              <el-tag size="small" type="warning" effect="plain">基础信息</el-tag>
            </div>
            
            <el-alert
              title="更新模式说明"
              type="info"
              :closable="false"
              style="margin-bottom: 16px;"
            >
              <template #default>
                <div style="font-size: 12px; line-height: 1.6;">
                  <p><strong>批量更新：</strong>从bond_info_cm查询所有债券简称，获取详细信息更新到bond_info_detail_cm</p>
                  <p><strong>增量更新：</strong>只更新bond_info_cm中存在但bond_info_detail_cm中缺失的债券信息</p>
                </div>
              </template>
            </el-alert>

            <div class="batch-config-grid">
              <div class="batch-config-field">
                <label class="batch-field-label">批次大小</label>
                <el-input-number
                  v-model="bondBasicBatchSize"
                  :min="100"
                  :max="5000"
                  :step="100"
                  controls-position="right"
                  style="width: 100%;"
                />
                <p class="batch-config-note">每批处理的债券数量，建议1000-2000</p>
              </div>
              <div class="batch-config-field">
                <label class="batch-field-label">并发线程数</label>
                <el-input-number
                  v-model="bondBasicConcurrentThreads"
                  :min="1"
                  :max="10"
                  :step="1"
                  controls-position="right"
                  style="width: 100%;"
                />
                <p class="batch-config-note">同时运行的线程数，建议3-5个</p>
              </div>
              <div class="batch-config-field">
                <label class="batch-field-label">保存间隔</label>
                <el-input-number
                  v-model="bondBasicSaveInterval"
                  :min="500"
                  :max="2000"
                  :step="100"
                  controls-position="right"
                  style="width: 100%;"
                />
                <p class="batch-config-note">每获取多少条数据保存一次</p>
              </div>
            </div>
            
            <div class="batch-config-actions">
              <el-button 
                type="primary"
                size="small"
                @click="startBondBasicBatchUpdate"
                :loading="bondBasicBatchUpdating"
                :disabled="refreshing || bondBasicBatchUpdating || bondBasicIncrementalUpdating"
              >
                {{ bondBasicBatchUpdating ? '批量更新中...' : '批量更新' }}
              </el-button>
              
              <el-button 
                type="success"
                size="small"
                @click="startBondBasicIncrementalUpdate"
                :loading="bondBasicIncrementalUpdating"
                :disabled="refreshing || bondBasicBatchUpdating || bondBasicIncrementalUpdating"
              >
                {{ bondBasicIncrementalUpdating ? '增量更新中...' : '增量更新' }}
              </el-button>
              
              <el-button 
                size="small"
                @click="getBondBasicUpdateStatistics"
                :loading="loadingBondBasicStats"
              >
                {{ loadingBondBasicStats ? '查询中...' : '查询统计' }}
              </el-button>
            </div>
            
            <!-- 统计信息显示 -->
            <div v-if="bondBasicStats" class="stats-display">
              <el-descriptions :column="2" size="small" border>
                <el-descriptions-item label="基础信息总数">{{ bondBasicStats.bond_info_cm_count || 0 }}</el-descriptions-item>
                <el-descriptions-item label="详细信息总数">{{ bondBasicStats.bond_info_detail_cm_count || 0 }}</el-descriptions-item>
                <el-descriptions-item label="覆盖率">{{ bondBasicStats.coverage_rate || 0 }}%</el-descriptions-item>
                <el-descriptions-item label="缺失详情数">{{ bondBasicStats.missing_detail_count || 0 }}</el-descriptions-item>
              </el-descriptions>
            </div>
            
            <!-- 进度显示 -->
            <div v-if="bondBasicProgress.show" class="bond-basic-progress">
              <el-progress
                :percentage="bondBasicProgress.percentage"
                :status="bondBasicProgress.status"
                :stroke-width="15"
              />
              <p class="progress-message">{{ bondBasicProgress.message }}</p>
              <div v-if="bondBasicProgress.details" class="progress-details">
                <el-descriptions :column="2" size="small">
                  <el-descriptions-item label="总数量">{{ bondBasicProgress.details.total || 0 }}</el-descriptions-item>
                  <el-descriptions-item label="已处理">{{ bondBasicProgress.details.processed || 0 }}</el-descriptions-item>
                  <el-descriptions-item label="已更新">{{ bondBasicProgress.details.updated || 0 }}</el-descriptions-item>
                  <el-descriptions-item label="错误数">{{ bondBasicProgress.details.errors || 0 }}</el-descriptions-item>
                </el-descriptions>
              </div>
            </div>
            
            <el-divider class="batch-config-divider" />
          </section>
        </template>

        <!-- bond_info_cm 查询参数 -->
        <template v-if="needsBondParams">
          <section class="batch-config-section">
            <div class="batch-config-header">
              <div>
                <p class="batch-config-title">批量更新参数</p>
                <p class="batch-config-subtitle">按年份批量刷新数据，适用于大范围同步</p>
              </div>
              <el-tag size="small" type="success" effect="plain">批量工具</el-tag>
            </div>
            <div class="batch-config-grid">
              <div class="batch-config-field">
                <label class="batch-field-label">并发线程数</label>
                <el-input-number
                  v-model="batchConcurrency"
                  :min="1"
                  :max="20"
                  :step="1"
                  controls-position="right"
                  style="width: 100%;"
                />
              </div>
              <div class="batch-config-field">
                <label class="batch-field-label">启动延迟 (秒)</label>
                <el-input-number
                  v-model="batchDelaySeconds"
                  :min="0"
                  :max="60"
                  :step="1"
                  controls-position="right"
                  style="width: 100%;"
                />
              </div>
              <div class="batch-config-field batch-config-action">
                <label class="batch-field-label">批量操作</label>
                <el-button 
                  type="success"
                  size="small"
                  class="batch-update-btn"
                  @click="refreshAllYears"
                  :loading="batchRefreshing"
                  :disabled="refreshing || batchRefreshing"
                >
                  {{ batchRefreshing ? `批量更新中 (${batchProgress.completed}/${batchProgress.total})...` : '更新全部年份' }}
                </el-button>
                <p class="batch-config-note">根据并发与延迟策略逐年执行，请确保系统资源充足</p>
              </div>
            </div>
            <el-divider class="batch-config-divider" />
          </section>

          <el-alert
            title="查询参数设置"
            type="info"
            :closable="false"
            style="margin-bottom: 16px;"
          >
            <template #default>
              <div style="font-size: 12px;">可设置查询条件，留空则查询所有数据（可能较慢）</div>
            </template>
          </el-alert>
          
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="债券类型">
                <el-select v-model="bondInfoParams.bond_type" clearable placeholder="选择债券类型" style="width: 100%">
                  <el-option label="短期融资券" value="短期融资券" />
                  <el-option label="中期票据" value="中期票据" />
                  <el-option label="企业债" value="企业债" />
                  <el-option label="公司债" value="公司债" />
                  <el-option label="可转债" value="可转债" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="发行年份">
                <el-select v-model="bondInfoParams.issue_year" clearable placeholder="选择发行年份" style="width: 100%">
                  <el-option 
                    v-for="year in availableYears" 
                    :key="year" 
                    :label="year" 
                    :value="year" 
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="付息方式">
                <el-select v-model="bondInfoParams.coupon_type" clearable placeholder="选择付息方式" style="width: 100%">
                  <el-option label="零息式" value="零息式" />
                  <el-option label="固定利率" value="固定利率" />
                  <el-option label="浮动利率" value="浮动利率" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="评级">
                <el-select v-model="bondInfoParams.grade" clearable placeholder="选择评级" style="width: 100%">
                  <el-option label="AAA+" value="AAA+" />
                  <el-option label="AAA" value="AAA" />
                  <el-option label="AAA-" value="AAA-" />
                  <el-option label="AA+" value="AA+" />
                  <el-option label="AA" value="AA" />
                  <el-option label="AA-" value="AA-" />
                  <el-option label="A+" value="A+" />
                  <el-option label="A" value="A" />
                  <el-option label="A-" value="A-" />
                  <el-option label="A-1" value="A-1" />
                  <el-option label="A-2" value="A-2" />
                  <el-option label="A-3" value="A-3" />
                  <el-option label="BBB+" value="BBB+" />
                  <el-option label="BBB" value="BBB" />
                  <el-option label="BBB-" value="BBB-" />
                  <el-option label="BB+" value="BB+" />
                  <el-option label="BB" value="BB" />
                  <el-option label="BB-" value="BB-" />
                  <el-option label="B+" value="B+" />
                  <el-option label="B" value="B" />
                  <el-option label="B-" value="B-" />
                  <el-option label="CCC+" value="CCC+" />
                  <el-option label="CCC" value="CCC" />
                  <el-option label="CCC-" value="CCC-" />
                  <el-option label="CC" value="CC" />
                  <el-option label="C" value="C" />
                  <el-option label="D" value="D" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="债券名称">
                <el-input v-model="bondInfoParams.bond_name" clearable placeholder="输入债券名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="债券代码">
                <el-input v-model="bondInfoParams.bond_code" clearable placeholder="输入债券代码" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="发行人">
                <el-input v-model="bondInfoParams.bond_issue" clearable placeholder="输入发行人名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="承销商">
                <el-input v-model="bondInfoParams.underwriter" clearable placeholder="输入承销商名称" />
              </el-form-item>
            </el-col>
          </el-row>
        </template>
        
        <el-alert
          title="更新说明"
          type="warning"
          :closable="false"
          style="margin-bottom: 16px;"
        >
          <template #default>
            <div style="font-size: 12px; line-height: 1.6;">
              <p v-if="collectionName === 'bond_basic_info'">将从AKShare获取最新的债券列表并更新到数据库，支持批量更新和增量更新</p>
              <p v-else-if="collectionName === 'yield_curve_daily'">将获取指定日期范围的收益率曲线数据（默认最近30天，范围需小于一年）</p>
              <p v-else-if="collectionName === 'bond_daily'">将为数据库中的债券更新历史行情数据（最多10个债券，默认最近7天）</p>
              <p v-else-if="collectionName === 'bond_cb_list_jsl'">将从集思录获取所有可转债的实时数据</p>
              <p v-else-if="collectionName === 'bond_cov_list'">将从东方财富获取可转债列表</p>
              <p v-else-if="collectionName === 'bond_cash_summary'">将获取指定日期的上交所现券市场概览数据</p>
              <p v-else-if="collectionName === 'bond_deal_summary'">将获取指定日期的上交所成交概览数据</p>
              <p v-else-if="collectionName === 'bond_nafmii_debts'">将从NAFMII获取银行间市场债务数据（前10页）</p>
              <p v-else-if="collectionName === 'bond_spot_quotes'">将获取当前所有银行间市场的现货报价数据</p>
              <p v-else-if="collectionName === 'bond_cb_profiles'">将从AKShare获取所有可转债的档案信息</p>
              <p v-else-if="collectionName === 'bond_info_cm'">将从中国外汇交易中心查询债券信息，可按上述参数筛选（不设置参数则查询所有，可能较慢）</p>
              <p v-else>该集合暂不支持自动更新，如需更新请联系管理员</p>
            </div>
          </template>
        </el-alert>
      </el-form>
      
      <template #footer>
        <el-button @click="cancelRefresh" :disabled="refreshing && progressPercentage < 10">
          {{ refreshing ? '取消' : '关闭' }}
        </el-button>
        <el-button 
          type="primary" 
          @click="refreshData" 
          :loading="refreshing"
          :disabled="refreshing || batchRefreshing"
        >
          {{ refreshing ? '更新中...' : '开始更新' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Box, Refresh, Search, Document, Calendar, Download, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { bondsApi } from '@/api/bonds'

use([CanvasRenderer, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

const route = useRoute()
const router = useRouter()

const collectionName = computed(() => route.params.collectionName as string)

// 数据状态
const loading = ref(false)
const items = ref<any[]>([])
const fields = ref<Array<{ name: string; type: string; example: string | null }>>([])
const page = ref(1)
const pageSize = ref(50)
const total = ref(0)

// 过滤条件
const filterField = ref('')
const filterValue = ref('')

// 排序条件
const sortBy = ref('')
const sortDir = ref<'asc' | 'desc'>('asc')

// 统计数据
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)
const issuanceLoading = ref(false)
const issuanceChartOption = ref<any>(null)
const bondTypePieOption = ref<any>(null)
const gradePieOption = ref<any>(null)

// 更新数据相关
const refreshDialogVisible = ref(false)
const refreshing = ref(false)
const refreshStartDate = ref('')
const refreshEndDate = ref('')
const currentTaskId = ref('')
const progressPercentage = ref(0)
const progressStatus = ref<'success' | 'exception' | 'warning' | ''>('')
const progressMessage = ref('')
let progressTimer: NodeJS.Timeout | null = null

// bond_info_cm 查询参数
const bondInfoParams = ref({
  bond_name: '',
  bond_code: '',
  bond_issue: '',
  bond_type: '',
  coupon_type: '',
  issue_year: '',
  underwriter: '',
  grade: ''
})

// 批量更新相关
const batchRefreshing = ref(false)
const batchProgress = ref({ completed: 0, total: 0, failed: 0 })
const batchTasks = ref<Array<{ year: string; taskId: string; status: string }>>([])
const batchConcurrency = ref(5)
const batchDelaySeconds = ref(5)
const sanitizedBatchConcurrency = computed(() => {
  const value = Number(batchConcurrency.value)
  if (Number.isNaN(value)) return 1
  return Math.max(1, Math.min(20, Math.floor(value)))
})
const sanitizedBatchDelaySeconds = computed(() => {
  const value = Number(batchDelaySeconds.value)
  if (Number.isNaN(value)) return 0
  return Math.max(0, Math.min(60, Math.floor(value)))
})

// 清空数据相关
const clearing = ref(false)

// bond_basic_info 批量更新和增量更新相关
const bondBasicBatchSize = ref(1000)
const bondBasicConcurrentThreads = ref(3)
const bondBasicSaveInterval = ref(1000)
const bondBasicBatchUpdating = ref(false)
const bondBasicIncrementalUpdating = ref(false)
const loadingBondBasicStats = ref(false)
const bondBasicStats = ref<any>(null)
const bondBasicProgress = ref({
  show: false,
  percentage: 0,
  status: '' as any,
  message: '',
  details: null as any
})

// 判断是否需要日期范围
const needsDateRange = computed(() => {
  return ['yield_curve_daily', 'bond_daily'].includes(collectionName.value)
})

// 判断是否需要单个日期
const needsSingleDate = computed(() => {
  return ['bond_cash_summary', 'bond_deal_summary'].includes(collectionName.value)
})

// 判断是否不需要日期
const needsNoDate = computed(() => {
  return ['bond_basic_info', 'bond_cb_list_jsl', 'bond_cov_list', 'bond_nafmii_debts', 'bond_spot_quotes', 'bond_cb_profiles'].includes(collectionName.value)
})

// 判断是否是bond_info_cm（需要查询参数）
const needsBondParams = computed(() => {
  return collectionName.value === 'bond_info_cm'
})

// 生成可选的年份列表（从1993年到当前年份，倒序排列）
const availableYears = computed(() => {
  const currentYear = new Date().getFullYear()
  const years: string[] = []
  for (let year = currentYear; year >= 1993; year--) {
    years.push(year.toString())
  }
  return years
})

const importFiles = ref<File[]>([])
const importing = ref(false)
const uploadRef = ref()

const handleImportFileChange = (file: any, fileList: any[]) => {
  importFiles.value = (fileList || [])
    .map((f: any) => f?.raw)
    .filter((f: any) => !!f)
}

const handleImportFileRemove = (file: any, fileList: any[]) => {
  importFiles.value = (fileList || [])
    .map((f: any) => f?.raw)
    .filter((f: any) => !!f)
}

const handleImportFile = async () => {
  if (!importFiles.value.length) {
    ElMessage.warning('请先选择要导入的文件')
    return
  }

  if (!['bond_info_cm', 'bond_basic_info'].includes(collectionName.value)) {
    ElMessage.warning('当前仅支持债券信息查询集合和债券基础信息集合的文件导入')
    return
  }

  try {
    importing.value = true

    let totalSaved = 0
    let totalRows = 0

    for (const file of importFiles.value) {
      const res = await bondsApi.importCollectionData(collectionName.value, file)

      if (res.success && res.data) {
        const data: any = res.data
        totalSaved += Number(data.saved || 0)
        totalRows += Number(data.rows || 0)
      } else {
        ElMessage.error((res as any).data?.message || '导入失败')
        return
      }
    }

    if (totalRows > 0) {
      ElMessage.success(`成功导入 ${importFiles.value.length} 个文件，合计 ${totalSaved} 条记录`)
    } else {
      ElMessage.warning('文件中没有可导入的数据')
    }

    await loadData()

    if (uploadRef.value && typeof uploadRef.value.clearFiles === 'function') {
      uploadRef.value.clearFiles()
    }
    importFiles.value = []
    refreshDialogVisible.value = false
  } catch (e: any) {
    let msg = '导入失败'
    if (e?.response?.data?.detail) {
      msg = e.response.data.detail
    } else if (e?.message) {
      msg = e.message
    }
    ElMessage.error(msg)
  } finally {
    importing.value = false
  }
}
const remoteSyncHost = ref('')
const remoteSyncDbType = ref('mongodb')
const remoteSyncBatchSize = ref(5000)
const remoteSyncCollection = ref('')
const remoteSyncUsername = ref('')
const remoteSyncAuthSource = ref('')
const remoteSyncPassword = ref('')
const remoteSyncing = ref(false)
const remoteSyncStats = ref<{ remote_total: number; synced: number } | null>(null)

const handleRemoteSync = async () => {
  if (!remoteSyncHost.value) {
    ElMessage.warning('请先输入远程服务器 IP 地址或连接串')
    return
  }

  if (!['bond_info_cm', 'bond_basic_info'].includes(collectionName.value)) {
    ElMessage.warning('当前仅支持债券信息查询集合和债券基础信息集合的远程同步')
    return
  }

  try {
    remoteSyncing.value = true
    remoteSyncStats.value = null

    const res = await bondsApi.syncCollectionFromRemote(collectionName.value, {
      remote_host: remoteSyncHost.value.trim(),
      db_type: remoteSyncDbType.value,
      batch_size: remoteSyncBatchSize.value,
      remote_collection: remoteSyncCollection.value || undefined,
      remote_username: remoteSyncUsername.value || undefined,
      remote_password: remoteSyncPassword.value || undefined,
      remote_auth_source: remoteSyncAuthSource.value || undefined,
    })

    if (res.success && res.data) {
      remoteSyncStats.value = {
        remote_total: Number(res.data.remote_total ?? 0),
        synced: Number(res.data.synced ?? 0),
      }
      ElMessage.success(res.data.message || '远程同步成功')
      await loadData()
    } else {
      ElMessage.error((res as any).data?.message || '远程同步失败')
    }
  } catch (e: any) {
    let msg = '远程同步失败'
    if (e?.response?.data?.detail) {
      msg = e.response.data.detail
    } else if (e?.message) {
      msg = e.message
    }
    ElMessage.error(msg)
  } finally {
    remoteSyncing.value = false
  }
}

const delay = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms))

const updateBondInfoDistributions = () => {
  if (collectionName.value !== 'bond_info_cm' || !stats.value) {
    bondTypePieOption.value = null
    gradePieOption.value = null
    return
  }

  const s: any = stats.value
  const typeStats: Array<{ type: string; count: number }> = s.bond_type_stats || []
  const gradeStats: Array<{ grade: string; count: number }> = s.grade_stats || []

  if (typeStats && typeStats.length > 0) {
    bondTypePieOption.value = {
      tooltip: {
        trigger: 'item',
      },
      legend: {
        type: 'scroll',
        bottom: 0,
        left: 'center',
      },
      series: [
        {
          name: '债券类型',
          type: 'pie',
          radius: ['35%', '65%'],
          center: ['50%', '45%'],
          avoidLabelOverlap: false,
          label: {
            formatter: '{b}\n{d}%',
          },
          data: typeStats.map((item) => ({
            name: item.type || '未知',
            value: item.count || 0,
          })),
        },
      ],
    }
  } else {
    bondTypePieOption.value = null
  }

  if (gradeStats && gradeStats.length > 0) {
    gradePieOption.value = {
      tooltip: {
        trigger: 'item',
      },
      legend: {
        type: 'scroll',
        bottom: 0,
        left: 'center',
      },
      series: [
        {
          name: '最新债项评级',
          type: 'pie',
          radius: ['35%', '65%'],
          center: ['50%', '45%'],
          avoidLabelOverlap: false,
          label: {
            formatter: '{b}\n{d}%',
          },
          data: gradeStats.map((item) => ({
            name: item.grade || '未知',
            value: item.count || 0,
          })),
        },
      ],
    }
  } else {
    gradePieOption.value = null
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载集合信息
    const collectionsRes = await bondsApi.getCollections()
    if (collectionsRes.success && collectionsRes.data) {
      collectionInfo.value = collectionsRes.data.find((c: any) => c.name === collectionName.value)
    }

    // 加载统计数据
    const statsRes = await bondsApi.getCollectionStats(collectionName.value)
    if (statsRes.success && statsRes.data) {
      stats.value = statsRes.data
    } else {
      stats.value = null
    }

    // 加载数据
    const dataRes = await bondsApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    
    if (dataRes.success && dataRes.data) {
      items.value = dataRes.data.items || []
      fields.value = dataRes.data.fields || []
      total.value = dataRes.data.total || 0
    } else {
      ElMessage.error('加载数据失败')
    }

    if (collectionName.value === 'bond_info_cm') {
      updateBondInfoDistributions()
      await loadIssuanceStats()
    } else {
      issuanceChartOption.value = null
      bondTypePieOption.value = null
      gradePieOption.value = null
    }
  } catch (e: any) {
    console.error('加载数据失败:', e)
    ElMessage.error('加载数据失败: ' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 格式化值
const formatValue = (value: any): string => {
  if (value === null || value === undefined) {
    return '-'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  page.value = 1
  loadData()
}

const handlePageChange = (p: number) => {
  page.value = p
  loadData()
}

// 过滤处理
const handleFilter = () => {
  page.value = 1
  loadData()
}

// 排序处理
const handleSortChange = ({ column, prop, order }: { column: any; prop: string; order: string | null }) => {
  if (order === null) {
    // 取消排序
    sortBy.value = ''
    sortDir.value = 'asc'
  } else {
    sortBy.value = prop
    sortDir.value = order === 'ascending' ? 'asc' : 'desc'
  }
  page.value = 1
  loadData()
}

const loadIssuanceStats = async () => {
  try {
    issuanceLoading.value = true
    const res = await bondsApi.getBondInfoIssuanceYearly()
    if (res.success && res.data?.items?.length) {
      const years = res.data.items.map((item: { year: string }) => item.year)
      const counts = res.data.items.map((item: { count: number }) => item.count)
      issuanceChartOption.value = {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '5%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: years,
          name: '年份',
          nameLocation: 'middle',
          nameGap: 30,
          axisLabel: {
            rotate: years.length > 10 ? 45 : 0
          }
        },
        yAxis: {
          type: 'value',
          name: '发行数量 (条)'
        },
        series: [
          {
            name: '发行量',
            type: 'bar',
            data: counts,
            itemStyle: {
              color: '#5b8ff9'
            }
          }
        ]
      }
    } else {
      issuanceChartOption.value = null
    }
  } catch (error: any) {
    console.error('加载发行统计失败:', error)
    ElMessage.warning(error?.message || '加载年度发行统计失败')
    issuanceChartOption.value = null
  } finally {
    issuanceLoading.value = false
  }
}

// 显示更新对话框
const showRefreshDialog = () => {
  // 设置默认日期范围（最近30天）
  const today = new Date()
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(today.getDate() - 30)
  
  refreshEndDate.value = today.toISOString().split('T')[0]
  refreshStartDate.value = thirtyDaysAgo.toISOString().split('T')[0]
  
  refreshDialogVisible.value = true
}

// 更新数据
const refreshData = async () => {
  refreshing.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = '正在创建任务...'
  
  try {
    const params: any = {}
    
    if (needsDateRange.value) {
      if (refreshStartDate.value) {
        params.start_date = refreshStartDate.value
      }
      if (refreshEndDate.value) {
        params.end_date = refreshEndDate.value
      }
    } else if (needsSingleDate.value) {
      if (refreshStartDate.value) {
        params.date = refreshStartDate.value
      }
    } else if (needsBondParams.value) {
      // 添加 bond_info_cm 的查询参数（只添加非空参数）
      if (bondInfoParams.value.bond_name) params.bond_name = bondInfoParams.value.bond_name
      if (bondInfoParams.value.bond_code) params.bond_code = bondInfoParams.value.bond_code
      if (bondInfoParams.value.bond_issue) params.bond_issue = bondInfoParams.value.bond_issue
      if (bondInfoParams.value.bond_type) params.bond_type = bondInfoParams.value.bond_type
      if (bondInfoParams.value.coupon_type) params.coupon_type = bondInfoParams.value.coupon_type
      if (bondInfoParams.value.issue_year) params.issue_year = bondInfoParams.value.issue_year
      if (bondInfoParams.value.underwriter) params.underwriter = bondInfoParams.value.underwriter
      if (bondInfoParams.value.grade) params.grade = bondInfoParams.value.grade
    }
    
    // 创建任务
    const res = await bondsApi.refreshCollectionData(collectionName.value, params)
    
    if (res.success && res.data?.task_id) {
      currentTaskId.value = res.data.task_id
      progressMessage.value = '任务已创建，正在更新数据...'
      
      // 开始轮询任务状态
      await pollTaskStatus()
    } else {
      throw new Error(res.data?.message || '创建任务失败')
    }
  } catch (e: any) {
    console.error('更新数据失败:', e)
    let errorMessage = '更新数据失败'
    if (e.response?.data?.detail) {
      errorMessage = e.response.data.detail
    } else if (e.response?.data?.error) {
      errorMessage = e.response.data.error  
    } else if (e.message) {
      errorMessage = e.message
    }
    ElMessage.error(errorMessage)
    progressStatus.value = 'exception'
    refreshing.value = false
  }
}

// 轮询任务状态
const pollTaskStatus = async () => {
  progressTimer = setInterval(async () => {
    try {
      const res = await bondsApi.getRefreshTaskStatus(currentTaskId.value)
      
      if (res.success && res.data) {
        const task = res.data
        
        // 更新进度
        progressPercentage.value = Math.round((task.progress / task.total) * 100)
        progressMessage.value = task.message || ''
        
        // 检查是否完成
        if (task.status === 'success') {
          progressStatus.value = 'success'
          
          // 构建成功消息
          let message = task.message || '数据更新成功'
          if (task.result) {
            if (task.result.saved !== undefined) {
              message = `成功更新 ${task.result.saved} 条数据`
            }
            if (task.result.success_count !== undefined) {
              message += `（成功 ${task.result.success_count}）`
            }
            if (task.result.fail_count !== undefined && task.result.fail_count > 0) {
              message += `（失败 ${task.result.fail_count}）`
            }
          }
          
          ElMessage.success(message)
          
          // 停止轮询
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          
          // 刷新页面数据
          await loadData()
          
          // 延迟关闭对话框
          setTimeout(() => {
            refreshDialogVisible.value = false
            refreshing.value = false
            progressPercentage.value = 0
            progressStatus.value = ''
          }, 1500)
          
        } else if (task.status === 'failed') {
          progressStatus.value = 'exception'
          ElMessage.error(task.error || '数据更新失败')
          
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          refreshing.value = false
        }
        // 如果是 running 或 pending，继续轮询
      }
    } catch (e) {
      console.error('查询任务状态失败:', e)
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
      progressStatus.value = 'exception'
      refreshing.value = false
    }
  }, 1000) // 每秒轮询一次
}

// 取消刷新
const cancelRefresh = () => {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
  refreshDialogVisible.value = false
  refreshing.value = false
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = ''
  batchRefreshing.value = false
  batchProgress.value = { completed: 0, total: 0, failed: 0 }
  batchTasks.value = []
}

// 批量更新所有年份（从1993到当前年份）
const refreshAllYears = async () => {
  try {
    const concurrency = sanitizedBatchConcurrency.value
    const delaySeconds = sanitizedBatchDelaySeconds.value
    const delayMs = delaySeconds * 1000
    // 确认操作
    await ElMessageBox.confirm(
      `将从1993年到今年，按年份逐年更新债券信息数据。将使用 ${concurrency} 个并发线程进行更新，并在每个任务开始前延迟 ${delaySeconds} 秒以避免触发频率限制。是否继续？`,
      '批量更新确认',
      {
        confirmButtonText: '开始更新',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    batchRefreshing.value = true
    
    // 生成年份列表（从1993到当前年份）
    const currentYear = new Date().getFullYear()
    const years: string[] = []
    for (let year = 1993; year <= currentYear; year++) {
      years.push(year.toString())
    }
    
    batchProgress.value = { completed: 0, total: years.length, failed: 0 }
    batchTasks.value = []
    
    ElMessage.info(`开始批量更新，共 ${years.length} 个年份，使用 ${concurrency} 个并发线程且每个任务启动前延迟 ${delaySeconds} 秒`)
    
    // 使用并发控制，最多 concurrency 个并发任务，并在任务启动前延迟
    const results: Array<{ year: string; success: boolean; error?: string }> = []
    const executing: Promise<void>[] = []
    
    const runYearTask = async (year: string) => {
      try {
        const params: Record<string, any> = {
          issue_year: year
        }
        
        if (bondInfoParams.value.bond_type) params.bond_type = bondInfoParams.value.bond_type
        if (bondInfoParams.value.coupon_type) params.coupon_type = bondInfoParams.value.coupon_type
        if (bondInfoParams.value.grade) params.grade = bondInfoParams.value.grade
        if (bondInfoParams.value.bond_name) params.bond_name = bondInfoParams.value.bond_name
        if (bondInfoParams.value.bond_code) params.bond_code = bondInfoParams.value.bond_code
        if (bondInfoParams.value.bond_issue) params.bond_issue = bondInfoParams.value.bond_issue
        if (bondInfoParams.value.underwriter) params.underwriter = bondInfoParams.value.underwriter
        
        const res = await bondsApi.refreshCollectionData(collectionName.value, params)
        
        if (res.success && res.data?.task_id) {
          const taskId = res.data.task_id
          batchTasks.value.push({ year, taskId, status: 'running' })
          await waitForTask(taskId)
          return { year, success: true as const }
        }
        throw new Error(res.data?.message || '创建任务失败')
      } catch (error: any) {
        batchProgress.value.failed++
        console.error(`更新${year}年数据失败:`, error)
        return { year, success: false as const, error: error?.message || '未知错误' }
      } finally {
        batchProgress.value.completed++
      }
    }
    
    for (const year of years) {
      if (delayMs > 0) {
        await delay(delayMs)
      }
      const taskPromise = (async () => {
        const result = await runYearTask(year)
        results.push(result)
      })()
      executing.push(taskPromise)
      taskPromise.finally(() => {
        const index = executing.indexOf(taskPromise)
        if (index > -1) {
          executing.splice(index, 1)
        }
      })
      
      if (executing.length >= concurrency) {
        await Promise.race(executing)
      }
    }
    
    await Promise.all(executing)
    console.log(`批量更新完成: ${batchProgress.value.completed}/${batchProgress.value.total}`)
    
    // 所有任务完成
    const successCount = results.filter(r => r.success).length
    const failCount = results.filter(r => !r.success).length
    
    if (failCount === 0) {
      ElMessage.success(`批量更新完成！成功更新 ${successCount} 个年份的数据`)
    } else {
      ElMessage.warning(`批量更新完成！成功 ${successCount} 个，失败 ${failCount} 个`)
    }
    
    // 刷新页面数据
    await loadData()
    
    // 关闭对话框
    setTimeout(() => {
      refreshDialogVisible.value = false
      batchRefreshing.value = false
      batchProgress.value = { completed: 0, total: 0, failed: 0 }
      batchTasks.value = []
    }, 1500)
    
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('批量更新失败:', error)
      ElMessage.error(error.message || '批量更新失败')
    }
    batchRefreshing.value = false
    batchProgress.value = { completed: 0, total: 0, failed: 0 }
    batchTasks.value = []
  }
}

// 等待单个任务完成
const waitForTask = async (taskId: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    const checkInterval = setInterval(async () => {
      try {
        const res = await bondsApi.getRefreshTaskStatus(taskId)
        
        if (res.success && res.data) {
          const task = res.data
          
          if (task.status === 'success') {
            clearInterval(checkInterval)
            resolve()
          } else if (task.status === 'failed') {
            clearInterval(checkInterval)
            reject(new Error(task.error || '任务执行失败'))
          }
          // 继续等待 running 或 pending 状态
        }
      } catch (error) {
        clearInterval(checkInterval)
        reject(error)
      }
    }, 2000) // 每2秒检查一次
  })
}

// 处理清空数据
const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(
      `确认要清空 "${collectionInfo.value?.display_name || collectionName.value}" 集合的所有数据吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确认清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    // 用户确认，执行清空
    clearing.value = true
    try {
      const res = await bondsApi.clearCollectionData(collectionName.value)
      if (res.success) {
        ElMessage.success(`成功清空 ${res.data?.deleted_count || 0} 条数据`)
        // 刷新页面数据
        await loadData()
      } else {
        ElMessage.error(res.message || '清空数据失败')
      }
    } catch (error: any) {
      console.error('清空数据失败:', error)
      ElMessage.error(error.message || '清空数据失败')
    } finally {
      clearing.value = false
    }
  } catch (error) {
    // 用户取消操作
    if (error !== 'cancel') {
      console.error('清空操作错误:', error)
    }
  }
}

// ========== bond_basic_info 相关方法 ==========

// 获取债券基础信息更新统计
const getBondBasicUpdateStatistics = async () => {
  try {
    loadingBondBasicStats.value = true
    const response = await bondsApi.getBondBasicUpdateStatistics()
    
    if (response.success && response.data) {
      bondBasicStats.value = response.data
      ElMessage.success('获取统计信息成功')
    } else {
      throw new Error(response.data?.message || '获取统计信息失败')
    }
  } catch (error: any) {
    console.error('获取统计信息失败:', error)
    ElMessage.error(`获取统计信息失败: ${error.message}`)
  } finally {
    loadingBondBasicStats.value = false
  }
}

// 开始批量更新
const startBondBasicBatchUpdate = async () => {
  try {
    const result = await ElMessageBox.confirm(
      `确认开始批量更新？\n批次大小: ${bondBasicBatchSize.value}\n并发线程: ${bondBasicConcurrentThreads.value}\n保存间隔: ${bondBasicSaveInterval.value}`,
      '批量更新确认',
      {
        confirmButtonText: '开始更新',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    if (result !== 'confirm') return
    
    bondBasicBatchUpdating.value = true
    bondBasicProgress.value = {
      show: true,
      percentage: 0,
      status: '',
      message: '正在启动批量更新...',
      details: null
    }
    
    const response = await bondsApi.startBondBasicBatchUpdate({
      batch_size: bondBasicBatchSize.value,
      concurrent_threads: bondBasicConcurrentThreads.value,
      save_interval: bondBasicSaveInterval.value
    })
    
    if (response.success && response.data) {
      const data = response.data
      
      // 更新进度
      bondBasicProgress.value = {
        show: true,
        percentage: 100,
        status: 'success',
        message: data.message || '批量更新完成',
        details: {
          total: data.total_bonds,
          processed: data.total_processed,
          updated: data.total_updated,
          errors: data.total_errors
        }
      }
      
      ElMessage.success('批量更新完成')
      
      // 刷新统计数据
      await getBondBasicUpdateStatistics()
      
      // 刷新页面数据
      await loadData()
      
    } else {
      throw new Error(response.data?.message || '批量更新失败')
    }
    
  } catch (error: any) {
    bondBasicProgress.value = {
      show: true,
      percentage: 0,
      status: 'exception',
      message: `批量更新失败: ${error.message}`,
      details: null
    }
    
    ElMessage.error(`批量更新失败: ${error.message}`)
  } finally {
    bondBasicBatchUpdating.value = false
  }
}

// 开始增量更新
const startBondBasicIncrementalUpdate = async () => {
  try {
    const missingCount = bondBasicStats.value?.missing_detail_count || 0
    
    const result = await ElMessageBox.confirm(
      `确认开始增量更新？\n预计需要更新 ${missingCount} 个缺失的债券基础信息。`,
      '增量更新确认',
      {
        confirmButtonText: '开始更新',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    if (result !== 'confirm') return
    
    bondBasicIncrementalUpdating.value = true
    bondBasicProgress.value = {
      show: true,
      percentage: 0,
      status: '',
      message: '正在启动增量更新...',
      details: null
    }
    
    const response = await bondsApi.startBondBasicIncrementalUpdate()
    
    if (response.success && response.data) {
      const data = response.data
      
      // 更新进度
      bondBasicProgress.value = {
        show: true,
        percentage: 100,
        status: data.updated > 0 ? 'success' : 'warning',
        message: data.message || '增量更新完成',
        details: {
          total: data.missing_codes,
          processed: data.missing_codes,
          updated: data.updated,
          errors: data.errors
        }
      }
      
      ElMessage.success('增量更新完成')
      
      // 刷新统计数据
      await getBondBasicUpdateStatistics()
      
      // 刷新页面数据
      await loadData()
      
    } else {
      throw new Error(response.data?.message || '增量更新失败')
    }
    
  } catch (error: any) {
    bondBasicProgress.value = {
      show: true,
      percentage: 0,
      status: 'exception',
      message: `增量更新失败: ${error.message}`,
      details: null
    }
    
    ElMessage.error(`增量更新失败: ${error.message}`)
  } finally {
    bondBasicIncrementalUpdating.value = false
  }
}

// 组件卸载时清理定时器
onUnmounted(() => {
  if (progressTimer) {
    clearInterval(progressTimer)
  }
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.collection-view {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.page-description {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.stats-card,
.fields-card,
.data-card {
  margin-bottom: 16px;
}

.issuance-card {
  margin-bottom: 16px;
}

.chart-wrapper {
  width: 100%;
  height: 360px;
}

.stats-label {
  font-size: 14px;
  color: #606266;
  margin-right: 8px;
}

.category-stats,
.exchange-stats {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.example-text {
  font-family: monospace;
  font-size: 12px;
  color: #606266;
}

.text-muted {
  color: #c0c4cc;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.batch-config-section {
  padding: 16px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background-color: #f8fafc;
  margin-bottom: 20px;
}

.batch-config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.batch-config-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.batch-config-subtitle {
  margin: 4px 0 0 0;
  font-size: 13px;
  color: #909399;
}

.batch-config-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.batch-config-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.batch-field-label {
  font-size: 13px;
  color: #606266;
  font-weight: 500;
}

.batch-config-action {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.batch-update-btn {
  width: fit-content;
  padding: 4px 18px;
  font-weight: 500;
}

.batch-config-note {
  margin: 0;
  font-size: 12px;
  color: #a0a4ab;
  line-height: 1.4;
}

.batch-config-divider {
  margin: 20px 0 0 0;
}

@media (max-width: 768px) {
  .batch-config-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }
}
</style>


