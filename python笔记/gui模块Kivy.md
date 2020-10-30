## 简介
Kivy 是一个开源的 Python 框架，用于快速开发应用，实现各种当前流行的用户界面，比如多点触摸等等。  
Kivy 可以运行于 Windows， Linux， MacOS， Android， iOS 等当前绝大部分主流桌面/移动端操作系统。只需编写一套代码，便可运行于各大桌面及移动平台上

## 下载模块
#保证pip和wheel是最新
python -m pip install --upgrade pip wheel setuptools
#安装必要依赖包
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer --extra-index-url https://kivy.org/downloads/packages/simple/
#安装kivy
python -m pip install kivy

## 导入

## 创建应用
    import kivy
    kivy.require('1.0.6') # 注意要把这个版本号改变成你现有的Kivy版本号!

    from kivy.app import App # 译者注：这里就是从kivy.app包里面导入App类.从这看,可以看出和安卓有些类似
    from kivy.uix.label import Label # 译者注：这里是从kivy.uix.label包中导入Label控件，这里都注意开头字母要大写."kivy.uix"这个包的作用是容纳用户界面元素，比如各种输出布局和控件

    class MyApp(App):

        def build(self): # 译者注：这里是实现build()方法
            return Label(text='Hello world') # 译者注：在这个方法里面使用了Label控件

    if __name__ == '__main__':
        MyApp().run() # 译者注：这里就是运行了。也是程序入口

(如果只是做一个简单脚本的界面,我没必要使用额外模块,学习该模块细节,并且中文文档少,所以暂时放弃,转向其他模块吧)
