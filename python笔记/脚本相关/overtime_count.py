#-*- coding: utf-8 -*-
import xlwings as xw
import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import datetime
import time
import re

# 需求:对某个部门进行员上班时常统计表进行加班时间计算
# 技术:1/xlwings 对表的操作
#     2/文件路径的正确获得,以及乱码路径解决
#     3/字符串转日期 datetime 的使用

部门所在列='C5'
过滤软件部="软件部"

class PyWinDesign:
    def __init__(self, 启动窗口):
        self.启动窗口 = 启动窗口
        self.启动窗口.title('')
        self.启动窗口.resizable(width=False, height=False)
        screenwidth = self.启动窗口.winfo_screenwidth()
        screenheight = self.启动窗口.winfo_screenheight()
        size = '%dx%d+%d+%d' % (333, 210, (screenwidth - 333) / 2, (screenheight - 210) / 2)
        self.启动窗口.geometry(size)
        
        self.input1_内容 = tk.StringVar()
        self.input1_内容.set('')
        self.input1 = tk.Entry(self.启动窗口,textvariable=self.input1_内容,justify=tk.LEFT) #注意使用 Entry 当输入框,而不要使用 Text
        self.input1.insert(tk.END,'表单地址')
        self.input1.place(x=58,y=17,width=217,height=35)
        
        self.按钮1_标题 = tk.StringVar() 
        self.按钮1_标题.set('执行')
        self.按钮1 = tk.Button(self.启动窗口,textvariable=self.按钮1_标题)
        self.按钮1.bind('<Button-1>',self.click)
        self.按钮1.place(x=104,y=80,width=84,height=22)

        self.编辑框3 = tk.Text(self.启动窗口,wrap=tk.NONE) #注意vscode编辑器的字符格式,和输出窗口的字符格式.我的就是因为输出窗口格式不对,一直认为是编辑框获得的文本有问题
        self.编辑框3.insert(tk.END,'输出地址') 
        self.编辑框3.place(x=62,y=124,width=216,height=42)

    def click(self,event):
        # "C:\Users\panjunlong\Documents\WeChat Files\wxid_3qb1i64u9ij422\FileStorage\File\2021-03\2021年2月考勤-软件.xlsx"
        path=os.path.abspath(self.input1.get())#注意 os.path.abspath 获得的文件路径,且路径不能有前后引号
        print(path)
        path2=str(path)
        path3=path2.replace("\\","/") # 适用于win的路径转换
        try: 
            wb = xw.Book(r''+path3)
            sht = wb.sheets[0]

            list_rjb=找到所有软件部的人(sht)
            #iterate_value(list_rjb)#只是打印日志看看
            for i in list_rjb:
                员工数据第一行=i.row
                该员工数据最后行=0
                该员工数据占几行=0
                if i.merge_cells:#是合并单元格
                    该员工数据最后行=员工数据第一行 + i.merge_area.count-1
                    该员工数据占几行=i.merge_area.count
                else:
                    该员工数据最后行=员工数据第一行
                    该员工数据占几行=i.merge_area.count
                #插入新的两行,后面添加数据
                sht.api.Rows(该员工数据最后行+1).Insert()#在 某行 前添加一行
                sht.api.Rows(该员工数据最后行+1).Insert()

                for j in range(1,31):
                    员工数据列=i.column+j
                    员数据list=np.array(sht.range((员工数据第一行,员工数据列),(该员工数据最后行,员工数据列)).value)
                    员工有效数据最后行=员数据list[-1]
                    try: 
                        for i in range(len(员数据list),1):
                            if(not_empty(员数据list[i])):
                                员工有效数据最后行=员数据list[i]
                                break

                        if(not_empty(员工有效数据最后行) and not_empty(员数据list[0])):
                            时间间隔对象=(返回时间对象(员工有效数据最后行)-返回时间对象(员数据list[0]))
                            间隔分钟=时间间隔对象.total_seconds()/60-9*60 #由于两个 datetime 对象相减(也只能是两个,不能多个),得到的是 timedelta 对象,该对象只有 day , seconds , microseconds属性,没有分钟
                            
                            sht.range(该员工数据最后行+1,员工数据列).value=str("%02d:%02d"%(int(间隔分钟/60),int(间隔分钟%60))) #显示间隔小时,使用了%d格式化字符串的方式
                            # print("时间间隔:"+str("%2d:%2d"%(int(间隔分钟/60),int(间隔分钟%60))))
                            sht.range(该员工数据最后行+2,员工数据列).value=间隔分钟 #显示间隔分钟
                            if(间隔分钟<0):
                                sht.range(该员工数据最后行+2,员工数据列).color = (255,0,0)
                            
                    except Exception as e: #注意异常的使用
                        print(""+i.address+"数据异常")
                        sht.range(该员工数据最后行+1,员工数据列).value="数据异常"
            self.编辑框3.insert(tk.END,''+str(path3))# 处理打开异常
        except Exception as e:
            self.编辑框3.insert(tk.END,''+str(e))# 处理打开异常

