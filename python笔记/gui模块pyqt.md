选择理由:听说能拖拽生成界面,使用的人多,教程有专门的中文网站
放弃原因:预装环境已经很折磨人了,装完后还发现转py不行,这让我思考,我是要学一种基于python的gui框架,还是学一种使用python的gui工具

创建一个空窗口:

    import sys
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtGui import QIcon

    class Example(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI() #界面绘制交给InitUi方法

        def initUI(self):
            #设置窗口的位置和大小
            self.setGeometry(300, 300, 300, 220)  
            #设置窗口的标题
            self.setWindowTitle('Icon')
            #设置窗口的图标，引用当前目录下的web.png图片
            self.setWindowIcon(QIcon('web.png'))        
            # otherUI(self)......在这里添加其他控件,我虚拟了一个otherUI的方法,后面其他控件的初始化,均假设发在该方法内,减少每次重复的窗口代码
            #显示窗口
            self.show()

    if __name__ == '__main__':
        #创建应用程序和对象
        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_()) 

创建一个button和控件提示:

    def otherUI(self):
        #这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))
        #创建一个窗口tooltip说明，我们称之为settooltip()方法。我们可以使用丰富的文本格式
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        #创建一个PushButton并为他设置一个tooltip说明
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        #设置点击功能为窗口退出
        btn.clicked.connect(QCoreApplication.instance().quit)
        #btn.sizeHint()显示默认尺寸
        btn.resize(btn.sizeHint())
        #移动窗口的位置
        btn.move(50, 50)

创建一个信息框和重写窗口关闭事件:

        def closeEvent(self,event):#关闭窗口的时候,触发了QCloseEvent。重写closeEvent()事件处理程序。
        #第一个参数是标题名。第二个参数消息对话框中显示的文本。第三个参数指定按钮的组合出现在对话框中。最后一个参数是默认按钮，这个是默认的按钮焦点。
            reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) 
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

            