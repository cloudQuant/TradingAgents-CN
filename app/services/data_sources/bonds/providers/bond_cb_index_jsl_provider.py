"""
可转债等权指数-集思录数据提供者（重构版）

数据集合名称: bond_cb_index_jsl
数据唯一标识: 日期
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCbIndexJslProvider(SimpleProvider):
    """可转债等权指数-集思录数据提供者"""
    
    collection_name = "bond_cb_index_jsl"
    display_name = "可转债等权指数-集思录"
    akshare_func = "bond_cb_index_jsl"
    unique_keys = ['日期']
    
    collection_description = "可转债等权指数-集思录数据"
    collection_route = "/bonds/collections/bond_cb_index_jsl"
    collection_order = 24
    
    field_info = [
        {"name": "日期", "type": "date", "description": "指数日期"},
        {"name": "指数", "type": "float", "description": "可转债等权指数"},
        {"name": "剩余规模", "type": "float", "description": "剩余规模，单位：亿元"},
        {"name": "成交额", "type": "float", "description": "成交额，单位：亿元"},
        {"name": "数量", "type": "int", "description": "可转债数量"},
        {"name": "涨跌", "type": "float", "description": "指数涨跌值"},
        {"name": "涨幅", "type": "float", "description": "指数涨幅(%)"},
        {"name": "平均价格", "type": "float", "description": "可转债平均价格(元)"},
        {"name": "中位数价格", "type": "float", "description": "可转债中位数价格(元)"},
        {"name": "中位数转股价值", "type": "float", "description": "可转债中位数转股价值"},
        {"name": "平均双底", "type": "float", "description": "平均双底指标"},
        {"name": "平均溢价率", "type": "float", "description": "平均溢价率(%)"},
        {"name": "中位数溢价率", "type": "float", "description": "中位数溢价率(%)"},
        {"name": "平均收益率", "type": "float", "description": "平均收益率(%)"},
        {"name": "换手率", "type": "float", "description": "换手率(%)"},
        {"name": "价格>90", "type": "int", "description": "价格大于90元的可转债数量"},
        {"name": "价格90~100", "type": "int", "description": "价格在90~100元区间的可转债数量"},
        {"name": "价格100~110", "type": "int", "description": "价格在100~110元区间的可转债数量"},
        {"name": "价格110~120", "type": "int", "description": "价格在110~120元区间的可转债数量"},
        {"name": "价格120~130", "type": "int", "description": "价格在120~130元区间的可转债数量"},
        {"name": "价格>130", "type": "int", "description": "价格大于130元的可转债数量"},
        {"name": ">90涨幅", "type": "float", "description": "价格大于90元区间的平均涨幅(%)"},
        {"name": "90~100涨幅", "type": "float", "description": "价格在90~100元区间的平均涨幅(%)"},
        {"name": "100~110涨幅", "type": "float", "description": "价格在100~110元区间的平均涨幅(%)"},
        {"name": "110~120涨幅", "type": "float", "description": "价格在110~120元区间的平均涨幅(%)"},
        {"name": "120~130涨幅", "type": "float", "description": "价格在120~130元区间的平均涨幅(%)"},
        {"name": ">130涨幅", "type": "float", "description": "价格大于130元区间的平均涨幅(%)"},
        {"name": "沪深300指数", "type": "float", "description": "沪深300指数"},
        {"name": "沪深300指数涨幅", "type": "float", "description": "沪深300指数涨幅(%)"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]

    def fetch_data(self, **kwargs):
        """获取集思录可转债等权指数数据，并将字段名转换为中文"""

        df = self._call_akshare(self.akshare_func, **kwargs)
        if df is None or df.empty:
            self.logger.warning(f"No data returned for {self.collection_name}")
            return df

        # 将 AkShare 返回的英文列名映射为中文列名
        rename_map = {
            "price_dt": "日期",
            "price": "指数",
            "amount": "剩余规模",
            "volume": "成交额",
            "count": "数量",
            "increase_val": "涨跌",
            "increase_rt": "涨幅",
            "avg_price": "平均价格",
            "mid_price": "中位数价格",
            "mid_convert_value": "中位数转股价值",
            "avg_dblow": "平均双底",
            "avg_premium_rt": "平均溢价率",
            "mid_premium_rt": "中位数溢价率",
            "avg_ytm_rt": "平均收益率",
            "turnover_rt": "换手率",
            "price_90": "价格>90",
            "price_90_100": "价格90~100",
            "price_100_110": "价格100~110",
            "price_110_120": "价格110~120",
            "price_120_130": "价格120~130",
            "price_130": "价格>130",
            "increase_rt_90": ">90涨幅",
            "increase_rt_90_100": "90~100涨幅",
            "increase_rt_100_110": "100~110涨幅",
            "increase_rt_110_120": "110~120涨幅",
            "increase_rt_120_130": "120~130涨幅",
            "increase_rt_130": ">130涨幅",
            "idx_price": "沪深300指数",
            "idx_increase_rt": "沪深300指数涨幅",
        }

        df = df.rename(columns=rename_map)

        # 添加元数据，如更新时间、来源等
        df = self._add_metadata(df)
        return df
