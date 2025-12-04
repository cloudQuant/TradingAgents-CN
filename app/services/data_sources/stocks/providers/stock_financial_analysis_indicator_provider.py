"""
财务指标数据提供者

新浪财经-财务分析-财务指标
接口: stock_financial_analysis_indicator
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialAnalysisIndicatorProvider(BaseProvider):
    """财务指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_analysis_indicator"
    display_name = "财务指标"
    akshare_func = "stock_financial_analysis_indicator"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-财务分析-财务指标"
    collection_route = "/stocks/collections/stock_financial_analysis_indicator"
    collection_category = "财务数据"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_year": "start_year"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_year']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "摊薄每股收益(元)", "type": "float64", "description": "-"},
        {"name": "加权每股收益(元)", "type": "float64", "description": "-"},
        {"name": "每股收益_调整后(元)", "type": "float64", "description": "-"},
        {"name": "扣除非经常性损益后的每股收益(元)", "type": "float64", "description": "-"},
        {"name": "每股净资产_调整前(元)", "type": "float64", "description": "-"},
        {"name": "每股净资产_调整后(元)", "type": "float64", "description": "-"},
        {"name": "每股经营性现金流(元)", "type": "float64", "description": "-"},
        {"name": "每股资本公积金(元)", "type": "float64", "description": "-"},
        {"name": "每股未分配利润(元)", "type": "float64", "description": "-"},
        {"name": "调整后的每股净资产(元)", "type": "float64", "description": "-"},
        {"name": "总资产利润率(%)", "type": "float64", "description": "-"},
        {"name": "主营业务利润率(%)", "type": "float64", "description": "-"},
        {"name": "总资产净利润率(%)", "type": "float64", "description": "-"},
        {"name": "成本费用利润率(%)", "type": "float64", "description": "-"},
        {"name": "营业利润率(%)", "type": "float64", "description": "-"},
        {"name": "主营业务成本率(%)", "type": "float64", "description": "-"},
        {"name": "销售净利率(%)", "type": "float64", "description": "-"},
        {"name": "股本报酬率(%)", "type": "float64", "description": "-"},
        {"name": "净资产报酬率(%)", "type": "float64", "description": "-"},
        {"name": "资产报酬率(%)", "type": "float64", "description": "-"},
        {"name": "销售毛利率(%)", "type": "float64", "description": "-"},
        {"name": "三项费用比重", "type": "float64", "description": "-"},
        {"name": "非主营比重", "type": "float64", "description": "-"},
        {"name": "主营利润比重", "type": "float64", "description": "-"},
        {"name": "股息发放率(%)", "type": "float64", "description": "-"},
        {"name": "投资收益率(%)", "type": "float64", "description": "-"},
        {"name": "主营业务利润(元)", "type": "float64", "description": "-"},
        {"name": "净资产收益率(%)", "type": "float64", "description": "-"},
        {"name": "加权净资产收益率(%)", "type": "float64", "description": "-"},
        {"name": "扣除非经常性损益后的净利润(元)", "type": "float64", "description": "-"},
        {"name": "主营业务收入增长率(%)", "type": "float64", "description": "-"},
        {"name": "净利润增长率(%)", "type": "float64", "description": "-"},
        {"name": "净资产增长率(%)", "type": "float64", "description": "-"},
        {"name": "总资产增长率(%)", "type": "float64", "description": "-"},
        {"name": "应收账款周转率(次)", "type": "float64", "description": "-"},
        {"name": "应收账款周转天数(天)", "type": "float64", "description": "-"},
        {"name": "存货周转天数(天)", "type": "float64", "description": "-"},
        {"name": "存货周转率(次)", "type": "float64", "description": "-"},
        {"name": "固定资产周转率(次)", "type": "float64", "description": "-"},
        {"name": "总资产周转率(次)", "type": "float64", "description": "-"},
        {"name": "总资产周转天数(天)", "type": "float64", "description": "-"},
        {"name": "流动资产周转率(次)", "type": "float64", "description": "-"},
        {"name": "流动资产周转天数(天)", "type": "float64", "description": "-"},
        {"name": "股东权益周转率(次)", "type": "float64", "description": "-"},
        {"name": "流动比率", "type": "float64", "description": "-"},
        {"name": "速动比率", "type": "float64", "description": "-"},
        {"name": "现金比率(%)", "type": "float64", "description": "-"},
        {"name": "利息支付倍数", "type": "float64", "description": "-"},
        {"name": "长期债务与营运资金比率(%)", "type": "float64", "description": "-"},
        {"name": "股东权益比率(%)", "type": "float64", "description": "-"},
        {"name": "长期负债比率(%)", "type": "float64", "description": "-"},
        {"name": "股东权益与固定资产比率(%)", "type": "float64", "description": "-"},
        {"name": "负债与所有者权益比率(%)", "type": "float64", "description": "-"},
        {"name": "长期资产与长期资金比率(%)", "type": "float64", "description": "-"},
        {"name": "资本化比率(%)", "type": "float64", "description": "-"},
        {"name": "固定资产净值率(%)", "type": "float64", "description": "-"},
        {"name": "资本固定化比率(%)", "type": "float64", "description": "-"},
        {"name": "产权比率(%)", "type": "float64", "description": "-"},
        {"name": "清算价值比率(%)", "type": "float64", "description": "-"},
        {"name": "固定资产比重(%)", "type": "float64", "description": "-"},
        {"name": "资产负债率(%)", "type": "float64", "description": "-"},
        {"name": "总资产(元)", "type": "float64", "description": "-"},
        {"name": "经营现金净流量对销售收入比率(%)", "type": "float64", "description": "-"},
        {"name": "资产的经营现金流量回报率(%)", "type": "float64", "description": "-"},
        {"name": "经营现金净流量与净利润的比率(%)", "type": "float64", "description": "-"},
        {"name": "经营现金净流量对负债比率(%)", "type": "float64", "description": "-"},
        {"name": "现金流量比率(%)", "type": "float64", "description": "-"},
        {"name": "短期股票投资(元)", "type": "float64", "description": "-"},
        {"name": "短期债券投资(元)", "type": "float64", "description": "-"},
        {"name": "短期其它经营性投资(元)", "type": "float64", "description": "-"},
        {"name": "长期股票投资(元)", "type": "float64", "description": "-"},
        {"name": "长期债券投资(元)", "type": "float64", "description": "-"},
        {"name": "长期其它经营性投资(元)", "type": "float64", "description": "-"},
        {"name": "1年以内应收帐款(元)", "type": "float64", "description": "-"},
        {"name": "1-2年以内应收帐款(元)", "type": "float64", "description": "-"},
        {"name": "2-3年以内应收帐款(元)", "type": "float64", "description": "-"},
        {"name": "3年以内应收帐款(元)", "type": "float64", "description": "-"},
        {"name": "1年以内预付货款(元)", "type": "float64", "description": "-"},
        {"name": "1-2年以内预付货款(元)", "type": "float64", "description": "-"},
        {"name": "2-3年以内预付货款(元)", "type": "float64", "description": "-"},
        {"name": "3年以内预付货款(元)", "type": "float64", "description": "-"},
        {"name": "1年以内其它应收款(元)", "type": "float64", "description": "-"},
        {"name": "1-2年以内其它应收款(元)", "type": "float64", "description": "-"},
        {"name": "2-3年以内其它应收款(元)", "type": "float64", "description": "-"},
        {"name": "3年以内其它应收款(元)", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
