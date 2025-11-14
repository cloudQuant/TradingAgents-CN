# 需求说明书：在现有架构中新增“债券、期货、基金”分析能力

本需求在不破坏现有 A/H/美股分析框架的前提下，扩展同一条数据管线（统一接口 → 数据源管理 → Provider → 缓存 → 分析 → 输出），新增债券、期货、基金三个资产类别的获取、校验、缓存、分析、回传与降级。

---

## 一、目标与范围

- **[目标]**
  - 在现有项目（已支持 A 股/港股/美股）基础上，增加：
    - 债券（中国国债、地方债、企业/公司债，先覆盖交易所挂牌债）
    - 期货（上期所/大商所/郑商所/中金所/上能所主力与具体合约）
    - 基金（公募开放式基金净值、ETF 基金）
  - 与当前“统一接口 + 数据源优先级 + 异步 Provider + Mongo 缓存 + 指标计算”的架构保持一致。
- **[不在本期范围]**
  - 量化回测引擎、策略交易撮合。
  - Wind/同花顺等商业数据源接入。
  - 深度债券估值（全量现金流、到期收益率等高精度模型）。

---

## 二、业务与数据需求

- **[债券（CN Bonds）]**
  - 基本信息：代码、名称、发行人、债券类型（国债/地方债/公司债等）、票面利率、起息日、到期日、上市交易所。
  - 历史数据：日级收盘价/净价/全价、成交量/额；优先支持交易所挂牌债（上交所/深交所）。
  - 实时/快照（可选）：最新价、涨跌幅。
  - 分析：MA/MACD/RSI、收益率简单推算、简化回撤/波动。
- **[期货（CN Futures）]**
  - 合约信息：交易所、品种代码、合约月份、乘数、最小变动、交易时间、上市/到期日。
  - 历史数据：日级 OHLCV + 持仓量（open_interest）。
  - 合约序列：具体合约历史、主力连续、指数连续（可按换月规则指定）。
  - 分析：MA/MACD/RSI、波动率、收益率、回撤、主力连续拼接质量校验。
- **[基金（CN Funds）]**
  - 基本信息：基金代码、名称、基金类型（主动/指数、股票/债券/混合等）、跟踪标的（ETF）、管理人、成立日期。
  - 历史数据：日级单位净值、累计净值，ETF 的日线档（OHLCV）。
  - 分析：区间收益、年化、波动率、夏普、回撤；ETF 跟踪误差（若有指数基准）。

---

## 三、架构设计

- **[资产类型抽象]**
  - 新增 `AssetClass`：
    - `EQUITY_A`, `EQUITY_HK`, `EQUITY_US`（已有）
    - `BOND_CN`, `FUTURES_CN`, `FUND_CN`
  - 统一接口根据资产类型分流到对应 Provider 与格式化方法。
- **[数据源优先级与降级]**
  - 为不同资产类型定义独立优先级（DB → 第一优先源 → 备用源1 → 备用源2）：
    - 债券：`MongoDB → Tushare → AKShare`
    - 期货：`MongoDB → AKShare → Tushare`
    - 基金：`MongoDB → AKShare → Tushare`
  - 复用现有 `_run_coro_safely`，杜绝事件循环冲突。
- **[模块与文件]**
  - `tradingagents/dataflows/providers/china/`
    - `bonds.py`（AKShare/Tushare 债券 Provider）
    - `futures.py`（AKShare/Tushare 期货 Provider）
    - `funds.py`（AKShare/Tushare 基金 Provider）
  - `tradingagents/dataflows/data_source_manager.py`
    - 扩展资产类型路由/降级逻辑/统一格式化
  - `tradingagents/dataflows/interface.py`
    - 新增统一接口函数（见后）
  - `tradingagents/utils/instrument_validator.py`
    - 统一代码标准化与资产识别（替代/扩展 `stock_validator.py`）
- **[代码规范与映射]**
  - 债券代码：尽量使用交易所通用代码，必要时做映射（AKShare/Tushare 对代码要求不同）。
  - 期货代码：统一内部标准（如 `RB2401.SHF`），与各 Provider 映射（`rb2401`/`SHFE.rb2401` 等）。
  - 基金代码：六位代码（基金/ETF），对接 AKShare/Tushare 的 `symbol`/`ts_code` 转换。
