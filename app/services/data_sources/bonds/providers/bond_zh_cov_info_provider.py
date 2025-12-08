"""
可转债详情-东财数据提供者（重构版）

数据集合名称: bond_zh_cov_info
数据唯一标识: 可转债代码, item
"""
from app.services.data_sources.base_provider import BaseProvider
import pandas as pd


class BondZhCovInfoProvider(BaseProvider):
    """可转债详情-东财数据提供者"""
    
    collection_name = "bond_zh_cov_info"
    display_name = "可转债详情-东财"
    akshare_func = "bond_zh_cov_info"
    unique_keys = ["债券代码", "指标类型"]
    
    collection_description = "可转债详情-东财数据"
    collection_route = "/bonds/collections/bond_zh_cov_info"
    collection_order = 15

    # 仅支持 indicator="基本信息"，以下字段均为中文列名，对应该指标返回的数据
    field_info = [
        {"name": "债券代码", "type": "string", "description": "可转债代码"},
        {"name": "指标类型", "type": "string", "description": "固定为 基本信息"},
        {"name": "证券代码", "type": "string", "description": "证券代码(带交易所后缀)"},
        {"name": "交易市场", "type": "string", "description": "交易市场代码"},
        {"name": "证券简称", "type": "string", "description": "证券简称"},
        {"name": "摘牌日期", "type": "string", "description": "摘牌日期"},
        {"name": "上市日期", "type": "string", "description": "上市日期"},
        {"name": "转股代码", "type": "string", "description": "转股代码"},
        {"name": "债券期限", "type": "string", "description": "债券期限"},
        {"name": "信用评级", "type": "string", "description": "信用评级"},
        {"name": "起息日", "type": "string", "description": "起息日"},
        {"name": "发行年度", "type": "string", "description": "发行年度"},
        {"name": "停止转股日", "type": "string", "description": "停止转股日"},
        {"name": "到期日", "type": "string", "description": "到期日"},
        {"name": "付息日", "type": "string", "description": "付息日"},
        {"name": "利率说明", "type": "string", "description": "利率说明"},
        {"name": "债券组合代码", "type": "string", "description": "债券组合代码"},
        {"name": "实际发行规模", "type": "number", "description": "实际发行规模"},
        {"name": "发行价格", "type": "number", "description": "发行价格"},
        {"name": "备注", "type": "string", "description": "备注"},
        {"name": "面值", "type": "number", "description": "面值"},
        {"name": "发行对象", "type": "string", "description": "发行对象"},
        {"name": "赎回类型", "type": "string", "description": "赎回类型"},
        {"name": "赎回触发原因_沪市", "type": "string", "description": "赎回触发原因(沪市)"},
        {"name": "赎回公告日期_沪市", "type": "string", "description": "赎回公告日期(沪市)"},
        {"name": "赎回公告日期_深市", "type": "string", "description": "赎回公告日期(深市)"},
        {"name": "赎回价格_沪市", "type": "number", "description": "赎回价格(沪市)"},
        {"name": "赎回价格_深市", "type": "string", "description": "赎回价格(深市)"},
        {"name": "股权登记日_深市", "type": "string", "description": "股权登记日(深市)"},
        {"name": "赎回起始日_深市", "type": "string", "description": "赎回起始日(深市)"},
        {"name": "赎回起始日_沪市", "type": "string", "description": "赎回起始日(沪市)"},
        {"name": "赎回结束日", "type": "string", "description": "赎回结束日"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股简称", "type": "string", "description": "正股简称"},
        {"name": "网上申购开始日期", "type": "string", "description": "网上申购开始日期"},
        {"name": "原股代码", "type": "string", "description": "原股代码"},
        {"name": "原股简称", "type": "string", "description": "原股简称"},
        {"name": "债券起始日", "type": "string", "description": "债券起始日"},
        {"name": "证券起始日", "type": "string", "description": "证券起始日"},
        {"name": "证券短名", "type": "string", "description": "证券短名"},
        {"name": "每股配售比例", "type": "number", "description": "每股配售比例"},
        {"name": "网上一般户申购上限", "type": "number", "description": "网上一般户申购上限"},
        {"name": "网上一般户申购下限", "type": "number", "description": "网上一般户申购下限"},
        {"name": "初始转股价", "type": "number", "description": "初始转股价格"},
        {"name": "转股结束日", "type": "string", "description": "转股结束日"},
        {"name": "转股开始日", "type": "string", "description": "转股开始日"},
        {"name": "回售条款", "type": "string", "description": "回售条款"},
        {"name": "赎回条款", "type": "string", "description": "赎回条款"},
        {"name": "发行人名称", "type": "string", "description": "发行人名称"},
        {"name": "当前转股价", "type": "number", "description": "当前转股价格"},
        {"name": "转股价格", "type": "number", "description": "转股价格"},
        {"name": "转股价值", "type": "number", "description": "转股价值"},
        {"name": "当前债券价格", "type": "number", "description": "当前债券价格"},
        {"name": "转股溢价率", "type": "number", "description": "转股溢价率"},
        {"name": "转股价行情", "type": "string", "description": "转股价格(行情)"},
        {"name": "市场", "type": "string", "description": "市场"},
        {"name": "回售触发价", "type": "number", "description": "回售触发价格"},
        {"name": "赎回触发价", "type": "number", "description": "赎回触发价格"},
        {"name": "市净率", "type": "number", "description": "市净率"},
        {"name": "申购起始日", "type": "string", "description": "申购起始日"},
        {"name": "申购截止日", "type": "string", "description": "申购截止日"},
        {"name": "现金流日期", "type": "string", "description": "现金流日期"},
        {"name": "票面利率", "type": "number", "description": "票面利率"},
        {"name": "参数名称", "type": "string", "description": "参数名称"},
        {"name": "发行类型", "type": "string", "description": "发行类型"},
        {"name": "赎回触发原因_深市", "type": "string", "description": "赎回触发原因(深市)"},
        {"name": "最新付息日", "type": "string", "description": "最新付息日"},
        {"name": "最新债券价格", "type": "string", "description": "最新债券价格"},
        {"name": "是否可转股", "type": "string", "description": "是否可转股"},
        {"name": "是否可赎回", "type": "string", "description": "是否可赎回"},
        {"name": "是否可回售", "type": "string", "description": "是否可回售"},
        {"name": "首日收益", "type": "number", "description": "首日收益"},
        {"name": "申购开始时间_含时分", "type": "string", "description": "申购开始时间(含时分)"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "数据来源", "type": "string", "description": "数据来源，例如 eastmoney"},
    ]

    def fetch_data(self, **kwargs):
        """获取可转债详情-基本信息，并展开所有字段为独立列。

        仅支持 indicator="基本信息"，忽略其它指标类型。
        """
        symbol = kwargs.get("symbol")
        indicator = kwargs.get("indicator") or "基本信息"

        if not symbol:
            raise ValueError("缺少必须参数: symbol")

        if indicator != "基本信息":
            raise ValueError("当前仅支持 indicator='基本信息'")

        # 调用 AkShare，仅请求基本信息
        df = self._call_akshare(self.akshare_func, symbol=str(symbol), indicator="基本信息")

        if df is None or df.empty:
            self.logger.warning(f"[bond_zh_cov_info] {symbol} 基本信息 未返回数据")
            return pd.DataFrame()

        df = df.copy()

        # 将英文列名映射为中文列名
        rename_mapping = {
            "SECURITY_CODE": "债券代码",
            "SECUCODE": "证券代码",
            "TRADE_MARKET": "交易市场",
            "SECURITY_NAME_ABBR": "证券简称",
            "DELIST_DATE": "摘牌日期",
            "LISTING_DATE": "上市日期",
            "CONVERT_STOCK_CODE": "转股代码",
            "BOND_EXPIRE": "债券期限",
            "RATING": "信用评级",
            "VALUE_DATE": "起息日",
            "ISSUE_YEAR": "发行年度",
            "CEASE_DATE": "停止转股日",
            "EXPIRE_DATE": "到期日",
            "PAY_INTEREST_DAY": "付息日",
            "INTEREST_RATE_EXPLAIN": "利率说明",
            "BOND_COMBINE_CODE": "债券组合代码",
            "ACTUAL_ISSUE_SCALE": "实际发行规模",
            "ISSUE_PRICE": "发行价格",
            "REMARK": "备注",
            "PAR_VALUE": "面值",
            "ISSUE_OBJECT": "发行对象",
            "REDEEM_TYPE": "赎回类型",
            "EXECUTE_REASON_HS": "赎回触发原因_沪市",
            "NOTICE_DATE_HS": "赎回公告日期_沪市",
            "NOTICE_DATE_SH": "赎回公告日期_深市",
            "EXECUTE_PRICE_HS": "赎回价格_沪市",
            "EXECUTE_PRICE_SH": "赎回价格_深市",
            "RECORD_DATE_SH": "股权登记日_深市",
            "EXECUTE_START_DATESH": "赎回起始日_深市",
            "EXECUTE_START_DATEHS": "赎回起始日_沪市",
            "EXECUTE_END_DATE": "赎回结束日",
            "CORRECODE": "正股代码",
            "CORRECODE_NAME_ABBR": "正股简称",
            "PUBLIC_START_DATE": "网上申购开始日期",
            "CORRECODEO": "原股代码",
            "CORRECODE_NAME_ABBRO": "原股简称",
            "BOND_START_DATE": "债券起始日",
            "SECURITY_START_DATE": "证券起始日",
            "SECURITY_SHORT_NAME": "证券短名",
            "FIRST_PER_PREPLACING": "每股配售比例",
            "ONLINE_GENERAL_AAU": "网上一般户申购上限",
            "ONLINE_GENERAL_LWR": "网上一般户申购下限",
            "INITIAL_TRANSFER_PRICE": "初始转股价",
            "TRANSFER_END_DATE": "转股结束日",
            "TRANSFER_START_DATE": "转股开始日",
            "RESALE_CLAUSE": "回售条款",
            "REDEEM_CLAUSE": "赎回条款",
            "PARTY_NAME": "发行人名称",
            "CONVERT_STOCK_PRICE": "当前转股价",
            "TRANSFER_PRICE": "转股价格",
            "TRANSFER_VALUE": "转股价值",
            "CURRENT_BOND_PRICE": "当前债券价格",
            "TRANSFER_PREMIUM_RATIO": "转股溢价率",
            "CONVERT_STOCK_PRICEHQ": "转股价行情",
            "MARKET": "市场",
            "RESALE_TRIG_PRICE": "回售触发价",
            "REDEEM_TRIG_PRICE": "赎回触发价",
            "PBV_RATIO": "市净率",
            "IB_START_DATE": "申购起始日",
            "IB_END_DATE": "申购截止日",
            "CASHFLOW_DATE": "现金流日期",
            "COUPON_IR": "票面利率",
            "PARAM_NAME": "参数名称",
            "ISSUE_TYPE": "发行类型",
            "EXECUTE_REASON_SH": "赎回触发原因_深市",
            "PAYDAYNEW": "最新付息日",
            "CURRENT_BOND_PRICENEW": "最新债券价格",
            "IS_CONVERT_STOCK": "是否可转股",
            "IS_REDEEM": "是否可赎回",
            "IS_SELLBACK": "是否可回售",
            "FIRST_PROFIT": "首日收益",
            "PUBLIC_START_DATE_HOURS": "申购开始时间_含时分",
        }

        df = df.rename(columns={k: v for k, v in rename_mapping.items() if k in df.columns})

        # 确保债券代码列存在
        if "债券代码" not in df.columns:
            if "SECURITY_CODE" in df.columns:
                df["债券代码"] = df["SECURITY_CODE"].astype(str)
            else:
                df["债券代码"] = str(symbol)

        df["指标类型"] = "基本信息"
        df["数据来源"] = "eastmoney"

        # 添加 "更新时间" 等元数据字段
        df = self._add_metadata(df)
        return df
