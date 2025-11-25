# 修复 stock_individual_info_em 集合 400 错误

## 问题描述
访问 `stock_individual_info_em` 集合数据时出现 400 错误：
```
GET http://localhost:3000/api/stocks/collections/stock_individual_info_em/data?page=1&page_size=20 400 (Bad Request)
```

## 问题原因
后端 API 的 `get_stock_collection_data` 函数中，`collection_map` 字典缺少了新添加的股票数据集合映射。

## 解决方案
在 `app/routers/stocks.py` 的 `collection_map` 字典中添加了以下集合：

```python
# 添加新的股票数据集合
"stock_individual_info_em": db["stock_individual_info_em"],
"stock_individual_basic_info_xq": db["stock_individual_basic_info_xq"],
"stock_zh_a_spot_em": db["stock_zh_a_spot_em"],
"stock_zh_a_hist": db["stock_zh_a_hist"],
"stock_zh_a_hist_min_em": db["stock_zh_a_hist_min_em"],
"stock_bid_ask_em": db["stock_bid_ask_em"],
```

## 受影响的集合
- ✅ stock_individual_info_em（个股信息查询-东财）
- ✅ stock_individual_basic_info_xq（个股信息查询-雪球）
- ✅ stock_zh_a_spot_em（沪深京A股实时行情-东财）
- ✅ stock_zh_a_hist（A股历史行情-东财）
- ✅ stock_zh_a_hist_min_em（A股分时数据-东财）
- ✅ stock_bid_ask_em（行情报价-东财）

## 需要的操作
**重启后端服务以应用更改**

Windows PowerShell:
```powershell
cd f:\source_code\TradingAgents-CN
.\tests\stocks\restart_backend.ps1
```

或手动重启：
1. 停止当前运行的后端服务（Ctrl+C）
2. 重新启动：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## 验证步骤
1. 重启后端服务
2. 刷新前端页面
3. 访问 http://localhost:3000/stocks/collections/stock_individual_info_em
4. 确认数据列表能正常加载（即使是空数据也应该返回200状态）

## 修改文件
- ✅ `app/routers/stocks.py` - 添加集合映射

## 相关文件
- `frontend/src/views/Stocks/Collection.vue` - 集合详情页面
- `frontend/src/views/Stocks/collectionRefreshConfig.ts` - 前端刷新配置
- `app/services/stock_refresh_service.py` - 后端刷新服务