- **[缓存设计（MongoDB）]**
  - Collection：
    - `bond_basic_info`, `bond_daily`
    - `futures_basic_info`, `futures_daily`（含 `open_interest`）
    - `fund_basic_info`, `fund_nav_daily`（ETF 进入 `fund_etf_daily` 或与 NAV 合并标注）
  - 索引：`code+date` 唯一索引；`updated_at`；常用维度索引。
  - 冷热数据：保留最近 2 年在热数据集合，历史归档（可后续）。
- **[统一输出格式]**
  - 保持现有字符串报表输出路径，短期内兼容数据分析页面。
  - 同时为内部调用提供 DataFrame/Dict（便于分析计算）。

---

## 四、统一接口（Interface）与服务（Service）

- **[新增统一接口函数]**
  - `get_cn_bond_data_unified(code, start_date, end_date, period='daily') -> str`
  - `get_cn_futures_data_unified(code, start_date, end_date, period='daily', continuous='main|index|none') -> str`
  - `get_cn_fund_data_unified(code, start_date, end_date, period='daily') -> str`
  - 基本信息：
    - `get_cn_bond_info_unified(code) -> Dict`
    - `get_cn_futures_info_unified(code) -> Dict`
    - `get_cn_fund_info_unified(code) -> Dict`
- **[服务层扩展]**
  - `simple_analysis_service.py` 新增上述资产的分析入口（与现有 A 股相同风格）。
  - 统一的日期智能扩展、日志追踪、异常提示复用当前实现。
- **[API/路由（如 FastAPI）]**
  - `/api/cn/bonds/{code}/history`
  - `/api/cn/futures/{code}/history?continuous=main`
  - `/api/cn/funds/{code}/history`
  - `/api/cn/{asset}/{code}/info`

---

## 五、Provider 设计（AKShare / Tushare）

- **[通用抽象]**
  - 为每类资产定义 Base 接口（异步）：
    - `get_symbol_list() -> List[Dict]`
    - `get_basic_info(code) -> Dict`
    - `get_historical_data(code, start_date, end_date, period=...) -> DataFrame`
    - `get_realtime_quote(code) -> Optional[Dict]`（可选）
  - Provider 内部：
    - 阻塞 IO 用 `asyncio.to_thread(...)`
    - 输出统一字段名，列名标准化函数（如 `_standardize_*_columns`）
- **[参考数据源能力]**
  - AKShare：
    - 债券：如 `bond_*`, `bond_zh_*`, `bond_china_*` 系列。
    - 期货：`futures_zh_*`（具体合约、主力、指数连续）、各交易所日线接口。
    - 基金：`fund_open_fund_daily_em`、`fund_etf_hist_sina`、`fund_basic` 等。
  - Tushare（需 token）：
    - 债券：`bond_basic`, `bond_tick`/`bond_daily`（以官方文档为准）。
    - 期货：期货日线 `fut_daily`、合约信息 `fut_basic`。
    - 基金：`fund_basic`, `fund_nav`, `fund_daily`、ETF `fund_etf` 等。
- **[代码映射要点]**
  - 债券：交易所代码 vs. tushare `ts_code`（如 `123001.SZ`）。
  - 期货：内部统一 `RB2401.SHF`，AKShare 需要 `rb2401`，Tushare 需要 `RB2401.SHFE`。
  - 基金：`510300`（ETF）可能需映射到 `510300.SH`/`sz510300` 视数据源而定。

---

## 六、数据模型与标准字段

- **[债券 basic_info]**
  - `code`, `name`, `issuer`, `bond_type`, `coupon_rate`, `issue_date`, `maturity_date`, `exchange`, `list_date`, `rating?`, `data_source`, `last_sync`
- **[债券 daily]**
  - `date`, `code`, `close`, `open?`, `high?`, `low?`, `volume?`, `amount?`, `net_price?`, `full_price?`
- **[期货 basic_info]**
  - `code`, `exchange`, `underlying`, `contract_month`, `multiplier`, `tick_size`, `list_date`, `delist_date`, `data_source`, `last_sync`
- **[期货 daily]**
  - `date`, `code`, `open`, `high`, `low`, `close`, `volume`, `amount?`, `open_interest`
- **[基金 basic_info]**
  - `code`, `name`, `fund_type`, `benchmark?`, `manager`, `establish_date`, `is_etf`, `data_source`, `last_sync`
- **[基金 NAV/daily]**
  - `date`, `code`, `nav`, `acc_nav`, `open?`, `high?`, `low?`, `close?`, `volume?`（ETF）

