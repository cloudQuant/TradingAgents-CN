# Futures 数据集合 TODO 列表

> 数据来源：`app/services/data_sources/futures/collection_metadata.py` 中的 `FUTURES_COLLECTION_METADATA`。所有任务默认未完成（复选框保持 `[ ]`）。

## 基础信息类
- [x] 期货交易费用参照表 (`futures_fees_info`)
- [x] 期货手续费与保证金 (`futures_comm_info`)
- [x] 期货规则-交易日历表 (`futures_rule`)

## 库存数据类
- [x] 库存数据-99期货网 (`futures_inventory_99`)
- [x] 库存数据-东方财富 (`futures_inventory_em`)

## 持仓排名类
- [ ] 大连商品交易所-持仓排名 (`futures_dce_position_rank`)
- [ ] 广州期货交易所-持仓排名 (`futures_gfex_position_rank`)

## 仓单日报类
- [ ] 仓单日报-郑州商品交易所 (`futures_warehouse_receipt_czce`)
- [ ] 仓单日报-大连商品交易所 (`futures_warehouse_receipt_dce`)
- [ ] 仓单日报-上海期货交易所 (`futures_shfe_warehouse_receipt`)
- [ ] 仓单日报-广州期货交易所 (`futures_gfex_warehouse_receipt`)

## 期转现类
- [ ] 期转现-大商所 (`futures_to_spot_dce`)
- [ ] 期转现-郑商所 (`futures_to_spot_czce`)
- [ ] 期转现-上期所 (`futures_to_spot_shfe`)

## 交割统计类
- [ ] 交割统计-大商所 (`futures_delivery_dce`)
- [ ] 交割统计-郑商所 (`futures_delivery_czce`)
- [ ] 交割统计-上期所 (`futures_delivery_shfe`)

## 交割配对类
- [ ] 交割配对-大商所 (`futures_delivery_match_dce`)
- [ ] 交割配对-郑商所 (`futures_delivery_match_czce`)

## 库存与持仓类
- [ ] 上海期货交易所-库存数据 (`futures_stock_shfe_js`)
- [ ] 成交持仓-新浪 (`futures_hold_pos_sina`)

## 现期图类
- [ ] 现期图 (`futures_spot_sys`)

## 合约信息类
- [ ] 上海期货交易所-合约信息 (`futures_contract_info_shfe`)
- [ ] 上海国际能源交易中心-合约信息 (`futures_contract_info_ine`)
- [ ] 大连商品交易所-合约信息 (`futures_contract_info_dce`)
- [ ] 郑州商品交易所-合约信息 (`futures_contract_info_czce`)
- [ ] 广州期货交易所-合约信息 (`futures_contract_info_gfex`)
- [ ] 中国金融期货交易所-合约信息 (`futures_contract_info_cffex`)

## 内盘行情类
- [ ] 内盘-实时行情数据 (`futures_zh_spot`)
- [ ] 内盘-实时行情数据(品种) (`futures_zh_realtime`)
- [ ] 内盘-分时行情数据 (`futures_zh_minute_sina`)
- [ ] 内盘-历史行情数据-东财 (`futures_hist_em`)
- [ ] 内盘-历史行情数据-新浪 (`futures_zh_daily_sina`)
- [ ] 内盘-历史行情数据-交易所 (`get_futures_daily`)

## 外盘行情类
- [ ] 外盘-品种代码表 (`futures_hq_subscribe_exchange_symbol`)
- [ ] 外盘-实时行情数据 (`futures_foreign_commodity_realtime`)
- [ ] 外盘-实时行情数据-东财 (`futures_global_spot_em`)
- [ ] 外盘-历史行情数据-东财 (`futures_global_hist_em`)
- [ ] 外盘-历史行情数据-新浪 (`futures_foreign_hist`)
- [ ] 外盘-合约详情 (`futures_foreign_detail`)

## 其他类
- [ ] 新加坡交易所期货-结算价 (`futures_settlement_price_sgx`)
- [ ] 期货连续合约-新浪 (`futures_main_sina`)
- [ ] 期货合约详情-新浪 (`futures_contract_detail`)
- [ ] 期货合约详情-东财 (`futures_contract_detail_em`)
- [ ] 中证商品指数 (`futures_index_ccidx`)
- [ ] 现货与股票 (`futures_spot_stock`)
- [ ] COMEX库存数据 (`futures_comex_inventory`)

## 生猪数据类
- [ ] 生猪-核心数据 (`futures_hog_core`)
- [ ] 生猪-成本维度 (`futures_hog_cost`)
- [ ] 生猪-供应维度 (`futures_hog_supply`)
- [ ] 生猪市场价格指数 (`index_hog_spot_price`)

## 期货资讯类
- [ ] 期货资讯 (`futures_news_shmet`)
