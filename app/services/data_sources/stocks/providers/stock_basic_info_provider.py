"""股票基础信息集合 Provider

用于将已有的 MongoDB 集合 `stock_basic_info` 暴露给通用的股票数据集合路由
(`/api/stocks/collections/{collection_name}`)，本身不负责从外部数据源拉取数据。

数据的采集和更新由独立的同步服务负责：
- BasicsSyncService / MultiSourceBasicsSyncService
- Tushare / AKShare / BaoStock 同步任务
"""

from app.services.data_sources.base_provider import BaseProvider


class StockBasicInfoProvider(BaseProvider):
    """股票基础信息 Provider（多数据源汇总，读现有库）"""

    # 与 MongoDB 中的集合名保持一致
    collection_name = "stock_basic_info"

    # 显示信息
    display_name = "股票基础信息（多数据源）"
    collection_description = "A股股票基础信息，多数据源汇总（Tushare / AKShare / BaoStock 等）"
    collection_route = "/stocks/collections/stock_basic_info"
    collection_category = "基础信息"

    # 这里不直接调用 akshare，留空即可；如需后续打通远程刷新再补充
    akshare_func = ""

    # 字段信息：只列常用主字段，其余字段前端会自动推断
    field_info = [
        {"name": "code", "type": "string", "example": "000001"},
        {"name": "symbol", "type": "string", "example": "000001"},
        {"name": "name", "type": "string", "example": "平安银行"},
        {"name": "market", "type": "string", "example": "SZ"},
        {"name": "industry", "type": "string", "example": "银行"},
        {"name": "area", "type": "string", "example": "广东"},
        {"name": "total_mv", "type": "number", "example": 1000.0},
        {"name": "circ_mv", "type": "number", "example": 800.0},
        {"name": "pe", "type": "number", "example": 10.5},
        {"name": "pb", "type": "number", "example": 1.2},
        {"name": "pe_ttm", "type": "number", "example": 9.8},
        {"name": "pb_mrq", "type": "number", "example": 1.1},
        {"name": "roe", "type": "number", "example": 15.0},
        {"name": "source", "type": "string", "example": "tushare"},
        {"name": "updated_at", "type": "datetime", "example": "2024-01-01T15:00:00Z"},
    ]

    def fetch_data(self, **kwargs):  # type: ignore[override]
        """占位实现：`stock_basic_info` 由独立同步任务维护，这里不做远程拉取。

        如果后续需要从远程接口重建数据，可在此处接入统一的
        Tushare / AKShare / BaoStock 管线，并返回 `pandas.DataFrame` 即可。
        """
        raise NotImplementedError(
            "stock_basic_info is maintained by dedicated sync services; "
            "refresh via /api/stocks/collections/stock_basic_info/refresh is not implemented."
        )
