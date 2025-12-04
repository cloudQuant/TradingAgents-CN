"""
债券数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
包含34个债券数据集合
"""

from typing import Dict, Any, List, Optional


# 债券集合更新配置（34个集合）
BOND_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = {
    # ==================== 01-02 基础数据 ====================
    "bond_info_cm": {
        "display_name": "债券信息查询",
        "update_description": "从中国外汇交易中心获取债券信息查询数据",
        "single_update": {
            "enabled": True,
            "description": "按条件查询债券信息",
            "params": [
                {"name": "bond_name", "label": "债券名称", "type": "text", "placeholder": "请输入债券名称", "required": False},
                {"name": "bond_code", "label": "债券代码", "type": "text", "placeholder": "请输入债券代码", "required": False},
                {"name": "issue_year", "label": "发行年份", "type": "text", "placeholder": "如 2024", "required": False}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量获取所有债券信息数据", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}]}
    },
    "bond_info_detail_cm": {
        "display_name": "债券基础信息",
        "update_description": "获取债券详细信息，包括发行条款、评级等",
        "single_update": {"enabled": True, "description": "更新单个债券的详细信息", "params": [{"name": "bond_code", "label": "债券代码", "type": "text", "required": True}]},
        "batch_update": {"enabled": True, "description": "从bond_info_cm批量获取债券详细信息", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}]}
    },
    # ==================== 03-04 沪深债券行情 ====================
    "bond_zh_hs_spot": {
        "display_name": "沪深债券实时行情",
        "update_description": "从新浪财经获取沪深债券实时行情数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有沪深债券实时行情", "params": []}
    },
    "bond_zh_hs_daily": {
        "display_name": "沪深债券历史行情",
        "update_description": "获取沪深债券历史行情数据（日线）",
        "single_update": {"enabled": True, "description": "更新单个债券的历史行情", "params": [{"name": "symbol", "label": "债券代码", "type": "text", "placeholder": "如 sh010107", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量更新债券历史行情", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}]}
    },
    # ==================== 05-07 可转债行情 ====================
    "bond_zh_hs_cov_spot": {
        "display_name": "可转债实时行情",
        "update_description": "从新浪财经获取沪深可转债实时行情数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有可转债实时行情", "params": []}
    },
    "bond_zh_hs_cov_daily": {
        "display_name": "可转债历史行情",
        "update_description": "获取沪深可转债历史行情数据（日线）",
        "single_update": {"enabled": True, "description": "更新单个可转债的历史行情", "params": [{"name": "symbol", "label": "可转债代码", "type": "text", "placeholder": "如 sh113009", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量更新可转债历史行情", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}]}
    },
    "bond_zh_cov": {
        "display_name": "可转债数据一览表",
        "update_description": "从东方财富网获取可转债综合数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有可转债数据", "params": []}
    },
    # ==================== 08-09 市场概览 ====================
    "bond_cash_summary_sse": {
        "display_name": "债券现券市场概览",
        "update_description": "获取上交所债券现券市场托管概览",
        "single_update": {"enabled": True, "description": "查询指定日期的市场概览", "params": [{"name": "date", "label": "日期", "type": "text", "placeholder": "20240101", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量获取市场概览数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    "bond_deal_summary_sse": {
        "display_name": "债券成交概览",
        "update_description": "获取上交所债券成交概览",
        "single_update": {"enabled": True, "description": "查询指定日期的成交概览", "params": [{"name": "date", "label": "日期", "type": "text", "placeholder": "20240101", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量获取成交概览数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    # ==================== 10-12 银行间市场 ====================
    "bond_debt_nafmii": {
        "display_name": "银行间市场债券发行",
        "update_description": "从银行间市场交易商协会获取债券发行数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "批量获取银行间市场债券发行数据", "params": [{"name": "page_count", "label": "页数", "type": "number", "default": 10, "min": 1, "max": 100}]}
    },
    "bond_spot_quote": {
        "display_name": "现券市场做市报价",
        "update_description": "从中国外汇交易中心获取现券市场做市报价",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有做市报价数据", "params": []}
    },
    "bond_spot_deal": {
        "display_name": "现券市场成交行情",
        "update_description": "从中国外汇交易中心获取现券市场成交行情",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有成交行情数据", "params": []}
    },
    # ==================== 13-14 可转债分时 ====================
    "bond_zh_hs_cov_min": {
        "display_name": "可转债分时行情",
        "update_description": "从东方财富网获取可转债分时行情数据",
        "single_update": {"enabled": True, "description": "获取单个可转债的分时数据", "params": [{"name": "symbol", "label": "可转债代码", "type": "text", "required": True}, {"name": "period", "label": "周期", "type": "select", "default": "1", "options": [{"label": "1分钟", "value": "1"}, {"label": "5分钟", "value": "5"}, {"label": "15分钟", "value": "15"}]}]},
        "batch_update": {"enabled": True, "description": "批量更新可转债分时数据", "params": [{"name": "period", "label": "周期", "type": "select", "default": "1", "options": [{"label": "1分钟", "value": "1"}, {"label": "5分钟", "value": "5"}]}, {"name": "concurrency", "label": "并发数", "type": "number", "default": 3}]}
    },
    "bond_zh_hs_cov_pre_min": {
        "display_name": "可转债盘前分时",
        "update_description": "从东方财富网获取可转债盘前分时数据",
        "single_update": {"enabled": True, "description": "获取单个可转债的盘前分时数据", "params": [{"name": "symbol", "label": "可转债代码", "type": "text", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量更新可转债盘前分时数据", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3}]}
    },
    # ==================== 15-18 可转债详细 ====================
    "bond_zh_cov_info": {
        "display_name": "可转债详情-东财",
        "update_description": "从东方财富网获取可转债详情",
        "single_update": {"enabled": True, "description": "获取单个可转债的详细信息", "params": [
            {"name": "symbol", "label": "可转债代码", "type": "text", "placeholder": "如123121", "required": True},
            {"name": "indicator", "label": "指标类型", "type": "select", "default": "基本信息", "options": [{"label": "基本信息", "value": "基本信息"}, {"label": "中签号", "value": "中签号"}, {"label": "筹资用途", "value": "筹资用途"}, {"label": "重要日期", "value": "重要日期"}]}
        ]},
        "batch_update": {"enabled": True, "description": "批量更新可转债详情", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3}]}
    },
    "bond_zh_cov_info_ths": {
        "display_name": "可转债详情-同花顺",
        "update_description": "从同花顺获取可转债详情（无需参数，返回所有数据）",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有可转债详情数据", "params": []}
    },
    "bond_cov_comparison": {
        "display_name": "可转债比价表",
        "update_description": "从东方财富网获取可转债与正股比价数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有可转债比价数据", "params": []}
    },
    "bond_zh_cov_value_analysis": {
        "display_name": "可转债价值分析",
        "update_description": "从东方财富网获取可转债价值分析历史数据",
        "single_update": {"enabled": True, "description": "获取指定可转债的价值分析历史", "params": [{"name": "symbol", "label": "可转债代码", "type": "text", "placeholder": "如113527", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量获取可转债价值分析数据", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3}]}
    },
    # ==================== 19-21 质押式回购 ====================
    "bond_sh_buy_back_em": {
        "display_name": "上证质押式回购",
        "update_description": "从东方财富网获取上证质押式回购实时行情",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取上证质押式回购数据", "params": []}
    },
    "bond_sz_buy_back_em": {
        "display_name": "深证质押式回购",
        "update_description": "从东方财富网获取深证质押式回购实时行情",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取深证质押式回购数据", "params": []}
    },
    "bond_buy_back_hist_em": {
        "display_name": "质押式回购历史数据",
        "update_description": "从东方财富网获取质押式回购历史行情",
        "single_update": {"enabled": True, "description": "获取单个回购品种的历史数据", "params": [{"name": "symbol", "label": "回购代码", "type": "text", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量更新质押式回购历史数据", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3}]}
    },
    # ==================== 22-25 集思录数据 ====================
    "bond_cb_jsl": {
        "display_name": "可转债实时数据-集思录",
        "update_description": "从集思录获取可转债实时数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取集思录可转债数据", "params": [{"name": "cookie", "label": "Cookie", "type": "text", "placeholder": "可选"}]}
    },
    "bond_cb_redeem_jsl": {
        "display_name": "可转债强赎-集思录",
        "update_description": "从集思录获取可转债强赎信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取可转债强赎数据", "params": []}
    },
    "bond_cb_index_jsl": {
        "display_name": "可转债等权指数-集思录",
        "update_description": "从集思录获取可转债等权指数",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取可转债等权指数数据", "params": []}
    },
    "bond_cb_adj_logs_jsl": {
        "display_name": "转股价调整记录-集思录",
        "update_description": "从集思录获取可转债转股价调整记录",
        "single_update": {"enabled": True, "description": "获取单个可转债的转股价调整记录", "params": [{"name": "symbol", "label": "可转债代码", "type": "text", "required": True}]},
        "batch_update": {"enabled": True, "description": "批量获取转股价调整记录", "params": [{"name": "concurrency", "label": "并发数", "type": "number", "default": 3}]}
    },
    # ==================== 26-27 收益率曲线 ====================
    "bond_china_close_return": {
        "display_name": "收益率曲线历史数据",
        "update_description": "从中国外汇交易中心获取债券收益率曲线历史数据",
        "single_update": {"enabled": True, "description": "按日期范围查询收益率曲线", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]},
        "batch_update": {"enabled": True, "description": "批量获取收益率曲线数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    "bond_zh_us_rate": {
        "display_name": "中美国债收益率",
        "update_description": "从东方财富网获取中美国债收益率对比数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取中美国债收益率数据", "params": []}
    },
    # ==================== 28-32 债券发行 ====================
    "bond_treasure_issue_cninfo": {
        "display_name": "国债发行",
        "update_description": "从巨潮资讯获取国债发行信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取国债发行数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    "bond_local_government_issue_cninfo": {
        "display_name": "地方债发行",
        "update_description": "从巨潮资讯获取地方债发行信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取地方债发行数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    "bond_corporate_issue_cninfo": {
        "display_name": "企业债发行",
        "update_description": "从巨潮资讯获取企业债发行信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取企业债发行数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    "bond_cov_issue_cninfo": {
        "display_name": "可转债发行",
        "update_description": "从巨潮资讯获取可转债发行信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取可转债发行数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    "bond_cov_stock_issue_cninfo": {
        "display_name": "可转债转股",
        "update_description": "从巨潮资讯获取可转债转股信息",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取可转债转股数据", "params": [{"name": "start_date", "label": "开始日期", "type": "text"}, {"name": "end_date", "label": "结束日期", "type": "text"}]}
    },
    # ==================== 33-34 中债指数 ====================
    "bond_new_composite_index_cbond": {
        "display_name": "中债新综合指数",
        "update_description": "从中国债券信息网获取中债新综合指数历史数据",
        "single_update": {
            "enabled": True,
            "description": "按指标和期限查询中债新综合指数历史数据",
            "params": [
                {
                    "name": "indicator",
                    "label": "指标类型",
                    "type": "select",
                    "default": "财富",
                    "required": True,
                    "options": [
                        {"label": "全价", "value": "全价"},
                        {"label": "净价", "value": "净价"},
                        {"label": "财富", "value": "财富"},
                        {"label": "平均市值法久期", "value": "平均市值法久期"},
                        {"label": "平均现金流法久期", "value": "平均现金流法久期"},
                        {"label": "平均市值法凸性", "value": "平均市值法凸性"},
                        {"label": "平均现金流法凸性", "value": "平均现金流法凸性"},
                        {"label": "平均现金流法到期收益率", "value": "平均现金流法到期收益率"},
                        {"label": "平均市值法到期收益率", "value": "平均市值法到期收益率"},
                        {"label": "平均基点价值", "value": "平均基点价值"},
                        {"label": "平均待偿期", "value": "平均待偿期"},
                        {"label": "平均派息率", "value": "平均派息率"},
                        {"label": "指数上日总市值", "value": "指数上日总市值"},
                        {"label": "财富指数涨跌幅", "value": "财富指数涨跌幅"},
                        {"label": "全价指数涨跌幅", "value": "全价指数涨跌幅"},
                        {"label": "净价指数涨跌幅", "value": "净价指数涨跌幅"},
                        {"label": "现券结算量", "value": "现券结算量"}
                    ]
                },
                {
                    "name": "period",
                    "label": "期限",
                    "type": "select",
                    "default": "总值",
                    "required": True,
                    "options": [
                        {"label": "总值", "value": "总值"},
                        {"label": "1年以下", "value": "1年以下"},
                        {"label": "1-3年", "value": "1-3年"},
                        {"label": "3-5年", "value": "3-5年"},
                        {"label": "5-7年", "value": "5-7年"},
                        {"label": "7-10年", "value": "7-10年"},
                        {"label": "10年以上", "value": "10年以上"}
                    ]
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量获取多个指标和期限的中债新综合指数数据",
            "params": [
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
    },
    "bond_composite_index_cbond": {
        "display_name": "中债综合指数",
        "update_description": "从中国债券信息网获取中债综合指数历史数据",
        "single_update": {
            "enabled": True,
            "description": "按指标和期限查询中债综合指数历史数据",
            "params": [
                {
                    "name": "indicator",
                    "label": "指标类型",
                    "type": "select",
                    "default": "财富",
                    "required": True,
                    "options": [
                        {"label": "全价", "value": "全价"},
                        {"label": "净价", "value": "净价"},
                        {"label": "财富", "value": "财富"},
                        {"label": "平均市值法久期", "value": "平均市值法久期"},
                        {"label": "平均现金流法久期", "value": "平均现金流法久期"},
                        {"label": "平均市值法凸性", "value": "平均市值法凸性"},
                        {"label": "平均现金流法凸性", "value": "平均现金流法凸性"},
                        {"label": "平均现金流法到期收益率", "value": "平均现金流法到期收益率"},
                        {"label": "平均市值法到期收益率", "value": "平均市值法到期收益率"},
                        {"label": "平均基点价值", "value": "平均基点价值"},
                        {"label": "平均待偿期", "value": "平均待偿期"},
                        {"label": "平均派息率", "value": "平均派息率"},
                        {"label": "指数上日总市值", "value": "指数上日总市值"},
                        {"label": "财富指数涨跌幅", "value": "财富指数涨跌幅"},
                        {"label": "全价指数涨跌幅", "value": "全价指数涨跌幅"},
                        {"label": "净价指数涨跌幅", "value": "净价指数涨跌幅"},
                        {"label": "现券结算量", "value": "现券结算量"}
                    ]
                },
                {
                    "name": "period",
                    "label": "期限",
                    "type": "select",
                    "default": "总值",
                    "required": True,
                    "options": [
                        {"label": "总值", "value": "总值"},
                        {"label": "1年以下", "value": "1年以下"},
                        {"label": "1-3年", "value": "1-3年"},
                        {"label": "3-5年", "value": "3-5年"},
                        {"label": "5-7年", "value": "5-7年"},
                        {"label": "7-10年", "value": "7-10年"},
                        {"label": "10年以上", "value": "10年以上"}
                    ]
                }
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量获取多个指标和期限的中债综合指数数据",
            "params": [
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
    },
}


def get_collection_update_config(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的更新配置"""
    if collection_name in BOND_UPDATE_CONFIGS:
        config = BOND_UPDATE_CONFIGS[collection_name].copy()
        config["collection_name"] = collection_name
        return config
    
    # 默认配置：只有批量更新，无参数
    return {
        "collection_name": collection_name,
        "display_name": collection_name,
        "update_description": "该集合暂不支持自动更新",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    }


def get_all_collection_update_configs() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的更新配置"""
    return BOND_UPDATE_CONFIGS
