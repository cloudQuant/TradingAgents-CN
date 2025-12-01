"""
指数型基金基本信息-东财数据提供者（重构版：继承SimpleProvider）
"""
from typing import Any

from app.services.data_sources.base_provider import SimpleProvider


class FundInfoIndexEmProvider(SimpleProvider):
    """指数型基金基本信息-东财数据提供者"""
    
    collection_name = "fund_info_index_em"
    display_name = "指数型基金基本信息"
    akshare_func = "fund_info_index_em"
    unique_keys = ["基金代码", "日期"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "近1周", "type": "float", "description": "注意单位: %"},
        {"name": "近1月", "type": "float", "description": "注意单位: %"},
        {"name": "近3月", "type": "float", "description": "注意单位: %"},
        {"name": "近6月", "type": "float", "description": "注意单位: %"},
        {"name": "近1年", "type": "float", "description": "注意单位: %"},
        {"name": "近2年", "type": "float", "description": "注意单位: %"},
        {"name": "近3年", "type": "float", "description": "注意单位: %"},
        {"name": "今年来", "type": "float", "description": "注意单位: %"},
        {"name": "成立来", "type": "float", "description": "注意单位: %"},
        {"name": "手续费", "type": "float", "description": "注意单位: %"},
        {"name": "起购金额", "type": "string", "description": ""},
        {"name": "跟踪标的", "type": "string", "description": ""},
        {"name": "跟踪方式", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_info_index_em"},
    ]

  
    collection_description = "东方财富网-指数型基金基本信息，包括单位净值、日期、各周期业绩、手续费、起购金额、跟踪标的和方式等"
    collection_route = "/funds/collections/fund_info_index_em"
    collection_order = 2
    def fetch_data(self, **kwargs: Any):
        """
        重写 SimpleProvider.fetch_data，补充标准化字段。

        - 将 "基金代码" 转成标准 code 字段（集合索引用）
        - 过滤掉缺少基金代码的数据，避免写入时触发唯一索引冲突
        """
        df = super().fetch_data(**kwargs)

        if df is None or df.empty:
            return df

        if "基金代码" not in df.columns:
            self.logger.warning("[fund_info_index_em] 数据缺少 '基金代码' 列，跳过标准化")
            return df

        normalized = (
            df["基金代码"]
            .astype(str)
            .str.strip()
            .replace({"None": "", "nan": ""})
        )

        df = df.copy()
        df["code"] = normalized
        df = df[df["code"] != ""]

        if df.empty:
            self.logger.warning("[fund_info_index_em] 全部记录缺少有效基金代码，返回空结果")

        return df
