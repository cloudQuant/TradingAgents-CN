"""
货币模块自定义异常类
"""


class CurrencyException(Exception):
    """货币模块基础异常类"""
    
    def __init__(self, message: str, code: str = "CURRENCY_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class CurrencyCollectionNotFound(CurrencyException):
    """货币集合未找到异常"""
    
    def __init__(self, collection_name: str):
        super().__init__(
            message=f"货币集合 '{collection_name}' 不存在",
            code="CURRENCY_COLLECTION_NOT_FOUND"
        )
        self.collection_name = collection_name


class CurrencyDataUpdateError(CurrencyException):
    """货币数据更新错误"""
    
    def __init__(self, message: str, collection_name: str = ""):
        super().__init__(
            message=f"更新货币集合 '{collection_name}' 数据失败: {message}",
            code="CURRENCY_DATA_UPDATE_ERROR"
        )
        self.collection_name = collection_name


class CurrencyDataValidationError(CurrencyException):
    """货币数据验证错误"""
    
    def __init__(self, message: str, field: str = ""):
        super().__init__(
            message=f"货币数据验证失败: {message}",
            code="CURRENCY_DATA_VALIDATION_ERROR"
        )
        self.field = field


class CurrencyProviderError(CurrencyException):
    """货币数据提供者错误"""
    
    def __init__(self, message: str, provider_name: str = ""):
        super().__init__(
            message=f"货币数据提供者 '{provider_name}' 错误: {message}",
            code="CURRENCY_PROVIDER_ERROR"
        )
        self.provider_name = provider_name


class CurrencyApiKeyError(CurrencyException):
    """货币API密钥错误"""
    
    def __init__(self, message: str = "API密钥无效或未配置"):
        super().__init__(
            message=f"货币API错误: {message}",
            code="CURRENCY_API_KEY_ERROR"
        )


class CurrencyTaskNotFound(CurrencyException):
    """货币任务未找到异常"""
    
    def __init__(self, task_id: str):
        super().__init__(
            message=f"货币任务 '{task_id}' 不存在",
            code="CURRENCY_TASK_NOT_FOUND"
        )
        self.task_id = task_id


class CurrencyDataFetchError(CurrencyException):
    """货币数据获取错误"""
    
    def __init__(self, message: str, source: str = ""):
        super().__init__(
            message=f"从 '{source}' 获取货币数据失败: {message}",
            code="CURRENCY_DATA_FETCH_ERROR"
        )
        self.source = source
