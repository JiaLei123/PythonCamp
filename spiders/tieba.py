#coding:utf8
import requests
import re

#url = 'http://tieba.baidu.com/f?ie=utf-8&kw=python'
url = 'http://www.jikexueyuan.com/course/?pageNum=1'

html = requests.get(url)
html.encoding='utf-8'
#print html.text


##rint html.text
title = re.search('<h2 class="lesson-info-h2"><a .* target="_blank" jktag=".*">(.*?)</a>', html.text, re.S)
print title
#for each in title:
 #   print each