---

## 七、分析指标与输出

- **[通用指标]**
  - `MA(5/10/20/60)`, `MACD`, `RSI`, `BOLL`（能计算的资产默认启用）
  - 区间收益、年化收益、波动率、最大回撤、夏普（NAV/收盘价驱动）
- **[期货增强]**
  - 年化波动率（合约连续）/收益率/回撤
  - 主力连续拼接诊断报告（换月逻辑、跳空提示）
- **[基金增强]**
  - 跟踪误差（ETF vs 对应指数，如有）
  - 分配/拆分事件提示（可后续）
- **[债券增强（简化）]**
  - 以价格序列计算趋势指标
  - 若可得收益率/久期字段，提供简化风险揭示

---

## 八、配置与环境

- **[.env 新增]**
  - `DEFAULT_CN_BOND_SOURCE=akshare|tushare`
  - `DEFAULT_CN_FUTURES_SOURCE=akshare|tushare`
  - `DEFAULT_CN_FUND_SOURCE=akshare|tushare`
  - `TS_TOKEN=...`（如启用 Tushare）
- **[数据源优先级表]**
  - 入库 `data_sources` 集合，按 `asset_class` 分配可用源与优先级。

---

## 九、错误处理与日志

- **[一致性]**
  - 始终返回字符串或标准 Dict，不返回 tuple 给上层 UI。
  - Provider 报错 → 统一封装消息 → DataSourceManager 进行降级。
- **[日志]**
  - “资产类型/代码/周期/来源/降级结果/耗时/数据条数”标准化日志。
  - 连续合约的拼接日志单独标签（便于审计）。

---

## 十、性能与稳定性

- **[异步与线程]**
  - 所有阻塞 IO 用 `asyncio.to_thread`。
  - 跨同步上下文统一用 `_run_coro_safely`（已实现）。
- **[缓存与限流]**
  - 首选 Mongo 缓存；命中立即返回并记录来源。
  - Provider 端尽量合批（如获取列表）并本地缓存 1h。
- **[可观测性]**
  - 指标：请求成功率、降级成功率、平均耗时、数据新鲜度、各 Provider 错误分布。

---

## 十一、测试计划

- **[单元测试]**
  - 代码标准化（债券/期货/基金代码互转）。
  - 列名标准化器输出校验。
  - 指标计算单元（MA/MACD/RSI/回撤）。
- **[集成测试]**
  - Provider 联网获取小样本（示例代码：国债、RB 主力、510300）。
  - 缓存命中/落库/回读一致性。
  - 降级路径：主源失败 → 备用源成功。
- **[端到端]**
  - 统一接口到服务到日志输出，验证返回字符串一致性、不抛异常。
- **[CI 建议]**
  - 分离“离线纯单测”和“需要网络的集成测试”。

---

## 十二、交付物与验收

- **[交付物]**
  - 新增 Provider 源码与测试用例。
  - 扩展后的 Interface/Service/API。
  - Mongo 集合与索引迁移脚本。
  - 文档：配置说明、代码规范、样例请求/响应。
- **[验收标准]**
  - 指定样例（3 个资产类别、各 3 个代码）均能成功返回历史数据与基础信息。
  - 无 `tuple.split`/事件循环类异常；降级日志清晰，缓存命中可见。
  - 指标计算字段在输出中呈现，数值合理。

---

## 十三、里程碑与排期（建议）

- **[M0：基础设施（~2 天）]**
  - 资产类型枚举、接口骨架、统一代码格式化与断言、Mongo 集合/索引。
- **[M1：基金（~3–4 天）]**
  - AKShare 基金（开放式净值、ETF 历史）+ Tushare 备用
  - 统一接口、服务、指标、日志与测试
- **[M2：期货（~5–7 天）]**
  - AKShare 期货（具体合约+主力/指数连续）+ Tushare 备用
  - 连续合约拼接与诊断、指标、测试
- **[M3：债券（~5–7 天）]**
  - 交易所挂牌债：AKShare/Tushare 历史基础覆盖
  - 简化风险指标、测试
- **[M4：文档与上线（~2 天）]**
  - 配置/部署/监控；小规模灰度；问题回收与修复

---

## 十四、风险与对策

- **[免费数据源不稳定]**
  - 多源降级、缓存优先、重试与熔断。
- **[代码格式多样]**
  - 集中封装标准化与映射表，写单测兜底。
