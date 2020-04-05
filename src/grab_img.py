#导入相应的库
from tkinter import *    #界面库
from PIL import ImageGrab  #图形库
from tkinter import filedialog #保存文件对话框
import PyHook3      #获得坐标
import pythoncom


hm = PyHook3.HookManager()  #初始化钩子对象

def OnMouseDownEvent(event):
    """Return start coordinate"""
    global start_x
    global start_y
    start_x,start_y = event.Position  #得到初始点的x,y坐标
    return True

def OnMouseUpEvent(event):
    """Return end coordinate"""
    end_x,end_y = 0,0
    end_x,end_y = event.Position
    hm.UnhookMouse()
    bbox = (start_x,end_y,end_x,start_y)  #顺序不能乱--
    screen = ImageGrab.grab(bbox)         # 默认全屏
    filesave = filedialog.asksaveasfilename() #添加文件保存对话框
    screen.save(filesave)  #保存对应文件
    root.quit()  #关闭窗口
    return True

def ScreenShoot():
    """ Return screen shot """
    hm.MouseLeftDown = OnMouseDownEvent
    hm.MouseLeftUp = OnMouseUpEvent
    hm.HookMouse()
    pythoncom.PumpMessages()

def ScreenShootAllGraph():
    """ Return all Screen"""
    root.wm_minsize(0,0)
    screen = ImageGrab.grab()         # 默认全屏
    filesave = filedialog.asksaveasfilename() #添加文件保存对话框
    screen.save(filesave)  #保存对应文件
    root.quit()  #关闭窗口

# 初始化tkinter
root = Tk()
root.title("YTouch截图 1.0")
root.geometry('300x400')  #窗口大小：宽*高
root.resizable(width=True, height=True) #设置宽高不可变

""" 截图按钮 """
btn_ScreenShot = Button(root,text="开始截图",command=ScreenShoot)
btn_ScreenShot.place(width=90,height=30,x=20,y=300)

""" 截图全图 """
btn_ScreenAllShot = Button(root,text="截取全图",command=ScreenShootAllGraph)
btn_ScreenAllShot.place(width=90,height=30,x=130,y=300)

root.mainloop()
