# 股票代码格式验证功能

## 功能概述

在单股分析页面添加了前端股票代码格式验证功能，支持 A 股、美股、港股三种市场的代码格式验证和自动识别。

## 支持的市场格式

### 1. A 股市场 🇨🇳

- *格式**：6 位数字

- *支持的前缀**：
- `60xxxx` - 上海主板（如：600519 贵州茅台）
- `68xxxx` - 科创板（如：688981 中芯国际）
- `00xxxx` - 深圳主板（如：000001 平安银行）
- `30xxxx` - 创业板（如：300750 宁德时代）
- `43xxxx` - 北交所
- `83xxxx` - 北交所
- `87xxxx` - 北交所

- *示例**：

```bash
000001  ✓ 平安银行
600519  ✓ 贵州茅台
000858  ✓ 五粮液
300750  ✓ 宁德时代

```bash

- *错误示例**：

```bash
00001   ✗ 只有 5 位数字
1234567 ✗ 超过 6 位数字
50xxxx  ✗ 前缀不正确

```bash

### 2. 美股市场 🇺🇸

- *格式**：1-5 个大写字母，可能包含一个点号

- *特点**：
- 大小写不敏感（自动转换为大写）
- 支持带点号的代码（如：BRK.B）

- *示例**：

```bash
AAPL    ✓ 苹果
MSFT    ✓ 微软
GOOGL   ✓ 谷歌
TSLA    ✓ 特斯拉
BRK.B   ✓ 伯克希尔 B 股

```bash

- *错误示例**：

```bash
ABCDEF  ✗ 超过 5 个字母
123     ✗ 纯数字
A.B.C   ✗ 多个点号

```bash

### 3. 港股市场 🇭🇰

- *格式**：1-5 位数字

- *特点**：
- 自动补齐前导 0（如：700 → 00700）
- 支持带前导 0 和不带前导 0 的格式

- *示例**：

```bash
00700   ✓ 腾讯控股
09988   ✓ 阿里巴巴
01810   ✓ 小米集团
03690   ✓ 美团
700     ✓ 腾讯控股（自动补齐为 00700）
9988    ✓ 阿里巴巴（自动补齐为 09988）

```bash

- *错误示例**：

```bash
123456  ✗ 超过 5 位数字
0       ✗ 无效代码

```bash

## 功能特性

### 1. 实时验证

- **输入时提示**：输入股票代码时显示格式提示
- **失焦验证**：离开输入框时自动验证格式
- **即时反馈**：显示错误信息或成功提示

### 2. 自动识别

系统会根据输入的代码格式自动识别市场类型：

```typescript
// 6 位数字 → A 股
000001 → 自动识别为 A 股

// 1-5 个字母 → 美股
AAPL → 自动识别为 美股

// 1-5 位数字（非 6 位）→ 港股
700 → 自动识别为 港股

```bash

### 3. 代码标准化

- **A 股**：保持 6 位数字格式
- **美股**：自动转换为大写
- **港股**：自动补齐前导 0 至 5 位

### 4. 市场切换验证

当用户切换市场类型时，系统会自动重新验证已输入的股票代码，确保代码与市场类型匹配。

## 用户界面

### 输入框增强

```vue
<el-input
  v-model="analysisForm.stockCode"
  placeholder="如：000001、AAPL、00700"
  clearable
  size="large"
  class="stock-input"
  :class="{ 'is-error': stockCodeError }"
  @blur="validateStockCodeInput"
  @input="onStockCodeInput"
>
  <template #prefix>
    <el-icon><TrendCharts /></el-icon>
  </template>
</el-input>

```bash

### 错误提示

```vue
<div v-if="stockCodeError" class="error-message">
  <el-icon><WarningFilled /></el-icon>
  {{ stockCodeError }}
</div>

```bash

### 成功提示

```vue
<div v-else-if="stockCodeHelp" class="help-message">
  <el-icon><InfoFilled /></el-icon>
  {{ stockCodeHelp }}
</div>

```bash

### 市场选择器增强

```vue
<el-select v-model="analysisForm.market" @change="onMarketChange">
  <el-option label="🇨🇳 A 股市场" value="A 股">
    <span>🇨🇳 A 股市场</span>
    <span style="color: #909399; font-size: 12px;">（6 位数字）</span>
  </el-option>
  <el-option label="🇺🇸 美股市场" value="美股">
    <span>🇺🇸 美股市场</span>
    <span style="color: #909399; font-size: 12px;">（1-5 个字母）</span>
  </el-option>
  <el-option label="🇭🇰 港股市场" value="港股">
    <span>🇭🇰 港股市场</span>
    <span style="color: #909399; font-size: 12px;">（1-5 位数字）</span>
  </el-option>
</el-select>

```bash

## 技术实现

### 核心工具函数

- *文件**：`frontend/src/utils/stockValidator.ts`

#### 1. `validateAStock(code: string)`

验证 A 股代码格式

```typescript
export function validateAStock(code: string): StockValidationResult {
  const cleanCode = code.trim().replace(/[^0-9]/g, '')

  if (!/^\d{6}$/.test(cleanCode)) {
    return { valid: false, message: 'A 股代码必须是 6 位数字' }
  }

  const prefix = cleanCode.substring(0, 2)
  const validPrefixes = ['60', '68', '00', '30', '43', '83', '87']

  if (!validPrefixes.includes(prefix)) {
    return { valid: false, message: 'A 股代码前缀不正确' }
  }

  return { valid: true, market: 'A 股', normalizedCode: cleanCode }
}

```bash

#### 2. `validateUSStock(code: string)`

验证美股代码格式

