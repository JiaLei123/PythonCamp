import requests
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
pa = re.compile('(.*?):(.*)')

header = {}

try:
    f = open(r"headers.txt")

    for line in f.readlines():
        if pa.search(line):
            re_result = pa.search(line)
            header[re_result.group(1).strip()] = re_result.group(2).strip()
except:
    print "ssss"

print header

html = requests.get('http://www.tingroom.com/lesson/syysyd/', headers = header)

html.encoding='utf-8'

##rint html.text
title = re.findall('class="goog" target="_blank">(.*?)</a>', html.text, re.S)
for each in title:
    print each

