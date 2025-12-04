"""
历史行情数据-腾讯服务

腾讯证券-日频-股票历史数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
接口: stock_zh_a_hist_tx
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_hist_tx_provider import StockZhAHistTxProvider


class StockZhAHistTxService(BaseService):
    """历史行情数据-腾讯服务"""
    
    collection_name = "stock_zh_a_hist_tx"
    provider_class = StockZhAHistTxProvider
    
    # 时间字段名
    time_field = "更新时间"
