'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-02-27 03:35:08
@LastEditTime: 2020-04-13 22:18:39
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
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class RealOCRWatchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path='.', patterns='*', logfunc=print, ocrfunc=print):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=False)
        self.log = logfunc
        self.ocr_app = ocrfunc

    def on_created(self, event):
        # This function is called when a file is created
        self.log(f"hey, {event.src_path} has been created!")
        self.ocr_app(event.src_path)

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
