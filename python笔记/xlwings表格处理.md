xwings安装:  

    pip install xlwings

xlwings导入:  

    import xlwings as xw

打开某个excel表:  

    wb = xw.Book("e:\example.xlsx")

打开excel表中某个表单(sheet)对象:  

    sht = wb.sheets["sheet1"] #注意这里的"sheet1"应该是该表单对应的名字,不区分大小写

获取/设置/清除单元格值:

    sht.range('A1').value
    sht.range('A1').value = "xlwings"
    sht.range('A1').clear()

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

