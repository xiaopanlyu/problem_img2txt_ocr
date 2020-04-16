'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-04-11 11:59:12
@LastEditTime: 2020-04-16 16:52:56
@LastEditors: Allen
'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
from real_ocr_watchdog import *
from ocr_method_api.baidu_aip import baidu_aip_ocr
from snipaste import snip
from file import file
import os


class AICloudService(object):
    def __init__(self):

        self.watchdog = None
        self.watch_path = file.watch_path
        self.save_path = file.save_path
        self.log = print
        self.ocr_res = print

    @staticmethod
    def update_entry_text(e, text):
        e.delete(0, tk.END)
        e.insert(0, text)

    def start_watchdog(self, watchdog=None):
        if self.watchdog is not None:
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog is none!!! Please init a watchdog.')

    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')

    def ocr_app(self, src_path):
        ocr_result = baidu_aip_ocr(src_path)
        with open('%s' % (self.save_path), 'a', encoding='utf-8') as f:
            f.write("{}\n".format(ocr_result))
            f.close()
        # self.log(f"OCR result: {ocr_result}")
        self.ocr_res(ocr_result)
        return ocr_result


class RealTimeOCRService(AICloudService):
    def __init__(self,
                 watch_path=None,
                 save_path=None,
                 logfunc=None,
                 ocrresfunc=None):
        super().__init__()

        if watch_path:
            self.watch_path = watch_path
        if save_path:
            self.save_path = save_path
        if logfunc:
            self.log = logfunc
        if ocrresfunc:
            self.ocr_res = ocrresfunc

        self.watchdog = RealOCRWatchdog(path=self.watch_path,
                                        logfunc=self.log,
                                        ocrfunc=self.ocr_app)

    def start_OCR_service(self):
        snip.start_snipaste(self.watch_path)

        self.start_watchdog()
        self.log('Start OCR service success!')

    def stop_OCR_service(self):
        snip.stop_snipaste()
        self.stop_watchdog()
        self.log('Stop OCR service success!')
