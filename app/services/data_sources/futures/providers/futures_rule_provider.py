"""期货规则-交易日历表数据提供者"""
from datetime import datetime

from app.services.data_sources.base_provider import BaseProvider


class FuturesRuleProvider(BaseProvider):
    """期货规则-交易日历表数据提供者"""
    
    collection_name = "futures_rule"
    display_name = "期货规则-交易日历表"
    akshare_func = "futures_rule"
    unique_keys = ["日期", "代码"]
    
    collection_description = "国泰君安期货交易日历数据表"
    collection_route = "/futures/collections/futures_rule"
    collection_order = 3

    def fetch_data(self, **kwargs):
        date = kwargs.get("date")
        if date:
            date_str = str(date)
            # 兼容 "YYYY-MM-DD" 或带时间的 "YYYY-MM-DD HH:MM:SS"，统一转成 "YYYYMMDD"
            if "-" in date_str:
                try:
                    dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
                    date_str = dt.strftime("%Y%m%d")
                except ValueError:
                    self.logger.warning(f"futures_rule 日期参数格式不正确，原始值: {date_str}")
            kwargs["date"] = date_str

        return super().fetch_data(**kwargs)
    
    param_mapping = {
        "date": "date",
    }
    # date 参数是可选的，akshare 的 futures_rule() 不传参数时返回最新数据
    required_params = []
    # 将 date 参数值添加到"日期"列，用于唯一键识别
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期 (YYYY-MM-DD)"},
        {"name": "交易所", "type": "string", "description": "期货交易所"},
        {"name": "品种", "type": "string", "description": "期货品种"},
        {"name": "代码", "type": "string", "description": "合约代码"},
        {"name": "交易保证金比例", "type": "float", "description": "单位: %"},
        {"name": "涨跌停板幅度", "type": "float", "description": "单位: %"},
        {"name": "合约乘数", "type": "int", "description": "每手合约乘数"},
        {"name": "最小变动价位", "type": "float", "description": "最小价格变动"},
        {"name": "限价单每笔最大下单手数", "type": "int", "description": "限价单最大手数"},
        {"name": "特殊合约参数调整", "type": "string", "description": "特殊调整信息"},
        {"name": "调整备注", "type": "string", "description": "调整说明"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
