import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# 全局日志器实例
_logger = None


def init_logger(level=logging.INFO, log_dir="logs", max_size=10, backup_count=5):
    """初始化全局日志系统"""
    global _logger

    logger = logging.getLogger("DOC_CONVERTER")  # 创建命名日志器
    logger.setLevel(level)  # 设置日志级别

    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)

    # 日志格式
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)  # 输出到标准输出
    console_handler.setFormatter(formatter)  # 应用格式
    logger.addHandler(console_handler)  # 添加到日志器

    # 文件处理器（按大小滚动）
    log_file = os.path.join(log_dir, "app.log")  # 日志文件路径
    file_handler = RotatingFileHandler(  # 滚动日志处理器
        log_file, maxBytes=max_size * 1024 * 1024, backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _logger = logger
    return logger


def get_logger():
    """
    获取全局日志器实例
    懒加载初始化：避免重复初始化
    """
    global _logger
    if _logger is None:
        return init_logger()  # 未初始化时自动初始化
    return _logger