# def test():
#     path=os.path.abspath(r"C:\Users\panjunlong\Documents\WeChat Files\wxid_3qb1i64u9ij422\FileStorage\File\2021-03\2021年2月考勤-软件.xlsx")
#     print(path)
#     path2=str(path)
#     path3=path2.replace("\\","/")

#     wb = xw.Book(r''+path3)
#     sht = wb.sheets[0]

#     list_rjb=找到所有软件部的人(sht)
#     #iterate_value(list_rjb)#只是打印日志看看
#     for i in list_rjb:
#         员工数据第一行=i.row
#         该员工数据最后行=0
#         该员工数据占几行=0
#         if i.merge_cells:#是合并单元格
#             该员工数据最后行=员工数据第一行 + i.merge_area.count-1
#             该员工数据占几行=i.merge_area.count
#         else:
#             该员工数据最后行=员工数据第一行
#             该员工数据占几行=i.merge_area.count
#         #每个人后面插入新的两行
#         sht.api.Rows(该员工数据最后行+1).Insert()#最后行新增一行
#         sht.api.Rows(该员工数据最后行+1).Insert()#再新增一行

#         for j in range(1,31):
#             员工数据列=i.column+j
#             员数据list=np.array(sht.range((员工数据第一行,员工数据列),(该员工数据最后行,员工数据列)).value)
#             员工有效数据最后行=员数据list[-1]
#             try: 
#                 for i in range(len(员数据list),1):
#                     if(not_empty(员数据list[i])):
#                         员工有效数据最后行=员数据list[i]
#                         break

#                 if(not_empty(员工有效数据最后行) and not_empty(员数据list[0])):
#                     间隔分钟=(返回时间对象(员工有效数据最后行)-返回时间对象(员数据list[0])).total_seconds()/60-9*60
#                     if(间隔分钟<0):
#                         sht.range(该员工数据最后行+1,员工数据列).color = (255,0,0)
#                     sht.range(该员工数据最后行+1,员工数据列).value=str(返回时间对象(员工有效数据最后行)-返回时间对象(员数据list[0])) #显示间隔小时
#                     sht.range(该员工数据最后行+2,员工数据列).value=间隔分钟 #显示间隔分钟
                       
#             except Exception as e:
#                 print(""+i.address+"数据异常")
#                 sht.range(该员工数据最后行+1,员工数据列).value="数据异常"
        
def not_empty(s):
	return s and s.strip()
        
def 返回时间对象(str_p):
    dateTime_p = datetime.datetime.strptime(str_p,'%H:%M')
    return dateTime_p #time2-time).total_seconds() 以分钟计算

# 通过固定的 C 列找到所有软件部的人
def 找到所有软件部的人(表单):
    部门=表单.range(部门所在列)
    list_部门=表单.range(部门,(表单.used_range.last_cell.row,部门.column))
    list_return=仅保留(list_部门,过滤软件部)
    return list_return

def 过滤(list,filter_str):# 排除过滤
    list_return=[]
    for j in list:
        if j.value ==None or j.value =="" or len(j.value)==0 or j.value==filter_str:
            continue
        else:
            list_return.append(j)
    return list_return

def 仅保留(list,filter_str):# 只保留
    list_return=[]
    for j in list:
        if j.value==filter_str:
            list_return.append(j)
    return list_return

def iterate_value(list):
    for i in list:
        print(i.value)

if __name__ == '__main__':
    root = tk.Tk()
    app = PyWinDesign(root)
    root.mainloop()

    #test()




