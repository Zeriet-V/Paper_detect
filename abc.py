import docx
from docx.oxml import parse_xml
from docx.oxml.xmlchemy import serialize_for_reading
from docx.oxml.ns import nsmap, qn

doc = docx.Document(r'D:\pyproject\paper_detect\template\test.docx')

for p in doc.paragraphs:
#     print("段落内容：", p.text)
    print("段落样式名称：", p.style.name)
    print('常规手段字体名称：', p.style.font.name)
    p_rpr = p.style.element.xpath('w:rPr')[0]
    # print(p_rpr[0].xml)
    if p_rpr.xpath('w:rFonts'):
        try:
        # 一般字体在w:ascii中，中文样式的字体可能在w:eastAsia
        # 找不到的话print一下p_rpr[0].xml找找关于字体信息在哪
            print("段落字体：", p_rpr.xpath('w:rFonts')[0].attrib[qn("w:eastAsia")])
        except:
            print("段落字体：", p_rpr.xpath('w:rFonts')[0].attrib[qn("w:ascii")])
