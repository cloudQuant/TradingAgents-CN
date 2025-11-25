# 股票数据集合API更新功能实现指南

## 当前实现状态

### 已完成的基础功能 ✅
通过前面的实现，所有股票数据集合现在都支持以下功能：

1. **文件导入** ✅
   - 支持CSV和Excel文件格式
   - 自动识别常见字段（code, symbol, 代码, 序号等）
   - 批量upsert避免重复数据
   - 文件：`frontend/src/views/Stocks/Collection.vue` (文件导入对话框)
   - 后端：`app/services/stock_data_service.py::import_data_from_file()`

2. **远程同步** ✅
   - 从远程MongoDB同步数据
   - 支持认证和批次大小配置
   - 显示同步进度和统计
   - 文件：`frontend/src/views/Stocks/Collection.vue` (远程同步对话框)
   - 后端：`app/services/stock_data_service.py::sync_data_from_remote()`

3. **API更新（无参数）** ✅
   - 点击"更新数据" → "API更新"直接触发刷新
   - 适用于不需要参数的数据集合
   - 文件：`frontend/src/views/Stocks/Collection.vue` (handleUpdateCommand)
   - 后端：`app/routers/stocks.py::refresh_collection()`

### 待完成的功能 ⏳

4. **API更新（带参数）** - 部分完成
   - 已创建配置文件框架：`frontend/src/views/Stocks/collectionRefreshConfig.ts`
   - 需要完成：参数输入对话框UI
   - 需要完成：参数验证和提交逻辑
   - 需要完成：为每个需求文档添加参数配置

## 需求文档处理状态

### 需要参数的集合（优先处理）
这些集合需要用户输入参数（如股票代码）才能更新：

| 需求文档 | 集合名称 | 参数 | 状态 |
|---------|---------|------|------|
| 02_个股信息查询-东财.md | stock_individual_info_em | symbol (股票代码) | 基础功能完成，参数功能待完成 |
| 03_个股信息查询-雪球.md | stock_individual_info_xq | symbol (股票代码) | 待实现 |
| 04_沪深京A股实时行情-东财.md | - | - | 待分析 |
| 05_A股历史行情-东财.md | - | symbol, period, adjust等 | 待分析 |
| 06_A股分时数据-东财.md | - | symbol, date等 | 待分析 |

### 不需要参数的集合（已可用）
这些集合可以直接使用"API更新"功能：

| 需求文档 | 集合名称 | 状态 |
|---------|---------|------|
| 07_上海证券交易所-完成.md | - | ✅ 已完成 |
| 08_证券类别统计-完成.md | - | ✅ 已完成 |
| ... | ... | ... |

## 实现方案建议

### 方案A：完整的参数化实现（推荐，但工作量大）

需要修改 `Collection.vue`，添加参数输入对话框：

```vue
<!-- API刷新参数对话框 -->
<el-dialog v-model="apiRefreshDialogVisible" title="API更新">
  <!-- 选择更新模式 -->
  <el-radio-group v-model="refreshMode">
    <el-radio label="all">批量更新全部</el-radio>
    <el-radio label="params">更新指定数据</el-radio>
  </el-radio-group>
  
  <!-- 参数输入（根据配置动态显示） -->
  <el-form v-if="refreshMode === 'params'">
    <el-form-item label="股票代码">
      <el-input v-model="refreshParams.symbol" 
                type="textarea" 
                placeholder="输入股票代码，多个用逗号或换行分隔&#10;例如：000001,000002" />
    </el-form-item>
  </el-form>
</el-dialog>
```

#### 实现步骤：
1. 在Collection.vue中添加参数对话框状态和UI
2. 修改handleUpdateCommand，检查是否需要参数
3. 为每个需求文档在collectionRefreshConfig.ts添加配置
4. 测试并标记需求文档为finished

### 方案B：简化的JSON输入实现（快速但需要用户了解API）

添加一个通用的JSON参数输入框：

```vue
<el-dialog v-model="apiRefreshDialogVisible" title="API更新">
  <el-radio-group v-model="refreshMode">
    <el-radio label="all">更新全部</el-radio>
    <el-radio label="params">带参数更新</el-radio>
  </el-radio-group>
  
  <el-input v-if="refreshMode === 'params'"
            v-model="refreshParamsJson"
            type="textarea"
            :rows="6"
            placeholder='输入JSON格式参数，例如：&#10;{"symbol": "000001,000002"}' />
            
  <template #footer>
    <el-button @click="apiRefreshDialogVisible = false">取消</el-button>
    <el-button type="primary" @click="handleSubmitRefresh">开始更新</el-button>
  </template>
</el-dialog>
```

优点：实现简单，一次修改适用所有集合  
缺点：需要用户了解API参数格式

## 后续工作计划

### 第一阶段：完善参数化支持
1. [ ] 选择实现方案（推荐方案B作为过渡）
2. [ ] 修改Collection.vue添加参数对话框
3. [ ] 测试基本功能

### 第二阶段：逐个处理需求文档
按以下顺序处理：
1. [ ] 02_个股信息查询-东财.md
2. [ ] 03_个股信息查询-雪球.md  
3. [ ] 18_京A股.md
4. [ ] 19_新股.md
5. [ ] ...其他文档

每完成一个需求文档后：
- 测试API更新功能（无参数直接更新，有参数显示对话框）
- 测试文件导入功能
- 测试远程同步功能
- 确认无误后，重命名文件添加"-finished"后缀

### 第三阶段：优化和完善
1. [ ] 添加进度提示
2. [ ] 添加错误处理和重试机制
3. [ ] 优化UI交互
4. [ ] 完善文档

## 当前可以标记为finished的文档

已经包含"-完成"或"-完成.md"后缀的文档不需要再处理。

对于新的未标记文档，如果满足以下条件可以标记finished：
1. 后端API接口已实现
2. 前端Collection.vue支持该集合的数据展示
3. 更新数据功能的三种方式都可用：
   - 文件导入 ✅
   - 远程同步 ✅
   - API更新（如果需要参数，则参数对话框已实现）

## 文件位置参考

### 前端
- 主要组件：`frontend/src/views/Stocks/Collection.vue`
- API接口：`frontend/src/api/stocks.ts`
- 刷新配置：`frontend/src/views/Stocks/collectionRefreshConfig.ts`
- 集合配置：`frontend/src/views/Stocks/collectionConfig.ts`

### 后端
- 路由：`app/routers/stocks.py`
- 服务：`app/services/stock_data_service.py`

### 测试
- 需求文档：`tests/stocks/requirements/`
- 测试用例：`tests/stocks/collections/`

## 总结

当前已完成：
- ✅ 文件导入功能（所有集合可用）
- ✅ 远程同步功能（所有集合可用）
- ✅ API更新基础框架（无参数集合可用）
- ✅ 参数配置文件框架

待完成：
- ⏳ API更新参数对话框UI
- ⏳ 逐个需求文档的参数配置
- ⏳ 测试和标记finished

建议先采用方案B（JSON输入）快速完成参数化支持，然后再逐步优化为方案A的友好UI。

最后更新：2025-11-24
