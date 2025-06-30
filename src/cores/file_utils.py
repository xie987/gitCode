import os
import shutil
import sys
import uuid
from .logger import get_logger

logger = get_logger()


def resource_path(relative_path: str) -> str:
    """将相对路径转换为绝对路径"""
    if hasattr(sys, "_MEIPASS"):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def is_word_file(file_path: str) -> bool:
    """验证是否为Word文件"""
    return file_path.lower().endswith((".doc", ".docx"))


def generate_pdf_path(original_path: str) -> str:
    """生成默认PDF输出路径"""
    return f"{os.path.splitext(original_path)[0]}.pdf"


def create_temp_dir() -> str:
    """创建临时目录"""
    temp_dir = os.path.join(os.getcwd(), f"temp_{uuid.uuid4().hex}")
    os.makedirs(temp_dir, exist_ok=True)
    logger.debug(f"创建临时目录: {temp_dir}")
    return temp_dir


def clean_temp_dir(dir_path: str):
    """清理临时目录"""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        logger.debug(f"已清理临时目录: {dir_path}")


def validate_output_path(path: str) -> bool:
    """验证输出路径是否可写"""
    if not os.access(os.path.dirname(path) or os.getcwd(), os.W_OK):
        logger.error(f"路径不可写: {path}")
        return False
    return True
