"""
指数数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any

# 指数集合更新配置
INDEX_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = {
    # A股指数实时行情-东财（需要symbol参数）
    "stock_zh_index_spot_em": {
        "display_name": "A股指数实时行情-东财",
        "update_description": "从东方财富网获取沪深京指数实时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定类型的指数实时行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数类型",
                    "type": "select",
                    "options": [
                        {"value": "沪深重要指数", "label": "沪深重要指数"},
                        {"value": "上证系列指数", "label": "上证系列指数"},
                        {"value": "深证系列指数", "label": "深证系列指数"},
                        {"value": "指数成份", "label": "指数成份"},
                        {"value": "中证系列指数", "label": "中证系列指数"},
                    ],
                    "default": "沪深重要指数",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有类型的指数实时行情",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # A股指数实时行情-新浪（无参数）
    "stock_zh_index_spot_sina": {
        "display_name": "A股指数实时行情-新浪",
        "update_description": "从新浪财经获取中国股票指数实时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新所有A股指数实时行情（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    # A股指数历史行情-新浪
    "stock_zh_index_daily": {
        "display_name": "A股指数历史行情-新浪",
        "update_description": "从新浪财经获取股票指数历史行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个指数的历史行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "text",
                    "placeholder": "请输入指数代码（如 sz399552）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有指数的历史行情（从实时行情集合获取代码）",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # A股指数历史行情-东财
    "stock_zh_index_daily_em": {
        "display_name": "A股指数历史行情-东财",
        "update_description": "从东方财富网获取股票指数历史行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个指数的历史行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "text",
                    "placeholder": "请输入指数代码（如 sz399552）",
                    "required": True
                },
                {
                    "name": "start_date",
                    "label": "开始日期",
                    "type": "text",
                    "placeholder": "如 19900101（可选）",
                    "required": False
                },
                {
                    "name": "end_date",
                    "label": "结束日期",
                    "type": "text",
                    "placeholder": "如 20500101（可选）",
                    "required": False
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有指数的历史行情",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # A股指数历史行情-通用
    "index_zh_a_hist": {
        "display_name": "A股指数历史行情-通用",
        "update_description": "从东方财富网获取中国股票指数行情数据（支持日/周/月）",
        "single_update": {
            "enabled": True,
            "description": "更新单个指数的历史行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "text",
                    "placeholder": "请输入指数代码（如 000016，不带市场标识）",
                    "required": True
                },
                {
                    "name": "period",
                    "label": "周期",
                    "type": "select",
                    "options": [
                        {"value": "daily", "label": "日线"},
                        {"value": "weekly", "label": "周线"},
                        {"value": "monthly", "label": "月线"},
                    ],
                    "default": "daily",
                    "required": False
                },
                {
                    "name": "start_date",
                    "label": "开始日期",
                    "type": "text",
                    "placeholder": "如 19700101（可选）",
                    "required": False
                },
                {
                    "name": "end_date",
                    "label": "结束日期",
                    "type": "text",
                    "placeholder": "如 22220101（可选）",
                    "required": False
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有指数的历史行情",
            "params": [
                {
                    "name": "period",
                    "label": "周期",
                    "type": "select",
                    "options": [
                        {"value": "daily", "label": "日线"},
                        {"value": "weekly", "label": "周线"},
                        {"value": "monthly", "label": "月线"},
                    ],
                    "default": "daily",
                    "required": False
                },
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # A股指数分时行情-东财
    "index_zh_a_hist_min_em": {
        "display_name": "A股指数分时行情-东财",
        "update_description": "从东方财富网获取指数分时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个指数的分时行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "text",
                    "placeholder": "请输入指数代码（如 000001，不带市场标识）",
                    "required": True
                },
                {
                    "name": "period",
                    "label": "周期",
                    "type": "select",
                    "options": [
                        {"value": "1", "label": "1分钟"},
                        {"value": "5", "label": "5分钟"},
                        {"value": "15", "label": "15分钟"},
                        {"value": "30", "label": "30分钟"},
                        {"value": "60", "label": "60分钟"},
                    ],
                    "default": "5",
                    "required": True
                },
                {
                    "name": "start_date",
                    "label": "开始时间",
                    "type": "text",
                    "placeholder": "如 2023-12-11 09:30:00（可选）",
                    "required": False
                },
                {
                    "name": "end_date",
                    "label": "结束时间",
                    "type": "text",
                    "placeholder": "如 2023-12-11 19:00:00（可选）",
                    "required": False
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有指数的分时行情",
            "params": [
                {
                    "name": "period",
                    "label": "周期",
                    "type": "select",
                    "options": [
                        {"value": "1", "label": "1分钟"},
                        {"value": "5", "label": "5分钟"},
                        {"value": "15", "label": "15分钟"},
                        {"value": "30", "label": "30分钟"},
                        {"value": "60", "label": "60分钟"},
                    ],
                    "default": "5",
                    "required": True
                },
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # 港股指数实时行情-新浪（无参数）
    "stock_hk_index_spot_sina": {
        "display_name": "港股指数实时行情-新浪",
        "update_description": "从新浪财经获取港股指数实时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新所有港股指数实时行情（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    # 港股指数历史行情-新浪
    "stock_hk_index_daily_sina": {
        "display_name": "港股指数历史行情-新浪",
        "update_description": "从新浪财经获取港股指数历史行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个港股指数的历史行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "text",
                    "placeholder": "请输入指数代码（如 CES100）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有港股指数的历史行情",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # 港股指数实时行情-东财（无参数）
    "stock_hk_index_spot_em": {
        "display_name": "港股指数实时行情-东财",
        "update_description": "从东方财富网获取港股指数实时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新所有港股指数实时行情（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    # 港股指数历史行情-东财
    "stock_hk_index_daily_em": {
        "display_name": "港股指数历史行情-东财",
        "update_description": "从东方财富网获取港股指数历史行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个港股指数的历史行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "text",
                    "placeholder": "请输入指数代码（如 HSTECF2L）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有港股指数的历史行情",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # 美股指数行情-新浪
    "index_us_stock_sina": {
        "display_name": "美股指数行情-新浪",
        "update_description": "从新浪财经获取美股指数行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个美股指数的行情数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数代码",
                    "type": "select",
                    "options": [
                        {"value": ".IXIC", "label": "纳斯达克综合指数"},
                        {"value": ".DJI", "label": "道琼斯工业平均指数"},
                        {"value": ".INX", "label": "标普500指数"},
                        {"value": ".NDX", "label": "纳斯达克100指数"},
                    ],
                    "default": ".INX",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有美股指数的行情数据",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
    # 全球指数实时行情-东财（无参数）
    "index_global_spot_em": {
        "display_name": "全球指数实时行情-东财",
        "update_description": "从东方财富网获取全球指数实时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新所有全球指数实时行情（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    # 全球指数历史行情-东财
    "index_global_hist_em": {
        "display_name": "全球指数历史行情-东财",
        "update_description": "从东方财富网获取全球指数历史行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个全球指数的历史行情",
            "params": [
                {
                    "name": "symbol",
                    "label": "指数名称",
                    "type": "text",
                    "placeholder": "请输入指数名称（如 美元指数）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有全球指数的历史行情",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    },
}


def get_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    return INDEX_UPDATE_CONFIGS.get(collection_name, {
        "display_name": collection_name,
        "update_description": f"更新 {collection_name} 数据",
        "single_update": {
            "enabled": True,
            "description": "单条更新",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }
            ]
        }
    })
