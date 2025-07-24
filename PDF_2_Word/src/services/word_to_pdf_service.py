import os
import comtypes.client

from src.cores.logger import get_logger

logger = get_logger()


def convert_document(word_path: str, pdf_path: str):
    """
    Word转PDF具体实现
    """
    word = None
    doc = None

    try:
        # 初始化Word应用
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False

        # 打开文档并转换
        logger.debug(f"打开文档: {word_path}")
        doc = word.Documents.Open(os.path.abspath(word_path))

        # 文件格式常量 17 = PDF格式
        logger.debug(f"转换到PDF: {pdf_path}")
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)

        return True
    except Exception as e:
        logger.exception(f"Word转换服务异常: {str(e)}")
        return False
    finally:
        # 确保资源释放
        if doc:
            try:
                doc.Close()
            except:
                pass
        if word:
            try:
                word.Quit()
            except:
                pass
        logger.debug("Word资源已清理")
