一种，直接建立链接，一般针对文件夹
使用命令

    ln -s 目标文件夹绝对路径 生成的链接放在哪个链接（一般是 ~/桌面/XXX ）

另一种，是需要sh XXX.sh 来启动的应用，建立桌面快捷方式
1.在桌面（或其他目录）建立后缀为 .desktop 的文件
2.在文件中添加以下内容

    [Desktop Entry]
    Encoding=UTF-8
    Name=Postman #软件名
    Comment=Postman Makes API Development Simple  #简介
    Exec="/home/xiao/Postman/app/Postman" #启动命令全路径
    Icon=/home/xiao/Postman/app/resources/app/assets/icon.png #图标全路径
    Version=1.0
    Type=Application
    Terminal=0
可以将上面的注释进行删除
3.对创建好的桌面快捷方式，右键，属性，权限，勾选“允许作为程序执行文件”
