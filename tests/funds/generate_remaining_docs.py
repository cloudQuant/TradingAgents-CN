#!/usr/bin/env python3
"""
批量生成基金需求文档的脚本
基于 _sources_data_fund_fund_public.md.txt.html 中的接口信息
"""

# 定义所有需要生成的文档信息
docs_info = [
    # 基金排行类
    {
        "num": 31,
        "name": "场内交易基金排行-东财",
        "collection": "fund_exchange_rank_em",
        "api": "fund_exchange_rank_em",
        "url": "https://fund.eastmoney.com/data/fbsfundranking.html",
        "desc": "东方财富网-数据中心-场内交易基金排行榜",
        "limit": "单次返回当前时刻所有数据, 每个交易日 17 点后更新",
        "input_params": "无",
        "output_fields": "序号, 基金代码, 基金简称, 类型, 日期, 单位净值, 累计净值, 近1周, 近1月, 近3月, 近6月, 近1年, 近2年, 近3年, 今年来, 成立来, 成立日期",
        "unique_key": "基金代码和日期",
        "update_mode": "文件导入、远程同步、更新"
    },
    {
        "num": 32,
        "name": "货币型基金排行-东财",
        "collection": "fund_money_rank_em",
        "api": "fund_money_rank_em",
        "url": "https://fund.eastmoney.com/data/hbxfundranking.html",
        "desc": "东方财富网-数据中心-货币型基金排行",
        "limit": "单次返回当前时刻所有数据, 每个交易日 17 点后更新",
        "input_params": "无",
        "output_fields": "序号, 基金代码, 基金简称, 日期, 万份收益, 年化收益率7日, 年化收益率14日, 年化收益率28日, 近1月, 近3月, 近6月, 近1年, 近2年, 近3年, 近5年, 今年来, 成立来, 手续费",
        "unique_key": "基金代码和日期",
        "update_mode": "文件导入、远程同步、更新"
    },
    {
        "num": 33,
        "name": "理财基金排行-东财",
        "collection": "fund_lcx_rank_em",
        "api": "fund_lcx_rank_em",
        "url": "https://fund.eastmoney.com/data/lcxfundranking.html",
        "desc": "东方财富网-数据中心-理财基金排行",
        "limit": "由于目标网站没有数据，该接口暂时未能返回数据",
        "input_params": "无",
        "output_fields": "序号, 基金代码, 基金简称, 日期, 万份收益, 年化收益率7日, 年化收益率14日, 年化收益率28日, 近1周, 近1月, 近3月, 近6月, 今年来, 成立来, 可购买, 手续费",
        "unique_key": "基金代码和日期",
        "update_mode": "文件导入、远程同步、更新"
    },
    {
        "num": 34,
        "name": "香港基金排行-东财",
        "collection": "fund_hk_rank_em",
        "api": "fund_hk_rank_em",
        "url": "https://overseas.1234567.com.cn/FundList",
        "desc": "东方财富网-数据中心-基金排行-香港基金排行",
        "limit": "单次返回当前时刻所有数据",
        "input_params": "无",
        "output_fields": "序号, 基金代码, 基金简称, 币种, 日期, 单位净值, 日增长率, 近1周, 近1月, 近3月, 近6月, 近1年, 近2年, 近3年, 今年来, 成立来, 可购买, 香港基金代码",
        "unique_key": "基金代码和日期",
        "update_mode": "文件导入、远程同步、更新"
    },
    # 基金分析类
    {
        "num": 36,
        "name": "净值估算-东财",
        "collection": "fund_value_estimation_em",
        "api": "fund_value_estimation_em",
        "url": "http://fund.eastmoney.com/fundguzhi.html",
        "desc": "东方财富网-数据中心-净值估算",
        "limit": "单次返回当前交易日指定 symbol 的所有数据",
        "input_params": "symbol (基金类型): 全部, 股票型, 混合型, 债券型, 指数型, QDII, ETF联接, LOF, 场内交易基金",
        "output_fields": "序号, 基金代码, 基金名称, 交易日-估算数据-估算值, 交易日-估算数据-估算增长率, 交易日-公布数据-单位净值, 交易日-公布数据-日增长率, 估算偏差, 交易日-单位净值",
        "unique_key": "基金代码和交易日",
        "update_mode": "文件导入、远程同步、单个更新、批量更新"
    },
    {
        "num": 37,
        "name": "基金数据分析-雪球",
        "collection": "fund_individual_analysis_xq",
        "api": "fund_individual_analysis_xq",
        "url": "https://danjuanfunds.com/funding/000001",
        "desc": "雪球基金-基金详情-数据分析",
        "limit": "返回单只基金历史表现分析数据",
        "input_params": "symbol (基金代码), timeout (超时参数)",
        "output_fields": "周期, 较同类风险收益比, 较同类抗风险波动, 年化波动率, 年化夏普比率, 最大回撤",
        "unique_key": "基金代码和周期",
        "update_mode": "文件导入、远程同步、单个更新、批量更新"
    },
    {
        "num": 38,
        "name": "基金盈利概率-雪球",
        "collection": "fund_individual_profit_probability_xq",
        "api": "fund_individual_profit_probability_xq",
        "url": "https://danjuanfunds.com/funding/000001",
        "desc": "雪球基金-基金详情-盈利概率",
        "limit": "单次返回单只基金历史任意时点买入，持有满 X 时间，盈利概率，以及平均收益",
        "input_params": "symbol (基金代码), timeout (超时参数)",
        "output_fields": "持有时长, 盈利概率, 平均收益",
        "unique_key": "基金代码和持有时长",
        "update_mode": "文件导入、远程同步、单个更新、批量更新"
    },
    {
        "num": 39,
        "name": "基金持仓资产比例-雪球",
        "collection": "fund_individual_detail_hold_xq",
        "api": "fund_individual_detail_hold_xq",
        "url": "https://danjuanfunds.com/rn/fund-detail/archive?id=103&code=000001",
        "desc": "雪球基金-基金详情-基金持仓-详情",
        "limit": "单次返回单只基金指定日期的持仓大类资产比例",
        "input_params": "symbol (基金代码), date (季度日期), timeout (超时参数)",
        "output_fields": "资产类型, 仓位占比",
        "unique_key": "基金代码、日期和资产类型",
        "update_mode": "文件导入、远程同步、单个更新、批量更新"
    },
    # 更多文档信息...
]

