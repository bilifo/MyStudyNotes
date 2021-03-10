xwings 安装:  

    pip install xlwings

xlwings导入:  

    import xlwings as xw

打开某个excel表:  

    wb = xw.Book("e:\example.xlsx") #注意这里使用"\"会打开失败,要用"//" 或者"\/" 或者"/"  或者 r"e:\example.xlsx". 使用 path.replace(r'\/'.replace(os.sep, ''), os.sep) 或者 os.path.abspath(path)

打开excel表中某个表单(sheet)对象:  

    sht = wb.sheets["sheet1"] #注意这里的"sheet1"应该是该表单对应的名字,不区分大小写
    或者
    sht = wb.sheets[0] #获取第一个表单

获取/设置/清除单元格值:

    sht.range('A1').value
    sht.range('A1:C3').value #获得A1到C3范围的值
    sht.range('A1').value = "xlwings"
    sht.range('A1').clear()
    或者
    sht.range((1,1)).value #直接得到1行1列的值
    sht.range((1,1),(3,3)).value
    或者
    sht.range('$D$9').value #通过 sht.range('A1').address获得的返回值'$D$9'
    sht.range('$D$9:$D$13').value

获得单元格的列标/行标:

    sht.range('A1').column
    sht.range('A1').row

获得单元格的列高/行宽:

    sht.range('A1').column_width
    sht.range('A1').row_height

列自适应/行自适应:

    sht.range('A1').columns.autofit()
    sht.range('A1').rows.autofit()

单元格获取/设置/清除颜色:

    sht.range('A1').color
    sht.range('A1').color = (34,139,34)
    sht.range('A1').color = None

输入公式，相应单元格会出现计算结果:

    sht.range('A1').formula='=SUM(B6:B7)'

获得单元格公式:

    sht.range('A1').formula_array

单元格中写入批量数据，只需要指定其实单元格位置即可:

    sht.range('A2').value = [['Foo 1', 'Foo 2', 'Foo 3'], [10.0, 20.0, 30.0]]

批量读取数据:

    sht.range('A2').expand().value

获得某个表单最后编辑单元的行列:
    sht.used_range.last_cell.row
    sht.used_range.last_cell.column
获得某个表单最后编辑单元的行列():
    sht.used_range.shape

获得某个表单所有单元的内容():
    sht.range('A1',sht.used_range.shape).value

在第一列前插入一行:
    sht.api.Rows(1).Insert()

行删除:
    sht.range('A3:A4').api.EntireRow.Delete()

列插入/删除:    
    sht1.range('c2').api.EntireColumn.Delete()  # 会删除 ’c2‘ 单元格所在的列。
    sht1.api.Columns(3).Insert()                # 会在第3列插入一列，原来的第3列右移。(也可以用列的字母表示)

判断是不是合并单元格:
    sht.Cells(1, 1).MergeCells

多选选中:
    sht.range('A1').expand()
    sht.range('A1').expand('right')
    sht.range('A1').expand().value  #显示多个单元格的值

更多:https://www.kancloud.cn/gnefnuy/xlwings-docs/1127474