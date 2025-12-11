"""期货交易费用参照表数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesFeesInfoProvider(SimpleProvider):
    """期货交易费用参照表数据提供者"""
    
    collection_name = "futures_fees_info"
    display_name = "期货交易费用参照表"
    akshare_func = "futures_fees_info"
    unique_keys = ["日期", "合约代码"]
    
    collection_description = "openctp期货交易费用参照表，包含手续费率、保证金率等信息"
    collection_route = "/futures/collections/futures_fees_info"
    collection_order = 1
    
    field_info = [
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "交易所", "type": "string", "description": "交易所名称"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "品种代码", "type": "string", "description": "品种代码"},
        {"name": "品种名称", "type": "string", "description": "品种名称"},
        {"name": "合约乘数", "type": "int", "description": "合约乘数"},
        {"name": "最小跳动", "type": "float", "description": "最小变动价位"},
        {"name": "开仓费率（按金额）", "type": "float", "description": ""},
        {"name": "开仓费用（按手）", "type": "float", "description": ""},
        {"name": "平仓费率（按金额）", "type": "float", "description": ""},
        {"name": "平仓费用（按手）", "type": "float", "description": ""},
        {"name": "平今费率（按金额）", "type": "float", "description": ""},
        {"name": "平今费用（按手）", "type": "float", "description": ""},
        {"name": "做多保证金率（按金额）", "type": "float", "description": ""},
        {"name": "做多保证金（按手）", "type": "int", "description": ""},
        {"name": "做空保证金率（按金额）", "type": "float", "description": ""},
        {"name": "做空保证金（按手）", "type": "int", "description": ""},
        {"name": "最新价", "type": "float", "description": "最新价格"},
        {"name": "上日结算价", "type": "float", "description": ""},
        {"name": "上日收盘价", "type": "float", "description": ""},
        {"name": "成交量", "type": "int", "description": ""},
        {"name": "持仓量", "type": "int", "description": ""},
        {"name": "1手开仓费用", "type": "float", "description": ""},
        {"name": "1手平仓费用", "type": "float", "description": ""},
        {"name": "1手平今费用", "type": "float", "description": ""},
        {"name": "做多1手保证金", "type": "float", "description": ""},
        {"name": "做空1手保证金", "type": "float", "description": ""},
        {"name": "1Tick平仓盈亏", "type": "float", "description": ""},
        {"name": "2Tick平仓盈亏", "type": "float", "description": ""},
        {"name": "1Tick平仓收益率", "type": "string", "description": ""},
        {"name": "2Tick平仓收益率", "type": "string", "description": ""},
        {"name": "1Tick平今盈亏", "type": "float", "description": ""},
        {"name": "2Tick平今盈亏", "type": "float", "description": ""},
        {"name": "1Tick平今收益率", "type": "string", "description": ""},
        {"name": "2Tick平今收益率", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]

    def fetch_data(self, **kwargs):
        """获取期货交易费用数据，并增加用于唯一键的“日期”列"""
        try:
            self.logger.info(f"Fetching {self.collection_name} data")
            df = self._call_akshare(self.akshare_func, **kwargs)

            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return df

            # 从原始“更新时间”列派生“日期”列（仅当不存在时）
            if "日期" not in df.columns and "更新时间" in df.columns:
                df["日期"] = df["更新时间"].astype(str).str[:10]

            # 添加抓取时间等元数据（覆盖/补充 "更新时间" 列）
            df = self._add_metadata(df)

            self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
            return df
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
