'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-04-03 01:55:51
@LastEditTime: 2020-04-05 23:21:20
@LastEditors: Allen
'''
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ocr_method_api.baidu_aip import baidu_aip_ocr
from snipaste import snip
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
watch_path = os.path.join(cur_path, 'images').replace('\\', '/')
ocr_result_save_path = os.path.join(cur_path,
                                    'ocr_text.txt').replace('\\', '/')

font_style = ('Microsoft YaHei', 12)


class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns='*', logfunc=print, ocrfunc=print):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc
        self.ocr_res = ocrfunc

    def on_created(self, event):
        # This function is called when a file is created
        self.log(f"hey, {event.src_path} has been created!")
        ocr_result = baidu_aip_ocr(event.src_path)
        with open('%s' % (ocr_result_save_path), 'a', encoding='utf-8') as f:
            f.write("{}\n".format(ocr_result))
            f.close()
        # self.log(f"OCR result: {ocr_result}")
        self.ocr_res(ocr_result)

    def on_deleted(self, event):
        # This function is called when a file is deleted
        self.log(f"what the f**k! Someone deleted {event.src_path}!")

    def on_modified(self, event):
        # This function is called when a file is modified
        self.log(f"hey buddy, {event.src_path} has been modified")

    def on_moved(self, event):
        # This function is called when a file is moved
        self.log(
            f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


class GUI:
    def __init__(self):
        self.watchdog = None
        self.watch_path = watch_path
        self.ocr_result_save_path = ocr_result_save_path

        self.root = tk.Tk()
        self.root.title('RealOCR')

        width = 960
        height = 800
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                (screenheight - height) / 2)
        self.root.geometry(size)  # width*height + pos_x + pos_y

        # entry:Set file path
        self.lf_entry_set_file_path = tk.LabelFrame(self.root,
                                                    text='Set file path',
                                                    font=font_style)
        self.lf_entry_set_file_path.grid(row=1,
                                         column=0,
                                         rowspan=1,
                                         padx=6,
                                         pady=6,
                                         ipadx=6,
                                         ipady=6,
                                         sticky='w')

        self.label_watch_path = tk.Label(self.lf_entry_set_file_path,
                                         text='watch path:',
                                         font=font_style)
        self.label_watch_path.grid(row=1,
                                   column=1,
                                   rowspan=1,
                                   padx=6,
                                   sticky='w')

        var_watch_path = tk.StringVar()
        var_watch_path.set(self.watch_path)
        self.entry_watch_path = tk.Entry(self.lf_entry_set_file_path,
                                         textvariable=var_watch_path,
                                         font=font_style,
                                         relief='solid')
        self.entry_watch_path.grid(row=1,
                                   column=2,
                                   rowspan=1,
                                   padx=6,
                                   sticky='w')

        self.btn_ask_watch_path = tk.Button(
            self.lf_entry_set_file_path,
            text='change',
            font=font_style,
            command=self.btn_ask_watch_path_click)
        self.btn_ask_watch_path.grid(row=1,
                                     column=3,
                                     rowspan=1,
                                     padx=6,
                                     sticky='w')

        self.label_ocr_ret = tk.Label(self.lf_entry_set_file_path,
                                      text='save path:',
                                      font=font_style)
        self.label_ocr_ret.grid(row=2, column=1, rowspan=1, padx=6, sticky='w')

        var_ocr_ret = tk.StringVar()
        var_ocr_ret.set(self.ocr_result_save_path)
        self.entry_ocr_ret = tk.Entry(self.lf_entry_set_file_path,
                                      textvariable=var_ocr_ret,
                                      font=font_style,
                                      relief='solid')
        self.entry_ocr_ret.grid(row=2, column=2, rowspan=1, padx=6, sticky='w')

        self.btn_ask_ocr_ret_path = tk.Button(
            self.lf_entry_set_file_path,
            text='change',
            font=font_style,
            command=self.btn_ask_ocr_ret_path_click)
        self.btn_ask_ocr_ret_path.grid(row=2,
                                       column=3,
                                       rowspan=1,
                                       padx=6,
                                       sticky='w')
        # button: service
        self.lf_button_service = tk.LabelFrame(self.root,
                                               font=font_style,
                                               text='RealOCR Service')
        self.lf_button_service.grid(row=2,
                                    column=0,
                                    columnspan=3,
                                    sticky='w',
                                    padx=6)

        self.button_start_OCR_service = tk.Button(
            self.lf_button_service,
            text='Start OCR service',
            font=font_style,
            command=self.button_start_OCR_service_click)
        self.button_start_OCR_service.grid(row=0,
                                           column=2,
                                           sticky='w',
                                           padx=10)

        self.button_stop_OCR_service = tk.Button(
            self.lf_button_service,
            text='Stop OCR service',
            font=font_style,
            command=self.button_stop_OCR_service_click)

        self.button_stop_OCR_service.grid(row=0, column=3, sticky='w', padx=10)

        # Text: OCR RESULTS
        self.lf_text_OCR_results = tk.LabelFrame(self.root,
                                                 font=font_style,
                                                 text='OCR Results')
        self.lf_text_OCR_results.grid(row=3,
                                      column=0,
                                      columnspan=3,
                                      padx=6,
                                      sticky='w')

        self.textbox_OCR_results = tk.Text(self.lf_text_OCR_results,
                                           font=font_style,
                                           relief='solid')
        self.textbox_OCR_results.grid(row=0,
                                      column=0,
                                      rowspan=3,
                                      padx=6,
                                      sticky='w')
        # Text: messagebox
        self.lf_text_messagebox = tk.LabelFrame(self.root,
                                                font=font_style,
                                                text='Logs')
        self.lf_text_messagebox.grid(row=4,
                                     column=0,
                                     columnspan=3,
                                     padx=3,
                                     sticky='w')
        self.text_messagebox = tk.Text(self.lf_text_messagebox,
                                       font=font_style)
        self.text_messagebox.grid(row=0,
                                  column=0,
                                  rowspan=3,
                                  padx=6,
                                  sticky='w')

        self.root.mainloop()

        # frm = Frame(self.root)
        # Button(frm, text='Set Watch Path',
        #        command=self.set_watch_path).grid(row=1)
        # Button(frm,
        #        text='Set OCR Result File',
        #        command=self.set_ocr_result_path).grid(row=2)
        # Button(frm, text='Start Watchdog',
        #        command=self.start_watchdog).grid(row=3)
        # Button(frm, text='Stop Watchdog',
        #        command=self.stop_watchdog).grid(row=4)

        # Button(frm, text='Start OCR Service',
        #        command=self.start_engine).grid(row=5)

        # # 第5步，用户信息
        # Label(frm, text='Watch path:', font=('Arial', 14)).grid(row=6,
        #                                                         column=0,
        #                                                         sticky='w',
        #                                                         padx=10)
        # Label(frm, text='OCR result file:',
        #       font=('Arial', 14)).grid(row=7, column=0, sticky='w', padx=10)

        # # 第6步，用户登录输入框entry
        # # 用户名
        # self.var_watch_path = StringVar()
        # self.var_watch_path.set(watch_path)
        # self.entry_watch_path = Entry(frm,
        #                               textvariable=self.var_watch_path,
        #                               width=20,
        #                               font=('Arial', 12)).grid(row=6,
        #                                                        column=1,
        #                                                        sticky='w',
        #                                                        padx=10)

        # # 用户密码
        # self.var_ocr_result = StringVar()
        # self.var_ocr_result.set(ocr_result_save_path)
        # self.entry_ocr_result = Entry(frm,
        #                               textvariable=self.var_ocr_result,
        #                               width=20,
        #                               font=('Arial', 12)).grid(row=7,
        #                                                        column=1,
        #                                                        sticky='w',
        #                                                        padx=10)

        # frm.place(x=6, y=2)
        # self.root.mainloop()

    def button_start_OCR_service_click(self):
        snip.start_snipaste(self.watch_path)
        self.start_watchdog()
        self.log('Start OCR service success!')

    def button_stop_OCR_service_click(self):
        snip.stop_snipaste()
        self.stop_watchdog()
        self.log('Stop OCR service success!')

    def start_watchdog(self):
        if self.watchdog is None:
            self.watchdog = Watchdog(path=self.watch_path,
                                     logfunc=self.log,
                                     ocrfunc=self.OCR_results)
            self.watchdog.start()
            self.log('Watchdog started')
        else:
            self.log('Watchdog already started')

    def stop_watchdog(self):
        if self.watchdog:
            self.watchdog.stop()
            self.watchdog = None
            self.log('Watchdog stopped')
        else:
            self.log('Watchdog is not running')

    @staticmethod
    def update_entry_text(e, text):
        e.delete(0, tk.END)
        e.insert(0, text)
        return

    def btn_ask_watch_path_click(self):
        path = filedialog.askdirectory()
        if path:
            self.update_entry_text(self.entry_watch_path, path)
            self.watch_path = path
            self.log(f'Selected watch path: {path}')

    def btn_ask_ocr_ret_path_click(self):
        path = filedialog.asksaveasfilename()
        if path:
            self.update_entry_text(self.entry_ocr_ret, path)
            self.ocr_result_save_path = path
            self.log(f'Selected OCR result path: {path}')

    def log(self, message):
        self.text_messagebox.insert(tk.END, f'{message}\n')
        self.text_messagebox.see(tk.END)

    def OCR_results(self, message):
        self.textbox_OCR_results.insert(tk.END, f'{message}\n\n')
        self.textbox_OCR_results.see(tk.END)


if __name__ == '__main__':
    GUI()