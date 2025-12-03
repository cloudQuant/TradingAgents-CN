"""
基金数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
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
    "fund_etf_spot_em": {
        "display_name": "ETF实时行情",
        "update_description": "将从东方财富网获取ETF基金实时行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新所有ETF实时行情数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
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
        "update_description": "获取基金分红数据（无参数，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金分红数据",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "此接口不支持批量更新",
            "params": []
        }
    },
    "fund_cf_em": {
        "display_name": "基金拆分数据",
        "update_description": "获取基金拆分数据（无参数接口，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金拆分数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_fh_rank_em": {
        "display_name": "基金分红排行数据",
        "update_description": "获取基金分红排行数据（无参数接口，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金分红排行数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_open_fund_rank_em": {
        "display_name": "开放式基金排行数据",
        "update_description": "获取开放式基金排行数据（无参数接口，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有开放式基金排行数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_exchange_rank_em": {
        "display_name": "场内基金排行数据",
        "update_description": "获取场内基金排行数据（无参数接口，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有场内基金排行数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_money_rank_em": {
        "display_name": "货币型基金排行数据",
        "update_description": "获取货币型基金排行数据（无参数接口，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有货币型基金排行数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_hk_rank_em": {
        "display_name": "香港基金排行数据",
        "update_description": "获取香港基金排行数据（无参数接口，直接获取所有历史数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有香港基金排行数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
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
    "fund_portfolio_industry_allocation_em": {
        "display_name": "基金行业配置",
        "update_description": "获取基金行业配置数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金指定年份的行业配置",
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
            "description": "批量更新所有基金的行业配置数据",
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
                },
                {
                    "name": "indicator",
                    "label": "指标类型",
                    "type": "select",
                    "options": [
                        {"value": "累计买入", "label": "累计买入"},
                        {"value": "累计卖出", "label": "累计卖出"}
                    ],
                    "default": "累计买入",
                    "required": False
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
                    "name": "indicator",
                    "label": "指标类型",
                    "type": "select",
                    "options": [
                        {"value": "累计买入", "label": "累计买入"},
                        {"value": "累计卖出", "label": "累计卖出"}
                    ],
                    "default": "累计买入",
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
    
    # 无参数接口集合
    "fund_rating_all_em": {
        "display_name": "基金评级总汇",
        "update_description": "获取基金评级总汇数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金评级总汇数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_manager_em": {
        "display_name": "基金经理",
        "update_description": "获取基金经理数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金经理数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_new_found_em": {
        "display_name": "新发基金",
        "update_description": "获取新发基金数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有新发基金数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_scale_open_sina": {
        "display_name": "开放式基金规模",
        "update_description": "获取开放式基金规模数据（自动遍历所有基金类型）",
        "single_update": {
            "enabled": True,
            "description": "更新所有开放式基金规模数据（自动遍历股票型、混合型、债券型、货币型、QDII基金）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "不需要批量更新，单条更新已遍历所有基金类型",
            "params": []
        }
    },
    "fund_scale_close_sina": {
        "display_name": "封闭式基金规模",
        "update_description": "获取封闭式基金规模数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有封闭式基金规模数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_aum_em": {
        "display_name": "基金规模详情",
        "update_description": "获取基金公司管理规模数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金公司管理规模数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_aum_trend_em": {
        "display_name": "基金规模走势",
        "update_description": "获取市场全部基金规模走势数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金规模走势数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_aum_hist_em": {
        "display_name": "基金公司历年管理规模",
        "update_description": "获取基金公司历年管理规模数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定年份的基金公司管理规模数据",
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
            "description": "批量更新所有年份的基金公司管理规模数据（从2001年开始）",
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
    "reits_realtime_em": {
        "display_name": "REITs实时行情",
        "update_description": "获取REITs实时行情数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有REITs实时行情数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "reits_hist_em": {
        "display_name": "REITs历史行情",
        "update_description": "获取REITs历史行情数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个REITs的历史行情数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "REITs代码",
                    "type": "text",
                    "placeholder": "请输入REITs代码（如 508097）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有REITs的历史行情数据（从reits_realtime_em获取代码）",
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
    "fund_report_stock_cninfo": {
        "display_name": "基金重仓股",
        "update_description": "获取基金重仓股数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定季度日期的基金重仓股数据",
            "params": [
                {
                    "name": "date",
                    "label": "季度日期",
                    "type": "select",
                    "placeholder": "请选择季度日期",
                    "required": True,
                    "options": sorted(
                        [
                            {"value": f"{year}-03-31", "label": f"{year}-03-31"}
                            for year in range(2017, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-06-30", "label": f"{year}-06-30"}
                            for year in range(2017, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-09-30", "label": f"{year}-09-30"}
                            for year in range(2017, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-12-31", "label": f"{year}-12-31"}
                            for year in range(2017, datetime.now().year + 1)
                        ],
                        key=lambda x: x["value"],
                        reverse=True  # 倒序排列，最新的在前面
                    )
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有季度日期的基金重仓股数据（从2017年Q1开始）",
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
    "fund_report_industry_allocation_cninfo": {
        "display_name": "基金行业配置",
        "update_description": "获取基金行业配置数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定季度日期的基金行业配置数据",
            "params": [
                {
                    "name": "date",
                    "label": "季度日期",
                    "type": "select",
                    "placeholder": "请选择季度日期",
                    "required": True,
                    "options": sorted(
                        [
                            {"value": f"{year}-03-31", "label": f"{year}-03-31"}
                            for year in range(2017, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-06-30", "label": f"{year}-06-30"}
                            for year in range(2017, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-09-30", "label": f"{year}-09-30"}
                            for year in range(2017, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-12-31", "label": f"{year}-12-31"}
                            for year in range(2017, datetime.now().year + 1)
                        ],
                        key=lambda x: x["value"],
                        reverse=True  # 倒序排列，最新的在前面
                    )
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有季度日期的基金行业配置数据（从2017年Q1开始）",
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
    "fund_report_asset_allocation_cninfo": {
        "display_name": "基金资产配置",
        "update_description": "获取基金资产配置数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金资产配置数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_scale_change_em": {
        "display_name": "规模变动",
        "update_description": "获取基金规模变动数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金规模变动数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_hold_structure_em": {
        "display_name": "持有人结构",
        "update_description": "获取基金持有人结构数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金持有人结构数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_stock_position_lg": {
        "display_name": "股票型基金仓位",
        "update_description": "获取股票型基金仓位数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有股票型基金仓位数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_balance_position_lg": {
        "display_name": "平衡混合型基金仓位",
        "update_description": "获取平衡混合型基金仓位数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有平衡混合型基金仓位数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_linghuo_position_lg": {
        "display_name": "灵活配置型基金仓位",
        "update_description": "获取灵活配置型基金仓位数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有灵活配置型基金仓位数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
        }
    },
    "fund_announcement_dividend_em": {
        "display_name": "基金分红公告",
        "update_description": "获取基金分红公告数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的分红公告数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的分红公告数据（从fund_name_em获取代码）",
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
    "fund_announcement_report_em": {
        "display_name": "基金定期报告公告",
        "update_description": "获取基金定期报告公告数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的定期报告公告数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的定期报告公告数据（从fund_name_em获取代码）",
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
    "fund_announcement_personnel_em": {
        "display_name": "基金人事调整公告",
        "update_description": "获取基金人事调整公告数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的人事调整公告数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的人事调整公告数据（从fund_name_em获取代码）",
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
    "fund_rating_sh_em": {
        "display_name": "上海证券评级",
        "update_description": "获取上海证券基金评级数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定季度日期的上海证券评级数据",
            "params": [
                {
                    "name": "quarter_date",
                    "label": "季度日期",
                    "type": "select",
                    "placeholder": "请选择季度日期（格式：YYYY-MM-DD）",
                    "required": True,
                    "options": sorted(
                        [
                            {"value": f"{year}-03-31", "label": f"{year}-03-31"}
                            for year in range(2010, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-06-30", "label": f"{year}-06-30"}
                            for year in range(2010, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-09-30", "label": f"{year}-09-30"}
                            for year in range(2010, datetime.now().year + 1)
                        ] + [
                            {"value": f"{year}-12-31", "label": f"{year}-12-31"}
                            for year in range(2010, datetime.now().year + 1)
                        ],
                        key=lambda x: x["value"],
                        reverse=True
                    )
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有季度日期的上海证券评级数据（从2010年Q1开始）",
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
    "fund_rating_zs_em": {
        "display_name": "招商证券评级",
        "update_description": "获取招商证券基金评级数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定季度日期的招商证券评级数据",
            "params": [
                {
                    "name": "quarter_date",
                    "label": "季度日期",
                    "type": "text",
                    "placeholder": "请输入季度日期（格式：YYYY-MM-DD，如 2024-03-31）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有季度日期的招商证券评级数据（从2010年Q1开始）",
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
    "fund_rating_ja_em": {
        "display_name": "济安金信评级",
        "update_description": "获取济安金信基金评级数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定季度日期的济安金信评级数据",
            "params": [
                {
                    "name": "quarter_date",
                    "label": "季度日期",
                    "type": "text",
                    "placeholder": "请输入季度日期（格式：YYYY-MM-DD，如 2024-03-31）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有季度日期的济安金信评级数据（从2010年Q1开始）",
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
    "fund_value_estimation_em": {
        "display_name": "基金净值估算",
        "update_description": "获取基金净值估算数据（无参数接口，默认获取全部数据）",
        "single_update": {
            "enabled": True,
            "description": "更新所有基金净值估算数据（无参数，直接获取全部数据）",
            "params": []
        },
        "batch_update": {
            "enabled": False,
            "description": "无参数接口，不需要批量更新",
            "params": []
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
    "fund_etf_hist_sina": {
        "display_name": "ETF基金历史行情-新浪",
        "update_description": "根据基金代码从新浪财经获取全部历史行情",
        "single_update": {
            "enabled": True,
            "description": "根据基金代码（如 sh510050）获取该ETF的历史行情",
            "params": [
                {
                    "name": "fund_code",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 sh510050）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_spot_sina 集合获取代码并批量更新",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 5,
                    "min": 1,
                    "max": 20,
                    "step": 1
                }
            ]
        }
    },
    "fund_hk_hist_em": {
        "display_name": "香港基金历史数据",
        "update_description": "从 fund_hk_rank_em 集合获取香港基金代码列表，批量更新历史净值明细数据（分红送配详情接口暂时有问题，已禁用）",
        "single_update": {
            "enabled": True,
            "description": "更新单个香港基金的历史净值明细数据",
            "params": [
                {
                    "name": "code",
                    "label": "香港基金代码",
                    "type": "text",
                    "placeholder": "请输入香港基金代码（如 1002200683）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_hk_rank_em 集合获取代码列表，分成多个批次批量更新（每批默认3个基金）",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "placeholder": "同时处理的基金数量（建议1-5）"
                }
            ]
        }
    },
    "fund_etf_dividend_sina": {
        "display_name": "基金累计分红-新浪",
        "update_description": "从 fund_spot_sina 集合获取基金代码列表，批量更新ETF基金累计分红数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的累计分红数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 sh510050）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_spot_sina 集合获取代码列表并批量更新",
            "params": [
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 5,
                    "min": 1,
                    "max": 20,
                    "step": 1
                }
            ]
        }
    },
    "fund_individual_achievement_xq": {
        "display_name": "基金业绩-雪球",
        "update_description": "从 fund_name_em 集合获取基金代码列表，批量更新基金业绩数据（需要基金代码参数）",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的业绩数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_name_em 集合获取代码列表，批量更新所有基金的业绩数据",
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
    "fund_individual_analysis_xq": {
        "display_name": "基金数据分析-雪球",
        "update_description": "从 fund_name_em 集合获取基金代码列表，批量更新基金数据分析数据（需要基金代码参数）",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的数据分析数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_name_em 集合获取代码列表，批量更新所有基金的数据分析数据",
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
    "fund_individual_profit_probability_xq": {
        "display_name": "基金盈利概率-雪球",
        "update_description": "从 fund_name_em 集合获取基金代码列表，批量更新基金盈利概率数据（需要基金代码参数）",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的盈利概率数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_name_em 集合获取代码列表，批量更新所有基金的盈利概率数据",
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
    "fund_individual_detail_hold_xq": {
        "display_name": "基金持仓资产比例-雪球",
        "update_description": "从 fund_name_em 集合获取基金代码列表，生成季度日期列表（从2010年开始），批量更新基金持仓资产比例数据（需要基金代码和季度日期参数）",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的持仓资产比例数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                },
                {
                    "name": "date",
                    "label": "季度日期",
                    "type": "text",
                    "placeholder": "请输入季度日期（如 2024-03-31）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_name_em 集合获取代码列表，生成季度日期列表（从2010年开始），批量更新所有基金的持仓资产比例数据",
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
    "fund_overview_em": {
        "display_name": "基金基本概况-东财",
        "update_description": "从 fund_name_em 集合获取基金代码列表，批量更新基金基本概况数据（需要基金代码参数）",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的基本概况数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_name_em 集合获取代码列表，批量更新所有基金的基本概况数据（增量更新：已存在的基金代码将跳过）",
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
    "fund_individual_detail_info_xq": {
        "display_name": "基金交易规则-雪球",
        "update_description": "从 fund_name_em 集合获取基金代码列表，批量更新基金交易规则数据（需要基金代码参数）",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金的交易规则数据",
            "params": [
                {
                    "name": "symbol",
                    "label": "基金代码",
                    "type": "text",
                    "placeholder": "请输入基金代码（如 000001）",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "从 fund_name_em 集合获取代码列表，批量更新所有基金的交易规则数据（增量更新：已存在的基金代码将跳过）",
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
    }
}


def get_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    if collection_name in FUND_UPDATE_CONFIGS:
        config = FUND_UPDATE_CONFIGS[collection_name].copy()
        config["collection_name"] = collection_name
        return config
    
    # 默认配置：只有批量更新，包含并发数参数
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
    }


def get_all_collection_update_configs() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的更新配置"""
    return FUND_UPDATE_CONFIGS