- **[事件循环问题]**
  - 全面使用 `_run_coro_safely` 与 `asyncio.to_thread`（已完成范式）。
- **[数据质量]**
  - 连续合约拼接验证；基金净值缺口与拆分识别；日志告警。
- **[速率限制与封禁]**
  - 限流与间隔；必要时支持代理/可配置退避。

---

## 十五、样例接口签名（示意）

```python
# interface.py
def get_cn_futures_data_unified(code: str, start_date: str, end_date: str,
                                period: str = "daily",
                                continuous: str = "main") -> str: ...
def get_cn_futures_info_unified(code: str) -> dict: ...

def get_cn_bond_data_unified(code: str, start_date: str, end_date: str,
                             period: str = "daily") -> str: ...
def get_cn_bond_info_unified(code: str) -> dict: ...

def get_cn_fund_data_unified(code: str, start_date: str, end_date: str,
                             period: str = "daily") -> str: ...
def get_cn_fund_info_unified(code: str) -> dict: ...
```

---

# Recommended Actions

- **[确认优先顺序]** 是否按“基金 → 期货 → 债券”的实现顺序推进？
- **[锁定数据源]** 是否启用 Tushare（需 Token），或先以 AKShare 为主？
- **[验收样例]** 提供 3×3 代码列表（基金/期货/债券各 3 个）作为测试基准。
- **[同意排期]** 确认里程碑与时间估算后，我开始按 M1 执行。

# 状态小结

- 已给出全面需求与落地方案，覆盖架构、数据模型、接口、Provider、缓存、指标、测试与排期。
- 待你确认优先级、数据源选择与样例清单后，我即可进入实现阶段。

---

## 十六、指数（国内/国际）支持

- **[业务需求]**
  - **国内指数**：上证综指、沪深300、中证500、创业板指、科创50、上证50等。
  - **国际指数**：标普500、道琼斯、纳指、日经225、恒生、DAX、FTSE100 等。
- **[数据内容]**
  - 基本信息：`code`, `name`, `market`, `provider_symbol`, `base_date?`, `data_source`, `last_sync`。
  - 历史数据（日级）：`date`, `code`, `open`, `high`, `low`, `close`, `volume?`, `amount?`。
- **[Provider 与优先级]**
  - 优先级：`MongoDB → AKShare → Tushare`（按可用性与覆盖面）。
  - 字段/代码映射与列名标准化，沿用现有股票格式化范式。
- **[接口]**
  - `get_index_data_unified(code, start_date, end_date, period='daily') -> str`
  - `get_index_info_unified(code) -> Dict`
- **[数据模型（Mongo）]**
  - `index_basic_info`，`index_daily`（`code+date` 唯一索引）。

---

## 十七、前端改进与交互（新增/通用）

- **[信息架构]**
  - 顶部/侧边导航按资产类分组：股票、基金、指数、期货、债券。
  - 代码输入组件支持资产类感知与自动格式化提示（如 sz/sh、合约月份）。
- **[图表与对比]**
  - 通用：K 线/面积/NAV 曲线，指标开关（MA/MACD/RSI/BOLL）。
  - 基金 vs 指数：支持选基准指数并显示跟踪误差（若可用）。
  - 期货：主力/具体合约切换、换月标记、显示持仓量（open_interest）。
- **[数据表与洞察]**
  - 基金：净值/累计净值、区间收益、年化、回撤、夏普（可选）。
  - 指数：区间收益、波动率、成分热力（可后续）。
  - 期货：合约属性、持仓量、主力标识；债券：价格/净价/全价（若有）。
- **[状态与可用性]**
  - 骨架屏/重试按钮/数据来源标签（Mongo/AKShare/Tushare）与缓存命中标识。
  - 本地记忆：最近资产类/日期范围/指标偏好。
- **[页面与路由]**
  - `/funds`、`/indices`、`/futures`、`/bonds` 专页；统一详情页支持分享与复制链接。

---

## 十八、后端扩展摘要更新

- **[资产类]**：新增 `INDEX_CN`, `INDEX_GLOBAL`；原有 `BOND_CN`, `FUTURES_CN`, `FUND_CN` 一并纳入统一路由。
- **[数据源管理]**：为指数定义独立优先级与降级顺序，复用 `_run_coro_safely` 与缓存优先策略。
- **[Provider]**：新增 `providers/china/indices.py`（AKShare/Tushare），输出列名标准化与代码映射工具。
- **[数据模型]**：`index_basic_info`、`index_daily` 集合与索引；对齐已有 timeseries 规范。
- **[统一接口]**：新增 `get_index_data_unified`、`get_index_info_unified`；服务层/日志同股指路径复用。
- **[校验与格式化]**：扩展 `instrument_validator`，新增指数识别与符号映射规则。

