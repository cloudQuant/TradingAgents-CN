"""
货币数据集合更新参数配置
定义每个货币数据集合的更新参数、选项等配置
注意：所有货币API都需要api_key参数
"""

CURRENCY_UPDATE_CONFIG = {
    # 01. 货币报价最新数据
    "currency_latest": {
        "display_name": "货币报价最新数据",
        "update_description": "获取指定基准货币的最新报价",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "base", "label": "基准货币", "type": "string", "required": True,
                 "default": "USD", "placeholder": "如: USD"},
                {"name": "symbols", "label": "目标货币", "type": "string", "required": False,
                 "placeholder": "如: CNY,EUR 或留空返回全部"},
                {"name": "api_key", "label": "API密钥", "type": "password", "required": True,
                 "placeholder": "请输入currencyscoop API密钥"},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 02. 货币报价历史数据
    "currency_history": {
        "display_name": "货币报价历史数据",
        "update_description": "获取指定日期的货币报价历史数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "base", "label": "基准货币", "type": "string", "required": True,
                 "default": "USD", "placeholder": "如: USD"},
                {"name": "date", "label": "日期", "type": "date", "required": True},
                {"name": "symbols", "label": "目标货币", "type": "string", "required": False,
                 "placeholder": "如: CNY,EUR 或留空返回全部"},
                {"name": "api_key", "label": "API密钥", "type": "password", "required": True,
                 "placeholder": "请输入currencyscoop API密钥"},
            ],
        },
        "batch_update": {
            "enabled": True,
            "params": [
                {"name": "base", "label": "基准货币", "type": "string", "required": True, "default": "USD"},
                {"name": "start_date", "label": "开始日期", "type": "date", "required": True},
                {"name": "end_date", "label": "结束日期", "type": "date", "required": True},
                {"name": "symbols", "label": "目标货币", "type": "string", "required": False},
                {"name": "api_key", "label": "API密钥", "type": "password", "required": True},
            ],
        },
    },
    # 03. 货币报价时间序列数据
    "currency_time_series": {
        "display_name": "货币报价时间序列数据",
        "update_description": "获取指定日期范围的货币报价时间序列",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "base", "label": "基准货币", "type": "string", "required": True,
                 "default": "USD", "placeholder": "如: USD"},
                {"name": "start_date", "label": "开始日期", "type": "date", "required": True},
                {"name": "end_date", "label": "结束日期", "type": "date", "required": True},
                {"name": "symbols", "label": "目标货币", "type": "string", "required": False,
                 "placeholder": "如: CNY,EUR 或留空返回全部"},
                {"name": "api_key", "label": "API密钥", "type": "password", "required": True,
                 "placeholder": "请输入currencyscoop API密钥"},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 04. 货币基础信息查询
    "currency_currencies": {
        "display_name": "货币基础信息查询",
        "update_description": "获取所有货币的基础信息",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "c_type", "label": "货币类型", "type": "select", "required": True,
                 "default": "fiat", "options": ["fiat", "crypto"]},
                {"name": "api_key", "label": "API密钥", "type": "password", "required": True,
                 "placeholder": "请输入currencyscoop API密钥"},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 05. 货币对价格转换
    "currency_convert": {
        "display_name": "货币对价格转换",
        "update_description": "获取指定货币对的转换价格",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "base", "label": "基准货币", "type": "string", "required": True,
                 "default": "USD", "placeholder": "如: USD"},
                {"name": "to", "label": "目标货币", "type": "string", "required": True,
                 "placeholder": "如: CNY"},
                {"name": "amount", "label": "金额", "type": "string", "required": True,
                 "default": "10000", "placeholder": "如: 10000"},
                {"name": "api_key", "label": "API密钥", "type": "password", "required": True,
                 "placeholder": "请输入currencyscoop API密钥"},
            ],
        },
        "batch_update": {"enabled": False},
    },
}
