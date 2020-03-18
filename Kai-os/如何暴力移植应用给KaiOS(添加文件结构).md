---
title: '''如何暴力移植应用给KaiOS'''
date: 2020-03-07 13:42:37
tags:
---

**注意:本教程仅适用于单一且元素简单的网页（如简单的在线音乐播放器）移植时要注意带上原作者。**

1.在任意目录下新建文件夹，用来做应用的根目录

2.将需要移植的网页另存为到新建的文件夹里；（以**网易云音乐随机播放器**为例，**原作者：墨渊**）

3.在文件夹中新建mainfest.webapps,使用编辑器打开，参照[这里](https://developer.kaiostech.com/getting-started/main-concepts/manifest)

***Tip:里面的路径根目录"/"指的是文件夹的根目录，如文件夹下的index.html路径就是/index.html***

4.至此，你的应用已经可以通过webIDE安装了！*（不保证正常使用）*

5.如果需要用omniSD/GerdaPkg安装请按照以下步骤；

6.将文件夹内的文件**（注：非文件夹）**压缩为application.zip；

7.新建metadata.json文件，填入以下内容：

```
{"version": 1, "manifestURL": "这里填任意网址，且与现有应用的不重复"}
#这个回车似乎必须有
```

8.将application.zip和metadata.json压缩为zip即可在omnisd或gerdapkg安装了。

具体目录结构为：

Myapp.zip{

​		application.zip{

​				manifest.webapp

​				index.html

​				icon.png//需要56,和112两种格式，必备！

​				。。。还有其他js之类的

​		}

​		metadata.json

}