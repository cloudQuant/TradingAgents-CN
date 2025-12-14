"""
清洁日志配置 - 专注于格式统一和可读性
"""
import logging
import logging.config
import sys
from pathlib import Path
import os


class UnifiedFormatter(logging.Formatter):
    """统一的日志格式化器"""
    
    def __init__(self, include_trace=True, max_length=None):
        self.include_trace = include_trace
        self.max_length = max_length or 200
        
        # 统一的格式模板
        if include_trace:
            fmt = "%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s | trace=%(trace_id)s"
        else:
            fmt = "%(asctime)s | %(name)-25s | %(levelname)-7s | %(message)s"
            
        super().__init__(fmt, datefmt="%Y-%m-%d %H:%M:%S")
    
    def format(self, record):
        # 确保trace_id存在
        if not hasattr(record, 'trace_id'):
            record.trace_id = "-"
        
        # 创建记录副本
        record_copy = logging.makeLogRecord(record.__dict__)
        
        # 清理logger名称
        name = record_copy.name
        if len(name) > 25:
            # 保留关键部分
            if '.' in name:
                parts = name.split('.')
                if len(parts) >= 2:
                    # 保留最后两个部分
                    name = '.'.join(parts[-2:])
                if len(name) > 25:
                    name = name[-25:]
            else:
                name = name[-25:]
        record_copy.name = name
        
        # 清理消息内容
        msg = record_copy.getMessage()
        if len(msg) > self.max_length:
            msg = msg[:self.max_length-3] + "..."
            record_copy.msg = msg
            record_copy.args = ()
        
        return super().format(record_copy)


def setup_clean_logging(level="INFO"):
    """设置清洁的日志配置"""
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_context": {
                "()": "app.core.logging_context.LoggingContextFilter"
            }
        },
        "formatters": {
            "unified": {
                "()": "app.core.clean_logging.UnifiedFormatter",
                "include_trace": True,
                "max_length": 150
            },
            "unified_file": {
                "()": "app.core.clean_logging.UnifiedFormatter", 
                "include_trace": True,
                "max_length": 300
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "unified",
                "level": level,
                "filters": ["request_context"],
                "stream": sys.stdout
            },
            "main_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "unified_file",
                "level": "INFO",
                "filename": str(log_dir / "tradingagents.log"),
                "maxBytes": 50 * 1024 * 1024,  # 50MB
                "backupCount": 3,
                "encoding": "utf-8",
                "filters": ["request_context"]
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "unified_file",
                "level": "WARNING",
                "filename": str(log_dir / "error.log"),
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8",
                "filters": ["request_context"]
            }
        },
        "loggers": {
            # 主要应用日志
            "app": {
                "level": "INFO",
                "handlers": ["console", "main_file", "error_file"],
                "propagate": False
            },
            "webapi": {
                "level": "INFO", 
                "handlers": ["console", "main_file", "error_file"],
                "propagate": False
            },
            "tradingagents": {
                "level": "INFO",
                "handlers": ["console", "main_file", "error_file"], 
                "propagate": False
            },
            # 第三方库 - 减少噪音
            "uvicorn.access": {
                "level": "WARNING",
                "handlers": ["main_file"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console", "main_file", "error_file"],
                "propagate": False
            },
            # 其他第三方库
            "requests": {"level": "WARNING", "propagate": True},
            "urllib3": {"level": "WARNING", "propagate": True},
            "matplotlib": {"level": "WARNING", "propagate": True},
        },
        "root": {
            "level": level,
            "handlers": ["console", "main_file"]
        }
    }
    
    logging.config.dictConfig(config)
    
    # 记录配置完成
    logger = logging.getLogger("app.logging")
    logger.info("🎯 清洁日志配置已启用")
    
    return True