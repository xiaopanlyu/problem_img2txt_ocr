'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-02-27 03:35:08
@LastEditTime: 2020-04-03 01:27:29
@LastEditors: Allen
'''
#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Allen
@file: watch_dog.py
@function:
@time: 2020/02/27
software: PyCharm
"""
import time

from watchdog.events import *
from watchdog.observers import Observer
from ocr_method_api.baidu_aip import baidu_aip_ocr

cur_path = os.path.abspath(os.path.dirname(__file__))
watch_path = os.path.join(cur_path, 'images')
ocr_result_save_path = os.path.join(cur_path, 'ocr_text.txt')


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(
                event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,
                                                      event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            try:
                general_text = baidu_aip_ocr(event.src_path)

                with open('%s' % (ocr_result_save_path), 'a',
                          encoding='utf-8') as f:
                    f.write("{}\n".format(general_text))
                    f.close()
                # print("{}\n".format(general_text))
            except:
                print("some errors happened!")
                return

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))


def watching(watch_path):
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, watch_path, True)
    observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    observer.join()


def start_watchdog():

    # watch_path = 'D:/xiaopanlyu_phd/code/problem_img2txt_ocr/src/images'
    watching(watch_path)


if __name__ == "__main__":
    start_watchdog()
