"""
日志过滤器 - 用于减少噪音和优化日志输出
"""
import logging
import re
from typing import Set, List


class NoiseFilter(logging.Filter):
    """过滤掉噪音日志"""
    
    def __init__(self, name: str = ""):
        super().__init__(name)
        # 定义要过滤的噪音模式
        self.noise_patterns = [
            # 过滤频繁的健康检查请求
            r'GET /api/health.*200',
            r'GET /api/notifications/unread_count.*200',
            # 过滤过于频繁的连接日志
            r'connection open',
            r'connection closed',
            # 过滤调试用的🔍日志
            r'🔍.*setup_logging',
            # 过滤重复的配置信息
            r'handlers配置:',
            r'main_handlers:',
            r'webapi_handlers:',
        ]
        self.compiled_patterns = [re.compile(pattern) for pattern in self.noise_patterns]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """返回True表示允许通过，False表示过滤掉"""
        message = record.getMessage()
        
        # 检查是否匹配噪音模式
        for pattern in self.compiled_patterns:
            if pattern.search(message):
                return False
        
        return True


class LevelBasedFilter(logging.Filter):
    """基于日志级别的智能过滤器"""
    
    def __init__(self, name: str = ""):
        super().__init__(name)
        # 定义不同模块的日志级别
        self.module_levels = {
            'uvicorn.access': logging.WARNING,  # 减少访问日志
            'uvicorn.error': logging.INFO,
            'requests': logging.WARNING,
            'urllib3': logging.WARNING,
            'matplotlib': logging.WARNING,
            'pandas': logging.WARNING,
        }
    
    def filter(self, record: logging.LogRecord) -> bool:
        """根据模块名调整日志级别"""
        module_name = record.name
        
        # 检查是否需要调整级别
        if module_name in self.module_levels:
            required_level = self.module_levels[module_name]
            return record.levelno >= required_level
        
        return True


class BusinessLogFilter(logging.Filter):
    """业务日志过滤器 - 突出重要的业务事件"""
    
    def __init__(self, name: str = ""):
        super().__init__(name)
        # 定义重要的业务关键词
        self.important_keywords = [
            '错误', 'ERROR', 'CRITICAL', 'FATAL',
            '启动', '停止', '初始化', '连接',
            '用户', '登录', '认证',
            '分析', '数据同步', '缓存',
            '异常', 'Exception', 'Traceback',
        ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """标记重要的业务日志"""
        message = record.getMessage()
        
        # 检查是否包含重要关键词
        for keyword in self.important_keywords:
            if keyword in message:
                # 为重要日志添加标记
                if not message.startswith('🔥'):
                    record.msg = f"🔥 {record.msg}"
                break
        
        return True