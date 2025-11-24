# ⚠️ 需要重启后端服务

## 已完成的工作

✅ **290个集合的代码已整合到后端**
- 已添加到 `app/routers/stocks.py`
- 共1160个新的API端点
- 已创建 `app/services/stock/providers/__init__.py`

## 🔴 立即执行：重启后端服务

### 方式1: 使用PowerShell脚本（推荐）

```powershell
cd F:\source_code\TradingAgents-CN\tests\stocks
.\restart_backend.ps1
```

### 方式2: 手动重启

```bash
# 1. 停止现有后端进程（如果有）
# 在任务管理器中停止 python.exe 进程，或按 Ctrl+C

# 2. 切换到项目根目录
cd F:\source_code\TradingAgents-CN

# 3. 启动后端服务
uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload
```

## 验证步骤

### 1. 等待服务启动（约10-30秒）

看到以下输出表示启动成功：
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8848
```

### 2. 验证API端点

打开新的终端窗口：
```powershell
cd F:\source_code\TradingAgents-CN\tests\stocks
python verify_integration.py
```

应该看到：
```
[SUCCESS] API响应成功!
集合总数: 365
✓ 集成成功! 所有集合都已加载
```

### 3. 检查前端页面

访问: http://localhost:3000/stocks/collections

应该显示 **365个集合**（之前是91个）

### 4. 测试一个新集合

访问任意新集合，例如：
- http://localhost:3000/stocks/collections/news_report_time_baidu
- http://localhost:3000/stocks/collections/stock_a_all_pb

## 常见问题

### Q: 后端启动失败

**检查错误信息**：
- 语法错误：检查 `app/routers/stocks.py` 是否有Python语法错误
- 导入错误：确认所有Provider和Service文件都已生成
- 端口占用：8848端口可能被占用，尝试更换端口或停止占用进程

### Q: 集合数量还是91个

可能原因：
1. **后端未重启** - 必须重启才能加载新代码
2. **缓存问题** - 清除浏览器缓存，刷新页面
3. **前端连接的是旧后端** - 检查前端配置的API地址

### Q: 某些集合报错

这是正常的，因为：
1. AKShare API可能需要参数
2. 某些接口可能需要特殊配置
3. 网络问题或API限流

**后续优化**：可以针对报错的集合单独调整

## 备份文件位置

原始的 `stocks.py` 已备份到：
```
F:\source_code\TradingAgents-CN\app\routers\stocks.py.backup
```

如果出现问题，可以还原备份。

## 技术支持文件

- **部署总结**: `DEPLOYMENT_SUMMARY.md`
- **生成的代码**: `generated_code/` 目录
- **汇总文件**:
  - `generated_api_routes.py`
  - `generated_collections_registration.py`
  - `generated_routes_config.ts`

---

**当前状态**: ⏸️ 等待重启后端服务

**下一步**: 🚀 立即重启后端服务