```typescript
export function validateUSStock(code: string): StockValidationResult {
  const cleanCode = code.trim().toUpperCase().replace(/[^A-Z.]/g, '')

  if (!/^[A-Z]{1,5}(\.[A-Z])?$/.test(cleanCode)) {
    return { valid: false, message: '美股代码格式不正确' }
  }

  return { valid: true, market: '美股', normalizedCode: cleanCode }
}

```bash

#### 3. `validateHKStock(code: string)`

验证港股代码格式

```typescript
export function validateHKStock(code: string): StockValidationResult {
  const cleanCode = code.trim().replace(/[^0-9]/g, '')

  if (!/^\d{1,5}$/.test(cleanCode)) {
    return { valid: false, message: '港股代码必须是 1-5 位数字' }
  }

  const normalizedCode = cleanCode.padStart(5, '0')

  return { valid: true, market: '港股', normalizedCode: normalizedCode }
}

```bash

#### 4. `validateStockCode(code: string, marketHint?: string)`

自动识别并验证股票代码

```typescript
export function validateStockCode(
  code: string,
  marketHint?: 'A 股' | '美股' | '港股'

): StockValidationResult {
  if (!code || !code.trim()) {

    return { valid: false, message: '请输入股票代码' }
  }

  // 如果提供了市场提示，优先验证该市场
  if (marketHint) {
    switch (marketHint) {
      case 'A 股': return validateAStock(code)
      case '美股': return validateUSStock(code)
      case '港股': return validateHKStock(code)
    }
  }

  // 自动识别市场类型
  // ...
}

```bash

### Vue 组件集成

- *文件**：`frontend/src/views/Analysis/SingleAnalysis.vue`

#### 响应式状态

```typescript
// 股票代码验证相关
const stockCodeError = ref<string>('')
const stockCodeHelp = ref<string>('')

```bash

#### 事件处理函数

```typescript
// 股票代码输入时的处理
const onStockCodeInput = () => {
  stockCodeError.value = ''
  stockCodeHelp.value = getStockCodeFormatHelp(analysisForm.market)
}

// 市场类型变更时的处理
const onMarketChange = () => {
  if (analysisForm.stockCode.trim()) {
    validateStockCodeInput()
  } else {
    stockCodeHelp.value = getStockCodeFormatHelp(analysisForm.market)
  }
}

// 验证股票代码输入
const validateStockCodeInput = () => {
  const code = analysisForm.stockCode.trim()

  if (!code) {
    stockCodeError.value = ''
    stockCodeHelp.value = ''
    return
  }

  const validation = validateStockCode(code, analysisForm.market)

  if (!validation.valid) {
    stockCodeError.value = validation.message || '股票代码格式不正确'

    stockCodeHelp.value = ''
  } else {
    stockCodeError.value = ''
    stockCodeHelp.value = `✓ ${validation.market}代码格式正确`

    // 自动更新市场类型
    if (validation.market && validation.market !== analysisForm.market) {
      analysisForm.market = validation.market
      ElMessage.success(`已自动识别为${validation.market}`)
    }

    // 标准化代码
    if (validation.normalizedCode) {
      analysisForm.stockCode = validation.normalizedCode
    }
  }
}

```bash

## 样式定义

```scss
.stock-input {
  :deep(.el-input__inner) {
    font-weight: 600;
    text-transform: uppercase;
  }

  &.is-error {
    :deep(.el-input__inner) {
      border-color: #f56c6c;
    }
  }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 12px;
  color: #f56c6c;
}

.help-message {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 12px;
  color: #67c23a;
}

```bash

## 使用流程

### 1. 用户输入股票代码

```bash
用户输入: 000001
↓
显示提示: "A 股代码必须是 6 位数字"

```bash

### 2. 失焦验证

```bash
用户离开输入框
↓
自动验证格式
↓
显示结果: "✓ A 股代码格式正确"

```bash

### 3. 提交分析

```bash
用户点击"开始智能分析"
↓
再次验证代码格式
↓
如果格式错误，显示错误提示并阻止提交
↓
如果格式正确，使用标准化后的代码提交分析

```bash

## 测试用例

### A 股测试

| 输入 | 预期结果 | 说明 |

|------|---------|------|

| `000001` | ✓ 通过 | 平安银行 |

| `600519` | ✓ 通过 | 贵州茅台 |

| `00001` | ✗ 失败 | 只有 5 位 |

| `1234567` | ✗ 失败 | 超过 6 位 |

| `500001` | ✗ 失败 | 前缀不正确 |

### 美股测试

| 输入 | 预期结果 | 标准化后 | 说明 |

|------|---------|---------|------|

| `aapl` | ✓ 通过 | `AAPL` | 苹果 |

| `MSFT` | ✓ 通过 | `MSFT` | 微软 |

| `brk.b` | ✓ 通过 | `BRK.B` | 伯克希尔 B 股 |

| `ABCDEF` | ✗ 失败 | - | 超过 5 个字母 |

| `123` | ✗ 失败 | - | 纯数字 |

### 港股测试

| 输入 | 预期结果 | 标准化后 | 说明 |

|------|---------|---------|------|

| `700` | ✓ 通过 | `00700` | 腾讯控股 |

| `00700` | ✓ 通过 | `00700` | 腾讯控股 |

| `9988` | ✓ 通过 | `09988` | 阿里巴巴 |

| `123456` | ✗ 失败 | - | 超过 5 位 |

## 总结

### 优点

1. ✅ **用户体验好**：实时反馈，即时提示
2. ✅ **智能识别**：自动识别市场类型
3. ✅ **代码标准化**：自动格式化代码
4. ✅ **防止错误**：提交前验证，避免无效请求
5. ✅ **易于维护**：独立的工具函数，易于测试和扩展

### 后续优化方向

1. 添加更多市场支持（如：新加坡、日本等）
2. 集成股票名称自动补全
3. 添加历史输入记录
4. 支持批量代码验证
