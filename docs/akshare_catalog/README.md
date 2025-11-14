# AKShare 数据字典本地镜像与离线索引

本目录用于保存 AKShare 官方文档“数据字典”（https://akshare.akfamily.xyz/data/index.html）的本地快照与结构化索引，按资产种类与接口划分，便于后续离线查阅与调用映射。

## 目录结构

- index.json
  - 总索引（抓取时间、来源 URL、页面清单、函数与资产类映射、统计信息）
- endpoints_flat.json
  - 扁平化的函数 -> 元数据映射（便于快速查询）
- raw_html/
  - 文档页面原始 HTML 快照（以 slug 命名）
- assets/
  - equity_cn/ | equity_hk/ | equity_us/
  - fund_cn/
  - index_cn/ | index_global/
  - futures_cn/
  - bond_cn/
  - macro/ | forex/ | crypto/ | options_cn/ | others/
  - 每个资产类目录下：
    - endpoints/<function_name>.json  按函数维度保存结构化信息
    - endpoints/<function_name>.md    可选的 Markdown 摘要（后续扩展）
- schema.endpoint.json
  - endpoint JSON 的结构说明（JSON Schema）

## endpoint JSON 字段约定

参见 schema.endpoint.json，核心字段：
- asset_class: 资产类（如 equity_cn/fund_cn/index_cn/index_global/futures_cn/bond_cn 等）
- source: 固定为 "akshare"
- endpoint_name: 函数名（如 stock_zh_a_hist）
- title: 文档页面标题
- category: 文档分类路径（若可解析）
- doc_url: 官方文档 URL
- description: 文本描述（若可解析）
- parameters: 参数数组（name/type/required/default/choices/description，若可解析）
- return_schema: 返回结构（DataFrame 列或字段列表，若可解析）
- examples: 代码示例（若可解析）
- tags: 标签列表
- last_crawled: 抓取时间（ISO8601）
- version_hint: 文档或页面中的版本提示（若存在）
- notes: 其他备注
- raw_html_file: 对应 raw_html 的相对路径

## 同步脚本

使用 scripts/sync_akshare_catalog.py 进行抓取与解析。

### 安装依赖

```bash
pip install requests beautifulsoup4
```

### 用法示例（Windows PowerShell）

```powershell
python scripts/sync_akshare_catalog.py `
  --base-url https://akshare.akfamily.xyz/data/index.html `
  --out docs/akshare_catalog `
  --max-workers 8 `
  --max-pages 2000 `
  --overwrite
```

可选参数：
- --asset-classes equity_cn,fund_cn,index_cn,index_global,futures_cn,bond_cn
- --include-raw-html true|false
- 代理：通过环境变量 HTTP_PROXY/HTTPS_PROXY 配置。

## 离线读取示例

```python
import json, pathlib
root = pathlib.Path('docs/akshare_catalog')
index = json.loads((root/'endpoints_flat.json').read_text(encoding='utf-8'))
fn = 'stock_zh_a_hist'
meta = index.get(fn)
print(meta['asset_class'], meta['doc_url'])
```

## 解析策略说明

- 首先下载 "data/index.html" 并在同域下递归发现位于 /data/ 路径下的链接（限制深度与数量）。
- 对每个页面：
  - 保存原始 HTML
  - 通过正则提取 `ak.<function>` 出现的函数名
  - 尝试解析“参数/返回字段”的表格（若存在），失败则留空占位
  - 通过函数前缀推断资产类（stock_* → equity_cn/hk/us；fund_* → fund_cn；index_* → index_cn/global；futures_* → futures_cn；bond_* → bond_cn；其余划到 macro/forex/crypto/options_cn/others）
- 以函数为粒度生成 endpoints/<function>.json，并生成扁平索引 endpoints_flat.json

## 注意事项

- AKShare 文档结构可能变化，解析器做了容错；若页面结构与预期不符，依然会保留原始 HTML 与最小元数据（标题、URL、函数名列表）。
- 如需严格的“时间窗口、字段精确类型”，建议在本地补充人工校验或针对重点接口定制解析器。
- 抓取频率请合理控制，避免给官方文档服务器带来压力。