---

  ## 十九、更新的里程碑与排期（建议）
  
  - **M0：基础设施（~2 天）** 资产类枚举、接口骨架、Mongo 集合/索引、代码映射与校验。
  - **M1：基金（~3–4 天）** 开放式/ETF/LOF，指标与对比、统一接口与前端页面。
  - **M2：指数（~2–3 天）** 国内/国际指数，数据模型、接口、前端指数页与基准选择。
  - **M3：期货（~5–7 天）** 合约/主力/指数连续，拼接诊断与前端合约切换。
  - **M4：债券（~5–7 天）** 挂牌债基础覆盖与简化风险指标、前端债券页。
  - **M5：整合与上线（~2 天）** 前端整合、监控、灰度与验收。
  
 ---

 ## 二十、变更摘要（本次更新）

 - 新增“指数（国内/国际）”后端与前端需求。
 - 扩展前端导航、图表对比、主力合约切换与基准选择能力。
 - 后端增加指数资产类、接口与数据模型，完善数据源与降级路径。

 ---

 ## 附录：债券（BOND_CN）实施计划（优先）

 - **[目标与范围（Phase 1）]**
   - 上市可转债：基础信息、日线、快照（可选）。
   - 收益率曲线：1Y/3Y/5Y/10Y 期限点；用于利差与基准显示。
   - 事件信息（赎回/回售/条款调整）为次优先，可后续补充。
 - **[数据源优先级]**
   - MongoDB → AKShare （主） → Tushare （禁用，预留）。
 - **[关键 AKShare 端点（本地目录已验证）]**
   - 行情/历史：`bond_zh_hs_cov_spot`、`bond_zh_hs_cov_daily`。
   - 信息/估值：`bond_zh_cov_info`、`bond_zh_cov_info_ths`、`bond_zh_cov_value_analysis`。
   - 收益率曲线：`bond_china_yield`、`bond_china_close_return` （及 `*_map`）。
 - **[数据模型与 Mongo]**
   - 集合：`bond_basic_info(code)`、`bond_daily(code+date)`、`yield_curve_daily(date+tenor)`、`bond_events(code+date+event_type)`（后续）。
   - 索引：`(code,date)`、`(date,tenor)` 唯一；常用 `code`、`date`、`updated_at`。
 - **[Provider（AKShare）]** 新增 `providers/china/bonds.py`
   - `get_symbol_list()`、`get_basic_info(code)`、`get_historical_data(code, start, end)`、`get_realtime_quote(code)`、`get_yield_curve(start,end)`。
   - 阻塞 IO 用 `asyncio.to_thread`；列名标准化；代码映射 `123001.SZ ↔ 123001`。
 - **[DataSourceManager 与统一接口]**
   - 路由新增 `BOND_CN`，沿用 `_run_coro_safely` 与缓存优先、降级逻辑。
   - `interface.py` 新增：`get_cn_bond_data_unified(...) -> str`、`get_cn_bond_info_unified(...) -> dict`。
 - **[分析指标（Phase 1）]**
   - 通用：MA/MACD/RSI/BOLL、区间收益、年化、波动、回撤。
   - 债券增强：简化利差（债券收益率 - 基准曲线）；若收益率缺失则以价格动量替代提示。
 - **[同步任务（Jobs）]**
   - 每日：基本信息增量、日线增量、收益率曲线同步（T+0/T+1）。
   - 回填：近 1 年日线与曲线，限流与重试，upsert 写入。
 - **[API 与前端（最小可用）]**
   - API：`GET /api/cn/bonds/{code}/history`、`/info`、`/analytics`、`/yield-curve`。
   - 前端：`/bonds` 列表页与 `/bonds/{code}` 详情页，行情图 + 指标开关 + 基准曲线卡片。
 - **[测试与验收]**
   - 单元：代码/列名标准化、指标计算；集成：3 支转债 × 近 60 天；端到端：接口→服务→API。
   - 验收：统一接口返回成功、无事件循环/类型错误；前端渲染合理；日志含来源与降级信息。
