import os

from src.services.word_to_pdf_service import convert_document
from src.cores import file_utils
from src.cores.logger import get_logger

logger = get_logger()


def convert_word_to_pdf(input_path: str, output_path: str = None):
    """
    Word转PDF路由入口
    参数校验 -> 调用服务层 -> 错误处理
    """

    try:
        # 验证输入文件
        if not file_utils.is_word_file(input_path):
            logger.error(f"无效Word文件: {input_path}")
            return False, "仅支持.doc或.docx文件"

        # 验证输出路径
        if output_path:
            if not file_utils.validate_output_path(output_path):
                return False, "输出路径不可写"
        else:
            output_path = file_utils.generate_pdf_path(input_path)

        # 调用服务层
        logger.info(f"开始转换: {os.path.basename(input_path)}")
        result = convert_document(input_path, output_path)

        if result:
            logger.info(f"转换成功: {output_path}")
            return True, output_path
        else:
            logger.warning(f"转换失败: {input_path}")
            return False, "转换失败"

    except FileNotFoundError as e:
        logger.error(f"文件不存在: {input_path}")
        return False, f"文件不存在: {os.path.basename(input_path)}"

    except Exception as e:
        logger.exception(f"Word路由层异常: {str(e)}")
        return False, f"系统错误: {str(e)}"
