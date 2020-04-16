'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-04-11 11:59:12
@LastEditTime: 2020-04-16 16:59:11
@LastEditors: Allen
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
from real_ocr_watchdog import *
from ai_cloud_service import *
from ocr_method_api.baidu_aip import baidu_aip_ocr
from snipaste import snip
from file import file
import os


class AICloudWin(object):
    def __init__(self):
        self.root = tk.Tk()
        # self.parent = self.root
        self.root.geometry("%dx%d" % (1200, 800))  # 窗体尺寸
        self.center_window(self.root)  # 将窗体移动到屏幕中央
        self.root.title("人工智能平台")  # 窗体标题
        self.root.iconbitmap("images\\Money.ico")  # 窗体图标
        self.root.grab_set()
        # self.global_widgets()  # 设置文本框的赋值变量, must set after body
        # self.body(self.root)  # 绘制窗体组件

    def win_loop_display(self):
        self.bind_win_close_event()
        self.root.mainloop()

    def bind_win_close_event(self):
        self.root.protocol('WM_DELETE_WINDOW', self.exit)

    def global_widgets(self):
        pass

    def body(self, frame):
        pass

    def exit(self):
        if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    @staticmethod
    def center_window(win, width=None, height=None):
        """ 将窗口屏幕居中 """
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        if width is None:
            width, height = AICloudWin.get_window_size(win)[:2]
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                (screenheight - height) / 3)
        win.geometry(size)

    @staticmethod
    def get_window_size(win, update=True):
        """ 获得窗体的尺寸 """
        if update:
            win.update()
        return win.winfo_width(), win.winfo_height(), win.winfo_x(
        ), win.winfo_y()

    @staticmethod
    def tkimg_resized(img, w_box, h_box, keep_ratio=True):
        """对图片进行按比例缩放处理"""
        w, h = img.size

        if keep_ratio:
            if w > h:
                width = w_box
                height = int(h_box * (1.0 * h / w))

            if h >= w:
                height = h_box
                width = int(w_box * (1.0 * w / h))
        else:
            width = w_box
            height = h_box

        img1 = img.resize((width, height), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(img1)
        return tkimg

    @staticmethod
    def image_label(frame, img, width, height, keep_ratio=True):
        """输入图片信息，及尺寸，返回界面组件"""
        if isinstance(img, str):
            _img = Image.open(img)
        else:
            _img = img
        lbl_image = tk.Label(frame, width=width, height=height)

        tk_img = AICloudWin.tkimg_resized(_img, width, height, keep_ratio)
        lbl_image.image = tk_img
        lbl_image.config(image=tk_img)
        return lbl_image

    @staticmethod
    def _font(fname="微软雅黑", size=12, bold=tkFont.NORMAL):
        """设置字体"""
        ft = tkFont.Font(family=fname, size=size, weight=bold)
        return ft

    @staticmethod
    def _ft(size=12, bold=False):
        """极简字体设置函数"""
        if bold:
            return AICloudWin._font(size=size, bold=tkFont.BOLD)
        else:
            return AICloudWin._font(size=size, bold=tkFont.NORMAL)

    @staticmethod
    def h_seperator(parent, height=2):  # height 单位为像素值
        """水平分割线, 水平填充 """
        tk.Frame(parent, height=height, bg="whitesmoke").pack(fill=tk.X)

    @staticmethod
    def v_seperator(parent, width, bg="whitesmoke"):  # width 单位为像素值
        """垂直分割线 , fill=tk.Y, 但如何定位不确定，直接返回对象，由容器决定 """
        frame = tk.Frame(parent, width=width, bg=bg)
        return frame


class RealTimeOCRWin(AICloudWin):
    def __init__(self):
        super().__init__()
        self.ocr_service = None

        self.global_widgets()  # 设置文本框的赋值变量, must set after body
        self.body(self.root)  # 绘制窗体组件

        self.win_loop_display()

    def init_RealTimeOCRService(self):
        return RealTimeOCRService(watch_path=self.var_watch_path.get(),
                                  save_path=self.var_ocr_ret.get(),
                                  logfunc=self.log,
                                  ocrresfunc=self.OCR_results)

    def global_widgets(self):
        '''
        @Description: set global variables & widgets

        @Args: None

        @Returns: global variables & widgets
        '''
        self.var_watch_path = tk.StringVar()
        self.var_watch_path.set(file.watch_path)
        self.var_ocr_ret = tk.StringVar()
        self.var_ocr_ret.set(file.save_path)
        self.text_log = None
        self.text_ocr = None

    def set_text_scroll(self, text):
        '''
        @Description: config scroll for Text widget

        @Args: 
          param: Text widget address

        @Returns: None
        '''
        scroll = ttk.Scrollbar(self.root)  # creat scroll
        scroll.pack(side=tk.RIGHT, fill=tk.Y)  # set position
        scroll.config(command=text.yview)  # associate with text widget
        text.config(yscrollcommand=scroll.set)

    # 绘制窗体组件
    def body(self, parent):
        '''
        @Description: divide the interface, and then create the windows widgets for each sub frame

        @Args: 
          param: parent frame
          
        @Returns: None
        '''
        self.title(parent).pack(fill=tk.X)
        self.main(parent).pack(expand=tk.YES, fill=tk.BOTH)
        self.bottom(parent).pack(fill=tk.X)

    def title(self, parent):
        '''
        @Description: set title frame

        @Args: 
          param: title frame

        @Returns: the title frame which has already configured.
        '''
        def label(frame, text, size, bold=False):
            return tk.Label(frame,
                            text=text,
                            bg="black",
                            fg="white",
                            height=2,
                            font=self._ft(size, bold))

        frame = tk.Frame(parent, bg="black")

        label(frame, "人工智能应用平台", 16, True).pack(side=tk.LEFT, padx=10)
        label(frame, "图像模型定制", 12).pack(side=tk.LEFT, padx=100)
        label(frame, "声音模型定制", 12).pack(side=tk.LEFT, padx=0)
        label(frame, "定制模型", 12).pack(side=tk.LEFT, padx=100)
        label(frame, "", 12).pack(side=tk.RIGHT, padx=20)
        label(frame, "登录用户", 12).pack(side=tk.RIGHT, padx=20)
        self.image_label(frame, "images\\user.png", 40, 40,
                         False).pack(side=tk.RIGHT)

        return frame

    def bottom(self, parent):
        '''
        @Description: config the bottom of windows

        @Args: 
          param: the bottom frame

        @Returns: the bottom frame which has already configured.
        '''

        frame = tk.Frame(parent, height=10, bg="whitesmoke")
        frame.propagate(True)
        return frame

    def main(self, parent):
        """ 窗体主体 """

        frame = tk.Frame(parent, bg="whitesmoke")

        self.main_top(frame).pack(fill=tk.X, padx=30, pady=15)
        self.main_left(frame).pack(side=tk.LEFT, fill=tk.Y, padx=30)
        self.v_seperator(frame, 30).pack(side=tk.RIGHT, fill=tk.Y)
        self.main_right(frame).pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        return frame

    def main_top(self, parent):
        def label(frame, text, size=12):
            return tk.Label(frame,
                            bg="white",
                            fg="gray",
                            text=text,
                            font=self._ft(size))

        frame = tk.Frame(parent, bg="white", height=150)

        self.image_label(frame,
                         "images\\img_title.png",
                         width=240,
                         height=120,
                         keep_ratio=False).pack(side=tk.LEFT, padx=10, pady=10)

        self.main_top_middle(frame).pack(side=tk.LEFT)

        label(frame, "收起^").pack(side=tk.RIGHT, padx=10)

        frame.propagate(False)
        return frame

    def main_top_middle(self, parent):
        str1 = "定制图像分类模型，可以识别一张图整体是什么物体/状态/场景。"
        str2 = "在各分类图片之间差异明显的情况下，训练数据每类仅需20-100张，最快10分钟可训练完毕"

        def label(frame, text):
            return tk.Label(frame,
                            bg="white",
                            fg="gray",
                            text=text,
                            font=self._ft(12))

        frame = tk.Frame(parent, bg="white")

        self.main_top_middle_top(frame).pack(anchor=tk.NW)

        label(frame, str1).pack(anchor=tk.W, padx=10, pady=2)
        label(frame, str2).pack(anchor=tk.W, padx=10)

        return frame

    def main_top_middle_top(self, parent):
        def label(frame, text, size=12, bold=True, fg="blue"):
            return tk.Label(frame,
                            text=text,
                            bg="white",
                            fg=fg,
                            font=self._ft(size, bold))

        frame = tk.Frame(parent, bg="white")

        label(frame, "图像分类模型", 20, True, "black").pack(side=tk.LEFT, padx=10)
        label(frame, "操作文档").pack(side=tk.LEFT, padx=10)
        label(frame, "教学视频").pack(side=tk.LEFT, padx=10)
        label(frame, "常见问题").pack(side=tk.LEFT, padx=10)

        return frame

    def main_left(self, parent):
        def label(frame, text, size=10, bold=False, bg="white"):
            return tk.Label(frame, text=text, bg=bg, font=self._ft(size, bold))

        frame = tk.Frame(parent, width=180, bg="white")

        label(frame, "服务中心", 12, True).pack(anchor=tk.W, padx=20, pady=10)
        # label(frame, "我的模型").pack(anchor=tk.W, padx=40, pady=5)

        f1 = tk.Frame(frame, bg="whitesmoke")
        AICloudWin.v_seperator(f1, width=5, bg="blue").pack(side=tk.LEFT,
                                                            fill=tk.Y)
        label(f1, "通用文本识别", bg="whitesmoke").pack(side=tk.LEFT,
                                                  anchor=tk.W,
                                                  padx=35,
                                                  pady=5)
        f1.pack(fill=tk.X)

        label(frame, "数学公式识别").pack(anchor=tk.W, padx=40, pady=5)
        label(frame, "几何图形识别").pack(anchor=tk.W, padx=40, pady=5)
        label(frame, "发布模型").pack(anchor=tk.W, padx=40, pady=5)

        AICloudWin.h_seperator(frame, 10)

        label(frame, "数据中心", 12, True).pack(anchor=tk.W, padx=20, pady=10)
        label(frame, "数据集管理").pack(anchor=tk.W, padx=40, pady=5)
        label(frame, "创建数据集").pack(anchor=tk.W, padx=40, pady=5)

        frame.propagate(False)
        return frame

    def main_right(self, parent):
        def label(frame, text, size=10, bold=False, fg="black"):
            return tk.Label(frame,
                            text=text,
                            bg="white",
                            fg=fg,
                            font=self._ft(size, bold))

        def space(n):
            s = " "
            r = ""
            for i in range(n):
                r += s
            return r

        frame = tk.Frame(parent, width=200, bg="white")

        label(frame, "通用文本识别", 12, True).pack(anchor=tk.W, padx=20, pady=5)

        self.h_seperator(frame)

        f1 = tk.Frame(frame, bg="white")
        label(f1, space(8) + "模型类别:").pack(side=tk.LEFT, pady=5)
        label(f1, "图像分类").pack(side=tk.LEFT, padx=20)
        btn_start = ttk.Button(
            f1,
            text="启动服务",
            command=lambda: self.btn_start_ocr_service(btn_start),
            width=12)
        btn_start.pack(side=tk.LEFT, padx=20)
        btn_stop = ttk.Button(
            f1,
            text="关闭服务",
            command=lambda: self.btn_stop_ocr_service(btn_start),
            width=12)
        btn_stop.pack(side=tk.LEFT, padx=20)
        f1.pack(fill=tk.X)

        f2 = tk.Frame(frame, bg="white")
        label(f2, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
        label(f2, "监控路径:").pack(side=tk.LEFT)

        tk.Entry(f2,
                 textvariable=self.var_watch_path,
                 bg="white",
                 font=self._ft(10),
                 width=50).pack(side=tk.LEFT, padx=20)
        ttk.Button(f2,
                   text="更改",
                   command=self.btn_ask_watch_path_click,
                   width=12).pack(side=tk.LEFT, padx=20)
        f2.pack(fill=tk.X)

        f3 = tk.Frame(frame, bg="white")
        label(f3, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
        label(f3, "保存路径:").pack(side=tk.LEFT)

        tk.Entry(f3,
                 textvariable=self.var_ocr_ret,
                 bg="white",
                 font=self._ft(10),
                 width=50).pack(side=tk.LEFT, padx=20)
        ttk.Button(f3,
                   text="更改",
                   command=self.btn_ask_ocr_ret_path_click,
                   width=12).pack(side=tk.LEFT, padx=20)
        f3.pack(fill=tk.X)

        f4 = tk.Frame(frame, bg="white")
        label(f4, space(5) + "*", fg="red").pack(side=tk.LEFT,
                                                 anchor=tk.N,
                                                 pady=5)
        label(f4, "识别结果:").pack(side=tk.LEFT, anchor=tk.N, pady=5)
        self.text_ocr = tk.Text(f4,
                                background="white",
                                height=15,
                                width=80,
                                font=self._ft(12))
        self.text_ocr.pack(side=tk.LEFT, padx=20, pady=5)
        self.set_text_scroll(self.text_ocr)
        # T = tk.Text(f4, height=2, width=30)
        # T.pack()
        # T.insert(tk.END, "Just a text Widget\nin two lines\n")
        f4.pack(fill=tk.X)

        f5 = tk.Frame(frame, bg="white")
        label(f5, space(5) + "*", fg="red").pack(side=tk.LEFT,
                                                 anchor=tk.N,
                                                 pady=5)
        label(f5, "执行日志:").pack(side=tk.LEFT, anchor=tk.N, pady=5)
        self.text_log = tk.Text(f5,
                                background="white",
                                font=self._ft(10),
                                height=5,
                                width=80)
        self.text_log.pack(side=tk.LEFT, padx=20, pady=5)
        self.set_text_scroll(self.text_log)
        f5.pack(fill=tk.X)

        return frame

    def btn_start_ocr_service(self, btn):
        if self.ocr_service is None:
            self.ocr_service = self.init_RealTimeOCRService()
        if btn:
            btn.config(state=tk.DISABLED)
            self.ocr_service.start_OCR_service()

    def btn_stop_ocr_service(self, btn):
        if btn:
            btn.config(state=tk.ACTIVE)
            self.ocr_service.stop_OCR_service()
            self.ocr_service = None

    def btn_ask_watch_path_click(self):
        path = filedialog.askdirectory()
        if path:
            # self.update_entry_text(self.entry_watch_path, path)
            self.var_watch_path.set(path)
            self.ocr_service.watch_path = path
            self.log(f'Selected watch path: {path}')

    def btn_ask_ocr_ret_path_click(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.var_ocr_ret.set(path)
            # self.update_entry_text(self.entry_ocr_ret, path)
            self.ocr_service.save_path = path
            self.log(f'Selected OCR result path: {path}')

    def log(self, message):
        self.text_log.insert(tk.END, f'{message}\n')
        self.text_log.see(tk.END)

    def OCR_results(self, message):
        self.text_ocr.insert(tk.END, f'{message}\n\n')
        self.text_ocr.see(tk.END)


if __name__ == "__main__":
    RealTimeOCRWin()
