"""
期权数据模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class OptionContractInfoCtp(BaseModel):
    """
    OpenCTP期权合约信息
    Collection: option_contract_info_ctp
    """
    exchange_id: Optional[str] = Field(None, description="交易所ID")
    instrument_id: Optional[str] = Field(None, description="合约ID")
    instrument_name: Optional[str] = Field(None, description="合约名称")
    product_class: Optional[str] = Field(None, description="商品类别")
    product_id: Optional[str] = Field(None, description="品种ID")
    volume_multiple: Optional[int] = Field(None, description="合约乘数")
    price_tick: Optional[float] = Field(None, description="最小变动价位")
    
    # Margin
    long_margin_ratio: Optional[float] = Field(None, description="做多保证金率")
    short_margin_ratio: Optional[float] = Field(None, description="做空保证金率")
    long_margin_per_lot: Optional[float] = Field(None, description="做多保证金/手")
    short_margin_per_lot: Optional[float] = Field(None, description="做空保证金/手")
    
    # Fees
    open_fee_ratio: Optional[float] = Field(None, description="开仓手续费率")
    open_fee_per_lot: Optional[float] = Field(None, description="开仓手续费/手")
    close_fee_ratio: Optional[float] = Field(None, description="平仓手续费率")
    close_fee_per_lot: Optional[float] = Field(None, description="平仓手续费/手")
    close_today_fee_ratio: Optional[float] = Field(None, description="平今手续费率")
    close_today_fee_per_lot: Optional[float] = Field(None, description="平今手续费/手")
    
    # Dates
    delivery_year: Optional[int] = Field(None, description="交割年份")
    delivery_month: Optional[int] = Field(None, description="交割月份")
    create_date: Optional[str] = Field(None, description="上市日期")
    expire_date: Optional[str] = Field(None, description="最后交易日")
    delivery_date: Optional[str] = Field(None, description="交割日")
    
    # Option specific
    underlying_instrument_id: Optional[str] = Field(None, description="标的合约ID")
    underlying_multiple: Optional[int] = Field(None, description="标的合约乘数")
    option_type: Optional[str] = Field(None, description="期权类型")
    strike_price: Optional[float] = Field(None, description="行权价")
    instrument_status: Optional[str] = Field(None, description="合约状态")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionFinanceBoard(BaseModel):
    """
    金融期权行情数据
    Collection: option_finance_board
    """
    date: Optional[str] = Field(None, description="日期")
    code: Optional[str] = Field(None, description="合约交易代码")
    current_price: Optional[float] = Field(None, description="当前价")
    change_pct: Optional[float] = Field(None, description="涨跌幅")
    pre_settle: Optional[float] = Field(None, description="前结价")
    strike_price: Optional[float] = Field(None, description="行权价")
    quantity: Optional[int] = Field(None, description="数量")
    
    # Extra fields to identify source
    symbol: Optional[str] = Field(None, description="标的名称")
    end_month: Optional[str] = Field(None, description="到期月份")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionRiskIndicatorSse(BaseModel):
    """
    上海证券交易所期权风险指标
    Collection: option_risk_indicator_sse
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    security_id: Optional[str] = Field(None, description="证券代码")
    contract_id: Optional[str] = Field(None, description="合约代码")
    contract_symbol: Optional[str] = Field(None, description="合约简称")
    delta: Optional[float] = Field(None, description="Delta")
    theta: Optional[float] = Field(None, description="Theta")
    gamma: Optional[float] = Field(None, description="Gamma")
    vega: Optional[float] = Field(None, description="Vega")
    rho: Optional[float] = Field(None, description="Rho")
    implied_volatility: Optional[float] = Field(None, description="隐含波动率")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCurrentDaySse(BaseModel):
    """
    上海证券交易所产品股票期权信息披露当日合约
    Collection: option_current_day_sse
    """
    contract_code: Optional[str] = Field(None, description="合约编码")
    trade_code: Optional[str] = Field(None, description="合约交易代码")
    contract_name: Optional[str] = Field(None, description="合约简称")
    underlying_name_code: Optional[str] = Field(None, description="标的券名称及代码")
    option_type: Optional[str] = Field(None, description="类型")
    strike_price: Optional[str] = Field(None, description="行权价")
    contract_unit: Optional[str] = Field(None, description="合约单位")
    exercise_date: Optional[str] = Field(None, description="期权行权日")
    delivery_date: Optional[str] = Field(None, description="行权交收日")
    expire_date: Optional[str] = Field(None, description="到期日")
    start_date: Optional[str] = Field(None, description="开始日期")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCurrentDaySzse(BaseModel):
    """
    深圳证券交易所期权子网行情数据当日合约
    Collection: option_current_day_szse
    """
    serial_number: Optional[int] = Field(None, description="序号")
    contract_code_id: Optional[int] = Field(None, description="合约编码")
    contract_code: Optional[str] = Field(None, description="合约代码")
    contract_name: Optional[str] = Field(None, description="合约简称")
    underlying_name_code: Optional[str] = Field(None, description="标的证券简称(代码)")
    contract_type: Optional[str] = Field(None, description="合约类型")
    strike_price: Optional[float] = Field(None, description="行权价")
    contract_unit: Optional[int] = Field(None, description="合约单位")
    last_trade_date: Optional[str] = Field(None, description="最后交易日")
    exercise_date: Optional[str] = Field(None, description="行权日")
    expire_date: Optional[str] = Field(None, description="到期日")
    delivery_date: Optional[str] = Field(None, description="交收日")
    is_new: Optional[str] = Field(None, description="新挂")
    limit_up: Optional[float] = Field(None, description="涨停价格")
    limit_down: Optional[float] = Field(None, description="跌停价格")
    pre_settle: Optional[float] = Field(None, description="前结算价")
    is_adjusted: Optional[str] = Field(None, description="合约调整")
    is_suspended: Optional[str] = Field(None, description="停牌")
    open_interest: Optional[float] = Field(None, description="合约总持仓")
    list_reason: Optional[str] = Field(None, description="挂牌原因")
    
    trade_date: Optional[str] = Field(None, description="交易日期")
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionDailyStatsSse(BaseModel):
    """
    上海证券交易所产品股票期权每日统计
    Collection: option_daily_stats_sse
    """
    underlying_code: Optional[str] = Field(None, description="合约标的代码")
    underlying_name: Optional[str] = Field(None, description="合约标的名称")
    contract_quantity: Optional[int] = Field(None, description="合约数量")
    total_turnover: Optional[float] = Field(None, description="总成交额(万元)")
    total_volume: Optional[int] = Field(None, description="总成交量(张)")
    call_volume: Optional[int] = Field(None, description="认购成交量(张)")
    put_volume: Optional[int] = Field(None, description="认沽成交量(张)")
    put_call_ratio: Optional[float] = Field(None, description="认沽/认购(%)")
    open_interest_total: Optional[int] = Field(None, description="未平仓合约总数")
    open_interest_call: Optional[int] = Field(None, description="未平仓认购合约数")
    open_interest_put: Optional[int] = Field(None, description="未平仓认沽合约数")
    
    trade_date: Optional[str] = Field(None, description="交易日期")
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionDailyStatsSzse(BaseModel):
    """
    深圳证券交易所市场数据期权数据日度概况
    Collection: option_daily_stats_szse
    """
    underlying_code: Optional[str] = Field(None, description="合约标的代码")
    underlying_name: Optional[str] = Field(None, description="合约标的名称")
    total_volume: Optional[int] = Field(None, description="成交量(张)")
    call_volume: Optional[int] = Field(None, description="认购成交量(张)")
    put_volume: Optional[int] = Field(None, description="认沽成交量(张)")
    put_call_ratio: Optional[float] = Field(None, description="认沽/认购持仓比(%)")
    open_interest_total: Optional[int] = Field(None, description="未平仓合约总数(张)")
    open_interest_call: Optional[int] = Field(None, description="未平仓认购合约数(张)")
    open_interest_put: Optional[int] = Field(None, description="未平仓认沽合约数(张)")
    
    trade_date: Optional[str] = Field(None, description="交易日期")
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexSz50ListSina(BaseModel):
    """
    中金所上证50指数所有合约
    Collection: option_cffex_sz50_list_sina
    """
    contract_code: Optional[str] = Field(None, description="合约代码")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexHs300ListSina(BaseModel):
    """
    中金所沪深300指数所有合约
    Collection: option_cffex_hs300_list_sina
    """
    contract_code: Optional[str] = Field(None, description="合约代码")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexZz1000ListSina(BaseModel):
    """
    中金所中证1000指数所有合约
    Collection: option_cffex_zz1000_list_sina
    """
    contract_code: Optional[str] = Field(None, description="合约代码")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexSz50SpotSina(BaseModel):
    """
    新浪财经中金所上证50指数指定合约实时行情
    Collection: option_cffex_sz50_spot_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    call_bid_volume: Optional[int] = Field(None, description="看涨合约-买量")
    call_bid_price: Optional[float] = Field(None, description="看涨合约-买价")
    call_last_price: Optional[float] = Field(None, description="看涨合约-最新价")
    call_ask_price: Optional[float] = Field(None, description="看涨合约-卖价")
    call_ask_volume: Optional[int] = Field(None, description="看涨合约-卖量")
    call_open_interest: Optional[int] = Field(None, description="看涨合约-持仓量")
    call_change: Optional[float] = Field(None, description="看涨合约-涨跌")
    strike_price: Optional[int] = Field(None, description="行权价")
    call_symbol: Optional[str] = Field(None, description="看涨合约-标识")
    put_bid_volume: Optional[int] = Field(None, description="看跌合约-买量")
    put_bid_price: Optional[float] = Field(None, description="看跌合约-买价")
    put_last_price: Optional[float] = Field(None, description="看跌合约-最新价")
    put_ask_price: Optional[float] = Field(None, description="看跌合约-卖价")
    put_ask_volume: Optional[int] = Field(None, description="看跌合约-卖量")
    put_open_interest: Optional[int] = Field(None, description="看跌合约-持仓量")
    put_change: Optional[float] = Field(None, description="看跌合约-涨跌")
    put_symbol: Optional[str] = Field(None, description="看跌合约-标识")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexHs300SpotSina(BaseModel):
    """
    新浪财经中金所沪深300指数指定合约实时行情
    Collection: option_cffex_hs300_spot_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    call_bid_volume: Optional[int] = Field(None, description="看涨合约-买量")
    call_bid_price: Optional[float] = Field(None, description="看涨合约-买价")
    call_last_price: Optional[float] = Field(None, description="看涨合约-最新价")
    call_ask_price: Optional[float] = Field(None, description="看涨合约-卖价")
    call_ask_volume: Optional[int] = Field(None, description="看涨合约-卖量")
    call_open_interest: Optional[int] = Field(None, description="看涨合约-持仓量")
    call_change: Optional[float] = Field(None, description="看涨合约-涨跌")
    strike_price: Optional[int] = Field(None, description="行权价")
    call_symbol: Optional[str] = Field(None, description="看涨合约-标识")
    put_bid_volume: Optional[int] = Field(None, description="看跌合约-买量")
    put_bid_price: Optional[float] = Field(None, description="看跌合约-买价")
    put_last_price: Optional[float] = Field(None, description="看跌合约-最新价")
    put_ask_price: Optional[float] = Field(None, description="看跌合约-卖价")
    put_ask_volume: Optional[int] = Field(None, description="看跌合约-卖量")
    put_open_interest: Optional[int] = Field(None, description="看跌合约-持仓量")
    put_change: Optional[float] = Field(None, description="看跌合约-涨跌")
    put_symbol: Optional[str] = Field(None, description="看跌合约-标识")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexZz1000SpotSina(BaseModel):
    """
    新浪财经中金所中证1000指数指定合约实时行情
    Collection: option_cffex_zz1000_spot_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    call_bid_volume: Optional[int] = Field(None, description="看涨合约-买量")
    call_bid_price: Optional[float] = Field(None, description="看涨合约-买价")
    call_last_price: Optional[float] = Field(None, description="看涨合约-最新价")
    call_ask_price: Optional[float] = Field(None, description="看涨合约-卖价")
    call_ask_volume: Optional[int] = Field(None, description="看涨合约-卖量")
    call_open_interest: Optional[int] = Field(None, description="看涨合约-持仓量")
    call_change: Optional[float] = Field(None, description="看涨合约-涨跌")
    strike_price: Optional[int] = Field(None, description="行权价")
    call_symbol: Optional[str] = Field(None, description="看涨合约-标识")
    put_bid_volume: Optional[int] = Field(None, description="看跌合约-买量")
    put_bid_price: Optional[float] = Field(None, description="看跌合约-买价")
    put_last_price: Optional[float] = Field(None, description="看跌合约-最新价")
    put_ask_price: Optional[float] = Field(None, description="看跌合约-卖价")
    put_ask_volume: Optional[int] = Field(None, description="看跌合约-卖量")
    put_open_interest: Optional[int] = Field(None, description="看跌合约-持仓量")
    put_change: Optional[float] = Field(None, description="看跌合约-涨跌")
    put_symbol: Optional[str] = Field(None, description="看跌合约-标识")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexSz50DailySina(BaseModel):
    """
    中金所上证50指数指定合约日频行情
    Collection: option_cffex_sz50_daily_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    date: Optional[str] = Field(None, description="日期")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexHs300DailySina(BaseModel):
    """
    中金所沪深300指数指定合约日频行情
    Collection: option_cffex_hs300_daily_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    date: Optional[str] = Field(None, description="日期")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCffexZz1000DailySina(BaseModel):
    """
    中金所中证1000指数指定合约日频行情
    Collection: option_cffex_zz1000_daily_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    date: Optional[str] = Field(None, description="日期")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseListSina(BaseModel):
    """
    上交所50ETF/300ETF合约到期月份列表
    Collection: option_sse_list_sina
    """
    symbol: Optional[str] = Field(None, description="品种代码")
    month: Optional[str] = Field(None, description="到期月份")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseExpireDaySina(BaseModel):
    """
    指定到期月份指定品种的剩余到期时间
    Collection: option_sse_expire_day_sina
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="品种代码")
    expire_days: Optional[int] = Field(None, description="剩余到期天数")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseCodesSina(BaseModel):
    """
    新浪期权看涨看跌合约合约的代码
    Collection: option_sse_codes_sina
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="品种代码")
    contract_code: Optional[str] = Field(None, description="合约代码")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCurrentEm(BaseModel):
    """
    期权实时数据
    Collection: option_current_em
    """
    code: Optional[str] = Field(None, description="代码")
    name: Optional[str] = Field(None, description="名称")
    trade_date: Optional[str] = Field(None, description="交易日")
    settlement_price: Optional[float] = Field(None, description="结算价")
    latest_price: Optional[float] = Field(None, description="最新价")
    change_pct: Optional[float] = Field(None, description="涨跌幅")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseUnderlyingSpotPriceSina(BaseModel):
    """
    期权标的物的实时数据
    Collection: option_sse_underlying_spot_price_sina
    """
    symbol: Optional[str] = Field(None, description="标的物代码")
    field: Optional[str] = Field(None, description="字段")
    value: Optional[str] = Field(None, description="值")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseGreeksSina(BaseModel):
    """
    新浪财经期权希腊字母信息表
    Collection: option_sse_greeks_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    delta: Optional[float] = Field(None, description="Delta")
    gamma: Optional[float] = Field(None, description="Gamma")
    theta: Optional[float] = Field(None, description="Theta")
    vega: Optional[float] = Field(None, description="Vega")
    rho: Optional[float] = Field(None, description="Rho")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseMinuteSina(BaseModel):
    """
    期权行情分钟数据
    Collection: option_sse_minute_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    datetime: Optional[str] = Field(None, description="日期时间")
    price: Optional[float] = Field(None, description="价格")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionSseDailySina(BaseModel):
    """
    期权行情日数据
    Collection: option_sse_daily_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    date: Optional[str] = Field(None, description="日期")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionFinanceMinuteSina(BaseModel):
    """
    新浪财经金融期权股票期权分时行情数据
    Collection: option_finance_minute_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    date: Optional[str] = Field(None, description="日期")
    time: Optional[str] = Field(None, description="时间")
    price: Optional[float] = Field(None, description="价格")
    average_price: Optional[float] = Field(None, description="均价")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionMinuteEm(BaseModel):
    """
    东方财富网行情中心期权市场分时行情
    Collection: option_minute_em
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    datetime: Optional[str] = Field(None, description="日期时间")
    price: Optional[float] = Field(None, description="价格")
    volume: Optional[int] = Field(None, description="成交量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionLhbEm(BaseModel):
    """
    东方财富网期权龙虎榜单金融期权
    Collection: option_lhb_em
    """
    rank: Optional[int] = Field(None, description="排名")
    code: Optional[str] = Field(None, description="代码")
    name: Optional[str] = Field(None, description="名称")
    latest_price: Optional[float] = Field(None, description="最新价")
    change_pct: Optional[float] = Field(None, description="涨跌幅")
    volume: Optional[int] = Field(None, description="成交量")
    turnover: Optional[float] = Field(None, description="成交额")
    amplitude: Optional[float] = Field(None, description="振幅")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionValueAnalysisEm(BaseModel):
    """
    东方财富网期权价值分析
    Collection: option_value_analysis_em
    """
    code: Optional[str] = Field(None, description="代码")
    name: Optional[str] = Field(None, description="名称")
    latest_price: Optional[float] = Field(None, description="最新价")
    intrinsic_value: Optional[float] = Field(None, description="内在价值")
    time_value: Optional[float] = Field(None, description="时间价值")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionRiskAnalysisEm(BaseModel):
    """
    东方财富网期权风险分析
    Collection: option_risk_analysis_em
    """
    code: Optional[str] = Field(None, description="代码")
    name: Optional[str] = Field(None, description="名称")
    leverage_ratio: Optional[float] = Field(None, description="杠杆比率")
    delta: Optional[float] = Field(None, description="Delta")
    gamma: Optional[float] = Field(None, description="Gamma")
    theta: Optional[float] = Field(None, description="Theta")
    vega: Optional[float] = Field(None, description="Vega")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionPremiumAnalysisEm(BaseModel):
    """
    东方财富网期权折溢价
    Collection: option_premium_analysis_em
    """
    code: Optional[str] = Field(None, description="代码")
    name: Optional[str] = Field(None, description="名称")
    premium_rate: Optional[float] = Field(None, description="溢价率")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCommodityContractSina(BaseModel):
    """
    新浪财经商品期权当前在交易的合约
    Collection: option_commodity_contract_sina
    """
    symbol: Optional[str] = Field(None, description="品种代码")
    contract: Optional[str] = Field(None, description="合约代码")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCommodityContractTableSina(BaseModel):
    """
    新浪财经商品期权T型报价表
    Collection: option_commodity_contract_table_sina
    """
    symbol: Optional[str] = Field(None, description="品种代码")
    contract: Optional[str] = Field(None, description="合约代码")
    call_code: Optional[str] = Field(None, description="看涨代码")
    call_price: Optional[float] = Field(None, description="看涨价格")
    strike_price: Optional[float] = Field(None, description="行权价")
    put_code: Optional[str] = Field(None, description="看跌代码")
    put_price: Optional[float] = Field(None, description="看跌价格")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCommodityHistSina(BaseModel):
    """
    新浪财经商品期权历史行情数据
    Collection: option_commodity_hist_sina
    """
    symbol: Optional[str] = Field(None, description="合约代码")
    date: Optional[str] = Field(None, description="日期")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCommInfo(BaseModel):
    """
    九期网商品期权手续费数据
    Collection: option_comm_info
    """
    exchange: Optional[str] = Field(None, description="交易所")
    symbol: Optional[str] = Field(None, description="品种")
    fee_type: Optional[str] = Field(None, description="手续费类型")
    fee_rate: Optional[str] = Field(None, description="手续费率")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionMargin(BaseModel):
    """
    唯爱期货期权保证金
    Collection: option_margin
    """
    exchange: Optional[str] = Field(None, description="交易所")
    symbol: Optional[str] = Field(None, description="品种")
    margin_rate: Optional[str] = Field(None, description="保证金率")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionHistShfe(BaseModel):
    """
    上海期货交易所商品期权数据
    Collection: option_hist_shfe
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="合约代码")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionHistDce(BaseModel):
    """
    大连商品交易所商品期权数据
    Collection: option_hist_dce
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="合约代码")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionHistCzce(BaseModel):
    """
    郑州商品交易所商品期权数据
    Collection: option_hist_czce
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="合约代码")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionHistGfex(BaseModel):
    """
    广州期货交易所商品期权数据
    Collection: option_hist_gfex
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="合约代码")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionVolGfex(BaseModel):
    """
    广州期货交易所商品期权隐含波动率
    Collection: option_vol_gfex
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="品种代码")
    implied_volatility: Optional[float] = Field(None, description="隐含波动率")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class OptionCzceHist(BaseModel):
    """
    郑州商品交易所商品期权历史行情
    Collection: option_czce_hist
    """
    trade_date: Optional[str] = Field(None, description="交易日期")
    symbol: Optional[str] = Field(None, description="合约代码")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    close: Optional[float] = Field(None, description="收盘价")
    volume: Optional[int] = Field(None, description="成交量")
    open_interest: Optional[int] = Field(None, description="持仓量")
    
    updated_at: Optional[datetime] = Field(None, description="更新时间")

