import os
import yaml
from .logger import get_logger

logger = get_logger()


class ConfigLoader:
    """统一配置加载器"""

    def __init__(self):
        self.config = {}
        self.config_path = None

    def load(self, config_path: str, required: bool = False) -> dict:
        """加载配置文件"""
        self.config_path = os.path.abspath(config_path)

        if not os.path.exists(self.config_path):
            if required:
                error_msg = f"必需配置文件不存在: {self.config_path}"
                logger.critical(error_msg)
                raise FileNotFoundError(error_msg)
            logger.warning(f"未找到配置文件: {self.config_path}，使用默认配置")
            return {}

        try:
            with open(self.config_path, "r") as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"成功加载配置文件: {self.config_path}")
            return self.config
        except Exception as e:
            error_msg = f"配置文件加载失败: {str(e)}"
            if required:
                logger.critical(error_msg)
                raise RuntimeError(error_msg)
            logger.error(error_msg)
            return {}

    def get(self, key_path: str, default=None):
        """按路径获取配置值"""
        keys = key_path.split(".")
        current = self.config

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current


# 全局配置加载器单例
global_config_loader = ConfigLoader()


def get_config(key: str = None, default=None):
    """快捷获取配置值"""
    if key:
        return global_config_loader.get(key, default)
    return global_config_loader.config
