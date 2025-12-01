/**
 * 基金模块统一错误处理
 */
import { ElMessage, ElMessageBox } from 'element-plus'
import { AxiosError } from 'axios'
import type { ApiResponse } from '@/types/funds'

export class FundError extends Error {
  constructor(
    message: string,
    public code?: string,
    public statusCode?: number,
    public details?: any
  ) {
    super(message)
    this.name = 'FundError'
  }
}

/**
 * 处理基金相关错误
 */
export function handleFundError(error: unknown, customMessage?: string): void {
  // 自定义消息优先
  if (customMessage) {
    ElMessage.error({
      message: customMessage,
      duration: 5000,
      showClose: true
    })
    return
  }

  // FundError 实例
  if (error instanceof FundError) {
    ElMessage.error({
      message: error.message,
      duration: 5000,
      showClose: true
    })
    return
  }

  // Axios 错误
  if (error instanceof AxiosError) {
    const response = error.response
    let message = '请求失败'

    if (response) {
      // 从响应中提取错误信息
      const data = response.data as ApiResponse
      if (data?.error) {
        message = data.error
      } else if (data?.detail) {
        message = data.detail
      } else if (response.status === 404) {
        message = '资源不存在'
      } else if (response.status === 403) {
        message = '没有权限执行此操作'
      } else if (response.status === 500) {
        message = '服务器内部错误'
      } else {
        message = error.message || `请求失败 (${response.status})`
      }
    } else if (error.request) {
      message = '网络请求失败，请检查网络连接'
    } else {
      message = error.message || '请求配置错误'
    }

    ElMessage.error({
      message: `基金操作失败: ${message}`,
      duration: 5000,
      showClose: true
    })
    return
  }

  // 普通 Error
  if (error instanceof Error) {
    ElMessage.error({
      message: `基金操作失败: ${error.message}`,
      duration: 5000,
      showClose: true
    })
    return
  }

  // 未知错误
  ElMessage.error({
    message: '发生未知错误，请稍后重试',
    duration: 5000,
    showClose: true
  })
}

/**
 * 处理需要确认的危险操作
 */
export async function handleDangerousOperation(
  message: string,
  title: string = '警告',
  confirmText: string = '确认',
  cancelText: string = '取消'
): Promise<boolean> {
  try {
    await ElMessageBox.confirm(
      message,
      title,
      {
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    return true
  } catch {
    return false
  }
}

/**
 * 处理 API 响应错误
 */
export function handleApiResponseError<T>(response: ApiResponse<T>): void {
  if (!response.success && response.error) {
    handleFundError(new FundError(response.error))
  }
}
