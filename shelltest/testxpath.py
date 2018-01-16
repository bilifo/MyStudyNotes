import os
from lxml import etree
def openXML(path:str):
    with open(path,"rb+") as fd:
        # print(""+fd.read())
        str1=fd.read()
        xml_file = etree.HTML(str1.lower())
        # listsz= xml_file.xpath('//a/@a1')
        listsz = xml_file.xpath('//')
        print( listsz)
        # print(xml_file)


openXML("C:/Users/PanJunLong/Desktop/shelltest/fragment_time.xml")
# openXML("C:/Users/PanJunLong/Desktop/shelltest/testxml.xml")