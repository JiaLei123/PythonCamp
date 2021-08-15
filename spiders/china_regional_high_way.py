#!/usr/bin/python2.6
# -*- coding: utf-8 -*-


from MyScraperUtil.MyScraperUtil import *


high_way_list = []


def preprocessHTML(inputHTML):
    try:
        inputHTML = inputHTML.decode('gb2312','ignore')
    except UnicodeDecodeError:
        raise BadHTMLError
    else:
        return inputHTML.encode('utf8')

def processPage(soup, url=None, urlPayload=None, addUrl=None, addListOfUrls=None):
    if soup:
        if urlPayload == 'topUrl':
            province_high_way = soup.findAll("div", {"class":"roadTxt"})
            if province_high_way:
                high_way_links = province_high_way[1].findAll('a')
                if high_way_links:
                    for high_way_link in high_way_links:
                        if high_way_link.has_key('href') and high_way_link['href'] != "#":
                            addUrl(url + high_way_link['href'], 'highWay')
                            print url + high_way_link['href']
        print "parse url: " + url + " payLoad: " + urlPayload
        if urlPayload == 'highWay':
            high_way_div_list = soup.findAll("div", {"class": "box bd"})
            if high_way_div_list:
                for high_way_div in high_way_div_list:
                    high_way_name_header = high_way_div.findAll('h2')
                    if high_way_name_header:
                        high_way_name = high_way_name_header[0].text[3:]
                        if not high_way_name.endswith(u"高速"):
                            high_way_name = high_way_name + u"高速"
                        if high_way_name not in high_way_list:
                            high_way_list.append(high_way_name)
                            print high_way_name.encode('utf8', 'ignore')


if __name__ == '__main__':
    url = 'http://gs.cngaosu.com/'
    urlPayload = "topUrl"
    #debug
    url = 'http://gs.cngaosu.com/gaosuluduan/difang/gansu/'
    urlPayload = "highWay"
    addUrl(url, urlPayload)
    run_scraper(processPage, preprocessHTML, websiteEncoding="GB2312")
