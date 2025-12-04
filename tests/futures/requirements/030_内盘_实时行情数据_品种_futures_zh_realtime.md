### 背景
内盘-实时行情数据(品种)

### 任务


参考docs/数据集合实现指南.md中数据集合的实现方法和funds中的数据集合的实现，为futures实现相应的数据集合

### 测试驱动
1. 需要认真思考研究债券数据集合bond_info_cm和基金数据集合的前端界面和后端实现的功能，结合该接口的字段，思考需要实现哪些功能，先写具体的测试用例
2. 测试用例文件：`tests/futures/collections/030_futures_zh_realtime_collection.py`
3. 开发实现相应的前端和后端功能
4. 运行测试，修复测试失败的问题

### 验收标准
1. 测试用例能够全部通过
2. 手动点击没有异常情况
3. 数据能够正确获取、存储和展示
4. 页面美观、交互流畅

### 获取数据的API接口、字段等

#### 内盘-实时行情数据(品种)

**接口**: `futures_zh_realtime`

**目标地址**: https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1

**描述**: 新浪财经-期货实时行情数据

**限量**: 单次返回指定 symbol 的数据

**输入参数**

| 名称     | 类型  | 描述                                                        |
|--------|-----|-----------------------------------------------------------|
| symbol | str | symbol="白糖", 品种名称；可以通过 ak.futures_symbol_mark() 获取所有品种命名表 |

**输出参数**

| 名称             | 类型      | 描述     |
|----------------|---------|--------|
| symbol         | object  | 合约代码   |
| exchange       | object  | 交易所    |
| name           | object  | 合约中文名称 |
| trade          | float64 | 最新价    |
| settlement     | float64 | 动态结算   |
| presettlement  | float64 | 昨日结算   |
| open           | float64 | 今开     |
| high           | float64 | 最高     |
| low            | float64 | 最低     |
| close          | float64 | 收盘     |
| bidprice1      | float64 | 买入     |
| askprice1      | float64 | 卖出     |
| bidvol1        | int64   | 买量     |
| askvol1        | int64   | 卖量     |
| volume         | int64   | 成交量    |
| position       | int64   | 持仓量    |
| ticktime       | object  | 时间     |
| tradedate      | object  | 日期     |
| preclose       | float64 | 前收盘价   |
| changepercent  | float64 | 涨跌幅    |
| bid            | float64 | -      |
| ask            | float64 | -      |
| prevsettlement | float64 | 前结算价   |

### 实现要点

1. **后端实现**：
   - 实现数据获取、存储、更新逻辑
   - 实现文件导入和远程同步功能
   - 注意API调用频率控制

2. **前端实现**：
   - 参考现有集合的布局
   - 实现数据概览、列表、更新等组件
   - 增加适当的数据可视化

3. **注意事项**：
   - 数据验证和清洗
   - 错误处理和日志记录
   - 性能优化（批量操作、索引等）
