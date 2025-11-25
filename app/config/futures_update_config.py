"""
期货数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any

# 期货集合更新配置
FUTURES_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = {
    # 无参数的集合
    "futures_fees_info": {
        "display_name": "期货交易费用参照表",
        "update_description": "从openctp获取期货交易费用数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有期货交易费用数据", "params": []}
    },
    "futures_contract_info_dce": {
        "display_name": "大连商品交易所合约信息",
        "update_description": "获取大连商品交易所合约信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有合约信息", "params": []}
    },
    "futures_contract_info_gfex": {
        "display_name": "广州期货交易所合约信息",
        "update_description": "获取广州期货交易所合约信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有合约信息", "params": []}
    },
    "futures_hq_subscribe_exchange_symbol": {
        "display_name": "外盘品种代码表",
        "update_description": "获取外盘期货品种代码",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有外盘品种代码", "params": []}
    },
    "futures_global_spot_em": {
        "display_name": "外盘实时行情数据-东财",
        "update_description": "获取外盘期货实时行情",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有外盘实时行情", "params": []}
    },
    "index_hog_spot_price": {
        "display_name": "生猪市场价格指数",
        "update_description": "获取生猪市场价格指数数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取生猪价格指数", "params": []}
    },
    
    # 需要交易所选择参数的集合
    "futures_comm_info": {
        "display_name": "期货手续费与保证金",
        "update_description": "获取期货手续费与保证金数据",
        "single_update": {
            "enabled": True,
            "description": "按交易所获取手续费数据",
            "params": [
                {"name": "symbol", "label": "交易所", "type": "select", "default": "所有",
                 "options": [{"label": "所有", "value": "所有"}, {"label": "上海", "value": "上海"},
                            {"label": "大连", "value": "大连"}, {"label": "郑州", "value": "郑州"},
                            {"label": "中金", "value": "中金"}, {"label": "能源", "value": "能源"},
                            {"label": "广期", "value": "广期"}]}
            ]
        },
        "batch_update": {"enabled": True, "description": "获取所有交易所手续费数据", "params": []}
    },
    
    # 需要日期参数的集合
    "futures_rule": {
        "display_name": "期货规则-交易日历表",
        "update_description": "获取期货交易规则数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的交易规则",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式，如20241125", "required": False}]
        },
        "batch_update": {"enabled": True, "description": "获取最新交易规则数据", "params": []}
    },
    "futures_dce_position_rank": {
        "display_name": "大连商品交易所持仓排名",
        "update_description": "获取大连商品交易所持仓排名数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的持仓排名",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_gfex_position_rank": {
        "display_name": "广州期货交易所持仓排名",
        "update_description": "获取广州期货交易所持仓排名数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的持仓排名",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_warehouse_receipt_czce": {
        "display_name": "仓单日报-郑州商品交易所",
        "update_description": "获取郑州商品交易所仓单数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的仓单日报",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_warehouse_receipt_dce": {
        "display_name": "仓单日报-大连商品交易所",
        "update_description": "获取大连商品交易所仓单数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的仓单日报",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_shfe_warehouse_receipt": {
        "display_name": "仓单日报-上海期货交易所",
        "update_description": "获取上海期货交易所仓单数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的仓单日报",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_gfex_warehouse_receipt": {
        "display_name": "仓单日报-广州期货交易所",
        "update_description": "获取广州期货交易所仓单数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的仓单日报",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_to_spot_dce": {
        "display_name": "期转现-大商所",
        "update_description": "获取大商所期转现数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定月份的期转现数据",
            "params": [{"name": "date", "label": "年月", "type": "text", "placeholder": "YYYYMM格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_to_spot_czce": {
        "display_name": "期转现-郑商所",
        "update_description": "获取郑商所期转现数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的期转现数据",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_to_spot_shfe": {
        "display_name": "期转现-上期所",
        "update_description": "获取上期所期转现数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定月份的期转现数据",
            "params": [{"name": "date", "label": "年月", "type": "text", "placeholder": "YYYYMM格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_contract_info_shfe": {
        "display_name": "上海期货交易所合约信息",
        "update_description": "获取上海期货交易所合约信息",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的合约信息",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_contract_info_ine": {
        "display_name": "上海国际能源交易中心合约信息",
        "update_description": "获取上海国际能源交易中心合约信息",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的合约信息",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_contract_info_czce": {
        "display_name": "郑州商品交易所合约信息",
        "update_description": "获取郑州商品交易所合约信息",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的合约信息",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_contract_info_cffex": {
        "display_name": "中国金融期货交易所合约信息",
        "update_description": "获取中金所合约信息",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的合约信息",
            "params": [{"name": "date", "label": "交易日期", "type": "text", "placeholder": "YYYYMMDD格式", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    
    # 需要品种代码参数的集合
    "futures_inventory_99": {
        "display_name": "库存数据-99期货网",
        "update_description": "获取99期货网库存数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的库存数据",
            "params": [{"name": "symbol", "label": "品种", "type": "text", "placeholder": "如：豆一", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_inventory_em": {
        "display_name": "库存数据-东方财富",
        "update_description": "获取东方财富库存数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的库存数据",
            "params": [{"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如：A", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_spot_sys": {
        "display_name": "现期图",
        "update_description": "获取现期图数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的现期图",
            "params": [
                {"name": "symbol", "label": "品种", "type": "text", "placeholder": "如：铜", "required": True},
                {"name": "indicator", "label": "合约", "type": "text", "placeholder": "如：主力", "required": True}
            ]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_zh_spot": {
        "display_name": "内盘实时行情数据",
        "update_description": "获取内盘期货实时行情",
        "single_update": {
            "enabled": True,
            "description": "获取实时行情数据",
            "params": [
                {"name": "market", "label": "市场", "type": "select", "default": "CF",
                 "options": [{"label": "商品期货", "value": "CF"}, {"label": "金融期货", "value": "FF"}]}
            ]
        },
        "batch_update": {"enabled": True, "description": "获取所有内盘实时行情", "params": []}
    },
    "futures_zh_realtime": {
        "display_name": "内盘实时行情数据(品种)",
        "update_description": "按品种获取内盘实时行情",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的实时行情",
            "params": [{"name": "symbol", "label": "品种", "type": "text", "placeholder": "如：白糖", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_zh_minute_sina": {
        "display_name": "内盘分时行情数据",
        "update_description": "获取内盘分时数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的分时数据",
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如：IF2008", "required": True},
                {"name": "period", "label": "周期", "type": "select", "default": "1",
                 "options": [{"label": "1分钟", "value": "1"}, {"label": "5分钟", "value": "5"},
                            {"label": "15分钟", "value": "15"}, {"label": "30分钟", "value": "30"},
                            {"label": "60分钟", "value": "60"}]}
            ]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_hist_em": {
        "display_name": "内盘历史行情数据-东财",
        "update_description": "获取东方财富历史行情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的历史行情",
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如：热卷主连", "required": True},
                {"name": "period", "label": "周期", "type": "select", "default": "daily",
                 "options": [{"label": "日线", "value": "daily"}, {"label": "周线", "value": "weekly"},
                            {"label": "月线", "value": "monthly"}]}
            ]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_zh_daily_sina": {
        "display_name": "内盘历史行情数据-新浪",
        "update_description": "获取新浪历史行情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的历史行情",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如：RB0", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "get_futures_daily": {
        "display_name": "内盘历史行情数据-交易所",
        "update_description": "获取交易所历史行情",
        "single_update": {
            "enabled": True,
            "description": "获取指定交易所的历史行情",
            "params": [
                {"name": "market", "label": "交易所", "type": "select", "default": "DCE",
                 "options": [{"label": "大连", "value": "DCE"}, {"label": "郑州", "value": "CZCE"},
                            {"label": "上海", "value": "SHFE"}, {"label": "中金", "value": "CFFEX"},
                            {"label": "能源", "value": "INE"}, {"label": "广期", "value": "GFEX"}]},
                {"name": "start_date", "label": "开始日期", "type": "text", "placeholder": "YYYYMMDD", "required": True},
                {"name": "end_date", "label": "结束日期", "type": "text", "placeholder": "YYYYMMDD", "required": True}
            ]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_foreign_commodity_realtime": {
        "display_name": "外盘实时行情数据",
        "update_description": "获取外盘商品期货实时数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的外盘实时数据",
            "params": [{"name": "symbol", "label": "品种", "type": "text", "placeholder": "如：黄金", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_global_hist_em": {
        "display_name": "外盘历史行情数据-东财",
        "update_description": "获取东方财富外盘历史行情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的外盘历史行情",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如：HG25J", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_foreign_hist": {
        "display_name": "外盘历史行情数据-新浪",
        "update_description": "获取新浪外盘历史行情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的外盘历史行情",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_foreign_detail": {
        "display_name": "外盘合约详情",
        "update_description": "获取外盘期货合约详情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的详情",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_settlement_price_sgx": {
        "display_name": "新加坡交易所期货",
        "update_description": "获取新加坡交易所期货结算价",
        "single_update": {
            "enabled": True,
            "description": "获取结算价格",
            "params": [{"name": "date", "label": "日期", "type": "text", "placeholder": "YYYYMMDD格式（可选）", "required": False}]
        },
        "batch_update": {"enabled": True, "description": "获取最新结算价", "params": []}
    },
    "futures_main_sina": {
        "display_name": "期货连续合约",
        "update_description": "获取主力连续合约历史数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的连续合约数据",
            "params": [{"name": "symbol", "label": "品种代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_contract_detail": {
        "display_name": "期货合约详情-新浪",
        "update_description": "获取新浪期货合约详情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的详情",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_contract_detail_em": {
        "display_name": "期货合约详情-东财",
        "update_description": "获取东财期货合约详情",
        "single_update": {
            "enabled": True,
            "description": "获取指定合约的详情",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_index_ccidx": {
        "display_name": "中证商品指数",
        "update_description": "获取中证商品指数数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定指数数据",
            "params": [{"name": "symbol", "label": "指数名称", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_spot_stock": {
        "display_name": "现货与股票",
        "update_description": "获取现货与股票关联数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的关联数据",
            "params": [{"name": "symbol", "label": "品种名称", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_comex_inventory": {
        "display_name": "COMEX库存数据",
        "update_description": "获取COMEX库存数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定品种的COMEX库存",
            "params": [{"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如：铜、金", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_hog_core": {
        "display_name": "核心数据",
        "update_description": "获取生猪核心数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定区域的核心数据",
            "params": [{"name": "symbol", "label": "区域代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_hog_cost": {
        "display_name": "成本维度",
        "update_description": "获取生猪成本数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定区域的成本数据",
            "params": [{"name": "symbol", "label": "区域代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_hog_supply": {
        "display_name": "供应维度",
        "update_description": "获取生猪供应数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定区域的供应数据",
            "params": [{"name": "symbol", "label": "区域代码", "type": "text", "required": True}]
        },
        "batch_update": {"enabled": False, "description": "", "params": []}
    },
    "futures_news_shmet": {
        "display_name": "期货资讯",
        "update_description": "获取上海金属网快讯",
        "single_update": {
            "enabled": True,
            "description": "获取期货资讯",
            "params": [{"name": "symbol", "label": "关键词", "type": "text", "required": False}]
        },
        "batch_update": {"enabled": True, "description": "获取最新资讯", "params": []}
    },
}


def get_futures_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    if collection_name in FUTURES_UPDATE_CONFIGS:
        config = FUTURES_UPDATE_CONFIGS[collection_name].copy()
        config["collection_name"] = collection_name
        return config
    
    # 默认配置
    return {
        "collection_name": collection_name,
        "display_name": collection_name,
        "update_description": "该集合暂无详细配置",
        "single_update": {"enabled": True, "description": "更新数据", "params": []},
        "batch_update": {"enabled": True, "description": "批量更新数据", "params": []}
    }


def get_all_futures_collection_update_configs() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的更新配置"""
    return FUTURES_UPDATE_CONFIGS
