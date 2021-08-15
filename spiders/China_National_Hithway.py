#!/usr/bin/python2.6
# -*- coding: utf-8 -*-


from MyScraperUtil.MyScraperUtil import *



def processPage(soup, url=None, urlPayload=None, addUrl=None, addListOfUrls=None):
    urlLevel = urlPayload[0]
    if soup and urlLevel == 'topUrl':
        high_way_list = []

        high_way_div = soup.find("div", {"class": "divright"})

        # high way around beijing
        capital_high_way_list = high_way_div.findAll(name="span", attrs={"style": re.compile('^color')})
        for capital_high_way in capital_high_way_list:
            high_way_list.append(capital_high_way.text)

        # high way from north to south and from east to west
        high_way_header_list = high_way_div.findAll(name="h3")
        for high_way_header in high_way_header_list:
            if high_way_header.text == u'南北纵线' or high_way_header.text == u"东西横线":
                parse_nation_high_way(high_way_header, high_way_list, straight_line)
            if high_way_header.text == u"地区环线":
                parse_nation_high_way(high_way_header, high_way_list, loop_line)

        # high way around the city
        city_high_way_table = high_way_div.findAll("table")[-1]
        city_high_way_list = city_high_way_table.findAll("p")
        for city_high_way in city_high_way_list:
            city_high_way_str = city_high_way.text.split(" ")
            if len(city_high_way_str) > 1:
                city = city_high_way_str[0]
                high_way_code = city_high_way_str[1]
                high_way_name = high_way_code + u"，" + city + u"绕城高速"
                high_way_list.append(high_way_name)

        # summary and output
        if high_way_list:
            for str_high_way in high_way_list:
                high_way = str_high_way.split(u"，")
                code = high_way[0].strip()
                name = high_way[1].strip()
                record = '\t'.join([code, name])
                print record
                # printToFile('', record)


def parse_nation_high_way(high_way_header, high_way_list, parse_highway):
    high_way_ul = high_way_header.nextSibling
    national_high_way_list = high_way_ul.findAll('p')
    for national_high_way in national_high_way_list:
        if national_high_way.text:
            index_start = national_high_way.text.find(u"（")
            index_end = national_high_way.text.find(u"）")
            if index_start > 0 and index_end > 0:
                high_way = parse_highway(index_end, index_start, national_high_way)
                special_handel(high_way_list, high_way)


def straight_line(index_end, index_start, national_high_way):
    high_way = national_high_way.text[index_start + 1:index_end]
    return high_way


def special_handel(high_way_list, high_way):
    '''
    handel the high way name which like G3012/G3013	吐和高速 it need split it to two different line
    :param high_way_list
    :param high_way: 
    '''
    if high_way.find(u'/') > 0:
        high_way_str = high_way.split(u"，")
        if len(high_way_str) > 1:
            code = high_way_str[0]
            name = high_way_str[1]
            high_way_codes = code.split(u'/')
            if len(high_way_codes) > 1:
                for high_way_code in high_way_codes:
                    high_way_name = high_way_code + u"，" + name
                    high_way_list.append(high_way_name)
    else:
        high_way_list.append(high_way)


def loop_line(index_end, index_start, national_high_way):
    high_way_name = national_high_way.text[:index_start]
    high_way_code = national_high_way.text[index_start + 1:index_end]
    if high_way_code.endswith(u"高速"):
        high_way = high_way_code
    elif high_way_code == "G9411":
        high_way_name_index = high_way_name.find(u"－");
        first_name = high_way_name[high_way_name_index - 1:high_way_name_index]
        last_name = high_way_name[high_way_name_index + 1:high_way_name_index + 2]
        high_way = high_way_code + u"，" + first_name + last_name + u"高速"
    else:
        high_way = high_way_code + u"，" + high_way_name + u"高速"
    return high_way


if __name__ == '__main__':
    url = 'http://www.china-highway.com/Home/Alonepage/item/id/5.html'
    urlPayload = ["topUrl"]
    addUrl(url, urlPayload)
    run_scraper(processPage)
