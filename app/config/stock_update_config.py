"""
股票数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any, List, Optional


# 集合类型定义 - 用于自动生成配置
COLLECTION_TYPES = {
    # 无参数 - 批量获取全部数据
    "no_params": [
        "stock_zh_a_spot_em", "stock_sh_a_spot_em", "stock_sz_a_spot_em", "stock_bj_a_spot_em",
        "stock_kc_a_spot_em", "stock_cy_a_spot_em", "stock_new_a_spot_em",
        "stock_hk_spot_em", "stock_us_spot_em", "stock_us_famous_spot_em",
        "stock_sse_summary", "stock_board_industry_name_em", "stock_board_concept_name_em",
        "stock_info_a_code_name", "stock_info_sh_name_code", "stock_info_sz_name_code",
        "stock_esg_hz_sina", "stock_esg_zd_sina", "stock_esg_rft_sina", "stock_esg_msci_sina",
        "stock_hot_rank_em", "stock_hot_up_em", "stock_hk_hot_rank_em",
        "stock_rank_xzjp_ths", "stock_rank_ljqs_ths", "stock_rank_ljqd_ths",
        "stock_rank_cxfl_ths", "stock_rank_cxsl_ths", "stock_rank_xxtp_ths", "stock_rank_xstp_ths",
        "stock_comment_em", "stock_market_activity_legu", "stock_a_congestion_lg",
        "stock_hsgt_fund_flow_summary_em", "stock_repurchase_em",
    ],
    # 需要日期参数
    "date_param": [
        "stock_zt_pool_em", "stock_zt_pool_previous_em", "stock_zt_pool_strong_em",
        "stock_zt_pool_sub_new_em", "stock_zt_pool_zbgc_em", "stock_zt_pool_dtgc_em",
        "stock_szse_summary", "stock_sse_deal_daily",
    ],
    # 需要股票代码参数
    "symbol_param": [
        "stock_individual_info_em", "stock_individual_basic_info_xq",
        "stock_financial_analysis_indicator", "stock_financial_analysis_indicator_em",
        "stock_gdfx_top_10_em", "stock_gdfx_free_top_10_em",
    ],
    # 需要股票代码和日期/周期参数
    "symbol_period_param": [
        "stock_zh_a_hist", "stock_hk_hist", "stock_us_hist",
        "stock_zh_a_hist_min_em", "stock_hk_hist_min_em",
    ],
    # 需要板块参数
    "board_param": [
        "stock_board_industry_cons_em", "stock_board_concept_cons_em",
        "stock_board_industry_hist_em", "stock_board_concept_hist_em",
    ],
}

# 默认唯一键
DEFAULT_UNIQUE_KEYS = {
    "spot": ["代码"],
    "hist": ["代码", "日期"],
    "pool": ["代码", "日期"],
    "summary": ["项目"],
    "board": ["板块名称"],
    "default": ["代码"],
}


def get_unique_keys(collection_name: str) -> List[str]:
    """根据集合名称获取唯一键"""
    if "spot" in collection_name:
        return DEFAULT_UNIQUE_KEYS["spot"]
    elif "hist" in collection_name:
        return DEFAULT_UNIQUE_KEYS["hist"]
    elif "pool" in collection_name:
        return DEFAULT_UNIQUE_KEYS["pool"]
    elif "summary" in collection_name:
        return DEFAULT_UNIQUE_KEYS["summary"]
    elif "board" in collection_name and "name" in collection_name:
        return DEFAULT_UNIQUE_KEYS["board"]
    return DEFAULT_UNIQUE_KEYS["default"]


def generate_config(collection_name: str, collection_type: str) -> Dict[str, Any]:
    """根据集合类型自动生成配置"""
    display_name = collection_name.replace("_", " ").title()
    
    config = {
        "display_name": display_name,
        "update_description": f"获取{display_name}数据",
        "akshare_func": collection_name,
        "unique_keys": get_unique_keys(collection_name),
    }
    
    if collection_type == "no_params":
        config["single_update"] = {"enabled": False, "description": "", "params": []}
        config["batch_update"] = {"enabled": True, "description": "一次性获取所有数据", "params": []}
        
    elif collection_type == "date_param":
        config["single_update"] = {
            "enabled": True,
            "description": "获取指定日期的数据",
            "params": [
                {"name": "date", "label": "日期", "type": "text", "placeholder": "20241125", "required": False}
            ]
        }
        config["batch_update"] = {"enabled": True, "description": "获取最新数据", "params": []}
        
    elif collection_type == "symbol_param":
        config["single_update"] = {
            "enabled": True,
            "description": "获取单个股票的数据",
            "params": [
                {"name": "symbol", "label": "股票代码", "type": "text", "placeholder": "000001", "required": True}
            ]
        }
        config["batch_update"] = {
            "enabled": True,
            "description": "批量更新所有股票数据",
            "params": [
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
        
    elif collection_type == "symbol_period_param":
        config["single_update"] = {
            "enabled": True,
            "description": "获取单个股票的历史数据",
            "params": [
                {"name": "symbol", "label": "股票代码", "type": "text", "placeholder": "000001", "required": True},
                {"name": "period", "label": "周期", "type": "select", "default": "daily",
                 "options": [{"label": "日线", "value": "daily"}, {"label": "周线", "value": "weekly"}, {"label": "月线", "value": "monthly"}]},
                {"name": "start_date", "label": "开始日期", "type": "text", "placeholder": "20200101"},
                {"name": "end_date", "label": "结束日期", "type": "text", "placeholder": "20241231"}
            ]
        }
        config["batch_update"] = {
            "enabled": True,
            "description": "批量更新历史数据",
            "params": [
                {"name": "period", "label": "周期", "type": "select", "default": "daily"},
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
        
    elif collection_type == "board_param":
        config["single_update"] = {
            "enabled": True,
            "description": "获取指定板块的数据",
            "params": [
                {"name": "symbol", "label": "板块名称", "type": "text", "required": True}
            ]
        }
        config["batch_update"] = {
            "enabled": True,
            "description": "批量更新所有板块数据",
            "params": [
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
    else:
        # 默认配置
        config["single_update"] = {"enabled": False, "description": "", "params": []}
        config["batch_update"] = {"enabled": True, "description": "一次性获取所有数据", "params": []}
    
    return config


def _build_configs() -> Dict[str, Dict[str, Any]]:
    """构建所有集合的配置"""
    configs = {}
    for ctype, collections in COLLECTION_TYPES.items():
        for cname in collections:
            configs[cname] = generate_config(cname, ctype)
    return configs


# 股票集合更新配置
STOCK_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = _build_configs()


def get_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    if collection_name in STOCK_UPDATE_CONFIGS:
        config = STOCK_UPDATE_CONFIGS[collection_name].copy()
        config["collection_name"] = collection_name
        return config
    
    # 默认配置：只有批量更新，无参数
    return {
        "collection_name": collection_name,
        "display_name": collection_name,
        "update_description": "获取数据",
        "akshare_func": collection_name,
        "unique_keys": ["代码"],
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    }


def get_all_collection_update_configs() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的更新配置"""
    return STOCK_UPDATE_CONFIGS
