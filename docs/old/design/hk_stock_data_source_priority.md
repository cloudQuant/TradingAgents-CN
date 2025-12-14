# 港股数据源优先级设计文档

## 问题描述

当前港股数据获取存在以下问题：

1. **基础信息 (`_get_hk_info`)**: 直接使用 yfinance，遇到 Rate Limit 就失败
2. **K 线数据 (`_get_hk_kline`)**: 直接使用 yfinance，遇到 Rate Limit 就失败
3. **新闻数据 (`get_hk_news`)**: 刚添加的使用 Finnhub，但应该优先使用 AKShare

- *核心问题**: 港股的实现没有参考美股的数据源优先级模式，导致单点失败。

## 美股实现模式分析

### 美股的标准流程

以 `_get_us_info` 为例：

```python
async def _get_us_info(self, code: str, force_refresh: bool = False) -> Dict:

# 1. 检查缓存（除非强制刷新）
    if not force_refresh:
        cache_key = self.cache.find_cached_stock_data(...)
        if cache_key:
            cached_data = self.cache.load_stock_data(cache_key)
            if cached_data:
                return self._parse_cached_data(cached_data, 'US', code)

# 2. 从数据库获取数据源优先级
    source_priority = await self._get_source_priority('US')

# 3. 按优先级尝试各个数据源
    info_data = None
    data_source = None

# 数据源名称映射（数据库名称 → 处理函数）
    source_handlers = {
        'alpha_vantage': ('alpha_vantage', self._get_us_info_from_alpha_vantage),
        'yahoo_finance': ('yfinance', self._get_us_info_from_yfinance),
        'finnhub': ('finnhub', self._get_us_info_from_finnhub),
    }

# 过滤有效数据源并去重
    valid_priority = []
    seen = set()
    for source_name in source_priority:
        source_key = source_name.lower()
        if source_key in source_handlers and source_key not in seen:
            seen.add(source_key)
            valid_priority.append(source_name)

    if not valid_priority:
        logger.warning("⚠️ 数据库中没有配置有效的美股数据源，使用默认顺序")
        valid_priority = ['yahoo_finance', 'alpha_vantage', 'finnhub']

    logger.info(f"📊 [US 基础信息有效数据源] {valid_priority}")

# 4. 循环尝试每个数据源
    for source_name in valid_priority:
        source_key = source_name.lower()
        handler_name, handler_func = source_handlers[source_key]
        try:
            info_data = handler_func(code)
            data_source = handler_name

            if info_data:
                logger.info(f"✅ {data_source}获取美股基础信息成功: {code}")
                break
        except Exception as e:
            logger.warning(f"⚠️ {source_name}获取基础信息失败: {e}")
            continue

    if not info_data:
        raise Exception(f"无法获取美股{code}的基础信息：所有数据源均失败")

# 5. 格式化数据
    formatted_data = {...}

# 6. 保存到缓存
    self.cache.save_stock_data(...)

    return formatted_data

```bash

### 关键特点

1. **缓存优先**: 先检查缓存，避免重复请求
2. **数据库配置**: 从 MongoDB 的 `data_sources` 集合读取优先级
3. **多数据源降级**: 按优先级尝试，一个失败自动切换下一个
4. **统一格式化**: 不同数据源的数据统一格式化为前端期望的字段
5. **缓存结果**: 成功后保存到缓存，下次直接使用

## 港股数据源分析

### 可用数据源

| 数据源 | 行情 | 基础信息 | K 线 | 新闻 | 优缺点 |

|--------|------|----------|-----|------|--------|

| **AKShare**| ✅ | ✅ | ✅ | ✅ | 免费、稳定、中文友好、数据全面 |

|**Yahoo Finance**| ✅ | ✅ | ✅ | ❌ | 免费、但有 Rate Limit |

|**Finnhub**| ✅ | ✅ | ✅ | ✅ | 需要 API Key、有配额限制 |

### 推荐优先级

1.**行情数据**: AKShare > Yahoo Finance > Finnhub

1. **基础信息**: AKShare > Yahoo Finance > Finnhub
2. **K 线数据**: AKShare > Yahoo Finance > Finnhub
3. **新闻数据**: AKShare > Finnhub

- *理由**: AKShare 免费、稳定、无 Rate Limit，应该作为首选。

## 实现方案

### 1. 重构 `_get_hk_info` (基础信息)

