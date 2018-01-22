import os
from lxml import etree
def openXML(path:str):
	with open(path,"rb+") as fd:
        # print(""+fd.read())
		str1=fd.read()
		print(str1)
		xml_file = etree.HTML(str1.lower())
		print(xml_file)
		listsz= xml_file.xpath(r'//a/@a3:a4')
		#listsz = xml_file.xpath('//*/(@android:id)')
		print( listsz)
        # print(xml_file)

def openXML2(path:str):
	str1=open(path,"rb+").read()
	xml_file = etree.HTML(str1)
	print(xml_file)

#openXML("C:/Users/PanJunLong/Desktop/shelltest/fragment_time.xml")
openXML("C:/数据和文档/git项目/MyStudyNotes/shelltest/testxml.xml")
#openXML2("C:/数据和文档/git项目/MyStudyNotes/shelltest/fragment_time.xml")