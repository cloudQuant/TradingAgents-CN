"""
新股申购与中签数据提供者

东方财富网-数据中心-新股数据-新股申购-新股申购与中签查询
接口: stock_xgsglb_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockXgsglbEmProvider(BaseProvider):
    """新股申购与中签数据提供者"""
    
    # 必填属性
    collection_name = "stock_xgsglb_em"
    display_name = "新股申购与中签"
    akshare_func = "stock_xgsglb_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股数据-新股申购-新股申购与中签查询"
    collection_route = "/stocks/collections/stock_xgsglb_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "交易所", "type": "object", "description": "-"},
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "申购代码", "type": "object", "description": "-"},
        {"name": "发行总数", "type": "float64", "description": "注意单位: 股"},
        {"name": "网上发行", "type": "int64", "description": "注意单位: 股"},
        {"name": "顶格申购需配市值", "type": "float64", "description": "注意单位: 股"},
        {"name": "申购上限", "type": "int64", "description": "-"},
        {"name": "发行价格", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "首日收盘价", "type": "float64", "description": "-"},
        {"name": "申购日期", "type": "object", "description": "-"},
        {"name": "中签号公布日", "type": "object", "description": "-"},
        {"name": "中签缴款日期", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "发行市盈率", "type": "float64", "description": "-"},
        {"name": "行业市盈率", "type": "float64", "description": "-"},
        {"name": "中签率", "type": "float64", "description": "注意单位: %"},
        {"name": "询价累计报价倍数", "type": "float64", "description": "-"},
        {"name": "配售对象报价家数", "type": "float64", "description": "-"},
        {"name": "连续一字板数量", "type": "object", "description": "-"},
        {"name": "涨幅", "type": "float64", "description": "注意单位: %"},
        {"name": "每中一签获利", "type": "float64", "description": "注意单位: 元"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "申购代码", "type": "object", "description": "-"},
        {"name": "发行总数", "type": "int64", "description": "注意单位: 股"},
        {"name": "网上-发行数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "网上-申购上限", "type": "int64", "description": "注意单位: 股"},
        {"name": "网上-顶格所需资金", "type": "int64", "description": "注意单位: 元"},
        {"name": "发行价格", "type": "float64", "description": "-"},
        {"name": "申购日", "type": "object", "description": "-"},
        {"name": "中签率", "type": "float64", "description": "-"},
        {"name": "稳获百股需配资金", "type": "float64", "description": "-"},
        {"name": "最新价格-价格", "type": "float64", "description": "-"},
        {"name": "最新价格-累计涨幅", "type": "float64", "description": "-"},
        {"name": "上市首日-上市日", "type": "object", "description": "-"},
        {"name": "上市首日-均价", "type": "float64", "description": "-"},
        {"name": "上市首日-涨幅", "type": "float64", "description": "-"},
        {"name": "上市首日-每百股获利", "type": "float64", "description": "-"},
        {"name": "上市首日-约合年化收益", "type": "float64", "description": "-"},
        {"name": "发行市盈率", "type": "float64", "description": "-"},
        {"name": "行业市盈率", "type": "float64", "description": "-"},
        {"name": "参与申购资金", "type": "float64", "description": "-"},
        {"name": "参与申购人数", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
