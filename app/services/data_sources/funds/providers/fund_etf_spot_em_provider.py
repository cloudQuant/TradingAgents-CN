"""
ETF实时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
import pandas as pd
from app.services.data_sources.base_provider import SimpleProvider


class FundEtfSpotEmProvider(SimpleProvider):
    
    """ETF实时行情-东财数据提供者"""

    collection_description = "东方财富网-ETF实时行情数据，包括最新价、涨跌幅、成交量、资金流向等"
    collection_route = "/funds/collections/fund_etf_spot_em"
    collection_order = 6

    collection_name = "fund_etf_spot_em"
    display_name = "ETF基金实时行情-东财"
    akshare_func = "fund_etf_spot_em"
    unique_keys = ["代码", "数据日期"]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取ETF实时行情数据
        
        该接口不需要任何参数，过滤掉所有传入的参数
        """
        try:
            self.logger.info(f"Fetching {self.collection_name} data")
            
            # fund_etf_spot_em 接口不需要任何参数，过滤掉所有传入的参数
            # 过滤掉前端特有参数和业务参数
            frontend_only_params = {
                'update_type', 'update_mode', 'batch_update', 'batch_size', 
                'page', 'limit', 'skip', 'filters', 'sort', 'order',
                'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
                'force', 'clear_first', 'overwrite', 'mode', 'concurrency',
                'fund_code', 'symbol', 'year', 'date', 'period', 'adjust',
                'start_year', 'end_year', 'delay', 'code'
            }
            
            # 过滤掉所有参数（该接口不需要参数）
            filtered_kwargs = {
                k: v for k, v in kwargs.items() 
                if k not in frontend_only_params and v is not None
            }
            
            # 如果还有未过滤的参数，记录警告
            if filtered_kwargs:
                self.logger.warning(
                    f"[{self.collection_name}] 收到未预期的参数: {list(filtered_kwargs.keys())}, "
                    f"将忽略这些参数（该接口不需要参数）"
                )
            
            # 调用akshare，不传递任何参数
            df = self._call_akshare(self.akshare_func)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "IOPV实时估值", "type": "float", "description": ""},
        {"name": "基金折价率", "type": "float", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "成交量", "type": "float", "description": ""},
        {"name": "成交额", "type": "float", "description": ""},
        {"name": "开盘价", "type": "float", "description": ""},
        {"name": "最高价", "type": "float", "description": ""},
        {"name": "最低价", "type": "float", "description": ""},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "换手率", "type": "float", "description": ""},
        {"name": "量比", "type": "float", "description": ""},
        {"name": "委比", "type": "float", "description": ""},
        {"name": "外盘", "type": "float", "description": ""},
        {"name": "内盘", "type": "float", "description": ""},
        {"name": "主力净流入-净额", "type": "float", "description": ""},
        {"name": "主力净流入-净占比", "type": "float", "description": ""},
        {"name": "超大单净流入-净额", "type": "float", "description": ""},
        {"name": "超大单净流入-净占比", "type": "float", "description": ""},
        {"name": "大单净流入-净额", "type": "float", "description": ""},
        {"name": "大单净流入-净占比", "type": "float", "description": ""},
        {"name": "中单净流入-净额", "type": "float", "description": ""},
        {"name": "中单净流入-净占比", "type": "float", "description": ""},
        {"name": "小单净流入-净额", "type": "float", "description": ""},
        {"name": "小单净流入-净占比", "type": "float", "description": ""},
        {"name": "现手", "type": "float", "description": ""},
        {"name": "买一", "type": "float", "description": ""},
        {"name": "卖一", "type": "float", "description": ""},
        {"name": "最新份额", "type": "float", "description": ""},
        {"name": "流通市值", "type": "int", "description": ""},
        {"name": "总市值", "type": "int", "description": ""},
        {"name": "数据日期", "type": "string", "description": ""},
        {"name": "更新时间", "type": "string", "description": ""},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_spot_em"},
    ]
