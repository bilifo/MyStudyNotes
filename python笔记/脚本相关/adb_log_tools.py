import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Widget
import subprocess
import re
import time
import asyncio
import typing
import os

save_path="D:/"


class Device:
    name=""#
    cmd=None
    
class DeviceFactory:
    devs:Device={}
    def __init__(self,array):
        for value in array:
            if(value in self.devs):
                pass
            else:
                dev=Device()
                dev.name=value
                cmd=None
                self.devs[value]=dev

    

class PyWinDesign:
    #由于点击事件的交互逻辑,依赖界面,也依赖逻辑,不能在界面类里面写死实现,要作为接口对外暴露,像安卓一样
    class click_interface:#按键接口
        def button1_click(self,button_state):
            pass

        def onClick(self,event):
            pass
        
        def winColse(self):
            pass

    def __init__(self, window_init,click_interface):
        self.click_interface_new=click_interface
        self.window_init = window_init
        self.window_init.title('')
        self.window_init.resizable(width=False, height=False)
        screenwidth = self.window_init.winfo_screenwidth()
        screenheight = self.window_init.winfo_screenheight()
        size = '%dx%d+%d+%d' % (272, 121, (screenwidth - 272) / 2, (screenheight - 121) / 2)
        self.window_init.geometry(size)
        self.window_init.protocol('WM_DELETE_WINDOW', lambda : (self.click_interface_new.winColse(),self.window_init.destroy()))#修改窗口的关闭事件,lambda的多行语句
        
        self.mCombobox1 = ttk.Combobox(self.window_init,values=(), state='readonly')
        self.mCombobox1.bind('<Enter>',self.click_interface_new.onClick)
        self.mCombobox1.bind("<<ComboboxSelected>>",self.click_interface_new.onClick) #绑定事件
        self.mCombobox1.place(x=16,y=25,width=109,height=20)
        
        self.mButton1_title = tk.StringVar()
        self.mButton1_title.set('抓log')#button1的状态,是跟随所选设备的,这个状态一个被包含进devices类中,而不是button类中,UI里面的button,只需做好接受到0或1时,显示什么字符就好
        self.mButton1_state = 0
        self.mButton1 = tk.Button(self.window_init,textvariable=self.mButton1_title)
        self.mButton1.bind('<Button-1>',self.click_interface_new.onClick)
        self.mButton1.place(x=172,y=21,width=80,height=32)
        
        self.mButton2_title = tk.StringVar()
        self.mButton2_title.set('打开交互窗口')
        self.mButton2 = tk.Button(self.window_init,textvariable=self.mButton2_title)
        self.mButton2.bind('<Button-1>',self.click_interface_new.onClick)
        self.mButton2.place(x=30,y=69,width=225,height=33)
    
    def setComboboxValue(self,mArray):
        self.mCombobox1['value']=mArray

    def getComboboxValue(self):
        return self.mCombobox1.get()

    def button1_on(self):
        self.mButton1_title.set('结束log')

    def button1_off(self):  
        self.mButton1_title.set('抓log')

    #def button_change(self,button_state):#可以将 button1_on 和 button1_off 捏合成一个方法对外暴露,让使用者只关心这个方法而不需要关心on和off,但根据奥卡姆剃刀原则,我不打算增加这个方法

        

class Logic:

    def getDevices_str(self):#使用adb devices获得连接设备 ,正则处理命令运行返回的结果,获得各种设备
        (status, output)=subprocess.getstatusoutput('adb devices')
        regular=r'\w+(?!\W+devices)(?=\W+device)'
        return_var=re.findall(regular,output)
        return return_var


    def cmd_logcat(self,device_name):
        return "adb -s "+device_name+" logcat -v time"

    def getSaveFile(self,device_name):
        return open(save_path+device_name+"_"+time.strftime("%Y_%m_%d_%H%M%S", time.localtime())+".txt", 'w')

    def addCmd(self,cmd_text,out_saveFile):
        print(cmd_text)
        p=subprocess.Popen(cmd_text, stdin=subprocess.PIPE,stdout=self.getSaveFile(out_saveFile), stderr=subprocess.PIPE,shell=False, close_fds=False)
        return p.pid

    def stopCmd(self,pid):
        subprocess.Popen("taskkill /F /T /PID " + str(pid) , shell=True)#使用 taskkill 来结束pid有效
    
    #新开cmd窗口执行命令mButton
    def cmd_click(self,cmd_text,out_saveFile):
        cmd="adb -s "+cmd_text+" shell\n"
        os.system("start cmd /k "+cmd)
        
    # def button1_click(self,button_state):#button的state,不应该由logic类来处理,这样的依赖,是不必要的,单纯的logic类,不需要依赖界面类


class Platform:#委托模式,处理界面类和logic的交互.
    popen_list={}#保存新建的命令popen,这个也应该是平台的事
    #由平台来实现点击事件接口click_interface,因为点击事件的交互逻辑,依赖界面,也依赖逻辑,这两个依赖,导致点击事件放在界面或逻辑中,都违背了单向依赖的原则
    class click_interface_new(PyWinDesign.click_interface):

        def onClick(self,event):
            if(event.widget.winfo_id()==Platform.mwin.mCombobox1.winfo_id()):#注意此时不能写self.mwin
                if(event.type==tk.EventType.Enter):
                    Platform.mwin.mCombobox1['values']=Platform.mlogic.getDevices_str()
                    Platform.df:DeviceFactory=DeviceFactory(Platform.mlogic.getDevices_str())                    
                elif(event.type==tk.EventType.VirtualEvent):
                    device=Platform.mwin.getComboboxValue()#获得下拉框当前选中
                    if(Platform.df.devs[device].cmd==None):
                        Platform.mwin.button1_off()
                    else:                    
                        Platform.mwin.button1_on()

            if(event.widget.winfo_id()==Platform.mwin.mButton2.winfo_id()):#注意此时不能写self.mwin
                device=Platform.mwin.getComboboxValue()
                Platform.mlogic.cmd_click(device,Platform.mlogic.getSaveFile(device))
                # asyncio.run(Platform.mlogic.cmd_click(device,Platform.mlogic.getSaveFile(device)))
            if(event.widget.winfo_id()==Platform.mwin.mButton1.winfo_id()):
                device=Platform.mwin.getComboboxValue()#获得下拉框当前选中

                if(Platform.df.devs[device].cmd==None):
                    pid=Platform.mlogic.addCmd(Platform.mlogic.cmd_logcat(device),device)
                    Platform.popen_list[device]=pid
                    Platform.mwin.button1_on()
                    Platform.df.devs[device].cmd=pid
                else:
                    Platform.mlogic.stopCmd(Platform.popen_list[device])
                    Platform.popen_list.pop(device)
                    Platform.mwin.button1_off()
                    Platform.df.devs[device].cmd=None 


        def winColse(self):            
            print("close all")
            Platform.stopAllCmd(Platform)
            
           
    def __init__(self, win,logic):
        Platform.mwin=win
        Platform.mlogic=logic

     #停止所有日志
    def stopAllCmd(self):
        if(len(self.popen_list)>0):
            for i in range(len(self.popen_list)):
                print(""+str(self.popen_list[i])+" stop")
                # popen_list[i].terminate()#实验证明是无效的
                # popen_list[i].kill()#实验证明是无效的
                Platform.mlogic.stopCmd(str(self.popen_list[i]))

if __name__ == '__main__':
    root = tk.Tk()
    click=Platform.click_interface_new()
    logic=Logic()
    app=PyWinDesign(root,click)
    platform=Platform(app,logic)


    root.mainloop()