```python
async def _get_hk_info(self, code: str, force_refresh: bool = False) -> Dict:
    """
    获取港股基础信息
    🔥 按照数据库配置的数据源优先级调用 API
    """

# 1. 检查缓存
    if not force_refresh:
        cache_key = self.cache.find_cached_stock_data(
            symbol=code,
            data_source="hk_basic_info"
        )
        if cache_key:
            cached_data = self.cache.load_stock_data(cache_key)
            if cached_data:
                logger.info(f"⚡ 从缓存获取港股基础信息: {code}")
                return self._parse_cached_data(cached_data, 'HK', code)

# 2. 从数据库获取数据源优先级
    source_priority = await self._get_source_priority('HK')

# 3. 按优先级尝试各个数据源
    info_data = None
    data_source = None

# 数据源名称映射
    source_handlers = {
        'akshare': ('akshare', self._get_hk_info_from_akshare),
        'yahoo_finance': ('yfinance', self._get_hk_info_from_yfinance),
        'finnhub': ('finnhub', self._get_hk_info_from_finnhub),
    }

# 过滤有效数据源并去重
    valid_priority = []
    seen = set()
    for source_name in source_priority:
        source_key = source_name.lower()
        if source_key in source_handlers and source_key not in seen:
            seen.add(source_key)
            valid_priority.append(source_name)

    if not valid_priority:
        logger.warning("⚠️ 数据库中没有配置有效的港股数据源，使用默认顺序")
        valid_priority = ['akshare', 'yahoo_finance', 'finnhub']

    logger.info(f"📊 [HK 基础信息有效数据源] {valid_priority}")

    for source_name in valid_priority:
        source_key = source_name.lower()
        handler_name, handler_func = source_handlers[source_key]
        try:
            info_data = handler_func(code)
            data_source = handler_name

            if info_data:
                logger.info(f"✅ {data_source}获取港股基础信息成功: {code}")
                break
        except Exception as e:
            logger.warning(f"⚠️ {source_name}获取基础信息失败: {e}")
            continue

    if not info_data:
        raise Exception(f"无法获取港股{code}的基础信息：所有数据源均失败")

# 4. 格式化数据
    formatted_data = self._format_hk_info(info_data, code, data_source)

# 5. 保存到缓存
    self.cache.save_stock_data(
        symbol=code,
        data=json.dumps(formatted_data, ensure_ascii=False),
        data_source="hk_basic_info"
    )
    logger.info(f"💾 港股基础信息已缓存: {code}")

    return formatted_data

```bash

### 2. 重构 `_get_hk_kline` (K 线数据)

类似模式，数据源优先级：AKShare > Yahoo Finance > Finnhub

### 3. 重构 `get_hk_news` (新闻数据)

类似模式，数据源优先级：AKShare > Finnhub

### 4. 新增数据源处理函数

需要为每个数据源添加对应的处理函数：

#### 基础信息

- `_get_hk_info_from_akshare(code)` - 从 AKShare 获取
- `_get_hk_info_from_yfinance(code)` - 从 Yahoo Finance 获取（已有）
- `_get_hk_info_from_finnhub(code)` - 从 Finnhub 获取

#### K 线数据

- `_get_hk_kline_from_akshare(code, period, limit)` - 从 AKShare 获取
- `_get_hk_kline_from_yfinance(code, period, limit)` - 从 Yahoo Finance 获取（已有）
- `_get_hk_kline_from_finnhub(code, period, limit)` - 从 Finnhub 获取

#### 新闻数据

- `_get_hk_news_from_akshare(code, days, limit)` - 从 AKShare 获取
- `_get_hk_news_from_finnhub(code, days, limit)` - 从 Finnhub 获取（已有）

### 5. 新增格式化函数

- `_format_hk_info(data, code, source)` - 格式化基础信息（已有）
- `_format_hk_kline(data, code, source)` - 格式化 K 线数据
- `_format_hk_news(data, code, source)` - 格式化新闻数据

## 实现步骤

1. ✅ **理解美股实现模式**- 已完成
2. ⏳**创建设计文档**- 当前步骤
3. ⏳**重构 `_get_hk_info`**- 添加数据源优先级
4. ⏳**重构 `_get_hk_kline`**- 添加数据源优先级
5. ⏳**重构 `get_hk_news`**- 改用 AKShare 优先
6. ⏳**添加 AKShare 数据源处理函数**
7. ⏳ **添加 Finnhub 数据源处理函数**
8. ⏳ **测试所有功能**
9. ⏳ **更新数据库配置**

## 数据库配置示例

在 `data_sources` 集合中添加港股数据源配置：

```json
{
  "market": "HK",
  "data_type": "basic_info",
  "priority": ["AKShare", "yahoo_finance", "finnhub"],
  "enabled": true
}

```bash

## 预期效果

1. **提高可用性**: 一个数据源失败自动切换，不会导致整个功能不可用
2. **降低成本**: 优先使用免费的 AKShare，减少 API 配额消耗
3. **提升性能**: 缓存机制避免重复请求
4. **统一体验**: 港股和美股使用相同的实现模式，代码更易维护
