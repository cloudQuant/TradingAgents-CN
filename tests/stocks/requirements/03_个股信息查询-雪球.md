### 背景
在个股信息查询-东财数据集合中获取了股票的基本信息，但信息不够完整详细。雪球网提供了更详细的公司概况信息，需要补充。

### 任务

参考债券数据集合bond_info_cm和基金数据集合fund_basic_info的前端界面和后端实现的功能，从个股信息查询-东财数据集合中获取股票代码，参考下面获取数据的API接口和字段，获取雪球股票详细信息，建立新的数据集合。

### 步骤
1. 数据集合：创建一个新的数据集合，名称为**个股信息查询-雪球** (http://localhost:3000/stocks/collections/stock_individual_basic_info_xq)
2. 页面里面需要包含数据概览、数据列表、刷新、清空数据、更新数据等功能，根据后端获取到的数据和数据列表里面的数据，增加一些基本的图形展示，让整个页面更加美观
3. 更新数据这个功能需要支持：
   - **文件导入**：支持CSV/Excel文件导入
   - **远程同步**：从其他数据库同步数据
   - **批量更新**：从个股信息查询-东财获取股票代码列表，批量获取雪球信息
   - **单个更新**：输入股票代码，单独更新某只股票的雪球信息
4. 数据唯一标识：以**股票代码**作为唯一标识，更新数据时，如果存在重复的股票代码，需要更新数据，否则需要插入数据

### 测试驱动
1. 需要认真思考研究债券数据集合bond_info_cm和基金数据集合fund_basic_info的前端界面和后端实现的功能，结合雪球个股信息查询的API接口和字段，思考需要实现哪些功能，先写具体的测试用例，网页的测试用例可以基于selenium或者playwright来实现
2. 测试用例文件：`tests/stocks/collections/02_stock_individual_basic_info_xq_collection.py`
3. 开发实现相应的前端和后端功能
4. 运行测试，修复测试失败的问题

### 验收标准
1. 测试用例能够全部通过
2. 手动点击没有异常情况
3. 数据能够正确获取、存储和展示
4. 页面美观、交互流畅
5. 批量更新功能能够正常运行，支持并发控制和进度显示

### 获取数据的API接口、字段等

#### 个股信息查询-雪球

**接口**: `stock_individual_basic_info_xq`

**目标地址**: https://xueqiu.com/snowman/S/SH601127/detail#/GSJJ

**描述**: 雪球财经-个股-公司概况-公司简介

**限量**: 单次返回指定 symbol 的个股详细信息

**输入参数**

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="SH601127"; 股票代码，注意需要带市场前缀(SH/SZ) |
| token   | str   | token=None;             |
| timeout | float | timeout=None; 默认不设置超时参数 |

**输出参数**

| 名称    | 类型     | 描述  |
|-------|--------|-----|
| item  | object | 字段名 |
| value | object | 字段值 |

**接口示例**

```python
import akshare as ak

stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SH601127")
print(stock_individual_basic_info_xq_df)
```

**数据示例**

```
                            item                                              value
0                         org_id                                         T000071215
1                    org_name_cn                                        赛力斯集团股份有限公司
2              org_short_name_cn                                                赛力斯
3                    org_name_en                               Seres Group Co.,Ltd.
4              org_short_name_en                                              SERES
5        main_operation_business      新能源汽车及核心三电(电池、电驱、电控)、传统汽车及核心部件总成的研发、制造、销售及服务。
6                operating_scope  　　一般项目：制造、销售：汽车零部件、机动车辆零部件、普通机械、电器机械、电器、电子产品（不...
7                district_encode                                             500106
8            org_cn_introduction  赛力斯始创于1986年，是以新能源汽车为核心业务的技术科技型汽车企业。现有员工1.6万人，A...
9           legal_representative                                                张正萍
10               general_manager                                                张正萍
11                     secretary                                                 申薇
12              established_date                                      1178812800000
13                     reg_asset                                       1509782193.0
14                     staff_num                                              16102
15                     telephone                                     86-23-65179666
16                      postcode                                             401335
17                           fax                                     86-23-65179777
18                         email                                    601127@seres.cn
19                   org_website                                   www.seres.com.cn
20                reg_address_cn                                      重庆市沙坪坝区五云湖路7号
21                reg_address_en                                               None
22             office_address_cn                                      重庆市沙坪坝区五云湖路7号
23             office_address_en                                               None
24               currency_encode                                             019001
25                      currency                                                CNY
26                   listed_date                                      1465920000000
27               provincial_name                                                重庆市
28             actual_controller                                       张兴海 (13.79%)
29                   classi_name                                               民营企业
30                   pre_name_cn                                     重庆小康工业集团股份有限公司
31                      chairman                                                张正萍
32               executives_nums                                                 20
33              actual_issue_vol                                        142500000.0
34                   issue_price                                               5.81
35             actual_rc_net_amt                                        738451000.0
36              pe_after_issuing                                              18.19
37  online_success_rate_of_issue                                           0.110176
38            affiliate_industry         {'ind_code': 'BK0025', 'ind_name': '汽车整车'}
```

### 实现要点

1. **后端实现**：
   - 扩展 `StockDataService` 服务类
   - 实现雪球数据获取、存储、更新逻辑
   - 实现股票代码转换（添加市场前缀：SH/SZ/BJ）
   - 实现批量获取（从个股信息查询-东财获取股票代码列表）
   - 实现并发控制（避免被限流）
   - 实现文件导入和远程同步功能

2. **前端实现**：
   - 参考 `Funds/Collection.vue` 的布局
   - 实现数据概览组件（显示总数、最近更新时间等）
   - 实现数据列表组件（支持分页、排序、筛选）
   - 实现更新数据组件：
     - 文件导入
     - 远程同步
     - 批量更新（配置批量大小、并发数、延迟时间）
     - 单个更新
   - 增加数据可视化（如：地区分布、企业类型分布等）

3. **数据模型**：
   ```python
   {
       "股票代码": str,
       "机构ID": str,
       "公司中文名": str,
       "公司简称": str,
       "公司英文名": str,
       "英文简称": str,
       "主营业务": str,
       "经营范围": str,
       "公司简介": str,
       "法定代表人": str,
       "总经理": str,
       "董事会秘书": str,
       "成立日期": str,
       "注册资本": float,
       "员工人数": int,
       "联系电话": str,
       "邮政编码": str,
       "传真": str,
       "电子邮箱": str,
       "公司网站": str,
       "注册地址": str,
       "办公地址": str,
       "货币": str,
       "上市日期": str,
       "所在省份": str,
       "实际控制人": str,
       "企业性质": str,
       "曾用名": str,
       "董事长": str,
       "高管人数": int,
       "发行量": float,
       "发行价": float,
       "募集资金": float,
       "所属行业": str,
       "更新时间": datetime
   }
   ```

4. **注意事项**：
   - 雪球API需要注意股票代码格式（需要带市场前缀）
   - 股票代码转换规则：
     - 60开头 → SH（上海主板）
     - 68开头 → SH（科创板）
     - 00开头 → SZ（深圳主板）
     - 30开头 → SZ（创业板）
     - 43/83/87/88开头 → BJ（北京）
   - API调用需要控制频率，建议每次请求间隔1-2秒
   - 批量更新时需要显示进度和剩余时间
   - 错误处理：网络异常、API限流、数据格式异常等
   - 数据验证和清洗

5. **批量更新配置**：
   - 批量大小：建议100-500只股票为一批
   - 并发数：建议1-3（避免被限流）
   - 延迟时间：建议1-2秒/次

### 扩展功能（可选）

1. 支持按地区、企业类型等条件筛选
2. 支持数据对比功能（对比东财和雪球的数据差异）
3. 支持关键字搜索（公司名称、实际控制人等）
4. 支持数据导出功能
5. 支持历史变更记录查看（如：公司改名、实际控制人变更等）
