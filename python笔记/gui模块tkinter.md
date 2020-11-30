当时选择的理由:Tkinter是python内置的,这就足够了.反正我只是用来写写脚本小工具
后面放弃的理由:没有拖拽式的控件放置,写个规矩点的布局都需要好久,还有控件功能简单,有坑
再次入坑的理由:其他模块同样有坑,而且需要环境,需要依赖,还不如tk.其实主要是我找到了能界面放置控件的辅助工具----PyWinDesign (https://bbs.125.la/thread-14519599-1-1.html)

|tkinter类|元素|
|-|-|
|Button|按钮|
|Canvas|画布|
|Checkbutton|复选框|
|Entry|单行输入框|
|Frame|框架|
|Label|标签|
|LabelFrame|容器控件|
|Listbox|列表框|
|Menu|菜单|
|Menubutton|菜单按钮|
|Message|消息框|
|OptionMenu|选择菜单|
|PanedWindow|窗口布局|
|Radiobutton|单选框|
|Scale|进度条|
|Scrollbar|滚动条|
|Spinbox|指定输入框|
|Text|多行输入框|
|Toplevel|顶层,提供窗口管理接口|
|messageBox|消息框|

所有控件都继承自BaseWidget类,使用winfo_id()可以获得控件id.(http://visionegg.sourceforge.net/reference/Tkinter.BaseWidget-class.html)

## 简单示例讲解创建过程
首先要创建一个主窗口，就像作画一样，先要架好架子和画板，然后才能在上面放画纸和各种绘画元素，创建好主窗口才能在上面放置各种控件元素。

    import tkinter as tk  # 使用Tkinter前需要先导入
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()    
    # 第2步，给窗口的可视化起名字
    window.title('My Window')   
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('500x300')  # 这里的乘是小x 

    # 第4步，在图形界面上设定标签
    l = tk.Label(window, text='你好！this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)
    # 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高    

    # 第5步，放置标签
    l.pack()    # Label内容content区域放置位置，自动调节尺寸
    # 放置lable的方法有：1）l.pack(); 2)l.place();  

    # 第6步，主窗口循环显示
    window.mainloop()
    # 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
    # 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。

## 部分控件详解
注意:所有控件都有回调响应,command.所有的控件都有textvariable可更改的双向文本,variable可更改的值,onvalue为on是的状态,offvalue为off时的状态.但是textvariable好像不能起效果
### Button

    b = tk.Button(tkinter.Tk() 或 父控件, text="hit me", command=hit_me) #command接按钮按下的事件实现函数

### Entry

    e1 = tk.Entry(tkinter.Tk() 或 父控件, show='*', font=('Arial', 14))   # 显示成密文形式
    e2 = tk.Entry(tkinter.Tk() 或 父控件, show=None, font=('Arial', 14))  # 显示成明文形式
    text=e1.get() #获得输入内容

### Text

    t = tk.Text(tkinter.Tk() 或 父控件, height=3) #指定height=3为文本框是三个字符高度

### Scale

    #定义一个触发函数功能,该函数自带传入参数v
    def print_selection(v):
        l.config(text='you have selected ' + v)

    #创建一个尺度滑条，长度200字符，从0开始10结束，以2为刻度，精度为0.01，触发调用print_selection函数
    s = tk.Scale(tkinter.Tk() 或 父控件, label='try me', from_=0, to=10, orient=tk.HORIZONTAL, length=200, showvalue=0,tickinterval=2, resolution=0.01, command=print_selection)

### Listbox

    #静态添加list数据        
    var2 = tk.StringVar() #为什么要用StringVar()封装的数组类型,因为这种类型带点击焦点
    var2.set((1,2,3,4)) # 为变量var2设置值

    lb = tk.Listbox(tkinter.Tk() 或 父控件, listvariable=var2)  #将var2的值赋给Listbox

    #动态添加list的数据
    list_items = [11,22,33,44]
    for item in list_items:
        lb.insert('end', item)  # 从最后一个位置开始加入值
    lb.insert(1, 'first')       # 在第一个位置加入'first'字符
    lb.insert(2, 'second')      # 在第二个位置加入'second'字符
    lb.delete(2)                # 删除第二个位置的字符

    value = lb.get(lb.curselection())   # 获取当前选中的文本

### messageBox

    messagebox.showinfo(title='Hi', message='你好！')            # 提示信息对话窗

    messagebox.showwarning(title='Hi', message='有警告！')       # 提出警告对话窗

    messagebox.showerror(title='Hi', message='出错了！')         # 提出错误对话窗

    print(messagebox.askquestion(title='Hi', message='你好！'))  # 询问选择对话窗return 'yes', 'no'

    print(messagebox.askyesno(title='Hi', message='你好！'))     # return 'True', 'False'

    print(messagebox.askokcancel(title='Hi', message='你好！'))  # return 'True', 'False'

### Checkbutton

    w = Checkbutton ( tkinter.Tk() 或 父控件, option=value, ... )#master: 按钮的父容器。options: 可选项，即该按钮的可设置的属性。这些选项可以用键 = 值的形式设置，并以逗号分隔。option的选择有很多,常用的variable控制变量,state组件的状态(正常：normal 禁用：disabled),selectcolor选中框内的颜色
    eg:
    v1 = tk.IntVar() #定义变量,有两个方法：.get()获取值， .set()设置值
    c1 = tk.Checkbutton(frame, text="北京", variable=v1, onvalue=1, offvalue=0) #创建控件,onvalue=1 表示 v1值为1时是选上
    c1.grid(row=0, column=0) #定位子
    #c1.select() #设置为选中
    #c1.delect() #设置为未选中
    #c1.toggle() #切换选中状态
    v1.get() #获得状态


### Menu和Menu item
menu支持窗口上方出现管理菜单,也可以右键弹出菜单

menubar = Menu(tkinter.Tk() 或 父控件,tearoff=False)#创建一个菜单
menubar.delete(0,END)#清空菜单
menubar.add_command(label='剪切',command=lambda: cut(editor))#添加子菜单
menubar.add_command(label='复制',command=lambda: copy(editor))
menubar.add_command(label='粘贴',command=lambda: paste(editor))
menubar.post(event.x_root, event.y_root)#菜单控件显示位置

右键菜单:
    控件.bind("<Button-3>", lambda x: 右键菜单(x, 参数)) # x是子菜单序号

### combobox下拉菜单

    combox = tk.Combobox(父控件)
    combox['values'] = (1, '2', ...)     # 设置下拉列表的值
    combox.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
    cmb.bind("<<ComboboxSelected>>",点击事件的def方法) #绑定事件

    cmb.get()   #获得当前选择值

### Frame绘制区
类似安卓的fragment
    frame = tk.Frame(父控件, bg="blue")
    frame.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.4) #绘制区域
    

## 控件放置方式
1. grid() 是方格, 所以所有的内容会被放在这些规律的方格中  

        tk.Label(window, text=1).grid(row=i, column=j, padx=10, pady=10, ipadx=10, ipady=10)
        #grid 就是用表格的形式定位的。这里的参数 row 为行，colum 为列，padx 就是单元格左右间距，pady 就是单元格上下间距，ipadx是单元格内部元素与单元格的左右间距，ipady是单元格内部元素与单元格的上下间距。

|参数|作用|
|-|-|
|column |指定组件插入的列（0 表示第 1 列）默认值是 0|
|columnspan |指定用多少列（跨列）显示该组件|
|row |指定组件插入的行（0 表示第 1 行）|
|rowspan |指定用多少行（跨行）显示该组件|
|in_|将该组件放到该选项指定的组件中,指定的组件必须是该组件的父组件
|ipadx  |水平方向上的内边距|
|ipady  |垂直方向上的内边距|
|padx |水平方向上的外边距|
|pady |垂直方向上的外边距|
|sticky |控制组件在 grid 分配的空间中的位置,可以使用 tk.N, tk.E, tk.S, tk.W 以及它们的组合来定位（ewsn代表东西南北，上北下南左西右东）,使用加号（+）表示拉长填充，例如 "n" + "s" 表示将组件垂直拉长填充网格，"n" + "s" + "w" + "e" 表示填充整个网格,不指定该值则居中显示选项 含义|

2. pack(), 他会按照上下左右的方式排列
注意：不要试图在一个主窗口中混合使用pack和grid
它的排列取决于上一个兄弟控件,即P2是在P1使用空间外的另外未使用空间的下面,P3是在P2使用空间外的另外未使用空间的左边
        tk.Label(window, text='P1', fg='red').pack(side='top')    # 上
        tk.Label(window, text='P2', fg='red').pack(side='bottom') # 下
        tk.Label(window, text='P3', fg='red').pack(side='left')   # 左
        tk.Label(window, text='P4', fg='red').pack(side='right')  # 右  

|参数|作用|
|anchor|控制组件在 pack 分配的空间中的位置"n", "ne", "e", "se", "s", "sw", "w", "nw", 或者 "center" 来定位（ewsn 代表东西南北，上北下南左西右东）,默认值是 "center"|
|expand|是否填充父组件的额外空间，默认值是 False|
|fill|指定填充 pack 分配的空间,默认值是 NONE，表示保持子组件的原始尺寸,还可以使用的值有："x"（水平填充），"y"（垂直填充）和 "both"（水平和垂直填充）|
|in_|将该组件放到该选项指定的组件中
指定的组件必须是该组件的父组件|
|ipadx|  水平方向上的内边距|
|ipady|  垂直方向上的内边距|
|padx| 水平方向上的外边距|
|pady| 垂直方向上的外边距|
|side| 指定组件的放置位置,默认值是 "top",还可以设置的值有："left"，"bottom"，"right"|

3. place(), 就是给精确的坐标来定位  

        tk.Label(window, text='Pl', font=('Arial', 20), ).place(x=50, y=100, anchor='nw')
        #此处给的(50, 100)，就是将这个部件放在坐标为(x=50, y=100)的这个位置, 后面的参数 anchor='nw'，就是前面所讲的锚定点是西北角。

|选项|含义|
|-|-|
|anchor|1.控制组件在 place 分配的空间中的位置<br>2."n", "ne", "e", "se", "s", "sw", "w", "nw", 或 "center" 来定位（ewsn代表东西南北，上北下南左西右东）<br>3.默认值是 "nw"|
|bordermode|1.指定边框模式（"inside" 或 "outside"）<br>2.默认值是 "inside"|
|height|指定该组件的高度（像素）|
|in_|1.将该组件放到该选项指定的组件中<br>2.指定的组件必须是该组件的父组件|
|relheight|1.指定该组件相对于父组件的高度<br>2.取值范围 0.0 ~ 1.0|
|relwidth|1.指定该组件相对于父组件的宽度<br>2.取值范围 0.0 ~ 1.0|
|relx|1.指定该组件相对于父组件的水平位置<br>2.取值范围 0.0 ~ 1.0|
|rely|1. 指定该组件相对于父组件的垂直位置<br>2. 取值范围 0.0 ~ 1.0|
|width|指定该组件的宽度（像素）|
|x|1. 指定该组件的水平偏移位置（像素）<br>2. 如同时指定了 relx 选项，优先实现 relx 选项|
|y|1. 指定该组件的垂直偏移位置（像素）<br>2. 如同时指定了 rely 选项，优先实现 rely 选项| 

### 控件的点击事件
声明控件时绑定一个点击事件:

    b = Button(root, text='按钮', command=clickhandler)

生成控件后绑定事件:
    
    控件.bind(('<event>', eventhandler, add='')

其中，<event>为事件类型，eventhandler为事件处理函数，可选参数add默认为''，表示事件处理函数替代其他绑定，如果为‘+’，则加入事件处理队列。

对某种类型进行事件绑定:

    c = Canvas(); c.bind_class('Canvas', '<Button-2>', eventhandler)

tkinter事件通常采用了将事件名称放置于尖括号内的字符串表示，尖括号中的内容我们称之为事件类型。
<[modifier-]…type[-detail]>
    方括号内的内容为可选参数
    modifier为组合键的定义，例如，同时按下Ctrl键；
    type为通用类型，例如，键盘按键（KeyPress）
    detail用于具体信息，如按下键盘中‘B’键

鼠标事件类型:
<Key>               随便一个按键，键值会以char的格式放入event对象。
<Button-1>          按下了鼠标左键        <ButtonPress-1>
<Button-2>          按下了鼠标中键        <ButtonPress-2>
<Button-3>          按下了鼠标右键        <ButtonPress-3>
<Enter>             鼠标进入组件区域
<Leave>             鼠标离开组件区域
<FocusIn>           控件获得焦点
<FocusOut>             控件失去焦点
<ButtonRelease-1>   释放了鼠标左键
<ButtonRelease-2>   释放了鼠标中键
<ButtonRelease-3>   释放了鼠标右键
<B1-Motion>          按住鼠标左键移动
<B2-Motion>          按住鼠标中键移动
<B3-Motion>          按住鼠标右键移动 
<Double-Button-1>   双击鼠标左键
<Double-Button-2>   双击鼠标中键
<Double-Button-3>   双击鼠标右键
<Button-4>        滚动鼠标滚轮 向上滚动
<Button-5>        滚动鼠标滚轮 向下滚动
注意： 如果同时绑定单击事件 (<Button-1>) 和双击事件 (<Double-Button-1>), 则两个回调都会被调用.

键盘事件类型:
<KeyPress>                       表示任何键盘按下
<KeyRelease>                   表示松开键盘任意按键
<KeyPress-A>                   表示按下键盘A键    A可以设置为其他的按键
<KeyRelease-A>               表示松开键盘A键    A可以设置为其他的按键
<Alt-KeyPress-A>             表示同时按下Alt和A键    A可以设置为其他的按键
<Control-KeyPress-A>      表示同时按下Ctrl和A键    A可以设置为其他的按键
<Shift-KeyPress-A>          表示同时按下Shift和A键    A可以设置为其他的按键
<Double-KeyPress-A>      表示双击键盘A键    A可以设置为其他的按键
<Lock-KeyPress-A>          表示开启大写之后键盘A键    A可以设置为其他的按键
<Alt-Control-KeyPress-A> 表示同时按下alt+Ctrl和A键    A可以设置为其他的按键
<Return>                键位绑定，回车键，其它还有<BackSpace>,<Escape>,<Left>,<Up>,<Right>,<Down>等等

控件属性改变事件:
<Configure>              重要:如果widget的大小改变了，或者是位置，新的大小（width和height）会打包到event发往handler。

窗口和组件相关事件类型
<Activate>           当中组件由不可以用变为可用时  针对于state的变值
<Deactivate>       当组件由可用变为不可用时触发 state=Tkinter.DISABLED
<Configure>        当组件大小发生变化时触发
<Destory>           当组件销毁时触发
<FocusIn>           当组件获取焦点时触发 针对于Entry和Text有效
<FocusOut>        组件失去焦点的时候触发
<Map>                 当组件由隐藏变为显示时触发
<UnMap>            当组件由显示变为隐藏时触发
<Perproty>          当窗口属性发生变化时触发

事件对象(这是事件方法隐藏携带的对象,一般写为event)中包含的信息:
x,y                     当前触发事件时鼠标相对触发事件的组件的坐标值
x_root,y_root    当前触发事件时鼠标相对于屏幕的坐标值
char                  获取当前键盘事件时按下的键对应的字符（仅键盘事件，string）
keycode            获取当前键盘事件时按下的键对应的的ascii码
type                  获取事件的类型
num                  获取鼠标按键类型  123 左中右(按钮num，仅鼠标事件)
widget              重要:触发事件的组件(产生event的实例，不是名字，所有对象拥有)
width/height     组件改变之后的大小和configure()相关（widget新大小）
type                 事件类型



#### 右键菜单
    #菜单功能一
    def right_click_connect():
    tkinter.messagebox.showinfo(title='Hi', message='连接！')
    #菜单功能二
    def right_click_disconnect():
    tkinter.messagebox.showinfo(title='Hi', message='断开！')
    #建立菜单
    menubar = tkinter.Menu(window,tearoff=False)#创建一个菜单
    menubar.add_command(label='连接',command=lambda: right_click_connect())#添加子菜单功能一
    menubar.add_command(label='断开',command=lambda: right_click_disconnect())#添加子菜单功能二
    #显示菜单的方法
    def right_click(event):
    menubar.post(event.x_root, event.y_root)
    #给某个控件添加右键菜单
    某种控件.bind("<Button-3>", lambda x: right_click(x))#<Button-3> 右键
#### 左键双击
    某种控件.bind("<Double-Button-1>",double_click(x)) #<Double-Button-1> 双击
#### 左键单击
    某种控件.bind("<Double-Button-1>",double_click(x)) #<Button-1> 单击,<Button-2>猜测是滚轮