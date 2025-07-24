import sys
import yaml
import os

from src.cores.logger import get_logger
from src.cores.config import global_config_loader
from src.app import ConverterApp

logger = get_logger()


def init_system():
    """系统初始化"""
    # 创建应用数据目录
    app_data_dir = os.path.join(os.getenv("APPDATA"), "DocConverter")
    os.makedirs(app_data_dir, exist_ok=True)

    # 加载配置文件
    config_path = os.path.join(app_data_dir, "config.yaml")
    if not os.path.exists(config_path):
        # 创建默认配置
        default_config = {
            "app": {"title": "MagicTools", "icon": "log_16x16.ico"},
            "logging": {"dir": os.path.join(app_data_dir, "logs"), "max_size": 10},
        }
        with open(config_path, "w") as f:
            yaml.dump(default_config, f)

    # 加载配置
    global_config_loader.load(config_path, required=True)

    # 初始化日志系统
    # log_dir = global_config_loader.get("logging.dir", "logs")
    # log_size = global_config_loader.get("logging.max_size", 10)
    # logger.init_logger(log_dir=log_dir, max_size=log_size)

    # 系统信息
    logger.info(f"系统初始化完成 | Python {sys.version}")
    logger.debug(f"配置路径: {config_path}")


if __name__ == "__main__":
    try:
        init_system()
        app = ConverterApp()
        app.run()
    except Exception as e:
        logger.critical(f"应用程序崩溃: " f"{str(e)}", exc_info=True)
        sys.exit(1)
