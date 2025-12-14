"""指数集合静态元信息"""

INDEX_COLLECTION_METADATA = {
    # A股指数实时行情
    'stock_zh_index_spot_em': {
        'display_name': 'A股指数实时行情-东财',
        'description': '东方财富网-行情中心-沪深京指数实时行情数据',
        'route': '/indexs/collections/stock_zh_index_spot_em',
        'order': 0,
    },
    'stock_zh_index_spot_sina': {
        'display_name': 'A股指数实时行情-新浪',
        'description': '新浪财经-中国股票指数实时行情数据',
        'route': '/indexs/collections/stock_zh_index_spot_sina',
        'order': 1,
    },
    # A股指数历史行情
    'stock_zh_index_daily': {
        'display_name': 'A股指数历史行情-新浪',
        'description': '新浪财经-股票指数历史行情数据（日频）',
        'route': '/indexs/collections/stock_zh_index_daily',
        'order': 2,
    },
    'stock_zh_index_daily_tx': {
        'display_name': 'A股指数历史行情-腾讯',
        'description': '腾讯财经-股票指数历史行情数据',
        'route': '/indexs/collections/stock_zh_index_daily_tx',
        'order': 3,
    },
    'stock_zh_index_daily_em': {
        'display_name': 'A股指数历史行情-东财',
        'description': '东方财富网-股票指数历史行情数据（日频）',
        'route': '/indexs/collections/stock_zh_index_daily_em',
        'order': 4,
    },
    'index_zh_a_hist': {
        'display_name': 'A股指数历史行情-通用',
        'description': '东方财富网-中国股票指数行情数据（支持日/周/月）',
        'route': '/indexs/collections/index_zh_a_hist',
        'order': 5,
    },
    # A股指数分时行情
    'index_zh_a_hist_min_em': {
        'display_name': 'A股指数分时行情-东财',
        'description': '东方财富网-指数分时行情数据（1/5/15/30/60分钟）',
        'route': '/indexs/collections/index_zh_a_hist_min_em',
        'order': 6,
    },
    # 港股指数
    'stock_hk_index_spot_sina': {
        'display_name': '港股指数实时行情-新浪',
        'description': '新浪财经-行情中心-港股指数实时行情',
        'route': '/indexs/collections/stock_hk_index_spot_sina',
        'order': 10,
    },
    'stock_hk_index_daily_sina': {
        'display_name': '港股指数历史行情-新浪',
        'description': '新浪财经-港股指数历史行情数据',
        'route': '/indexs/collections/stock_hk_index_daily_sina',
        'order': 11,
    },
    'stock_hk_index_spot_em': {
        'display_name': '港股指数实时行情-东财',
        'description': '东方财富网-行情中心-港股指数实时行情',
        'route': '/indexs/collections/stock_hk_index_spot_em',
        'order': 12,
    },
    'stock_hk_index_daily_em': {
        'display_name': '港股指数历史行情-东财',
        'description': '东方财富网-港股指数历史行情数据',
        'route': '/indexs/collections/stock_hk_index_daily_em',
        'order': 13,
    },
    # 美股指数
    'index_us_stock_sina': {
        'display_name': '美股指数行情-新浪',
        'description': '新浪财经-美股指数行情数据（纳斯达克、道琼斯、标普500等）',
        'route': '/indexs/collections/index_us_stock_sina',
        'order': 20,
    },
    # 全球指数
    'index_global_spot_em': {
        'display_name': '全球指数实时行情-东财',
        'description': '东方财富网-行情中心-全球指数实时行情数据',
        'route': '/indexs/collections/index_global_spot_em',
        'order': 30,
    },
    'index_global_hist_em': {
        'display_name': '全球指数历史行情-东财',
        'description': '东方财富网-行情中心-全球指数历史行情数据',
        'route': '/indexs/collections/index_global_hist_em',
        'order': 31,
    },
}
