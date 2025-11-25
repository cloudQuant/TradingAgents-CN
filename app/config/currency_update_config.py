"""
外汇数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any


# 外汇集合更新配置
CURRENCY_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "currency_latest": {
        "display_name": "货币报价最新数据",
        "update_description": "从 CurrencyScoop API 获取货币最新汇率数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定基础货币的最新汇率",
            "params": [
                {
                    "name": "base",
                    "label": "基础货币",
                    "type": "text",
                    "placeholder": "如 USD",
                    "default": "USD",
                    "required": False
                },
                {
                    "name": "symbols",
                    "label": "目标货币",
                    "type": "text",
                    "placeholder": "多个用逗号分隔，如 CNY,EUR",
                    "required": False
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量同步 USD 和 CNY 两个基础货币的所有汇率",
            "params": [
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        }
    },
    "currency_history": {
        "display_name": "货币报价历史数据",
        "update_description": "从 CurrencyScoop API 获取货币历史汇率数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定日期的历史汇率",
            "params": [
                {
                    "name": "base",
                    "label": "基础货币",
                    "type": "text",
                    "placeholder": "如 USD",
                    "default": "USD",
                    "required": False
                },
                {
                    "name": "date",
                    "label": "日期",
                    "type": "text",
                    "placeholder": "YYYY-MM-DD",
                    "required": True
                },
                {
                    "name": "symbols",
                    "label": "目标货币",
                    "type": "text",
                    "placeholder": "多个用逗号分隔",
                    "required": False
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量同步指定日期的所有货币历史汇率",
            "params": [
                {
                    "name": "base",
                    "label": "基础货币",
                    "type": "text",
                    "placeholder": "如 USD",
                    "default": "USD",
                    "required": False
                },
                {
                    "name": "date",
                    "label": "日期",
                    "type": "text",
                    "placeholder": "YYYY-MM-DD",
                    "required": True
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                },
                {
                    "name": "max_codes",
                    "label": "最大货币数",
                    "type": "number",
                    "default": 100,
                    "min": 1,
                    "max": 500
                },
                {
                    "name": "batch_size",
                    "label": "每批数量",
                    "type": "number",
                    "default": 20,
                    "min": 1,
                    "max": 100
                }
            ]
        }
    },
    "currency_time_series": {
        "display_name": "货币报价时间序列",
        "update_description": "从 CurrencyScoop API 获取货币时间序列数据",
        "single_update": {
            "enabled": True,
            "description": "更新指定时间范围的汇率数据",
            "params": [
                {
                    "name": "base",
                    "label": "基础货币",
                    "type": "text",
                    "placeholder": "如 USD",
                    "default": "USD",
                    "required": False
                },
                {
                    "name": "start_date",
                    "label": "开始日期",
                    "type": "text",
                    "placeholder": "YYYY-MM-DD",
                    "required": True
                },
                {
                    "name": "end_date",
                    "label": "结束日期",
                    "type": "text",
                    "placeholder": "YYYY-MM-DD",
                    "required": True
                },
                {
                    "name": "symbols",
                    "label": "目标货币",
                    "type": "text",
                    "placeholder": "多个用逗号分隔",
                    "required": False
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量同步指定时间范围的所有货币汇率",
            "params": [
                {
                    "name": "base",
                    "label": "基础货币",
                    "type": "text",
                    "placeholder": "如 USD",
                    "default": "USD",
                    "required": False
                },
                {
                    "name": "start_date",
                    "label": "开始日期",
                    "type": "text",
                    "placeholder": "YYYY-MM-DD",
                    "required": True
                },
                {
                    "name": "end_date",
                    "label": "结束日期",
                    "type": "text",
                    "placeholder": "YYYY-MM-DD",
                    "required": True
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                },
                {
                    "name": "max_codes",
                    "label": "最大货币数",
                    "type": "number",
                    "default": 100,
                    "min": 1,
                    "max": 500
                },
                {
                    "name": "batch_size",
                    "label": "每批数量",
                    "type": "number",
                    "default": 20,
                    "min": 1,
                    "max": 100
                }
            ]
        }
    },
    "currency_currencies": {
        "display_name": "货币基础信息",
        "update_description": "从 CurrencyScoop API 获取所有货币的基础信息",
        "single_update": {
            "enabled": True,
            "description": "更新指定类型的货币基础信息",
            "params": [
                {
                    "name": "c_type",
                    "label": "货币类型",
                    "type": "select",
                    "default": "fiat",
                    "options": [
                        {"label": "法定货币", "value": "fiat"},
                        {"label": "加密货币", "value": "crypto"}
                    ]
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量同步所有类型的货币基础信息（fiat + crypto）",
            "params": [
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        }
    },
    "currency_convert": {
        "display_name": "货币转换",
        "update_description": "从 CurrencyScoop API 进行实时货币转换",
        "single_update": {
            "enabled": True,
            "description": "执行单次货币转换",
            "params": [
                {
                    "name": "base",
                    "label": "基础货币",
                    "type": "text",
                    "placeholder": "如 USD",
                    "default": "USD",
                    "required": True
                },
                {
                    "name": "to",
                    "label": "目标货币",
                    "type": "text",
                    "placeholder": "如 CNY",
                    "default": "CNY",
                    "required": True
                },
                {
                    "name": "amount",
                    "label": "金额",
                    "type": "text",
                    "placeholder": "如 1000",
                    "default": "1",
                    "required": False
                },
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量执行多个货币对的转换",
            "params": [
                {
                    "name": "api_key",
                    "label": "API Key",
                    "type": "text",
                    "placeholder": "CurrencyScoop API Key",
                    "required": True
                },
                {
                    "name": "concurrency",
                    "label": "并发数",
                    "type": "number",
                    "default": 2,
                    "min": 1,
                    "max": 5
                }
            ]
        }
    }
}


def get_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    if collection_name in CURRENCY_UPDATE_CONFIGS:
        config = CURRENCY_UPDATE_CONFIGS[collection_name].copy()
        config["collection_name"] = collection_name
        return config
    
    # 默认配置
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
            "enabled": False,
            "description": "",
            "params": []
        }
    }


def get_all_collection_update_configs() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的更新配置"""
    return CURRENCY_UPDATE_CONFIGS
