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
          <el-button :icon="Box" @click="showOverviewDialog">数据概览</el-button>
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
          <el-button :icon="Download" type="primary" @click="handleRefreshData" :loading="refreshing">更新数据</el-button>
          <el-button :icon="Delete" type="danger" @click="handleClearData" :loading="clearing">清空数据</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 可视化分析 Tabs -->
      <el-tabs type="border-card" class="analysis-tabs" v-if="hasCharts">
        <el-tab-pane label="结构分布分析">
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">{{ collectionName === 'fund_purchase_status' ? '基金类型分布' : '基金类型分布' }}</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="typePieOption"
                  :option="typePieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无类型数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="stat-distribution-group" style="border-left: none; padding-left: 0; height: 100%; display: flex; flex-direction: column;">
                <div class="chart-title" style="margin-bottom: 12px; text-align: left;">主要构成</div>
                <div class="distribution-list" v-if="categoryDistribution.length > 0" style="max-height: 320px; overflow-y: auto; padding-right: 8px;">
                  <div v-for="item in categoryDistribution" :key="item.category" class="distribution-item">
                    <div class="dist-info">
                      <span class="dist-name">{{ item.category }}</span>
                      <span class="dist-count">{{ item.count?.toLocaleString() }} ({{ item.percentage }}%)</span>
                    </div>
                    <el-progress 
                      :percentage="Number(item.percentage)" 
                      :show-text="false" 
                      :stroke-width="6" 
                      :color="item.color"
                    />
                  </div>
                </div>
                <div v-else class="text-muted" style="text-align: center; margin-top: 20px;">暂无分类数据</div>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- 基金申购状态专用Tab -->
        <el-tab-pane label="申购赎回状态" v-if="collectionName === 'fund_purchase_status'">
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">申购状态分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="purchaseStatusPieOption"
                  :option="purchaseStatusPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无申购状态数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">赎回状态分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="redeemStatusPieOption"
                  :option="redeemStatusPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无赎回状态数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- ETF实时行情专用Tab -->
        <el-tab-pane label="市场概况" v-if="collectionName === 'fund_etf_spot_em'">
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="24">
              <el-row :gutter="24">
                <el-col :span="6">
                  <div class="stat-card rise">
                    <div class="stat-label">上涨</div>
                    <div class="stat-value">{{ stats?.rise_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card fall">
                    <div class="stat-label">下跌</div>
                    <div class="stat-value">{{ stats?.fall_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card flat">
                    <div class="stat-label">平盘</div>
                    <div class="stat-value">{{ stats?.flat_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-label">总计</div>
                    <div class="stat-value">{{ stats?.total_count || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">涨跌分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="etfRiseFallPieOption"
                  :option="etfRiseFallPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">成交额TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="etfVolumeBarOption"
                  :option="etfVolumeBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- 同花顺ETF实时行情专用Tab -->
        <el-tab-pane label="市场分析" v-if="collectionName === 'fund_etf_spot_ths'">
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="24">
              <el-row :gutter="24">
                <el-col :span="6">
                  <div class="stat-card rise">
                    <div class="stat-label">上涨</div>
                    <div class="stat-value">{{ stats?.rise_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card fall">
                    <div class="stat-label">下跌</div>
                    <div class="stat-value">{{ stats?.fall_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card flat">
                    <div class="stat-label">平盘</div>
                    <div class="stat-value">{{ stats?.flat_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-label">总计</div>
                    <div class="stat-value">{{ stats?.total_count || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="12">
              <div class="chart-title">涨跌分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsRiseFallPieOption"
                  :option="thsRiseFallPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">基金类型分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsTypePieOption"
                  :option="thsTypePieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">涨幅TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsGainersBarOption"
                  :option="thsGainersBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">跌幅TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="thsLosersBarOption"
                  :option="thsLosersBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <!-- LOF基金实时行情专用Tab -->
        <el-tab-pane label="市场行情" v-if="collectionName === 'fund_lof_spot_em'">
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="24">
              <el-row :gutter="24">
                <el-col :span="6">
                  <div class="stat-card rise">
                    <div class="stat-label">上涨</div>
                    <div class="stat-value">{{ stats?.rise_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card fall">
                    <div class="stat-label">下跌</div>
                    <div class="stat-value">{{ stats?.fall_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card flat">
                    <div class="stat-label">平盘</div>
                    <div class="stat-value">{{ stats?.flat_count || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-label">总计</div>
                    <div class="stat-value">{{ stats?.total_count || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
          <el-row :gutter="24" style="margin-bottom: 24px;">
            <el-col :span="12">
              <div class="chart-title">涨跌分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofRiseFallPieOption"
                  :option="lofRiseFallPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">成交额TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofVolumeBarOption"
                  :option="lofVolumeBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="24">
            <el-col :span="12">
              <div class="chart-title">涨幅TOP10</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofGainersBarOption"
                  :option="lofGainersBarOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-title">市值分布</div>
              <div class="chart-wrapper-medium">
                <v-chart
                  v-if="lofMarketCapPieOption"
                  :option="lofMarketCapPieOption"
                  :autoresize="true"
                  style="height: 320px; width: 100%"
                />
                <el-empty v-else description="暂无数据" />
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>

      <!-- 数据列表 -->
      <el-card shadow="hover" class="data-card">
        <template #header>
          <div class="card-header">
            <div style="display: flex; align-items: center;">
              <span>数据</span>
              <el-popover
                placement="right"
                title="字段说明"
                :width="600"
                trigger="hover"
                v-if="fields && fields.length > 0"
              >
                <template #reference>
                  <el-icon style="margin-left: 8px; cursor: pointer; color: #909399;"><QuestionFilled /></el-icon>
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
              </el-popover>
            </div>
            <div class="header-actions">
              <el-select
                v-if="collectionName === 'fund_info_index_em'"
                v-model="filterCompany"
                placeholder="基金公司"
                style="width: 150px; margin-right: 8px;"
                clearable
                filterable
                @change="handleFilterChange('company', $event)"
              >
                <el-option label="全部基金公司" value="全部" />
                <el-option v-for="company in companyOptions" :key="company" :label="company" :value="company" />
              </el-select>
              <el-input
                v-model="filterValue"
                placeholder="搜索..."
                style="width: 200px; margin-right: 8px;"
                clearable
                @clear="loadData"
                @keyup.enter="loadData"
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
              <el-button size="small" :icon="Search" @click="loadData">搜索</el-button>
            </div>
          </div>
        </template>
        
        <!-- 指数型基金筛选栏 (整合到数据卡片内部) -->
        <div class="filter-section" v-if="collectionName === 'fund_info_index_em'">
          <div class="filter-row">
            <span class="filter-label">跟踪标的：</span>
            <div class="filter-options">
              <span 
                v-for="opt in targetOptions" 
                :key="opt" 
                class="filter-option" 
                :class="{ active: filterTarget === opt }"
                @click="handleFilterChange('target', opt)"
              >
                {{ opt }}
              </span>
            </div>
          </div>
          <div class="filter-row" style="margin-top: 10px;">
            <span class="filter-label">跟踪方式：</span>
            <div class="filter-options">
               <span 
                v-for="opt in methodOptions" 
                :key="opt" 
                class="filter-option" 
                :class="{ active: filterMethod === opt }"
                @click="handleFilterChange('method', opt)"
              >
                {{ opt }}
              </span>
            </div>
          </div>
          <el-divider style="margin: 15px 0;" />
        </div>

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
            :min-width="getColumnWidth(field.name)"
            show-overflow-tooltip
            sortable="custom"
          >
            <template #default="{ row }">
              <span v-if="row[field.name] !== null && row[field.name] !== undefined">
                {{ row[field.name] }}
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
            @size-change="loadData"
            @current-change="loadData"
          />
        </div>
      </el-card>
    </div>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="refreshDialogVisible"
      title="更新数据"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form label-width="100px">
        <el-form-item label="集合名称">
          <el-input :value="collectionInfo?.display_name || collectionName" disabled />
        </el-form-item>

        <!-- 批量更新等配置 (针对特定集合) -->
        <template v-if="collectionName === 'fund_basic_info'">
          
          <!-- 文件导入 -->
          <el-divider content-position="left">文件导入</el-divider>
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
                  支持 CSV 或 Excel 文件，列结构需包含基金代码、基金名称等字段
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
          
          <!-- 远程同步 -->
          <el-divider content-position="left">远程同步</el-divider>
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
                  :placeholder="collectionName === 'fund_name_em' ? '远程集合名称，默认 fund_name_em' : '远程集合名称，默认 fund_basic_info'"
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
                  placeholder="认证库（authSource），通常为创建该用户时所在的数据库，例如 admin"
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
              {{ remoteSyncStats.synced_count }} 条
            </div>
          </div>

          <!-- 单个更新 -->
          <el-divider content-position="left">单个更新</el-divider>
          <div style="width: 100%">
             <el-input 
               v-model="singleFundCode" 
               placeholder="请输入基金代码（如 000001）"
               clearable
             >
                <template #append>
                   <el-button 
                     @click="refreshData('single')" 
                     :loading="refreshing"
                     :disabled="!singleFundCode || refreshing"
                   >
                     更新单个
                   </el-button>
                </template>
             </el-input>
          </div>

          <!-- 批量更新配置 -->
          <el-divider content-position="left">批量更新配置</el-divider>
          <el-alert
            title="雪球基金详情更新需要较长时间"
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 16px;"
          />
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="每批数量">
                <el-input-number v-model="batchSize" :min="10" :max="200" :step="10" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="并发数">
                <el-input-number v-model="concurrency" :min="1" :max="20" :step="1" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="请求延迟(秒)">
                <el-input-number v-model="delay" :min="0" :max="5" :step="0.1" :precision="1" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
        </template>

        <!-- fund_name_em、fund_purchase_status、fund_etf_spot_em、fund_etf_spot_ths、fund_lof_spot_em、fund_spot_sina、fund_etf_hist_min_em、fund_etf_hist_em、fund_lof_hist_em、fund_hist_sina、fund_open_fund_daily_em、fund_open_fund_info_em 和 fund_money_fund_daily_em 的文件导入和远程同步 -->
        <template v-else-if="collectionName === 'fund_name_em' || collectionName === 'fund_purchase_status' || collectionName === 'fund_etf_spot_em' || collectionName === 'fund_etf_spot_ths' || collectionName === 'fund_lof_spot_em' || collectionName === 'fund_spot_sina' || collectionName === 'fund_etf_hist_min_em' || collectionName === 'fund_etf_hist_em' || collectionName === 'fund_lof_hist_em' || collectionName === 'fund_hist_sina' || collectionName === 'fund_open_fund_daily_em' || collectionName === 'fund_open_fund_info_em' || collectionName === 'fund_money_fund_daily_em'">
          <!-- 文件导入 -->
          <el-divider content-position="left">文件导入</el-divider>
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
                  <span v-if="collectionName === 'fund_name_em'">支持 CSV 或 Excel 文件，列结构需包含基金代码、基金简称等字段</span>
                  <span v-else-if="collectionName === 'fund_purchase_status'">支持 CSV 或 Excel 文件，列结构需包含基金代码、申购状态、赎回状态等字段</span>
                  <span v-else-if="collectionName === 'fund_etf_spot_em'">支持 CSV 或 Excel 文件，列结构需包含代码、名称、最新价、涨跌幅等字段</span>
                  <span v-else-if="collectionName === 'fund_etf_spot_ths'">支持 CSV 或 Excel 文件，列结构需包含基金代码、基金名称、当前单位净值、增长率等字段</span>
                  <span v-else-if="collectionName === 'fund_lof_spot_em'">支持 CSV 或 Excel 文件，列结构需包含代码、名称、最新价、涨跌幅、市值等字段</span>
                  <span v-else-if="collectionName === 'fund_spot_sina'">支持 CSV 或 Excel 文件，列结构需包含代码、名称、最新价、涨跌幅、成交量、基金类型等字段</span>
                  <span v-else-if="collectionName === 'fund_etf_hist_min_em'">支持 CSV 或 Excel 文件，列结构需包含代码、时间、开盘、收盘、最高、最低、成交量、成交额等字段</span>
                  <span v-else-if="collectionName === 'fund_etf_hist_em'">支持 CSV 或 Excel 文件，列结构需包含代码、日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率等字段</span>
                  <span v-else-if="collectionName === 'fund_lof_hist_em'">支持 CSV 或 Excel 文件，列结构需包含代码、日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率等字段</span>
                  <span v-else-if="collectionName === 'fund_hist_sina'">支持 CSV 或 Excel 文件，列结构需包含 code、date、open、high、low、close、volume 等字段</span>
                  <span v-else-if="collectionName === 'fund_open_fund_daily_em'">支持 CSV 或 Excel 文件，列结构需包含基金代码、基金简称、单位净值、累计净值等字段（列名格式如 "2024-01-01-单位净值"）</span>
                  <span v-else-if="collectionName === 'fund_open_fund_info_em'">支持 CSV 或 Excel 文件，列结构需包含日期、基金代码、单位净值、日增长率、累计净值等字段</span>
                  <span v-else-if="collectionName === 'fund_money_fund_daily_em'">支持 CSV 或 Excel 文件，列结构需包含基金代码、基金简称、每万份收益、7日年化收益率等字段</span>
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

          <!-- 远程同步 -->
          <el-divider content-position="left">远程同步</el-divider>
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
                  :placeholder="`远程集合名称，默认 ${collectionName}`"
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
                  placeholder="认证库（authSource），通常为创建该用户时所在的数据库，例如 admin"
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
              {{ remoteSyncStats.synced_count }} 条
            </div>
          </div>

          <!-- fund_open_fund_info_em 特殊配置：添加单个更新和批量更新 -->
          <template v-if="collectionName === 'fund_open_fund_info_em'">
            <!-- 单个更新 -->
            <el-divider content-position="left">单个更新</el-divider>
            <div style="width: 100%">
              <el-input 
                v-model="singleFundCode" 
                placeholder="请输入基金代码（如 000001）"
                clearable
              >
                <template #append>
                  <el-button 
                    @click="refreshData('single')" 
                    :loading="refreshing"
                    :disabled="!singleFundCode || refreshing"
                  >
                    更新单个
                  </el-button>
                </template>
              </el-input>
            </div>

            <!-- 批量更新配置 -->
            <el-divider content-position="left">批量更新配置</el-divider>
            <el-alert
              title="批量更新说明"
              type="info"
              :closable="false"
              style="margin-bottom: 12px;"
            >
              <div>从开放式基金实时行情集合（fund_open_fund_daily_em）获取基金代码列表，并发更新历史行情数据</div>
            </el-alert>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="并发数">
                  <el-input-number v-model="concurrency" :min="1" :max="10" :step="1" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
          </template>
        </template>

        <!-- 指数型基金基本信息更新配置 -->
        <template v-else-if="collectionName === 'fund_info_index_em'">
          <!-- 文件导入 -->
          <el-divider content-position="left">文件导入</el-divider>
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
                  支持 CSV 或 Excel 文件，列结构需包含基金代码、日期等字段
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

          <!-- 远程同步 -->
          <el-divider content-position="left">远程同步</el-divider>
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
                  placeholder="远程集合名称，默认 fund_info_index_em"
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
                  placeholder="认证库（authSource），通常为创建该用户时所在的数据库，例如 admin"
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
              {{ remoteSyncStats.synced_count }} 条
            </div>
          </div>
        </template>

        <!-- ETF/LOF分时行情参数配置 -->
        <template v-if="collectionName === 'fund_etf_hist_min_em' || collectionName === 'fund_lof_hist_min_em'">
          <!-- 单个更新 -->
          <el-divider content-position="left">单个更新</el-divider>
          <div style="width: 100%; margin-bottom: 16px;">
            <el-form label-width="120px">
              <el-form-item label="基金代码">
                <el-input v-model="singleSymbol" placeholder="请输入基金代码（如 513500）" clearable />
              </el-form-item>
              <el-form-item label="时间周期">
                <el-select v-model="singlePeriod" placeholder="选择时间周期" style="width: 100%">
                  <el-option label="1分钟" value="1" />
                  <el-option label="5分钟" value="5" />
                  <el-option label="15分钟" value="15" />
                  <el-option label="30分钟" value="30" />
                  <el-option label="60分钟" value="60" />
                </el-select>
              </el-form-item>
              <el-form-item label="复权方式">
                <el-select v-model="singleAdjust" placeholder="选择复权方式" style="width: 100%">
                  <el-option label="不复权" value="" />
                  <el-option label="前复权" value="qfq" />
                  <el-option label="后复权" value="hfq" />
                </el-select>
              </el-form-item>
              <el-form-item label="开始时间">
                <el-date-picker
                  v-model="singleStartDate"
                  type="datetime"
                  placeholder="选择开始时间"
                  format="YYYY-MM-DD HH:mm:ss"
                  value-format="YYYY-MM-DD HH:mm:ss"
                  style="width: 100%"
                />
              </el-form-item>
              <el-form-item label="结束时间">
                <el-date-picker
                  v-model="singleEndDate"
                  type="datetime"
                  placeholder="选择结束时间"
                  format="YYYY-MM-DD HH:mm:ss"
                  value-format="YYYY-MM-DD HH:mm:ss"
                  style="width: 100%"
                />
              </el-form-item>
            </el-form>
            <el-button
              type="primary"
              @click="refreshData('single')"
              :loading="refreshing"
              :disabled="!singleSymbol || refreshing"
            >
              更新单个基金
            </el-button>
          </div>

          <!-- 批量更新配置 -->
          <el-divider content-position="left">批量更新配置</el-divider>
          <div style="width: 100%; margin-bottom: 16px;">
            <el-form label-width="120px">
              <el-form-item label="时间周期">
                <el-select v-model="batchPeriod" placeholder="选择时间周期" style="width: 100%">
                  <el-option label="1分钟" value="1" />
                  <el-option label="5分钟（推荐）" value="5" />
                  <el-option label="15分钟" value="15" />
                  <el-option label="30分钟" value="30" />
                  <el-option label="60分钟" value="60" />
                </el-select>
              </el-form-item>
              <el-form-item label="复权方式">
                <el-select v-model="batchAdjust" placeholder="选择复权方式" style="width: 100%">
                  <el-option label="不复权" value="" />
                  <el-option label="前复权" value="qfq" />
                  <el-option label="后复权（推荐）" value="hfq" />
                </el-select>
              </el-form-item>
              <el-form-item label="并发数">
                <el-input-number v-model="batchConcurrency" :min="1" :max="10" :step="1" style="width: 100%" />
              </el-form-item>
            </el-form>
            <el-alert
              title="批量更新说明"
              type="info"
              :closable="false"
              style="margin-bottom: 12px;"
            >
              <div style="font-size: 12px; line-height: 1.6;">
                <p>• 自动从{{ collectionName === 'fund_etf_hist_min_em' ? 'ETF基金实时行情' : 'LOF基金实时行情' }}集合获取基金代码</p>
                <p>• 1分钟数据仅返回近5个交易日且不复权</p>
                <p>• 其他周期支持复权，建议使用后复权</p>
                <p>• 数据达到1000条自动保存一次，退出时不足1000条也会保存</p>
              </div>
            </el-alert>
          </div>
        </template>

        <!-- 基金类型选择（仅对fund_spot_sina显示） -->
        <template v-if="collectionName === 'fund_spot_sina'">
          <el-divider content-position="left">基金类型选择</el-divider>
          <div style="margin-bottom: 16px;">
            <div style="margin-bottom: 8px; font-weight: 500; color: #606266;">更新类型</div>
            <el-select v-model="selectedFundType" placeholder="请选择基金类型" style="width: 100%">
              <el-option label="全部更新（封闭式+ETF+LOF）" value="全部" />
              <el-option label="封闭式基金" value="封闭式基金" />
              <el-option label="ETF基金" value="ETF基金" />
              <el-option label="LOF基金" value="LOF基金" />
            </el-select>
          </div>
          <el-alert
            title="提示"
            type="info"
            :closable="false"
            style="margin-bottom: 16px;"
          >
            <template #default>
              <div style="font-size: 12px; line-height: 1.6;">
                <p><strong>全部更新</strong>：一次性获取三种类型的所有基金数据（推荐）</p>
                <p><strong>单个更新</strong>：仅获取选定类型的基金数据</p>
              </div>
            </template>
          </el-alert>
        </template>

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
        
        <el-alert
          title="更新说明"
          type="warning"
          :closable="false"
          style="margin-bottom: 16px; margin-top: 16px;"
        >
          <template #default>
            <div style="font-size: 12px; line-height: 1.6;">
              <p v-if="collectionName === 'fund_name_em'">将从东方财富网获取所有基金的基本信息数据</p>
              <p v-else-if="collectionName === 'fund_basic_info'">将从雪球获取所有基金的详细基本信息数据（fund_individual_basic_info_xq接口）</p>
              <p v-else-if="collectionName === 'fund_info_index_em'">将从东方财富网获取指数型基金的基本信息数据（fund_info_index_em接口）</p>
              <p v-else-if="collectionName === 'fund_purchase_status'">将从东方财富网获取所有基金的申购赎回状态数据（fund_purchase_em接口）</p>
              <p v-else-if="collectionName === 'fund_open_fund_daily_em'">将从东方财富网一次性获取所有开放式基金的实时净值数据（fund_open_fund_daily_em接口），每个交易日16:00-23:00更新当日最新数据</p>
              <p v-else-if="collectionName === 'fund_open_fund_info_em'">支持单个更新和批量更新开放式基金历史行情数据。单个更新：获取指定基金的单位净值走势和累计净值走势。批量更新：从fund_open_fund_daily_em集合获取基金代码列表后批量更新（fund_open_fund_info_em接口）</p>
              <p v-else-if="collectionName === 'fund_money_fund_daily_em'">将从东方财富网一次性获取所有货币型基金的实时行情数据（fund_money_fund_daily_em接口），包括每万份收益、7日年化收益率等指标</p>
              <p v-else-if="collectionName === 'fund_spot_sina'">将从新浪财经获取{{ selectedFundType === '全部' ? '三种类型' : selectedFundType }}的实时行情数据（fund_etf_category_sina接口）</p>
              <p v-else-if="collectionName === 'fund_etf_hist_min_em'">支持单个更新和批量更新ETF基金分时行情数据（fund_etf_hist_min_em接口）</p>
              <p v-else-if="collectionName === 'fund_lof_hist_min_em'">支持单个更新和批量更新LOF基金分时行情数据（fund_lof_hist_min_em接口）</p>
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
          :disabled="refreshing"
        >
          {{ refreshing ? '更新中...' : '开始更新' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 数据概览对话框 -->
    <el-dialog
      v-model="overviewDialogVisible"
      title="数据概览"
      width="600px"
      :close-on-click-modal="false"
    >
      <div style="padding: 10px;">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="集合名称" label-align="right">
            {{ currentCollectionInfo.name }}
          </el-descriptions-item>
          <el-descriptions-item label="显示名称" label-align="right">
            {{ currentCollectionInfo.displayName }}
          </el-descriptions-item>
          <el-descriptions-item label="数据总数" label-align="right">
            {{ formatNumber(stats?.total_count || 0) }} 条
          </el-descriptions-item>
          <el-descriptions-item label="字段数量" label-align="right">
            {{ currentCollectionInfo.fieldCount }} 个
          </el-descriptions-item>
          <el-descriptions-item label="最后更新" label-align="right" :span="2">
            {{ stats?.latest_date || stats?.latest_time || '暂无数据' }}
          </el-descriptions-item>
          <el-descriptions-item label="数据来源" label-align="right" :span="2">
            <el-link :href="currentCollectionInfo.dataSource" target="_blank" type="primary" v-if="currentCollectionInfo.dataSource !== '暂无'">
              {{ currentCollectionInfo.dataSource }}
            </el-link>
            <span v-else>{{ currentCollectionInfo.dataSource }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="描述" label-align="right" :span="2">
            {{ collectionInfo?.description || `数据集合：${collectionName}` }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="overviewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Box, Refresh, Search, Download, Delete, QuestionFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fundsApi } from '@/api/funds'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import dayjs from 'dayjs'

use([CanvasRenderer, PieChart, GridComponent, TooltipComponent, LegendComponent])

const route = useRoute()
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

// 指数型基金筛选
const filterTarget = ref('全部')
const filterMethod = ref('全部')
const targetOptions = [
  '全部', '沪深指数', '行业主题', '大盘指数', '中盘指数', '小盘指数', '股票指数', '债券指数'
]
const methodOptions = [
  '全部', '被动指数型', '增强指数型'
]
// const filterAbnormal = ref(true) // 已移除
const filterCompany = ref('全部')
const companyOptions = ref<string[]>([])

const loadCompanies = async () => {
  try {
    const res = await fundsApi.getFundCompanies()
    if (res.success && res.data) {
      companyOptions.value = res.data
    }
  } catch (e) {
    console.error('加载基金公司列表失败:', e)
  }
}

const handleFilterChange = (type: 'target' | 'method' | 'company', value: string) => {
  if (type === 'target') {
    filterTarget.value = value
  } else if (type === 'method') {
    filterMethod.value = value
  } else if (type === 'company') {
    filterCompany.value = value
  }
  page.value = 1 // 重置页码
  loadData()
}

// 排序条件
const sortBy = ref('')
const sortDir = ref<'asc' | 'desc'>('desc')

// 统计数据
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)

// 计算时间跨度
const dataDuration = computed(() => {
  if (!stats.value?.earliest_date || !stats.value?.latest_date) return '-'
  const start = dayjs(stats.value.earliest_date)
  const end = dayjs(stats.value.latest_date)
  const days = end.diff(start, 'day')
  if (days < 365) return `${days}天`
  return `${(days / 365).toFixed(1)}年`
})

// 是否有图表数据
const hasCharts = computed(() => {
  // fund_purchase_status 有申购赎回状态图表
  if (collectionName.value === 'fund_purchase_status') {
    return stats.value && (stats.value.purchase_status_stats || stats.value.redeem_status_stats)
  }
  // fund_etf_spot_em 有涨跌分布和成交额TOP图表
  if (collectionName.value === 'fund_etf_spot_em') {
    return stats.value && stats.value.total_count > 0
  }
  // fund_etf_spot_ths 有涨跌分布、基金类型、涨跌幅TOP、申赎状态图表
  if (collectionName.value === 'fund_etf_spot_ths') {
    return stats.value && stats.value.total_count > 0
  }
  // fund_lof_spot_em 有涨跌分布、成交额TOP、涨跌幅TOP、市值分布图表
  if (collectionName.value === 'fund_lof_spot_em') {
    return stats.value && stats.value.total_count > 0
  }
  // fund_spot_sina 有涨跌分布、基金类型、成交额TOP、涨跌幅TOP图表
  if (collectionName.value === 'fund_spot_sina') {
    return stats.value && stats.value.total_count > 0
  }
  // 其他集合有type_stats图表
  return stats.value && stats.value.type_stats && stats.value.type_stats.length > 0
})

// 颜色池
const colorPalette = [
  '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
  '#36CBCB', '#975FE4', '#F2637B', '#FAD337', '#4DCB73'
]

// 基金类型分布数据 - Progress Bar
const categoryDistribution = computed(() => {
  if (!stats.value || !stats.value.type_stats) return []
  
  const total = stats.value.type_stats.reduce((sum: number, item: any) => sum + item.count, 0)
  
  return stats.value.type_stats.map((item: any, index: number) => ({
    category: item.type || '未分类',
    count: item.count,
    percentage: ((item.count / total) * 100).toFixed(1),
    color: colorPalette[index % colorPalette.length]
  })).sort((a: any, b: any) => b.count - a.count)
})

// 饼图配置
const typePieOption = computed(() => {
  if (!stats.value || !stats.value.type_stats) return null
  
  const chartData = stats.value.type_stats.map((item: any, index: number) => ({
    name: item.type || '未分类',
    value: item.count,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll'
    },
    series: [
      {
        name: '基金类型',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: chartData
      }
    ]
  }
})

// 申购状态饼图配置
const purchaseStatusPieOption = computed(() => {
  if (!stats.value || !stats.value.purchase_status_stats) return null
  
  const chartData = stats.value.purchase_status_stats.map((item: any, index: number) => ({
    name: item.status || '未知',
    value: item.count,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll'
    },
    series: [
      {
        name: '申购状态',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: chartData
      }
    ]
  }
})

// 赎回状态饼图配置
const redeemStatusPieOption = computed(() => {
  if (!stats.value || !stats.value.redeem_status_stats) return null
  
  const chartData = stats.value.redeem_status_stats.map((item: any, index: number) => ({
    name: item.status || '未知',
    value: item.count,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll'
    },
    series: [
      {
        name: '赎回状态',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: chartData
      }
    ]
  }
})

// ETF涨跌分布饼图配置
const etfRiseFallPieOption = computed(() => {
  if (!stats.value || stats.value.total_count === 0) return null
  
  const chartData = [
    {
      name: '上涨',
      value: stats.value.rise_count || 0,
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '下跌',
      value: stats.value.fall_count || 0,
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '平盘',
      value: stats.value.flat_count || 0,
      itemStyle: { color: '#909399' }
    }
  ]
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '涨跌分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
})

// ETF成交额TOP10柱状图配置
const etfVolumeBarOption = computed(() => {
  if (!stats.value || !stats.value.top_volume || stats.value.top_volume.length === 0) return null
  
  const names = stats.value.top_volume.map((item: any) => item.name || item.code)
  const volumes = stats.value.top_volume.map((item: any) => (item.volume / 100000000).toFixed(2)) // 转换为亿元
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>成交额: ${item.value}亿元`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '成交额(亿元)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 8 ? value.substring(0, 8) + '...' : value
        }
      }
    },
    series: [
      {
        name: '成交额',
        type: 'bar',
        data: volumes,
        itemStyle: {
          color: '#409EFF',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}亿'
        }
      }
    ]
  }
})

// 同花顺ETF涨跌分布饼图配置
const thsRiseFallPieOption = computed(() => {
  if (!stats.value || stats.value.total_count === 0) return null
  
  const chartData = [
    {
      name: '上涨',
      value: stats.value.rise_count || 0,
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '下跌',
      value: stats.value.fall_count || 0,
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '平盘',
      value: stats.value.flat_count || 0,
      itemStyle: { color: '#909399' }
    }
  ]
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '涨跌分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
})

// 同花顺ETF基金类型分布饼图配置
const thsTypePieOption = computed(() => {
  if (!stats.value || !stats.value.type_stats || stats.value.type_stats.length === 0) return null
  
  const chartData = stats.value.type_stats.map((item: any, index: number) => ({
    name: item.type || '未知',
    value: item.count,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll'
    },
    series: [
      {
        name: '基金类型',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
})

// 同花顺ETF涨幅TOP10柱状图配置
const thsGainersBarOption = computed(() => {
  if (!stats.value || !stats.value.top_gainers || stats.value.top_gainers.length === 0) return null
  
  const names = stats.value.top_gainers.map((item: any) => item.name || item.code)
  const rates = stats.value.top_gainers.map((item: any) => item.rate)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>涨幅: ${item.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '涨幅(%)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 8 ? value.substring(0, 8) + '...' : value
        }
      }
    },
    series: [
      {
        name: '涨幅',
        type: 'bar',
        data: rates,
        itemStyle: {
          color: '#F56C6C',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }
})

// 同花顺ETF跌幅TOP10柱状图配置
const thsLosersBarOption = computed(() => {
  if (!stats.value || !stats.value.top_losers || stats.value.top_losers.length === 0) return null
  
  const names = stats.value.top_losers.map((item: any) => item.name || item.code)
  const rates = stats.value.top_losers.map((item: any) => item.rate)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>跌幅: ${item.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '跌幅(%)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 8 ? value.substring(0, 8) + '...' : value
        }
      }
    },
    series: [
      {
        name: '跌幅',
        type: 'bar',
        data: rates,
        itemStyle: {
          color: '#67C23A',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }
})

// LOF基金涨跌分布饼图配置
const lofRiseFallPieOption = computed(() => {
  if (!stats.value || stats.value.total_count === 0) return null
  
  const chartData = [
    {
      name: '上涨',
      value: stats.value.rise_count || 0,
      itemStyle: { color: '#F56C6C' }
    },
    {
      name: '下跌',
      value: stats.value.fall_count || 0,
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '平盘',
      value: stats.value.flat_count || 0,
      itemStyle: { color: '#909399' }
    }
  ]
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '涨跌分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
})

// LOF基金成交额TOP10柱状图配置
const lofVolumeBarOption = computed(() => {
  if (!stats.value || !stats.value.top_volume || stats.value.top_volume.length === 0) return null
  
  const names = stats.value.top_volume.map((item: any) => item.name || item.code)
  const amounts = stats.value.top_volume.map((item: any) => (item.amount / 100000000).toFixed(2))
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>成交额: ${item.value}亿`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '成交额(亿)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 10 ? value.substring(0, 10) + '...' : value
        }
      }
    },
    series: [
      {
        name: '成交额',
        type: 'bar',
        data: amounts,
        itemStyle: {
          color: '#409EFF',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}亿'
        }
      }
    ]
  }
})

// LOF基金涨幅TOP10柱状图配置
const lofGainersBarOption = computed(() => {
  if (!stats.value || !stats.value.top_gainers || stats.value.top_gainers.length === 0) return null
  
  const names = stats.value.top_gainers.map((item: any) => item.name || item.code)
  const rates = stats.value.top_gainers.map((item: any) => item.rate)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>涨幅: ${item.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '涨幅(%)'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true,
      axisLabel: {
        formatter: (value: string) => {
          return value.length > 10 ? value.substring(0, 10) + '...' : value
        }
      }
    },
    series: [
      {
        name: '涨幅',
        type: 'bar',
        data: rates,
        itemStyle: {
          color: '#F56C6C',
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}%'
        }
      }
    ]
  }
})

// LOF基金市值分布饼图配置
const lofMarketCapPieOption = computed(() => {
  if (!stats.value || !stats.value.market_cap_stats || stats.value.market_cap_stats.length === 0) return null
  
  const chartData = stats.value.market_cap_stats.map((item: any, index: number) => ({
    name: item.range || '未知',
    value: item.count,
    itemStyle: { color: colorPalette[index % colorPalette.length] }
  }))
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '市值分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
})

// 更新数据相关
const refreshDialogVisible = ref(false)
const refreshing = ref(false)
const currentTaskId = ref('')
const progressPercentage = ref(0)
const progressStatus = ref<'success' | 'exception' | 'warning' | ''>('')
const progressMessage = ref('')
let progressTimer: NodeJS.Timeout | null = null

// 批量更新配置
const batchSize = ref(50)
const concurrency = ref(5)
const delay = ref(0.1)
const singleFundCode = ref('')

// 指数型基金更新参数
const indexSymbol = ref('全部')

// 新浪基金类型选择
const selectedFundType = ref('全部')
const indexIndicator = ref('全部')
const indexSymbolOptions = [
  { label: '全部', value: '全部' },
  { label: '沪深指数', value: '沪深指数' },
  { label: '行业主题', value: '行业主题' },
  { label: '大盘指数', value: '大盘指数' },
  { label: '中盘指数', value: '中盘指数' },
  { label: '小盘指数', value: '小盘指数' },
  { label: '股票指数', value: '股票指数' },
  { label: '债券指数', value: '债券指数' }
]
const indexIndicatorOptions = [
  { label: '全部', value: '全部' },
  { label: '被动指数型', value: '被动指数型' },
  { label: '增强指数型', value: '增强指数型' }
]

// ETF/LOF分时行情参数 - 单个更新
const singleSymbol = ref('')
const singlePeriod = ref('5')
const singleAdjust = ref('hfq')
const singleStartDate = ref('')
const singleEndDate = ref('')

// ETF/LOF分时行情参数 - 批量更新
const batchPeriod = ref('5')
const batchAdjust = ref('hfq')
const batchConcurrency = ref(5)

// 文件导入相关
const uploadRef = ref()
const importFiles = ref<any[]>([])
const importing = ref(false)

// 远程同步相关
const remoteSyncHost = ref('')
const remoteSyncDbType = ref('mongodb')
const remoteSyncCollection = ref('')
const remoteSyncUsername = ref('')
const remoteSyncPassword = ref('')
const remoteSyncAuthSource = ref('admin')
const remoteSyncBatchSize = ref(1000)
const remoteSyncing = ref(false)
const remoteSyncStats = ref<any>(null)

// 清空数据相关
const clearing = ref(false)

// 数据概览对话框
const overviewDialogVisible = ref(false)

// 集合固定信息映射
const collectionStaticInfo: Record<string, any> = {
  fund_name_em: {
    name: 'fund_name_em',
    displayName: '基金基本信息',
    fieldCount: 5,
    dataSource: 'http://fund.eastmoney.com/fund.html'
  },
  fund_basic_info: {
    name: 'fund_basic_info',
    displayName: '雪球基金基本信息',
    fieldCount: 10,
    dataSource: 'https://xueqiu.com/'
  },
  fund_info_index_em: {
    name: 'fund_info_index_em',
    displayName: '指数型基金基本信息',
    fieldCount: 18,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_purchase_status: {
    name: 'fund_purchase_status',
    displayName: '基金申购状态',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_spot_em: {
    name: 'fund_etf_spot_em',
    displayName: 'ETF基金实时行情-东财',
    fieldCount: 37,
    dataSource: 'https://quote.eastmoney.com/center/gridlist.html#fund_etf'
  },
  fund_etf_spot_ths: {
    name: 'fund_etf_spot_ths',
    displayName: 'ETF基金实时行情-同花顺',
    fieldCount: 15,
    dataSource: 'http://q.10jqka.com.cn/'
  },
  fund_lof_spot_em: {
    name: 'fund_lof_spot_em',
    displayName: 'LOF基金实时行情-东财',
    fieldCount: 15,
    dataSource: 'https://quote.eastmoney.com/center/gridlist.html#fund_lof'
  },
  fund_spot_sina: {
    name: 'fund_spot_sina',
    displayName: '基金实时行情-新浪',
    fieldCount: 15,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_etf_hist_min_em: {
    name: 'fund_etf_hist_min_em',
    displayName: 'ETF基金分时行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/sz159707.html'
  },
  fund_lof_hist_min_em: {
    name: 'fund_lof_hist_min_em',
    displayName: 'LOF基金分时行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_etf_hist_em: {
    name: 'fund_etf_hist_em',
    displayName: 'ETF基金历史行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_lof_hist_em: {
    name: 'fund_lof_hist_em',
    displayName: 'LOF基金历史行情-东财',
    fieldCount: 14,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_hist_sina: {
    name: 'fund_hist_sina',
    displayName: '基金历史行情-新浪',
    fieldCount: 7,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_open_fund_daily_em: {
    name: 'fund_open_fund_daily_em',
    displayName: '开放式基金实时行情-东方财富',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1'
  },
  fund_open_fund_info_em: {
    name: 'fund_open_fund_info_em',
    displayName: '开放式基金历史行情-东方财富',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_money_fund_daily_em: {
    name: 'fund_money_fund_daily_em',
    displayName: '货币型基金实时行情-东方财富',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_money_fund_info_em: {
    name: 'fund_money_fund_info_em',
    displayName: '货币型基金历史行情-东方财富',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_financial_fund_daily_em: {
    name: 'fund_financial_fund_daily_em',
    displayName: '理财型基金实时行情-东方财富',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_financial_fund_info_em: {
    name: 'fund_financial_fund_info_em',
    displayName: '理财型基金历史行情-东方财富',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_graded_fund_daily_em: {
    name: 'fund_graded_fund_daily_em',
    displayName: '分级基金实时数据-东方财富',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_fund_daily_em: {
    name: 'fund_etf_fund_daily_em',
    displayName: '场内交易基金实时数据-东方财富',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_graded_fund_info_em: {
    name: 'fund_graded_fund_info_em',
    displayName: '分级基金历史数据-东方财富',
    fieldCount: 8,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_hk_hist_em: {
    name: 'fund_hk_hist_em',
    displayName: '香港基金-历史数据',
    fieldCount: 13,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_fund_info_em: {
    name: 'fund_etf_fund_info_em',
    displayName: '场内交易基金-历史行情',
    fieldCount: 8,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_etf_dividend_sina: {
    name: 'fund_etf_dividend_sina',
    displayName: '基金累计分红-新浪',
    fieldCount: 6,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_fh_em: {
    name: 'fund_fh_em',
    displayName: '基金分红-东财',
    fieldCount: 8,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_cf_em: {
    name: 'fund_cf_em',
    displayName: '基金拆分-东方财富',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_fh_rank_em: {
    name: 'fund_fh_rank_em',
    displayName: '基金分红排行-东方财富',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_open_fund_rank_em: {
    name: 'fund_open_fund_rank_em',
    displayName: '开放式基金排行-东方财富',
    fieldCount: 22,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_exchange_rank_em: {
    name: 'fund_exchange_rank_em',
    displayName: '场内交易基金排行-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_money_rank_em: {
    name: 'fund_money_rank_em',
    displayName: '货币型基金排行-东财',
    fieldCount: 23,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_lcx_rank_em: {
    name: 'fund_lcx_rank_em',
    displayName: '理财基金排行-东财',
    fieldCount: 22,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_hk_rank_em: {
    name: 'fund_hk_rank_em',
    displayName: '香港基金排行-东财',
    fieldCount: 23,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_individual_achievement_xq: {
    name: 'fund_individual_achievement_xq',
    displayName: '基金业绩-雪球',
    fieldCount: 12,
    dataSource: 'https://xueqiu.com/'
  },
  fund_value_estimation_em: {
    name: 'fund_value_estimation_em',
    displayName: '净值估算-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_individual_analysis_xq: {
    name: 'fund_individual_analysis_xq',
    displayName: '基金数据分析-雪球',
    fieldCount: 11,
    dataSource: 'https://xueqiu.com/'
  },
  fund_individual_profit_probability_xq: {
    name: 'fund_individual_profit_probability_xq',
    displayName: '基金盈利概率-雪球',
    fieldCount: 9,
    dataSource: 'https://xueqiu.com/'
  },
  fund_individual_detail_hold_xq: {
    name: 'fund_individual_detail_hold_xq',
    displayName: '基金持仓资产比例-雪球',
    fieldCount: 11,
    dataSource: 'https://xueqiu.com/'
  },
  fund_overview_em: {
    name: 'fund_overview_em',
    displayName: '基金基本概况-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_fee_em: {
    name: 'fund_fee_em',
    displayName: '基金交易费率-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_individual_detail_info_xq: {
    name: 'fund_individual_detail_info_xq',
    displayName: '基金交易规则-雪球',
    fieldCount: 14,
    dataSource: 'https://xueqiu.com/'
  },
  fund_portfolio_hold_em: {
    name: 'fund_portfolio_hold_em',
    displayName: '基金持仓-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_portfolio_bond_hold_em: {
    name: 'fund_portfolio_bond_hold_em',
    displayName: '债券持仓-东财',
    fieldCount: 15,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_portfolio_industry_allocation_em: {
    name: 'fund_portfolio_industry_allocation_em',
    displayName: '行业配置-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_portfolio_change_em: {
    name: 'fund_portfolio_change_em',
    displayName: '重大变动-东财',
    fieldCount: 16,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_all_em: {
    name: 'fund_rating_all_em',
    displayName: '基金评级总汇-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_sh_em: {
    name: 'fund_rating_sh_em',
    displayName: '上海证券评级-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_zs_em: {
    name: 'fund_rating_zs_em',
    displayName: '招商证券评级-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_rating_ja_em: {
    name: 'fund_rating_ja_em',
    displayName: '济安金信评级-东财',
    fieldCount: 21,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_manager_em: {
    name: 'fund_manager_em',
    displayName: '基金经理-东财',
    fieldCount: 13,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_new_found_em: {
    name: 'fund_new_found_em',
    displayName: '新发基金-东财',
    fieldCount: 12,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_scale_open_sina: {
    name: 'fund_scale_open_sina',
    displayName: '开放式基金规模-新浪',
    fieldCount: 12,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_scale_close_sina: {
    name: 'fund_scale_close_sina',
    displayName: '封闭式基金规模-新浪',
    fieldCount: 12,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_scale_structured_sina: {
    name: 'fund_scale_structured_sina',
    displayName: '分级子基金规模-新浪',
    fieldCount: 12,
    dataSource: 'http://vip.stock.finance.sina.com.cn/'
  },
  fund_aum_em: {
    name: 'fund_aum_em',
    displayName: '基金规模详情-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_aum_trend_em: {
    name: 'fund_aum_trend_em',
    displayName: '基金规模走势-东财',
    fieldCount: 11,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_aum_hist_em: {
    name: 'fund_aum_hist_em',
    displayName: '基金公司历年管理规模-东财',
    fieldCount: 14,
    dataSource: 'http://fund.eastmoney.com/'
  },
  reits_realtime_em: {
    name: 'reits_realtime_em',
    displayName: 'REITs实时行情-东财',
    fieldCount: 17,
    dataSource: 'https://quote.eastmoney.com/'
  },
  reits_hist_em: {
    name: 'reits_hist_em',
    displayName: 'REITs历史行情-东财',
    fieldCount: 12,
    dataSource: 'https://quote.eastmoney.com/'
  },
  fund_report_stock_cninfo: {
    name: 'fund_report_stock_cninfo',
    displayName: '基金重仓股-巨潮',
    fieldCount: 15,
    dataSource: 'http://www.cninfo.com.cn/'
  },
  fund_report_industry_allocation_cninfo: {
    name: 'fund_report_industry_allocation_cninfo',
    displayName: '基金行业配置-巨潮',
    fieldCount: 15,
    dataSource: 'http://www.cninfo.com.cn/'
  },
  fund_report_asset_allocation_cninfo: {
    name: 'fund_report_asset_allocation_cninfo',
    displayName: '基金资产配置-巨潮',
    fieldCount: 13,
    dataSource: 'http://www.cninfo.com.cn/'
  },
  fund_scale_change_em: {
    name: 'fund_scale_change_em',
    displayName: '规模变动-东财',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_hold_structure_em: {
    name: 'fund_hold_structure_em',
    displayName: '持有人结构-东财',
    fieldCount: 10,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_stock_position_lg: {
    name: 'fund_stock_position_lg',
    displayName: '股票型基金仓位-乐咕乐股',
    fieldCount: 5,
    dataSource: 'https://www.legulegu.com/'
  },
  fund_balance_position_lg: {
    name: 'fund_balance_position_lg',
    displayName: '平衡混合型基金仓位-乐咕乐股',
    fieldCount: 5,
    dataSource: 'https://www.legulegu.com/'
  },
  fund_linghuo_position_lg: {
    name: 'fund_linghuo_position_lg',
    displayName: '灵活配置型基金仓位-乐咕乐股',
    fieldCount: 5,
    dataSource: 'https://www.legulegu.com/'
  },
  fund_announcement_dividend_em: {
    name: 'fund_announcement_dividend_em',
    displayName: '基金公告分红配送-东财',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_announcement_report_em: {
    name: 'fund_announcement_report_em',
    displayName: '基金公告定期报告-东财',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  },
  fund_announcement_personnel_em: {
    name: 'fund_announcement_personnel_em',
    displayName: '基金公告人事调整-东财',
    fieldCount: 6,
    dataSource: 'http://fund.eastmoney.com/'
  }
}

// 显示数据概览对话框
const showOverviewDialog = () => {
  overviewDialogVisible.value = true
}

// 获取当前集合的固定信息
const currentCollectionInfo = computed(() => {
  return collectionStaticInfo[collectionName.value] || {
    name: collectionName.value,
    displayName: collectionInfo.value?.display_name || collectionName.value,
    fieldCount: fields.value.length,
    dataSource: '暂无'
  }
})

// 格式化数字
const formatNumber = (num: number): string => {
  return num.toLocaleString('zh-CN')
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载集合信息
    const collectionsRes = await fundsApi.getCollections()
    if (collectionsRes.success && collectionsRes.data) {
      collectionInfo.value = collectionsRes.data.find((c: any) => c.name === collectionName.value)
    }

    // 加载统计数据
    const statsRes = await fundsApi.getCollectionStats(collectionName.value)
    if (statsRes.success && statsRes.data) {
      stats.value = statsRes.data
    }

    // 加载数据
    const dataRes = await fundsApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
      tracking_target: collectionName.value === 'fund_info_index_em' ? filterTarget.value : undefined,
      tracking_method: collectionName.value === 'fund_info_index_em' ? filterMethod.value : undefined,
      fund_company: collectionName.value === 'fund_info_index_em' ? filterCompany.value : undefined,
    })
    
    if (dataRes.success && dataRes.data) {
      items.value = dataRes.data.items || []
      
      // 调整字段顺序：将系统字段移到最后
      const allFields = dataRes.data.fields || []
      const metaFields = ['code', 'endpoint', 'source', 'updated_at']
      const mainFields = allFields.filter((f: any) => !metaFields.includes(f.name))
      const metaFieldsData = allFields.filter((f: any) => metaFields.includes(f.name))
      fields.value = [...mainFields, ...metaFieldsData]
      
      total.value = dataRes.data.total || 0
    } else {
      ElMessage.error('加载数据失败')
    }
  } catch (error: any) {
    console.error('加载数据失败:', error)
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

// 排序处理
const handleSortChange = ({ prop, order }: any) => {
  if (!order) {
    sortBy.value = ''
    sortDir.value = 'desc'
  } else {
    sortBy.value = prop
    sortDir.value = order === 'ascending' ? 'asc' : 'desc'
  }
  loadData()
}

// 获取列宽
const getColumnWidth = (fieldName: string): number => {
  if (fieldName.includes('代码') || fieldName.includes('code')) return 120
  if (fieldName.includes('类型') || fieldName.includes('type')) return 100
  if (fieldName.includes('简称') || fieldName.includes('name')) return 200
  if (fieldName.includes('全称')) return 300
  return 150
}

// 处理更新数据
const handleRefreshData = () => {
  refreshDialogVisible.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = ''
}

// 更新数据
const refreshData = async (mode: string = 'batch') => {
  // 支持 fund_name_em / fund_basic_info / fund_info_index_em / fund_purchase_status / fund_etf_spot_em / fund_etf_spot_ths / fund_lof_spot_em / fund_spot_sina / fund_etf_hist_min_em / fund_etf_hist_em / fund_lof_hist_em / fund_hist_sina / fund_open_fund_daily_em / fund_open_fund_info_em / fund_money_fund_daily_em / fund_money_fund_info_em / fund_financial_fund_daily_em / fund_financial_fund_info_em / fund_graded_fund_daily_em / fund_etf_fund_daily_em 集合的更新
  const supportedCollections = ['fund_name_em', 'fund_basic_info', 'fund_info_index_em', 'fund_purchase_status', 'fund_etf_spot_em', 'fund_etf_spot_ths', 'fund_lof_spot_em', 'fund_spot_sina', 'fund_etf_hist_min_em', 'fund_etf_hist_em', 'fund_lof_hist_em', 'fund_hist_sina', 'fund_open_fund_daily_em', 'fund_open_fund_info_em', 'fund_money_fund_daily_em', 'fund_money_fund_info_em', 'fund_financial_fund_daily_em', 'fund_financial_fund_info_em', 'fund_graded_fund_daily_em', 'fund_etf_fund_daily_em']
  if (!supportedCollections.includes(collectionName.value)) {
    ElMessage.warning('该集合暂不支持自动更新')
    return
  }

  refreshing.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  
  try {
    // 构建参数
    const params: any = {}
    
    // ETF/LOF分时行情的参数处理
    if (collectionName.value === 'fund_etf_hist_min_em' || collectionName.value === 'fund_lof_hist_min_em') {
      if (mode === 'single') {
        // 单个更新模式
        if (!singleSymbol.value) {
          ElMessage.warning('请输入基金代码')
          return
        }
        params.symbol = singleSymbol.value
        params.period = singlePeriod.value
        params.adjust = singleAdjust.value
        if (singleStartDate.value) params.start_date = singleStartDate.value
        if (singleEndDate.value) params.end_date = singleEndDate.value
      } else {
        // 批量更新模式
        params.period = batchPeriod.value
        params.adjust = batchAdjust.value
        params.concurrency = batchConcurrency.value
      }
    }
    if (collectionName.value === 'fund_basic_info') {
      if (mode === 'single' && singleFundCode.value) {
        params.fund_code = singleFundCode.value
      } else {
        params.batch_size = batchSize.value
        params.concurrency = concurrency.value
        params.delay = delay.value
      }
    } else if (collectionName.value === 'fund_info_index_em') {
      params.symbol = indexSymbol.value || '全部'
      params.indicator = indexIndicator.value || '全部'
    } else if (collectionName.value === 'fund_spot_sina') {
      params.symbol = selectedFundType.value || '全部'
    } else if (collectionName.value === 'fund_open_fund_info_em') {
      if (mode === 'single' && singleFundCode.value) {
        params.fund_code = singleFundCode.value
      } else {
        // 批量更新模式
        params.concurrency = concurrency.value
      }
    }
    
    const res = await fundsApi.refreshCollectionData(collectionName.value, params)
    
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
    ElMessage.error(e.message || '更新数据失败')
    progressStatus.value = 'exception'
    refreshing.value = false
  }
}

// 轮询任务状态
const pollTaskStatus = async () => {
  let pollCount = 0
  const maxPollCount = 300 // 最多轮询5分钟（300秒）
  
  progressTimer = setInterval(async () => {
    try {
      pollCount++
      
      // 超时检查
      if (pollCount > maxPollCount) {
        if (progressTimer) {
          clearInterval(progressTimer)
          progressTimer = null
        }
        progressStatus.value = 'warning'
        progressMessage.value = '任务超时，请刷新页面查看结果'
        ElMessage.warning('任务执行时间过长，请刷新页面查看结果')
        refreshing.value = false
        return
      }
      
      const res = await fundsApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
      
      if (res.success && res.data) {
        const task = res.data
        
        // 更新进度
        if (task.progress !== undefined && task.total !== undefined) {
          progressPercentage.value = Math.round((task.progress / task.total) * 100)
        }
        progressMessage.value = task.message || ''
        
        // 检查是否完成
        if (task.status === 'success') {
          progressStatus.value = 'success'
          progressPercentage.value = 100
          
          let message = task.message || '数据更新成功'
          if (task.result && task.result.saved !== undefined) {
            message = `成功更新 ${task.result.saved} 条数据`
          }
          
          progressMessage.value = message + ' - 正在刷新数据...'
          
          // 清除轮询定时器
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          
          // 刷新页面数据
          await loadData()
          
          // 数据刷新完成后更新提示信息，但不关闭对话框
          progressMessage.value = message + ' - 数据已刷新，请手动关闭对话框'
          ElMessage.success(message)
          refreshing.value = false
          
        } else if (task.status === 'failed') {
          progressStatus.value = 'exception'
          ElMessage.error(task.error || '数据更新失败')
          
          if (progressTimer) {
            clearInterval(progressTimer)
            progressTimer = null
          }
          refreshing.value = false
        }
      }
    } catch (e) {
      if (progressTimer) {
        clearInterval(progressTimer)
        progressTimer = null
      }
      progressStatus.value = 'exception'
      progressMessage.value = '查询任务状态失败'
      refreshing.value = false
    }
  }, 1000)
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
}

// 文件处理
const handleImportFileChange = (file: any, fileList: any[]) => {
  importFiles.value = fileList.slice(-1) // 仅允许单文件
}

const handleImportFileRemove = () => {
  importFiles.value = []
}

const handleImportFile = async () => {
  if (!importFiles.value.length) return
  
  importing.value = true
  const file = importFiles.value[0].raw
  
  try {
    const res = await fundsApi.uploadData(collectionName.value, file)
    
    if (res.success) {
      ElMessage.success(res.data.message || '导入成功')
      if (uploadRef.value) uploadRef.value.clearFiles()
      importFiles.value = []
      loadData()
    } else {
      ElMessage.error(res.error || '导入失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

// 远程同步处理
const handleRemoteSync = async () => {
  if (!remoteSyncHost.value) {
    ElMessage.warning('请输入远程主机地址')
    return
  }
  
  remoteSyncing.value = true
  remoteSyncStats.value = null
  
  try {
    const config = {
      host: remoteSyncHost.value,
      username: remoteSyncUsername.value,
      password: remoteSyncPassword.value,
      authSource: remoteSyncAuthSource.value,
      collection: remoteSyncCollection.value || collectionName.value,
      batch_size: remoteSyncBatchSize.value
    }
    
    const res = await fundsApi.syncData(collectionName.value, config)
    
    if (res.success) {
      remoteSyncStats.value = res.data
      ElMessage.success(res.data.message || '同步成功')
      loadData()
    } else {
      ElMessage.error(res.error || '同步失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '同步失败')
  } finally {
    remoteSyncing.value = false
  }
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
    
    clearing.value = true
    try {
      const res = await fundsApi.clearCollectionData(collectionName.value)
      if (res.success) {
        ElMessage.success(`成功清空 ${res.data?.deleted_count || 0} 条数据`)
        await loadData()
      } else {
        ElMessage.error(res.message || '清空数据失败')
      }
    } catch (error: any) {
      ElMessage.error(error.message || '清空数据失败')
    } finally {
      clearing.value = false
    }
  } catch (error) {
    // 用户取消
  }
}

onMounted(() => {
  if (collectionName.value === 'fund_info_index_em') {
    loadCompanies()
  }
  loadData()
})

onUnmounted(() => {
  if (progressTimer) {
    clearInterval(progressTimer)
  }
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
.data-card {
  margin-bottom: 16px;
}

.analysis-tabs {
  margin-bottom: 16px;
}

.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 12px;
  text-align: center;
}

.chart-wrapper-medium {
  width: 100%;
  height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
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

.stat-metric-group {
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 100%;
}

.stat-metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.metric-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.metric-value-large {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.metric-value-medium {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
  margin-bottom: 4px;
}

.metric-sub {
  font-size: 12px;
  color: #909399;
}

.stat-distribution-group {
  padding-left: 24px;
  border-left: 1px solid #ebeef5;
}

@media screen and (max-width: 768px) {
  .stat-distribution-group {
    padding-left: 0;
    border-left: none;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #ebeef5;
  }
}

.distribution-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.distribution-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dist-info {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.dist-name {
  color: #606266;
}

.dist-count {
  color: #909399;
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

.filter-card {
  margin-bottom: 16px;
}

.filter-section {
  margin-bottom: 10px;
  padding: 0 10px;
}

.filter-row {
  display: flex;
  align-items: flex-start;
}

.filter-label {
  font-weight: bold;
  width: 80px;
  color: #333;
  padding-top: 2px;
  flex-shrink: 0;
}

.filter-options {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-option {
  cursor: pointer;
  padding: 2px 8px;
  border-radius: 4px;
  color: #606266;
  transition: all 0.3s;
  font-size: 14px;
}

.filter-option:hover {
  color: #409eff;
}

.filter-option.active {
  background-color: #ecf5ff;
  color: #409eff;
  font-weight: 500;
}

/* ETF统计卡片样式 */
.stat-card {
  padding: 20px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.stat-card.rise {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card.fall {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card.flat {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.stat-card .stat-label {
  font-size: 14px;
  margin-bottom: 8px;
  opacity: 0.9;
}

.stat-card .stat-value {
  font-size: 28px;
  font-weight: bold;
}
</style>