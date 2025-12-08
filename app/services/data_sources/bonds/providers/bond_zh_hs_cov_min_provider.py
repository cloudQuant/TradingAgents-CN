"""
可转债分时行情数据提供者（重构版）

数据集合名称: bond_zh_hs_cov_min
数据唯一标识: 可转债代码, 时间
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhHsCovMinProvider(BaseProvider):
    """可转债分时行情数据提供者"""
    
    collection_name = "bond_zh_hs_cov_min"
    display_name = "可转债分时行情"
    akshare_func = "bond_zh_hs_cov_min"
    unique_keys = ['代码', '时间', "周期", "复权"]
    
    collection_description = "可转债分时行情数据"
    collection_route = "/bonds/collections/bond_zh_hs_cov_min"
    collection_order = 13
    
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "时间", "type": "datetime", "description": "分时数据时间"},
        {"name": "开盘", "type": "number", "description": "开盘价"},
        {"name": "收盘", "type": "number", "description": "收盘价"},
        {"name": "最高", "type": "number", "description": "最高价"},
        {"name": "最低", "type": "number", "description": "最低价"},
        {"name": "成交量", "type": "number", "description": "成交量"},
        {"name": "成交额", "type": "number", "description": "成交额"},
        {"name": "振幅", "type": "number", "description": "振幅"},
        {"name": "换手率", "type": "number", "description": "换手率"},
        {"name": "周期", "type": "string", "description": "分时周期，如 1、5、15 分钟"},
        {"name": "复权", "type": "string", "description": "复权类型，''/qfq/hfq"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]

    def fetch_data(self, **kwargs):
        """获取可转债分时数据，默认使用 5 分钟周期和后复权(hfq)，并增加代码/周期/复权字段。

        AkShare 参数：
        - symbol: 可转债代码，如 'sz123124'
        - period: 分钟周期，{'1','5','15','30','60'}，这里默认 '5'
        - adjust: 复权方式，{'', 'qfq', 'hfq'}，这里默认 'hfq'
        其余 start_date/end_date 如有传入则原样透传。
        """
        # 默认周期和复权
        period = kwargs.get("period") or "5"
        adjust = kwargs.get("adjust") or "hfq"
        kwargs["period"] = period
        kwargs["adjust"] = adjust

        df = super().fetch_data(**kwargs)
        if df is None or df.empty:
            return df

        df = df.copy()

        symbol = kwargs.get("symbol")
        if symbol:
            df["代码"] = symbol
        df["周期"] = period
        df["复权"] = adjust or ""

        return df
