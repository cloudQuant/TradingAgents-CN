# 股票数据集合 API 更新定制化进度

## 总体进度

已完成定制化 API 更新配置的需求：**6 个**

## 已完成需求

### 02_个股信息查询-东财 ✅

- **集合名称**: `stock_individual_info_em`
- **UI 类型**: single-batch（单个更新 + 批量更新）
- **配置完成时间**: 2024-11-24
- **配置详情**:
  - 单个更新：输入股票代码（6 位）
  - 批量更新：从沪深京 A 股实时行情数据中获取代码列表
  - 并发数：1-10（默认 3）
  - 延迟：0-5 秒（默认 0.5 秒）
- **文档状态**: ✅ 已标记为 finished

### 03_个股信息查询-雪球 ✅

- **集合名称**: `stock_individual_basic_info_xq`
- **UI 类型**: single-batch（单个更新 + 批量更新）
- **配置完成时间**: 2024-11-24
- **配置详情**:
  - 单个更新：输入股票代码（雪球格式：SH/SZ/BJ + 6 位）
  - 批量更新：从个股信息查询-东财中获取代码列表并自动转换格式
  - 并发数：1-5（默认 2）
  - 延迟：0.5-5 秒（默认 1 秒）
  - 特别提示：雪球 API 限流严格
- **文档状态**: ✅ 已标记为 finished

### 04_沪深京 A 股实时行情-东财 ✅

- **集合名称**: `stock_zh_a_spot_em`
- **UI 类型**: none（全部更新）
- **配置完成时间**: 2024-11-24
- **配置详情**:
  - 一次性获取所有沪深京 A 股（约 5000+只）实时行情
  - 数据以【股票代码+日期】作为唯一标识保存
  - 无需额外参数
- **文档状态**: ✅ 已标记为 finished

### 05_A 股历史行情-东财 ✅

- **集合名称**: `stock_zh_a_hist`
- **UI 类型**: single-batch（单个更新 + 批量更新）
- **配置完成时间**: 2024-11-24（配置已存在）
- **配置详情**:
  - 单个更新：输入股票代码、周期、复权类型
  - 批量更新：从股票列表批量获取历史行情
  - 周期选项：日线/周线/月线
  - 复权类型：不复权/前复权/后复权
  - 并发数：1-10（默认 5）
- **文档状态**: ✅ 已标记为 finished

### 06_A 股分时数据-东财 ✅

- **集合名称**: `stock_zh_a_hist_min_em`
- **UI 类型**: single（单个更新）
- **配置完成时间**: 2024-11-24（配置已存在）
- **配置详情**:
  - 单个更新：输入股票代码、周期、复权类型
  - 周期选项：1 分钟/5 分钟/15 分钟/30 分钟/60 分钟
  - 复权类型：不复权/前复权/后复权
  - 特别说明：1 分钟数据只返回近 5 个交易日且不复权
- **文档状态**: ✅ 已标记为 finished

## 技术架构

### 前端配置文件

- **位置**: `frontend/src/views/Stocks/collectionRefreshConfig.ts`
- **配置类型**: TypeScript 配置对象
- **UI 类型**:
  - `none`: 不需要参数，直接全部更新
  - `single`: 只支持单个更新
  - `batch`: 只支持批量更新
  - `single-batch`: 同时支持单个和批量更新

### 后端服务

- **刷新服务**: `app/services/stock_refresh_service.py`
- **数据服务**: `app/services/stock_data_service.py`
- **API 路由**: `app/routers/stocks.py`
- **核心端点**:
  - `POST /api/stocks/collections/{collection_name}/refresh` - 启动刷新任务
  - `GET /api/stocks/collections/{collection_name}/refresh/status/{task_id}` - 查询任务状态
  - `GET /api/stocks/collections/{collection_name}/data` - 获取数据
  - `GET /api/stocks/collections/{collection_name}/stats` - 获取统计

### 前端组件

- **集合列表**: `frontend/src/views/Stocks/Collections.vue`
- **集合详情**: `frontend/src/views/Stocks/Collection.vue`
- **API 更新对话框**: 在 Collection.vue 中集成，根据配置动态渲染

## 配置参考（基金数据集合）

参考了基金数据集合的实现方式：

- 基金列表页面：`frontend/src/views/Funds/Collections.vue`
- 基金详情页面：`frontend/src/views/Funds/Collection.vue`
- 实现了类似的定制化 API 更新对话框功能

## 下一步工作

继续处理 requirements 文件夹中未标记为 finished 的需求文档，逐个完成定制化配置。

## 测试建议

1. 启动后端服务和前端开发服务器
2. 访问 <http://localhost:3000/stocks/collections>
3. 点击各个已配置的集合，验证 API 更新对话框功能
4. 测试单个更新和批量更新功能
5. 验证进度显示和错误处理

## 注意事项

1. **API 限流**: 批量更新时注意控制并发数和延迟时间，避免触发限流
2. **数据唯一性**: 确保后端正确处理数据的唯一标识（股票代码、日期等）
3. **错误处理**: 完善网络异常、API 限流、数据格式异常等错误处理
4. **进度显示**: 批量更新时显示详细进度信息
5. **用户体验**: 提示信息清晰，操作流畅
