# 期货数据集合API测试汇总

## 测试时间
2025-12-14 (更新)

## 前端功能测试结果 (最新)
- **更新配置API (update-config)**: 52/52 全部成功 ✅
- **刷新API (refresh)**: 52/52 全部成功 ✅

## AKShare数据源测试结果统计
- 通过: 31
- 警告(空数据): 2
- 失败: 19 (外部数据源问题，非代码问题)
- 总计: 52

## 接口状态分类

### ✅ 正常工作的接口 (31个)

| 序号 | 接口名称 | 显示名称 | 数据量 |
|-----|---------|---------|-------|
| 1 | futures_fees_info | 期货交易费用参照表 | 848 |
| 3 | futures_contract_info_gfex | 广州期货交易所合约信息 | 47 |
| 4 | futures_hq_subscribe_exchange_symbol | 外盘品种代码表 | 30 |
| 5 | futures_global_spot_em | 外盘实时行情数据-东财 | 620 |
| 6 | index_hog_spot_price | 生猪市场价格指数 | 550 |
| 7 | futures_news_shmet | 期货资讯 | 20 |
| 9 | futures_rule | 期货规则-交易日历表 | 134 |
| 11 | futures_gfex_position_rank | 广州期货交易所-持仓排名 | 9 |
| 12 | futures_warehouse_receipt_czce | 仓单日报-郑州商品交易所 | 25 |
| 14 | futures_shfe_warehouse_receipt | 仓单日报-上海期货交易所 | 28 |
| 15 | futures_gfex_warehouse_receipt | 仓单日报-广州期货交易所 | 2 |
| 16 | futures_contract_info_shfe | 上海期货交易所-合约信息 | 276 |
| 17 | futures_contract_info_ine | 上海国际能源交易中心-合约信息 | 62 |
| 18 | futures_contract_info_czce | 郑州商品交易所-合约信息 | 232 |
| 19 | futures_contract_info_cffex | 中国金融期货交易所-合约信息 | 898 |
| 21 | futures_to_spot_czce | 期转现-郑州 | 1 |
| 28 | futures_settlement_price_sgx | 新加坡交易所期货-结算价 | 2448 |
| 29 | futures_comm_info | 期货手续费与保证金 | 819 |
| 30 | futures_inventory_99 | 库存数据-99期货网 | 4196 |
| 31 | futures_inventory_em | 库存数据-东方财富 | 67 |
| 33 | futures_spot_sys | 现期图 | 11 |
| 35 | futures_zh_realtime | 内盘-实时行情数据(品种) | 7 |
| 36 | futures_zh_minute_sina | 内盘-分钟数据 | 1023 |
| 37 | futures_zh_daily_sina | 内盘-日线数据 | 4060 |
| 38 | futures_main_sina | 期货连续合约-新浪 | 4017 |
| 39 | futures_contract_detail | 期货合约详情-新浪 | 123 |
| 41 | futures_foreign_commodity_realtime | 外盘-实时行情 | 1 |
| 43 | futures_foreign_hist | 外盘-历史行情 | 2593 |
| 44 | futures_foreign_detail | 外盘-合约详情 | 4 |
| 47 | futures_comex_inventory | COMEX库存数据 | 1246 |
| 52 | get_futures_daily | 内盘-历史行情-交易所 | 2800 |

### ⚠️ 返回空数据的接口 (2个)

| 序号 | 接口名称 | 显示名称 | 原因 |
|-----|---------|---------|-----|
| 8 | futures_stock_shfe_js | 上海期货交易所-库存数据 | 返回空DataFrame |
| 32 | futures_hold_pos_sina | 持仓数据-新浪 | 返回空DataFrame（可能是非交易时间） |

### ❌ 失败的接口 (19个)

#### 大连商品交易所相关 (网络/数据源问题)
| 序号 | 接口名称 | 显示名称 | 错误原因 |
|-----|---------|---------|---------|
| 2 | futures_contract_info_dce | 大连商品交易所合约信息 | JSON解析错误 |
| 10 | futures_dce_position_rank | 大连商品交易所-持仓排名 | 文件格式错误 |
| 13 | futures_warehouse_receipt_dce | 仓单日报-大连商品交易所 | JSON解析错误 |
| 20 | futures_to_spot_dce | 期转现-大连 | 未找到表格 |
| 23 | futures_delivery_dce | 交割信息-大连 | 未找到表格 |
| 26 | futures_delivery_match_dce | 交割配对-大连 | 未找到表格 |

#### 上海期货交易所相关 (网络问题)
| 序号 | 接口名称 | 显示名称 | 错误原因 |
|-----|---------|---------|---------|
| 22 | futures_to_spot_shfe | 期转现-上海 | DNS解析失败 |
| 25 | futures_delivery_shfe | 交割信息-上海 | DNS解析失败 |

#### 郑州商品交易所相关
| 序号 | 接口名称 | 显示名称 | 错误原因 |
|-----|---------|---------|---------|
| 24 | futures_delivery_czce | 交割信息-郑州 | Excel格式错误 |
| 27 | futures_delivery_match_czce | 交割配对-郑州 | 参数错误 |

#### AKShare接口bug
| 序号 | 接口名称 | 显示名称 | 错误原因 |
|-----|---------|---------|---------|
| 34 | futures_zh_spot | 内盘-实时行情数据 | 数组长度不匹配 |
| 40 | futures_contract_detail_em | 期货合约详情-东财 | NoneType错误 |
| 42 | futures_global_hist_em | 外盘-历史行情-东财 | NoneType错误 |
| 45 | futures_index_ccidx | 中证商品指数 | JSON解析错误 |
| 46 | futures_spot_stock | 现货库存 | 索引错误 |
| 51 | futures_hist_em | 内盘-历史行情-东财 | 索引越界 |

#### 生猪数据相关 (数据源问题)
| 序号 | 接口名称 | 显示名称 | 错误原因 |
|-----|---------|---------|---------|
| 48 | futures_hog_core | 生猪核心数据 | 返回None |
| 49 | futures_hog_cost | 生猪成本数据 | 返回None |
| 50 | futures_hog_supply | 生猪供应数据 | 返回None |

## 问题分析

### 1. 大连商品交易所接口问题
大连商品交易所的多个接口返回JSON解析错误或找不到表格，可能是：
- 交易所网站结构变更
- 数据格式变更
- 需要更新AKShare版本

### 2. 上海期货交易所网络问题
`tsite.shfe.com.cn` DNS解析失败，可能是：
- 网络环境问题
- 交易所域名变更

### 3. AKShare接口bug
多个东财(em)相关接口出现NoneType错误，可能是：
- 东方财富网站结构变更
- AKShare版本需要更新

### 4. 生猪数据接口
生猪相关的三个接口都返回None，可能是：
- 数据源不可用
- 需要特定参数

## 建议

1. **更新AKShare版本**: `pip install akshare --upgrade`
2. **检查网络环境**: 确保可以访问各交易所网站
3. **对于失败的接口**: 在服务端添加错误处理，返回友好的错误信息
4. **定期运行测试**: 监控接口可用性变化
