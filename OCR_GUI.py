'''
@#!/usr/bin/env: Python3.7.6
@# -*- encoding: utf-8-*-
@Description: construct a OCR GUI 
@Author: Allen
@Date: 2020-03-31 16:44:54
@LastEditTime: 2020-04-16 12:05:39
@LastEditors: Allen
'''
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pickle
import os
from PIL import Image, ImageTk
from snipaste import start_snipaste
from watch_dog import start_watchdog
# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('Wellcome to Hongwei Website')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('400x300')  # 这里的乘是小x

# 第4步，加载 wellcome image
# 绝对路径，注意要获取到项目根目录，若文件不在根目录下，需要调整
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = cur_path[:cur_path.find("src") + len("src")]
fpath = os.path.join(root_path, 'images', 'demo_icon.jpg')
print(fpath)
bg_img = Image.open(fpath)
photo = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(window, width=400, height=135, bg='green')
# image_file = tk.PhotoImage(file=fpath)#just support .gif and .bmp
image_file = photo
image = canvas.create_image(200, 0, anchor='n', image=image_file)
canvas.pack(side='top')
tk.Label(window, text='Wellcome', font=('Arial', 16)).pack()

# 第5步，用户信息
tk.Label(window, text='User name:', font=('Arial', 14)).place(x=10, y=170)
tk.Label(window, text='Password:', font=('Arial', 14)).place(x=10, y=210)

# 第6步，用户登录输入框entry
# 用户名
var_usr_name = tk.StringVar()
var_usr_name.set('example@python.com')
entry_usr_name = tk.Entry(window,
                          textvariable=var_usr_name,
                          font=('Arial', 14))
entry_usr_name.place(x=120, y=175)
# 用户密码
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window,
                         textvariable=var_usr_pwd,
                         font=('Arial', 14),
                         show='*')
entry_usr_pwd.place(x=120, y=215)


def cfg_snipaste(btn, action):
    if btn:
        btn.config(state=tk.DISABLED)
        action()


def start_ocr_service(btn, action):
    if btn:
        btn.config(state=tk.DISABLED)
        action()


# 第7步，login and sign up 按钮
btn_start_ocr = tk.Button(
    window,
    text='启动OCR服务',
)
btn_start_ocr.config(
    command=lambda: start_ocr_service(btn_start_ocr, start_watchdog))
btn_start_ocr.place(x=120, y=240)

# start snipaste
btn_start_snipaste = tk.Button(
    window,
    text='启动截图软件',
)
btn_start_snipaste.config(
    command=lambda: cfg_snipaste(btn_start_snipaste, start_snipaste))
btn_start_snipaste.place(x=280, y=240)

# 第10步，主窗口循环显示
window.mainloop()