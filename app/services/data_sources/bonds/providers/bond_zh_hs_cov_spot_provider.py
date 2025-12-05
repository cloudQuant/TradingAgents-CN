"""
可转债实时行情-沪深数据提供者（重构版：继承SimpleProvider）

需求文档: tests/bonds/requirements/05_可转债实时行情-沪深.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondZhHsCovSpotProvider(SimpleProvider):
    """可转债实时行情-沪深数据提供者"""
    
    # 基本属性
    collection_name = "bond_zh_hs_cov_spot"
    display_name = "可转债实时行情-沪深"
    akshare_func = "bond_zh_hs_cov_spot"
    unique_keys = ["代码","更新时间"]  # 以代码和更新时间作为唯一标识
    
    # 元信息
    collection_description = "沪深可转债实时行情数据"
    collection_route = "/bonds/collections/bond_zh_hs_cov_spot"
    collection_order = 5
    
    # 字段信息
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "名称", "type": "string", "description": "可转债名称"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
        {"name": "涨跌额", "type": "float", "description": "涨跌额"},
        {"name": "成交量", "type": "float", "description": "成交量(手)"},
        {"name": "成交额", "type": "float", "description": "成交额"},
        {"name": "今开", "type": "float", "description": "今日开盘价"},
        {"name": "昨收", "type": "float", "description": "昨日收盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "申买价", "type": "float", "description": "申买价"},
        {"name": "申卖价", "type": "float", "description": "申卖价"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]

    def fetch_data(self, **kwargs):
        """获取并规范化可转债实时行情数据列名"""
        df = super().fetch_data(**kwargs)
        if df is None or df.empty:
            return df

        df = df.copy()

        # akshare.bond_zh_hs_cov_spot 返回的原始列名为英文，需要映射到中文字段
        rename_mapping = {
            "code": "代码",
            "name": "名称",
            "trade": "最新价",
            "pricechange": "涨跌额",
            "changepercent": "涨跌幅",
            "volume": "成交量",
            "amount": "成交额",
            "open": "今开",
            "settlement": "昨收",
            "high": "最高",
            "low": "最低",
            "buy": "申买价",
            "sell": "申卖价",
        }

        columns_to_rename = {k: v for k, v in rename_mapping.items() if k in df.columns}
        if columns_to_rename:
            df = df.rename(columns=columns_to_rename)

        return df

