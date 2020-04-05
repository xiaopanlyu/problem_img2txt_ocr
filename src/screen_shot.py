import pyautogui as pg

from PIL import Image

from PyQt5.QtWidgets import QPushButton, QFileDialog, QFrame
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
import cv2
import sys, os


class MyLabel(QLabel):
    '''鼠标选择框'''
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        self.xy_l = event.pos()
        global x_l, y_l
        x_l = self.xy_l.x()
        y_l = self.xy_l.y()
        # return self.x_l, self.y_l

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False
        self.xy_r = event.pos()
        global x_r, y_r
        x_r = self.xy_r.x()
        y_r = self.xy_r.y()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, (self.x1 - self.x0), (self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, .5, Qt.SolidLine))
        painter.drawRect(rect)


class Main(QWidget):
    '''主窗体'''

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        '''窗体GUI部分'''

        # 设置窗体大小
        self.setGeometry(300, 300, 300, 50)
        # 窗体Title
        self.setWindowTitle('PyAutoGui截图工具')
        # 窗体图标
        # self.setWindowIcon(QIcon('c:/ICON/666043.png'))
        # 禁止窗口最大化和拉伸
        self.setFixedSize(self.width(), self.height())
        # 设置窗体置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.closeEvent(self, QCloseEvent=exit())
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        # 创建新建按钮
        self.btn_new = QPushButton('新建(N)', self)

        # 设定按钮图标
        # self.btn_new.setIcon(QIcon('c:/ICON/1271658.png'))
        # 创建按钮并移动到指定位置
        self.btn_new.move(10, 10)
        self.btn_new.setFixedSize(140, 30)
        # 点击按钮，连接事件函数
        self.btn_new.clicked.connect(self.set_btnnew_action)
        # self.btn_new.clicked.connect(self.output_dialog)

        # 创建结束按钮
        self.btn_quit = QPushButton('结束', self)
        # 设定按钮图标
        # self.btn_quit.setIcon(QIcon('c:/ICON/1271658.png'))
        # 创建按钮并移动到指定位置
        self.btn_quit.move(150, 10)
        self.btn_quit.setFixedSize(140, 30)
        # 点击按钮，连接事件函数
        self.btn_quit.clicked.connect(self.quit_app)
        self.btn_quit.clicked.connect(QApplication.quit)
        # self.btn_quit.clicked.connect(self.cut_pic)

        # 标签框用于存放文件路径
        self.lab_select_path = QLabel('文件路径', self)
        self.lab_select_path.move(150, 230)
        self.lab_select_path.setFixedSize(320, 20)
        self.lab_select_path.setFrameShape(QFrame.Box)
        self.lab_select_path.setFrameShadow(QFrame.Raised)

    def quit_app(self):
        '''删除屏幕截图'''
        my_file = 'screenshot.png'  # 文件路径
        if os.path.exists(my_file):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(my_file)  # 则删除

    def set_btnnew_action(self):
        if self.btn_new.text() == '新建(N)':
            self.get_screenshot()
            self.btn_new.setText('保存路径')
            self.btn_new.setIcon(QIcon('c:/ICON/436496.png'))

        elif self.btn_new.text() == '保存路径':
            self.output_dialog()
            self.btn_new.setText('保存')

        else:
            self.btn_new.setText('新建(N)')
            path = self.lab_select_path.text()
            self.cut_pic(path)
            # self.cl = CutPic()
            # self.cl.close(self)

    def output_dialog(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self, '选取文件', './', "Files (*.png)")
        self.lab_select_path.setText(fileName_choose)
        self.btn_new.setText('保存')
        return fileName_choose

    def get_screenshot(self):
        '''屏幕截图'''
        # 隐藏Main窗体
        self.hide()
        # 截屏
        pg.screenshot('screenshot.png')
        # 显示窗体
        self.show()

        # 虚化图片
        def addTransparency(img, factor=0.7):
            img = img.convert('RGBA')
            img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
            img = Image.blend(img_blender, img, factor)
            return img

        # img = Image.open('pics/screenshot.png')
        # img = addTransparency(img, factor=0.8)
        # img.save('pics/screenshot.png', 'png')

    def cut_pic(self, path):
        '''
        截取图片到指定位置
        :param path: 图片保存路径
        :param mouse_position_l: 左上角坐标
        :param mouse_position_r: 右下角坐标
        :return:返回截取的图像
        '''
        xl = x_l
        yl = y_l
        xr = x_r
        yr = y_r
        if xl > xr:
            xl, xr = xr, xl
            yl, yr = yr, yl
        # -4是要去掉边框
        width = xr - xl - 4
        height = yr - yl - 4
        pic = pg.screenshot(path, region=(xl + 2, yl + 2, width, height))
        return pic

    # 检测键盘回车按键，函数名字不要改，这是重写键盘事件
    def keyPressEvent(self, event):
        # todo 这里是测试代码
        # 这里event.key（）显示的是按键的编码
        print("按下：" + str(event.key()))
        # 举例，这里Qt.Key_A注意虽然字母大写，但按键事件对大小写不敏感
        if (event.key() == Qt.Key_Escape):
            print('测试：ESC')
        if (event.key() == Qt.Key_A):
            print('测试：A')
        if (event.key() == Qt.Key_1):
            print('测试：1')
        if (event.key() == Qt.Key_Enter):
            print('测试：Enter')
        if (event.key() == Qt.Key_Space):
            print('测试：Space')
        # 当需要组合键时，要很多种方式，这里举例为“shift+单个按键”，也可以采用shortcut、或者pressSequence的方法。
        # if (event.key() == Qt.Key_P):
        #     if QApplication.keyboardModifiers() == Qt.CTRL:
        #         print("ctrl + p")
        #     else:
        #         print("p")

        # todo 这个是快捷键代码
        # 执行新建操作
        # Shift + N
        # if (QApplication.keyboardModifiers() == Qt.ShiftModifier and event.key() == Qt.Key_N):
        #     self.btn_new.click()
        # Ctrl + N
        if (QApplication.keyboardModifiers() == Qt.ControlModifier and event.key() == Qt.Key_N):
            self.btn_new.click()


class CutPic(QWidget):
    '''剪切图片遮罩层（也是一个窗体）'''

    def __init__(self):
        super().__init__()

    def init_ui(self):
        '''这部分代码是我从CSDN拷贝的，OpenCV我也不是很懂，所以直接借用了'''

        # 重定义的label
        self.lb = MyLabel(self)
        img = cv2.imread('screenshot.png')

        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.lb.setPixmap(pixmap)
        self.lb.setCursor(Qt.CrossCursor)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    child = CutPic()
    # 显示主窗体
    main.show()
    # 点击主窗体按钮后调用鼠标选框并加载屏幕截图
    btn = main.btn_new
    btn.clicked.connect(child.init_ui)
    # 再最大化窗体
    btn.clicked.connect(child.showFullScreen)
    # main.btn_quit.connect(QApplication.quit)
    sys.exit(app.exec_())
