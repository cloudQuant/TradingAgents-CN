"""全市场实时行情快照 Provider

用于将已有的 MongoDB 集合 `market_quotes` 暴露给通用的股票数据集合路由
(`/api/stocks/collections/{collection_name}`)，本身不负责从外部数据源拉取数据。

数据的采集和更新由 QuotesIngestionService、Tushare 同步任务等独立服务负责。
"""

from app.services.data_sources.base_provider import BaseProvider


class MarketQuotesProvider(BaseProvider):
    """全市场实时行情快照 Provider（只读现有 Mongo 集合）"""

    # 与 MongoDB 中的集合名保持一致
    collection_name = "market_quotes"

    # 显示信息
    display_name = "A股实时行情快照"
    collection_description = "全市场近实时行情快照，由 QuotesIngestionService 定时入库"
    collection_route = "/stocks/collections/market_quotes"
    collection_category = "行情"
    collection_order = 10
    collection_tags = ["行情", "实时", "快照"]

    # 不通过 akshare 直接拉数，由独立的行情入库任务维护
    akshare_func = ""

    # 字段信息：根据 QuotesIngestionService 以及下游使用习惯整理
    field_info = [
        {"name": "code", "type": "string", "description": "股票代码（6位）"},
        {"name": "symbol", "type": "string", "description": "股票代码（6位，兼容字段）"},
        {"name": "full_symbol", "type": "string", "description": "带交易所后缀的代码，如 600000.SS"},
        {"name": "close", "type": "number", "description": "最新价"},
        {"name": "pct_chg", "type": "number", "description": "涨跌幅(%)"},
        {"name": "amount", "type": "number", "description": "成交额"},
        {"name": "open", "type": "number", "description": "今开"},
        {"name": "high", "type": "number", "description": "最高价"},
        {"name": "low", "type": "number", "description": "最低价"},
        {"name": "pre_close", "type": "number", "description": "昨收价"},
        {"name": "trade_date", "type": "string", "description": "交易日期"},
        {"name": "updated_at", "type": "datetime", "description": "入库/更新时间"},
    ]

    def fetch_data(self, **kwargs):  # type: ignore[override]
        """占位实现：`market_quotes` 由独立行情入库任务维护，这里不做远程拉取。

        如果后续需要从远程接口重建数据，可在此处接入统一的数据源管线，
        并返回 `pandas.DataFrame` 即可。
        """
        raise NotImplementedError(
            "market_quotes is maintained by QuotesIngestionService and other sync jobs; "
            "refresh via /api/stocks/collections/market_quotes/refresh is not implemented."
        )
