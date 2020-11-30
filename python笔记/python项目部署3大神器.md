### pip 包管理工具(python自带)

### virtualenv 独立的python环境管理 (环境虚拟机)
比如一个项目依赖Django1.3 而当前全局开发环境为Django1.7, 版本跨度过大, 导致不兼容使项目无法正在运行, 使用virtualenv可以解决这些问题.

安装

    pip install virtualenv

基本使用

    virtualenv XXX  #创建一个名为‘XXX’的虚拟环境，并在当前目录下新建同名文件夹

    source XXX/bin/activate  #激活并使用虚拟环境(linux下)
    XXX\scripts\activate 或 直接进入到activate所在目录，使用.\activate激活(win下)
    
    deactivate  #退出虚拟环境

    创建时,virtualenv拷贝了Python可执行文件的副本，并创建一些有用的脚本和安装了项目需要的软件包.当启用虚拟环境后,安装包时，它们被安装在当前活动的virtualenv里，而不是系统范围内的Python路径。

### fabric 服务器管理和应用发布 ()