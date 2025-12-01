import pandas as pd

# 创建示例DataFrame，基于用户提供的数据
data = {
    'item': ['基金代码', '基金名称', '基金全称', '成立时间', '最新规模', '基金公司', '基金经理', '托管银行', '基金类型', '评级机构', '基金评级', '投资策略', '投资目标', '业绩比较基准'],
    'value': ['000001', '华夏成长混合', '华夏成长前收费', '2001-12-18', '27.30亿', '华夏基金管理有限公司', '王泽实 万方方', '中国建设银行股份有限公司', '混合型-偏股', '晨星评级', '一星基金', '在股票投资方面，本基金重点投资于预期利润或收入具有良好增长潜力的成长型上市公司发行的股票，从而分享中国经济增长成果。', '本基金属成长型基金，主要通过投资于具有良好成长性的上市公司的股票，在保持基金资产安全性和流动性的前提下，实现基金的长期资本增值。', '本基金暂不设业绩比较基准']
}
df = pd.DataFrame(data)

print("原始DataFrame:")
print(df)

# 添加常量列作为行标识符，确保pivot操作生成单行数据
df['constant'] = 0

# 使用pivot进行转换：以constant为索引，item值为列名，value为数据
pivot_df = df.pivot(index='constant', columns='item', values='value').reset_index(drop=True)

print("\n转换后的DataFrame:")
print(pivot_df)