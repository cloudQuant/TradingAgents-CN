"""
期权模块自定义异常类
"""


class OptionException(Exception):
    """期权模块基础异常类"""
    
    def __init__(self, message: str, code: str = "OPTION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class OptionCollectionNotFound(OptionException):
    """期权集合未找到异常"""
    
    def __init__(self, collection_name: str):
        super().__init__(
            message=f"期权集合 '{collection_name}' 不存在",
            code="OPTION_COLLECTION_NOT_FOUND"
        )
        self.collection_name = collection_name


class OptionDataUpdateError(OptionException):
    """期权数据更新错误"""
    
    def __init__(self, message: str, collection_name: str = ""):
        super().__init__(
            message=f"更新期权集合 '{collection_name}' 数据失败: {message}",
            code="OPTION_DATA_UPDATE_ERROR"
        )
        self.collection_name = collection_name


class OptionDataValidationError(OptionException):
    """期权数据验证错误"""
    
    def __init__(self, message: str, field: str = ""):
        super().__init__(
            message=f"期权数据验证失败: {message}",
            code="OPTION_DATA_VALIDATION_ERROR"
        )
        self.field = field


class OptionProviderError(OptionException):
    """期权数据提供者错误"""
    
    def __init__(self, message: str, provider_name: str = ""):
        super().__init__(
            message=f"期权数据提供者 '{provider_name}' 错误: {message}",
            code="OPTION_PROVIDER_ERROR"
        )
        self.provider_name = provider_name


class OptionTaskNotFound(OptionException):
    """期权任务未找到异常"""
    
    def __init__(self, task_id: str):
        super().__init__(
            message=f"期权任务 '{task_id}' 不存在",
            code="OPTION_TASK_NOT_FOUND"
        )
        self.task_id = task_id


class OptionDataFetchError(OptionException):
    """期权数据获取错误"""
    
    def __init__(self, message: str, source: str = ""):
        super().__init__(
            message=f"从 '{source}' 获取期权数据失败: {message}",
            code="OPTION_DATA_FETCH_ERROR"
        )
        self.source = source
