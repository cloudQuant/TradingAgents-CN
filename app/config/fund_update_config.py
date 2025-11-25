"""
基金数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class UpdateParam(BaseModel):
    """更新参数定义"""
    name: str  # 参数名称（后端使用）
    label: str  # 显示标签
    type: str  # 参数类型：text, number, select
    placeholder: str = ""  # 占位符
    required: bool = False  # 是否必填
    default: Any = None  # 默认值
    options: Optional[List[Dict[str, Any]]] = None  # select类型的选项
    min: Optional[float] = None  # number类型的最小值
    max: Optional[float] = None  # number类型的最大值
    step: Optional[float] = None  # number类型的步长


class UpdateConfig(BaseModel):
    """更新配置"""
    enabled: bool = True  # 是否启用
    description: str = ""  # 更新说明
    params: List[UpdateParam] = []  # 参数列表


class CollectionUpdateConfig(BaseModel):
    """集合更新配置"""
    collection_name: str
    display_name: str
    update_description: str  # 总体更新说明
    single_update: UpdateConfig  # 单条更新配置
    batch_update: UpdateConfig  # 批量更新配置


# 基金集合更新配置
FUND_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = {
    # 无参数的集合 - 只有批量更新
    "fund_name_em": {
        "display_name": "基金名称列表",
        "update_description": "将从东方财富网获取所有基金的基本信息数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有基金名称数据",
            "params": []
        }
    },
    "fund_purchase_status": {
        "display_name": "基金申购状态",
        "update_description": "将从东方财富网获取所有基金的申购赎回状态数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有基金的申购赎回状态",
            "params": []
        }
    },
    "fund_open_fund_daily_em": {
        "display_name": "开放式基金实时行情",
        "update_description": "将从东方财富网获取所有开放式基金的实时净值数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有开放式基金实时净值",
            "params": []
        }
    },
    "fund_money_fund_daily_em": {
        "display_name": "货币型基金实时行情",
        "update_description": "将从东方财富网获取所有货币型基金的实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有货币型基金实时行情",
            "params": []
        }
    },
    "fund_financial_fund_daily_em": {
        "display_name": "理财型基金实时行情",
        "update_description": "将从东方财富网获取所有理财型基金的实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有理财型基金实时行情",
            "params": []
        }
    },
    "fund_etf_fund_daily_em": {
        "display_name": "场内交易基金实时行情",
        "update_description": "将从东方财富网获取所有场内交易基金的实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有场内交易基金实时行情",
            "params": []
        }
    },
    "fund_etf_spot_em": {
        "display_name": "ETF实时行情",
        "update_description": "将从东方财富网获取ETF基金实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有ETF实时行情",
            "params": []
        }
    },
    "fund_lof_spot_em": {
        "display_name": "LOF实时行情",
        "update_description": "将从东方财富网获取LOF基金实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有LOF实时行情",
            "params": []
        }
    },
    
    # 需要基金代码参数的集合
    "fund_basic_info": {
        "display_name": "基金基本信息",
        "update_description": "将从雪球获取基金的详细基本信息数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的基本信息",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的基本信息",
            "params": [
                {
                    "name": "batch_size",
                    "label": "每批数量",
                    "type": "number",
                    "default": 50,
                    "min": 10,
                    "max": 200,
                    "step": 10
                },
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 20,
                    "step": 1
                }
            ]
        }
    },
    "fund_open_fund_info_em": {
        "display_name": "开放式基金历史行情",
        "update_description": "获取开放式基金的历史净值数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的历史净值",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从fund_open_fund_daily_em集合获取代码列表批量更新",
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
    "fund_money_fund_info_em": {
        "display_name": "货币型基金历史行情",
        "update_description": "获取货币型基金的历史收益数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的历史收益",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从fund_money_fund_daily_em集合获取代码列表批量更新",
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
    "fund_financial_fund_info_em": {
        "display_name": "理财型基金历史行情",
        "update_description": "获取理财型基金的历史净值数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的历史净值",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从fund_financial_fund_daily_em集合获取代码列表批量更新",
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
    "fund_etf_fund_info_em": {
        "display_name": "场内交易基金历史行情",
        "update_description": "获取场内交易基金的历史净值数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的历史净值",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 511280）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从fund_etf_fund_daily_em集合获取代码列表批量更新",
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
    
    # 需要年份参数的集合
    "fund_fh_em": {
        "display_name": "基金分红数据",
        "update_description": "获取基金分红数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定年份的分红数据",
            "params": [
                {
                    "name": "year",
                    "label": "年份",
                    "type": "text",
                    "placeholder": "请输入年份（如 2024）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新1999年至今所有年份的分红数据",
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
    "fund_cf_em": {
        "display_name": "基金拆分数据",
        "update_description": "获取基金拆分数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定年份的拆分数据",
            "params": [
                {
                    "name": "year",
                    "label": "年份",
                    "type": "text",
                    "placeholder": "请输入年份（如 2020）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新2005年至今所有年份的拆分数据",
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
    
    # 需要基金代码和年份参数的集合
    "fund_portfolio_hold_em": {
        "display_name": "基金股票持仓",
        "update_description": "获取基金股票持仓数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金指定年份的股票持仓",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                },
                {
                    "name": "year",
                    "label": "年份",
                    "type": "text",
                    "placeholder": "请输入年份（如 2024）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的股票持仓数据",
            "params": [
                {
                    "name": "year",
                    "label": "年份（可选）",
                    "type": "text",
                    "placeholder": "留空更新所有年份，如 2024",
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
    "fund_portfolio_bond_hold_em": {
        "display_name": "基金债券持仓",
        "update_description": "获取基金债券持仓数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金指定年份的债券持仓",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                },
                {
                    "name": "year",
                    "label": "年份",
                    "type": "text",
                    "placeholder": "请输入年份（如 2024）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的债券持仓数据",
            "params": [
                {
                    "name": "year",
                    "label": "年份（可选）",
                    "type": "text",
                    "placeholder": "留空更新所有年份，如 2024",
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
    "fund_portfolio_change_em": {
        "display_name": "基金重大变动",
        "update_description": "获取基金重大变动数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金指定年份的重大变动",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                },
                {
                    "name": "year",
                    "label": "年份",
                    "type": "text",
                    "placeholder": "请输入年份（如 2024）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的重大变动数据",
            "params": [
                {
                    "name": "year",
                    "label": "年份",
                    "type": "text",
                    "placeholder": "必填，如 2024",
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
    
    # 基金类型选择的集合
    "fund_value_estimation_em": {
        "display_name": "基金净值估算",
        "update_description": "获取基金净值估算数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "按基金类型获取净值估算数据",
            "params": [
                {
                    "name": "fund_type",
                    "label": "基金类型",
                    "type": "select",
                    "default": "全部",
                    "options": [
                        {"label": "全部", "value": "全部"},
                        {"label": "股票型", "value": "股票型"},
                        {"label": "混合型", "value": "混合型"},
                        {"label": "债券型", "value": "债券型"},
                        {"label": "指数型", "value": "指数型"},
                        {"label": "QDII", "value": "QDII"},
                        {"label": "LOF", "value": "LOF"},
                        {"label": "FOF", "value": "FOF"}
                    ]
                }
            ]
        }
    },
    "fund_spot_sina": {
        "display_name": "新浪基金实时行情",
        "update_description": "从新浪财经获取基金实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "按基金类型获取实时行情",
            "params": [
                {
                    "name": "fund_type",
                    "label": "基金类型",
                    "type": "select",
                    "default": "全部",
                    "options": [
                        {"label": "全部", "value": "全部"},
                        {"label": "封闭式基金", "value": "封闭式基金"},
                        {"label": "ETF基金", "value": "ETF基金"},
                        {"label": "LOF基金", "value": "LOF基金"}
                    ]
                }
            ]
        }
    },
}


def get_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    if collection_name in FUND_UPDATE_CONFIGS:
        config = FUND_UPDATE_CONFIGS[collection_name].copy()
        config["collection_name"] = collection_name
        return config
    
    # 默认配置：只有批量更新，无参数
    return {
        "collection_name": collection_name,
        "display_name": collection_name,
        "update_description": "该集合暂不支持自动更新",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有数据",
            "params": []
        }
    }


def get_all_collection_update_configs() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的更新配置"""
    return FUND_UPDATE_CONFIGS
