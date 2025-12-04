"""
股票模块自定义异常

定义股票数据处理中可能出现的各种异常
"""


class StockException(Exception):
    """股票模块基础异常"""
    
    def __init__(self, message: str = "股票数据处理错误", code: int = 50001):
        self.message = message
        self.code = code
        super().__init__(self.message)


class StockDataFetchError(StockException):
    """数据获取错误"""
    
    def __init__(self, message: str = "获取股票数据失败", collection_name: str = ""):
        self.collection_name = collection_name
        super().__init__(
            message=f"{message}: {collection_name}" if collection_name else message,
            code=50002
        )


class StockDataSaveError(StockException):
    """数据保存错误"""
    
    def __init__(self, message: str = "保存股票数据失败", collection_name: str = ""):
        self.collection_name = collection_name
        super().__init__(
            message=f"{message}: {collection_name}" if collection_name else message,
            code=50003
        )


class StockCollectionNotFoundError(StockException):
    """集合不存在错误"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        super().__init__(
            message=f"股票数据集合不存在: {collection_name}",
            code=40004
        )


class StockInvalidParameterError(StockException):
    """参数无效错误"""
    
    def __init__(self, param_name: str, message: str = ""):
        self.param_name = param_name
        super().__init__(
            message=f"无效参数 {param_name}: {message}" if message else f"无效参数: {param_name}",
            code=40001
        )


class StockProviderNotFoundError(StockException):
    """Provider不存在错误"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        super().__init__(
            message=f"股票数据Provider不存在: {collection_name}",
            code=50004
        )


class StockServiceNotFoundError(StockException):
    """Service不存在错误"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        super().__init__(
            message=f"股票数据Service不存在: {collection_name}",
            code=50005
        )


class StockApiRateLimitError(StockException):
    """API频率限制错误"""
    
    def __init__(self, message: str = "API调用频率超限"):
        super().__init__(message=message, code=42901)


class StockDataValidationError(StockException):
    """数据验证错误"""
    
    def __init__(self, message: str = "股票数据验证失败"):
        super().__init__(message=message, code=40002)


class StockTaskError(StockException):
    """任务执行错误"""
    
    def __init__(self, task_id: str, message: str = "任务执行失败"):
        self.task_id = task_id
        super().__init__(
            message=f"任务 {task_id} 执行失败: {message}",
            code=50006
        )


class StockImportError(StockException):
    """数据导入错误"""
    
    def __init__(self, message: str = "导入股票数据失败"):
        super().__init__(message=message, code=50007)


class StockExportError(StockException):
    """数据导出错误"""
    
    def __init__(self, message: str = "导出股票数据失败"):
        super().__init__(message=message, code=50008)


class StockSyncError(StockException):
    """数据同步错误"""
    
    def __init__(self, message: str = "同步股票数据失败"):
        super().__init__(message=message, code=50009)
