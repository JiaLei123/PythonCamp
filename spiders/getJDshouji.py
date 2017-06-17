#coding:utf-8
import requests
import re
from lxml import etree

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
        now_page = int(re.search('page=(\d+)', url, re.S).group(1))
        page_group = []
        for i in range(now_page, total_page+1):
            link = re.sub('page=\d+', 'page=%s' % i, url, re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self, tree):
        nodes = tree.xpath('//*[@id="plist"]/ul/li[1]')
        return nodes

    def geteveryclassfinfo(self, source):
        everyclassinfo = re.findall('<div class="p-name p-name-type3">.*?</div>', source, re.S)
        return everyclassinfo

    def getinfo(self, eachclass):
        info = {}
        info['title'] = re.search('<em>(.*?)</em>', eachclass, re.S).group(1)
        #info['price'] = re.search('<i>(.*?)</i>', eachclass, re.S).group(1).strip()
        #timeandLevel = re.findall('<em>(.*?)</em>', eachclass, re.S)
        #info['classtime'] = timeandLevel[0]
        #info['classlevel'] = timeandLevel[1]
        #info['leannum'] = re.search('<em class="learn-number">(.*?)</em>', eachclass, re.S).group(1).strip()
        return info

    def saveinfo(self, classinfo):
        f = open('jd.txt', 'a')
        for each in classinfo:
            f.writelines('商品名称: ' + each['title'] + '\n')
            #f.writelines('商品价格: ' + each['content'] + '\n')
            #f.writelines('课程时间: ' + each['classtime'] + '\n')
            #f.writelines('课程等级: ' + each['classlevel'] + '\n')
            #f.writelines('课程人数: ' + each['leannum'] + '\n')
            f.writelines("")
        f.close()


if __name__ == "__main__":
    classinfo = []
    url = 'https://list.jd.com/list.html?cat=9987,653,655&page=1'
    jikespider = spider()
    all_links = jikespider.changepage(url, 2)
    for link in all_links:
        print u"正在处理页面：" + link
        html = jikespider.getsource(link)
        tree = etree.HTML(html)
        everyclass = jikespider.geteveryclass(tree)
        for each in everyclass:
            #for eachinfo in each:
            info = jikespider.getinfo(each)
            classinfo.append(info)
    jikespider.saveinfo(classinfo)

