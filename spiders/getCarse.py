#coding:utf-8
import requests
import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u"开始爬去内容。。。"

    def getsource(self, url):
        html = requests.get(url)
        return html.text

    def changepage(self, url, total_page):
        now_page = int(re.search('pageNum=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page+1):
            link = re.sub('pageNum=\d+', 'pageNum=%s' % i, url, re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self, source):
        everyclass = re.findall('<div class="lesson-infor" style="height: 88px;">.*?</div>', source, re.S)
        return everyclass

    def geteveryclassfinfo(self, source):
        everyclassinfo = re.findall('<div class="lesson-infor" style="height: 88px;">.*?</div>', source, re.S)
        return everyclassinfo

    def getinfo(self, eachclass):
        info = {}
        info['title'] = re.search('target="_blank" jktag=".*">(.*?)</a>', eachclass, re.S).group(1)
        info['content'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>', eachclass, re.S).group(1).strip()
        timeandLevel = re.findall('<em>(.*?)</em>', eachclass, re.S)
        info['classtime'] = timeandLevel[0]
        info['classlevel'] = timeandLevel[1]
        info['leannum'] = re.search('<em class="learn-number">(.*?)</em>', eachclass, re.S).group(1).strip()
        return info

    def saveinfo(self, classinfo):
        f = open('info.txt', 'a')
        for each in classinfo:
            f.writelines('课程名称: ' + each['title'] + '\n')
            f.writelines('课程内容: ' + each['content'] + '\n')
            f.writelines('课程时间: ' + each['classtime'] + '\n')
            f.writelines('课程等级: ' + each['classlevel'] + '\n')
            f.writelines('课程人数: ' + each['leannum'] + '\n')
            f.writelines("")
        f.close()


if __name__ == "__main__":
    classinfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider()
    all_links = jikespider.changepage(url, 2)
    for link in all_links:
        print u"正在处理页面：" + link
        html = jikespider.getsource(link)
        everyclass = jikespider.geteveryclass(html)
        for each in everyclass:
            #for eachinfo in each:
            info = jikespider.getinfo(each)
            classinfo.append(info)
    jikespider.saveinfo(classinfo)

