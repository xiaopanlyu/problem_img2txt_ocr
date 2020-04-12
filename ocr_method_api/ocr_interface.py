#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:Allen
@file: ocr_interface.py
@function:
@time: 2020/03/06
software: PyCharm
"""
class OCR_BASE(object):
    def set_parameters(self):
        raise NotImplementedError

    def request_ocr_service(self):
        raise NotImplementedError

    @classmethod
    def read_file(image_path):
        f = None
        try:
            f = open(image_path, 'rb')
            return f.read()
        except:
            print('read image file fail')
            return None
        finally:
            if f:
                f.close()


