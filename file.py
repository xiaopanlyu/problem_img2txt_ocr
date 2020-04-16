'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: 
@Author: Allen
@Date: 2020-04-16 16:50:06
@LastEditTime: 2020-04-16 16:52:11
@LastEditors: Allen
'''
import os


class File(object):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    watch_path = os.path.join(cur_path, 'images').replace('\\', '/')
    save_path = os.path.join(cur_path, 'ocr_text.txt').replace('\\', '/')


file = File()
