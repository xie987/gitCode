import os
import threading
import tkinter as tk

from tkinter import filedialog, ttk, messagebox
from src.cores.logger import get_logger
from src.cores.config import get_config
from src.cores.file_utils import resource_path
from src.routers.word_to_pdf import convert_word_to_pdf

logger = get_logger()


class ConverterApp(tk.Tk):
    """
    Word转PDF工具主界面
    """

    def __init__(self):
        super().__init__()
        self.title(get_config("app.title", "MagicTools"))
        # 画布比例
        self.geometry("800x600")
        # 初始化界面
        self._init_ui()
        self._init_config()
        logger.info("应用程序初始化完成")

    def _init_config(self):
        """加载应用配置"""
        # 设置应用图标
        try:
            icon_path = resource_path(get_config("app.icon", "log_16x16.ico"))
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                logger.debug(f"设置应用图标: {icon_path}")
        except Exception as e:
            logger.warning(f"图标加载失败: {str(e)}")

    def _init_ui(self):
        """
        初始化界面组件
        """
        # 主框架
        """
        在GUI中，每个Button、Label、输入框等，都是一个Widget
        Frame则是可以容纳其他Widget的Widget，所有的Widget组合起来就是一棵树。
        ttk是 tkinter 的一个扩展模块，提供了更多现代化、主题化的控件，它们不仅外观更好，而且通常支持更多样式和主题。
        """
        # 创建主框架main_frame。 padding=20:添加 20 像素的内边距。
        # 将 main_frame 放到窗口中，并使其填充整个窗口。fill=tk.BOTH表示水平和垂直方向都扩展，expand=True表示主框架可以扩展来占据可用空间
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 文件选择区域，fill=tk.X：横向填充
        file_frame = ttk.LabelFrame(main_frame, text="选择Word文件")
        file_frame.pack(fill=tk.X, pady=10)

        self.file_entry = ttk.Entry(file_frame)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # command=self._browse_file：方法名
        browse_btn = ttk.Button(file_frame, text="浏览...", command=self._browse_file)
        browse_btn.pack(side=tk.RIGHT, padx=5)

        # 转换按钮
        convert_btn = ttk.Button(
            main_frame, text="转换为PDF", command=self._start_conversion, width=15
        )
        convert_btn.pack(pady=20)

        # 进度显示
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)

        self.status_label = ttk.Label(progress_frame, text="准备就绪")
        self.status_label.pack(anchor=tk.W)

        self.progress = ttk.Progressbar(
            progress_frame, orient=tk.HORIZONTAL, mode="determinate"
        )
        self.progress.pack(fill=tk.X)

    def _browse_file(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Word文档", "*.doc *.docx"), ("所有文件", "*.*")]
        )
        # 如果文件路径不为空，则显示文件路径
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def _start_conversion(self):
        """启动转换过程"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showwarning("输入错误", "请先选择Word文件")
            return

        # 更新UI状态
        self.status_label.config(text="转换中...")
        self.progress["value"] = 0

        # 异步处理转换
        threading.Thread(
            target=self._do_conversion, args=(file_path,), daemon=True
        ).start()

    def _do_conversion(self, file_path):
        """执行转换逻辑"""
        try:
            # 调用路由层
            success, result = convert_word_to_pdf(file_path)

            if success:
                messagebox.showinfo(
                    "转换成功", f"文件已转换为: {os.path.basename(result)}"
                )
                self.status_label.config(text="转换完成")
                self.progress["value"] = 100
            else:
                messagebox.showerror("转换失败", f"错误: {result}")
                self.status_label.config(text="转换失败")
        except Exception as e:
            self.status_label.config(text=f"系统错误: {str(e)}")

    def run(self):
        """启动应用"""
        logger.info("启动GUI应用程序")
        self.mainloop()
