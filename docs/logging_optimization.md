# 云子量化 日志系统优化

## 优化概述

本次优化主要解决了以下问题：
1. **日志格式不统一** - 统一了所有日志的输出格式
2. **长日志换行混乱** - 实现了智能消息截断和格式化
3. **调试信息过多** - 减少了启动时的噪音日志
4. **可读性差** - 改善了字段对齐和视觉效果

## 优化后的特性

### ✅ 统一的日志格式
```
2025-12-14 14:04:37 | webapi                    | INFO    | ✅ GET /api/health - 状态: 200 - 耗时: 0.004s | trace=a8dea390...
```

格式说明：
- `时间戳` - 精确到秒的时间
- `模块名` - 25字符宽度，左对齐
- `日志级别` - 7字符宽度，左对齐
- `消息内容` - 智能截断，避免过长
- `trace_id` - 请求追踪ID，便于调试

### ✅ 智能消息处理
- **长消息截断**：控制台显示150字符，文件显示300字符
- **模块名优化**：保留关键部分，避免过长的模块路径
- **trace_id统一**：所有日志都包含追踪信息

### ✅ 分级日志管理
- **控制台日志**：INFO级别，适合开发调试
- **文件日志**：完整记录，支持轮转
- **错误日志**：WARNING及以上，便于问题排查

## 配置文件

### 主配置文件
- `config/logging.toml` - 主要的日志配置
- `app/core/clean_logging.py` - 清洁日志实现
- `app/core/log_filter.py` - 日志过滤器

### 环境变量控制
```bash
# 启用清洁日志模式（默认启用）
USE_CLEAN_LOGGING=true

# 启用调试模式（显示详细配置信息）
LOGGING_DEBUG=false
```

## 日志文件结构

```
logs/
├── tradingagents.log    # 主日志文件（50MB轮转）
├── error.log           # 错误日志（10MB轮转）
└── *.log.1, *.log.2    # 轮转备份文件
```

## 使用工具

### 日志查看工具
```bash
# 查看最近50条日志
python scripts/view_logs.py

# 查看最近100条日志
python scripts/view_logs.py --lines 100

# 只显示错误和警告
python scripts/view_logs.py --level ERROR WARNING

# 只显示webapi模块的日志
python scripts/view_logs.py --module webapi

# 显示最近1小时的日志
python scripts/view_logs.py --since 1h

# 显示日志统计信息
python scripts/view_logs.py --stats

# 实时跟踪日志
python scripts/view_logs.py --follow
```

### 日志级别说明
- **DEBUG** - 详细的调试信息
- **INFO** - 一般信息，正常运行状态
- **WARNING** - 警告信息，需要注意但不影响运行
- **ERROR** - 错误信息，影响功能但不致命
- **CRITICAL** - 严重错误，可能导致程序崩溃

## 性能优化

### 减少日志噪音
- 过滤频繁的健康检查请求
- 降低第三方库的日志级别
- 减少启动时的调试输出

### 文件管理
- 自动轮转，避免日志文件过大
- 保留适量备份，节省磁盘空间
- UTF-8编码，支持中文内容

## 开发建议

### 记录日志的最佳实践
```python
import logging

logger = logging.getLogger(__name__)

# ✅ 好的日志记录
logger.info("🔄 开始处理用户请求: %s", request_id)
logger.warning("⚠️ 数据源响应缓慢: %s, 耗时: %.2fs", source_name, duration)
logger.error("❌ 数据库连接失败: %s", str(error))

# ❌ 避免的做法
logger.info("Processing request...")  # 信息不足
logger.error(f"Error: {error}")      # 使用f-string而非%格式化
```

### 使用表情符号增强可读性
- 🔄 - 开始处理
- ✅ - 成功完成
- ⚠️ - 警告信息
- ❌ - 错误信息
- 🔍 - 调试信息
- 📊 - 统计信息
- 🔗 - 连接相关

## 故障排查

### 常见问题
1. **日志文件权限问题** - 确保logs目录可写
2. **日志轮转失败** - 检查磁盘空间
3. **格式不统一** - 确认USE_CLEAN_LOGGING=true

### 调试步骤
1. 检查环境变量设置
2. 查看error.log中的错误信息
3. 使用--stats查看日志分布
4. 启用LOGGING_DEBUG查看配置详情

## 未来改进

- [ ] 支持结构化日志（JSON格式）
- [ ] 集成日志聚合系统
- [ ] 添加性能监控日志
- [ ] 支持远程日志传输
- [ ] 实现日志告警机制