# 文档模板
TEMPLATE = """### 背景
基金数据信息还不完善，继续补充基金的数据。

### 任务

参考债券数据集合bond_info_cm的前端界面和后端实现的功能，参考下面获取数据的API接口和字段，获取信息,更新到对应的数据集合中。

### 步骤
1. 数据集合：创建一个新的数据集合，名称为{name}
2. 页面里面需要包含数据概览、数据列表、刷新、清空数据、更新数据等功能、根据后端获取到的数据和数据列表里面的数据，增加一些基本的图形展示，让整个页面更加美观
3. 更新数据这个功能需要支持{update_mode}等功能。这个数据集合以{unique_key}作为唯一标识，更新数据的时候，如果存在重复记录，需要更新数据，否则需要插入数据。

### 测试驱动
1. 需要认真思考研究债券数据集合bond_info_cm的前端界面和后端实现的功能，结合{name}的API接口和字段，思考需要实现哪些功能，先写具体的测试用例，网页的测试用例可以基于selenium或者playwright来实现
2. 开发实现相应的前端和后端功能
3. 运行测试，修复测试失败的问题

### 验收标准
1. 测试用例能够全部通过
2. 手动点击没有异常情况

### 获取数据的API接口、字段等

{name}
接口: {api}

目标地址: {url}

描述: {desc}

限量: {limit}

输入参数: {input_params}

输出参数: {output_fields}

接口示例

```python
import akshare as ak

{collection}_df = ak.{api}()
print({collection}_df)
```
"""

def generate_doc(info):
    """生成单个需求文档"""
    content = TEMPLATE.format(**info)
    filename = f"{info['num']:02d}_{info['name']}.md"
    filepath = f"/Users/yunjinqi/Documents/TradingAgents-CN/tests/funds/{filename}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    print("开始批量生成需求文档...")
    for info in docs_info:
        generate_doc(info)
    print(f"\n✅ 共生成 {len(docs_info)} 个需求文档")
