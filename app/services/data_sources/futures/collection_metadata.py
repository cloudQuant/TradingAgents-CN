"""期货集合静态元信息配置"""

FUTURES_COLLECTION_METADATA = {
    # ==================== 基础信息类 ====================
    'futures_fees_info': {
        'display_name': '期货交易费用参照表',
        'description': 'openctp期货交易费用参照表，包含手续费率、保证金率等信息',
        'route': '/futures/collections/futures_fees_info',
        'order': 1,
    },
    'futures_comm_info': {
        'display_name': '期货手续费与保证金',
        'description': '期货手续费与保证金数据',
        'route': '/futures/collections/futures_comm_info',
        'order': 2,
    },
    'futures_rule': {
        'display_name': '期货规则-交易日历表',
        'description': '期货交易规则与交易日历',
        'route': '/futures/collections/futures_rule',
        'order': 3,
    },
    
    # ==================== 库存数据类 ====================
    'futures_inventory_99': {
        'display_name': '库存数据-99期货网',
        'description': '99期货网期货库存数据',
        'route': '/futures/collections/futures_inventory_99',
        'order': 4,
    },
    'futures_inventory_em': {
        'display_name': '库存数据-东方财富',
        'description': '东方财富期货库存数据',
        'route': '/futures/collections/futures_inventory_em',
        'order': 5,
    },
    
    # ==================== 持仓排名类 ====================
    'futures_dce_position_rank': {
        'display_name': '大连商品交易所-持仓排名',
        'description': '大连商品交易所期货持仓排名数据',
        'route': '/futures/collections/futures_dce_position_rank',
        'order': 6,
    },
    'futures_gfex_position_rank': {
        'display_name': '广州期货交易所-持仓排名',
        'description': '广州期货交易所期货持仓排名数据',
        'route': '/futures/collections/futures_gfex_position_rank',
        'order': 7,
    },
    
    # ==================== 仓单日报类 ====================
    'futures_warehouse_receipt_czce': {
        'display_name': '仓单日报-郑州商品交易所',
        'description': '郑州商品交易所仓单日报数据',
        'route': '/futures/collections/futures_warehouse_receipt_czce',
        'order': 8,
    },
    'futures_warehouse_receipt_dce': {
        'display_name': '仓单日报-大连商品交易所',
        'description': '大连商品交易所仓单日报数据',
        'route': '/futures/collections/futures_warehouse_receipt_dce',
        'order': 9,
    },
    'futures_shfe_warehouse_receipt': {
        'display_name': '仓单日报-上海期货交易所',
        'description': '上海期货交易所仓单日报数据',
        'route': '/futures/collections/futures_shfe_warehouse_receipt',
        'order': 10,
    },
    'futures_gfex_warehouse_receipt': {
        'display_name': '仓单日报-广州期货交易所',
        'description': '广州期货交易所仓单日报数据',
        'route': '/futures/collections/futures_gfex_warehouse_receipt',
        'order': 11,
    },
    
    # ==================== 期转现类 ====================
    'futures_to_spot_dce': {
        'display_name': '期转现-大商所',
        'description': '大连商品交易所期转现数据',
        'route': '/futures/collections/futures_to_spot_dce',
        'order': 12,
    },
    'futures_to_spot_czce': {
        'display_name': '期转现-郑商所',
        'description': '郑州商品交易所期转现数据',
        'route': '/futures/collections/futures_to_spot_czce',
        'order': 13,
    },
    'futures_to_spot_shfe': {
        'display_name': '期转现-上期所',
        'description': '上海期货交易所期转现数据',
        'route': '/futures/collections/futures_to_spot_shfe',
        'order': 14,
    },
    
    # ==================== 交割统计类 ====================
    'futures_delivery_dce': {
        'display_name': '交割统计-大商所',
        'description': '大连商品交易所交割统计数据',
        'route': '/futures/collections/futures_delivery_dce',
        'order': 15,
    },
    'futures_delivery_czce': {
        'display_name': '交割统计-郑商所',
        'description': '郑州商品交易所交割统计数据',
        'route': '/futures/collections/futures_delivery_czce',
        'order': 16,
    },
    'futures_delivery_shfe': {
        'display_name': '交割统计-上期所',
        'description': '上海期货交易所交割统计数据',
        'route': '/futures/collections/futures_delivery_shfe',
        'order': 17,
    },
    
    # ==================== 交割配对类 ====================
    'futures_delivery_match_dce': {
        'display_name': '交割配对-大商所',
        'description': '大连商品交易所交割配对数据',
        'route': '/futures/collections/futures_delivery_match_dce',
        'order': 18,
    },
    'futures_delivery_match_czce': {
        'display_name': '交割配对-郑商所',
        'description': '郑州商品交易所交割配对数据',
        'route': '/futures/collections/futures_delivery_match_czce',
        'order': 19,
    },
    
    # ==================== 库存与持仓类 ====================
    'futures_stock_shfe_js': {
        'display_name': '上海期货交易所-库存数据',
        'description': '上海期货交易所库存数据(金十)',
        'route': '/futures/collections/futures_stock_shfe_js',
        'order': 20,
    },
    'futures_hold_pos_sina': {
        'display_name': '成交持仓-新浪',
        'description': '新浪期货成交持仓数据',
        'route': '/futures/collections/futures_hold_pos_sina',
        'order': 21,
    },
    
    # ==================== 现期图类 ====================
    'futures_spot_sys': {
        'display_name': '现期图',
        'description': '期货现期图数据',
        'route': '/futures/collections/futures_spot_sys',
        'order': 22,
    },
    
    # ==================== 合约信息类 ====================
    'futures_contract_info_shfe': {
        'display_name': '上海期货交易所-合约信息',
        'description': '上海期货交易所合约信息',
        'route': '/futures/collections/futures_contract_info_shfe',
        'order': 23,
    },
    'futures_contract_info_ine': {
        'display_name': '上海国际能源交易中心-合约信息',
        'description': '上海国际能源交易中心合约信息',
        'route': '/futures/collections/futures_contract_info_ine',
        'order': 24,
    },
    'futures_contract_info_dce': {
        'display_name': '大连商品交易所-合约信息',
        'description': '大连商品交易所合约信息',
        'route': '/futures/collections/futures_contract_info_dce',
        'order': 25,
    },
    'futures_contract_info_czce': {
        'display_name': '郑州商品交易所-合约信息',
        'description': '郑州商品交易所合约信息',
        'route': '/futures/collections/futures_contract_info_czce',
        'order': 26,
    },
    'futures_contract_info_gfex': {
        'display_name': '广州期货交易所-合约信息',
        'description': '广州期货交易所合约信息',
        'route': '/futures/collections/futures_contract_info_gfex',
        'order': 27,
    },
    'futures_contract_info_cffex': {
        'display_name': '中国金融期货交易所-合约信息',
        'description': '中国金融期货交易所合约信息',
        'route': '/futures/collections/futures_contract_info_cffex',
        'order': 28,
    },
    
    # ==================== 内盘行情类 ====================
    'futures_zh_spot': {
        'display_name': '内盘-实时行情数据',
        'description': '内盘期货实时行情数据',
        'route': '/futures/collections/futures_zh_spot',
        'order': 29,
    },
    'futures_zh_realtime': {
        'display_name': '内盘-实时行情数据(品种)',
        'description': '内盘期货实时行情数据(按品种)',
        'route': '/futures/collections/futures_zh_realtime',
        'order': 30,
    },
    'futures_zh_minute_sina': {
        'display_name': '内盘-分时行情数据',
        'description': '内盘期货分时行情数据(新浪)',
        'route': '/futures/collections/futures_zh_minute_sina',
        'order': 31,
    },
    'futures_hist_em': {
        'display_name': '内盘-历史行情数据-东财',
        'description': '内盘期货历史行情数据(东方财富)',
        'route': '/futures/collections/futures_hist_em',
        'order': 32,
    },
    'futures_zh_daily_sina': {
        'display_name': '内盘-历史行情数据-新浪',
        'description': '内盘期货历史行情数据(新浪)',
        'route': '/futures/collections/futures_zh_daily_sina',
        'order': 33,
    },
    'get_futures_daily': {
        'display_name': '内盘-历史行情数据-交易所',
        'description': '内盘期货历史行情数据(交易所)',
        'route': '/futures/collections/get_futures_daily',
        'order': 34,
    },
    
    # ==================== 外盘行情类 ====================
    'futures_hq_subscribe_exchange_symbol': {
        'display_name': '外盘-品种代码表',
        'description': '外盘期货品种代码表',
        'route': '/futures/collections/futures_hq_subscribe_exchange_symbol',
        'order': 35,
    },
    'futures_foreign_commodity_realtime': {
        'display_name': '外盘-实时行情数据',
        'description': '外盘期货实时行情数据',
        'route': '/futures/collections/futures_foreign_commodity_realtime',
        'order': 36,
    },
    'futures_global_spot_em': {
        'display_name': '外盘-实时行情数据-东财',
        'description': '外盘期货实时行情数据(东方财富)',
        'route': '/futures/collections/futures_global_spot_em',
        'order': 37,
    },
    'futures_global_hist_em': {
        'display_name': '外盘-历史行情数据-东财',
        'description': '外盘期货历史行情数据(东方财富)',
        'route': '/futures/collections/futures_global_hist_em',
        'order': 38,
    },
    'futures_foreign_hist': {
        'display_name': '外盘-历史行情数据-新浪',
        'description': '外盘期货历史行情数据(新浪)',
        'route': '/futures/collections/futures_foreign_hist',
        'order': 39,
    },
    'futures_foreign_detail': {
        'display_name': '外盘-合约详情',
        'description': '外盘期货合约详情',
        'route': '/futures/collections/futures_foreign_detail',
        'order': 40,
    },
    
    # ==================== 其他类 ====================
    'futures_settlement_price_sgx': {
        'display_name': '新加坡交易所期货-结算价',
        'description': '新加坡交易所期货结算价',
        'route': '/futures/collections/futures_settlement_price_sgx',
        'order': 41,
    },
    'futures_main_sina': {
        'display_name': '期货连续合约-新浪',
        'description': '期货连续合约数据(新浪)',
        'route': '/futures/collections/futures_main_sina',
        'order': 42,
    },
    'futures_contract_detail': {
        'display_name': '期货合约详情-新浪',
        'description': '期货合约详情(新浪)',
        'route': '/futures/collections/futures_contract_detail',
        'order': 43,
    },
    'futures_contract_detail_em': {
        'display_name': '期货合约详情-东财',
        'description': '期货合约详情(东方财富)',
        'route': '/futures/collections/futures_contract_detail_em',
        'order': 44,
    },
    'futures_index_ccidx': {
        'display_name': '中证商品指数',
        'description': '中证商品指数数据',
        'route': '/futures/collections/futures_index_ccidx',
        'order': 45,
    },
    'futures_spot_stock': {
        'display_name': '现货与股票',
        'description': '现货与股票对比数据',
        'route': '/futures/collections/futures_spot_stock',
        'order': 46,
    },
    'futures_comex_inventory': {
        'display_name': 'COMEX库存数据',
        'description': 'COMEX库存数据',
        'route': '/futures/collections/futures_comex_inventory',
        'order': 47,
    },
    
    # ==================== 生猪数据类 ====================
    'futures_hog_core': {
        'display_name': '生猪-核心数据',
        'description': '生猪核心数据',
        'route': '/futures/collections/futures_hog_core',
        'order': 48,
    },
    'futures_hog_cost': {
        'display_name': '生猪-成本维度',
        'description': '生猪成本维度数据',
        'route': '/futures/collections/futures_hog_cost',
        'order': 49,
    },
    'futures_hog_supply': {
        'display_name': '生猪-供应维度',
        'description': '生猪供应维度数据',
        'route': '/futures/collections/futures_hog_supply',
        'order': 50,
    },
    'index_hog_spot_price': {
        'display_name': '生猪市场价格指数',
        'description': '生猪市场价格指数',
        'route': '/futures/collections/index_hog_spot_price',
        'order': 51,
    },
    'futures_news_shmet': {
        'display_name': '期货资讯',
        'description': '上海金属网期货资讯',
        'route': '/futures/collections/futures_news_shmet',
        'order': 52,
    },
}
