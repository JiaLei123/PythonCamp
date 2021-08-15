#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

######################################################################
#                                                                    #
# Trade secret and confidential information of                       #
# Nuance Communications, Inc.                                        #
#                                                                    #
# Copyright (c) 2001-2017 Nuance Communications, Inc.                #
# All rights reserved.                                               #
#                                                                    #
# Copyright protection claimed includes all forms and matters of     #
# copyrightable material and information now allowed by statutory or #
# judicial law or hereinafter granted, including without limitation, #
# material generated from the software programs which are displayed  #
# on the screen such as icons, screen display looks, etc.            #
#                                                                    #
######################################################################

######################################################################
#
# iqiyi_tv.py
#
# Purpose : #81102 Scrape media and app content for Xiaomi
#
# Ticket Link  : https://bn-fbdb01.nuance.com/f/cases/81102
#
# Jeff Jia , for Nuance Corporation, Chengdu, China
#
# Date Started: 5-9-2017
#
# Modules:
#
# Revision History:
#
#####################################################################


try:
    import lmtoolspath
except ImportError:
    pass

import os
import sys
from optparse import OptionParser
from lmscraperkit_v02 import *
import traceback
from lmtoolkit import Logger
import re
import requests

#########################################################################
total_list = list()
run_small = False


def processPage(soup, url, urlPayload, addUrl, addListOfUrls, printToFile):
    """
    Grab the text from the page as well as links to
    subsequent pages.

    Keyword arguments:
    soup        -- BeautifulSoup parsing of webpage
    url         -- URL of the webpage
    urlPayload  -- payload to carry information across webpage scrapes
    addUrl      -- function that adds to the list of URLs to scrape
    printToFile -- function that prints text to a file
stock
    """
    try:
        if urlPayload[0] == "topUrl":
            total_page = 30
            for p in range(1, total_page + 1):
                tv_page_url = u"http://list.iqiyi.com/www/2/-------------11-" + str(p) + u"-1-iqiyi--.html"
                addUrl(tv_page_url, payload=["tv_page"])
                # for samll run only need get first page data
                if run_small:
                    break

        if urlPayload[0] == "tv_page":
            p_page_tv_ul = soup.findAll('ul', attrs={'class': 'site-piclist site-piclist-180236 site-piclist-auto'})
            p_page_tv_list = p_page_tv_ul[0].findAll('li')
            for i in range(len(p_page_tv_list)):
                tv_title_info = p_page_tv_list[i].find('p', attrs={'class': 'site-piclist_info_title '})
                tv_url = tv_title_info.find('a')['href']
                addUrl(tv_url, payload=["tv_url_page", tv_title_info.find('a').string.strip()])

        if urlPayload[0] == "tv_url_page":
            parse_tv_url_page(soup, urlPayload[1])

    except Exception as e:
        print "Error Happened: ", e


def parse_tv_url_page(soup, tv_title):
    # print soup
    scr = soup.findAll('script')
    # print len(scr)
    ids = re.findall(r"albumId:(.+?),", str(scr[4]))
    id = ''
    if len(ids)!=0:
        id = ids[0]
    url = 'http://up-video.iqiyi.com/ugc-updown/quud.do?dataid='+ id +\
          '&type=1&userid='
    response = requests.get(url)
    scoreinfo = response.text
    scores = re.findall(r"score\":(.+?),", str(scoreinfo))
    score = '0'
    if len(scores)!=0:
        score = scores[0]

    area = ''
    vv = '0'
    director = ''
    language = ''
    year = ''
    artist = ''
    type = ''
    tv_info = soup.findAll('div', attrs={'class': 'info-intro'})
    # style 1
    if len(tv_info)!=0:
        # tv_titles = tv_info[0].find("h1").contents[1].string.strip()
        # if u'立即播放' in tv_titles:
        #     tv_title=tv_titles[:-4]
        # else:
        #     tv_title = tv_titles

        pvnum = soup.findAll('span', attrs={'class': 'effrct-PVNum'})

        if len(pvnum) != 0:
            vv = pvnum[0].string.strip()[:-2]

        area_info = soup.findAll('p', attrs={'class': 'episodeIntro-area'})

        if len(area_info)!=0:
            area = area_info[0].find('a').string.strip()

        dir_info = soup.findAll('p', attrs={'class': 'episodeIntro-director'})

        if len(dir_info)!=0:
            director = dir_info[0].find('a').string.strip()

        type_infos = soup.findAll('p', attrs={'class': 'episodeIntro-type'})

        if len(type_infos)!=0:
            type_info = type_infos[0].findAll('a')
            if len(type_info)!= 0:
                type = ','.join([type_name.string.strip() for type_name in type_info])

        lang_infos = soup.findAll('p', attrs={'class': 'episodeIntro-lang'})

        if len(lang_infos) != 0:
            lang_info = lang_infos[0].findAll('a')
            if len(lang_info) != 0:
                if len(lang_info)<2:
                    year = lang_info[0].string.strip()
                else:
                    language = lang_info[0].string.strip()
                    year = lang_info[1].string.strip()

        artist_infos = soup.findAll('ul', attrs={'class': 'headImg-7575 clearfix'})

        if len(artist_infos) != 0:
            artist_info = artist_infos[0].findAll('li')
            if len(artist_info) != 0:
                for i in range(len(artist_info)):
                    art = artist_info[i].findAll('p', attrs={'class': 'headImg-bottom-title'})
                    artist = artist + art[0].find('a').string.strip() + ','
    # style 2
    else:
        msg_div = soup.find("div", {"class": "album-msg"})
        pvnum = msg_div.find('i', attrs={'id': 'widget-playcount'})
        vv = pvnum.string.strip()

        mini_info = msg_div.findAll('p', attrs={'class': 'li-mini'})

        if len(mini_info) != 0:
            area = mini_info[0].find('a').string.strip()
            language = mini_info[1].find('a').string.strip()
            director = mini_info[2].find('a').string.strip()

        mini_large_info = msg_div.findAll('p', attrs={'class': 'li-large'})
        if len(mini_large_info) != 0:
            type_infos = mini_large_info[0]
            type_info = type_infos.findAll('a')
            if len(type_info) != 0:
                type = ','.join([type_name.string.strip() for type_name in type_info])

            artist_infos = mini_large_info[1]
            artist_info = artist_infos.findAll('a')
            if len(artist_info) != 0:
                artist = ','.join([artist_name.string.strip() for artist_name in artist_info])

    each_list = []
    each_list.append(tv_title)
    each_list.append(artist[:-1])
    if u'万' in vv:
        vv = vv[:-1]
        vv = vv.split(".")
        if len(vv) > 1:
            play_count_int = int(vv[0]) * 10000 + int(vv[1]) * 1000
        else:
            play_count_int = int(vv[0]) * 10000
    elif u'亿' in vv:
        vv = vv[:-1]
        vv = vv.split(".")
        if len(vv) > 1:
            play_count_int = int(vv[0]) * 100000000 + int(vv[1]) * 10000000
        else:
            play_count_int = int(vv[0]) * 100000000
    else:
        play_count_int = int(vv)
    each_list.append(play_count_int)
    each_list.append(score)
    each_list.append(area)
    each_list.append(director)
    each_list.append(type)
    each_list.append(language)
    each_list.append(year)
    total_list.append(each_list)

################################################################################
usage = """

 python2.6 %prog [--debug] [--dateTag] [--restart]
 [--robots] [--basepath]

 <<NOTE>> basepath and robots should be set for other than /lm/data2/

"""
################################################################################

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option(
        '--basepath',
        '-b',
        dest='basepath',
        default='/lm/data2/')

    parser.add_option(
        '--restart',
        '-r',
        default=False,
        action='store_true',
        help='Restart the scraper from a previous incomplete run.'
    )

    parser.add_option(
        '--html',
        default=None,
        help='HTML databall that will be used as input'
    )

    parser.add_option(
        '--robots',
        default='/lm/data2/scrapers/zho-CHN/epg/iqiyi.com.dianshiju/log.inc/'
                'robots.txt.zip',
        help='robots.zip file'
    )

    parser.add_option(
        '--delay',
        type='int',
        dest='delay',
        default=2,
        help='specify delay in seconds between acessing web pages'
    )

    parser.add_option(
        '--debug',
        action='store_true',
        dest='debug',
        default=False,
        help='print status messages to stdout'
    )

    parser.add_option(
        '--dateTag',
        '-d',
        dest='dateTag',
        default=None,
        help='Date used for path creation; defaults to current date'
    )

    parser.add_option(
        '--badUrlsFile',
        dest='badUrlsFile',
        default='/lm/data2/scrapers/zho-CHN/epg/iqiyi.com.dianshiju'
                '/log.inc/iqiyi.com.dianshiju.badUrls.lst',
        help='Prints unusable URLs to external file instead of halting the scraper.'
    )
    parser.add_option(
        '--small',
        action='store_true',
        dest='run_small',
        default=False,
        help='if run spider by small data set, this is for debug.'
    )

    options, args = parser.parse_args()
    log = Logger(options.debug)
    if options.run_small:
        run_small = options.run_small

    if options.html:
        myScraper = HTMLScraper(
            scraperType=u'scrapers',
            topic=u'epg',
            lang=u'zho-CHN',
            name=u'iqiyi.com.dianshiju',
            frequency=u'versions'
        )
        myScraper.inputDataBall(options.html)

    else:
        myScraper = WebScraper(
            scraperType=u'scrapers',
            topic=u'epg',
            lang=u'zho-CHN',
            name=u'iqiyi.com.dianshiju',
            frequency=u'versions'
        )
        if options.robots:
            # set the robots.txt for the scraper
            myScraper.setRobotsTxt(url='http://www.iqiyi.com/',
                                   zip=options.robots)

    # Set the base path ...
    # over ride the default of /lm/data2 with the --basepath option
    myScraper.setBasePath(options.basepath)

    # Use the date specified at the command line if provided
    if options.dateTag:
        y, m, d = options.dateTag.split(u'_')
    else:
        # otherwise default to current date
        y, m, d = yearMonthDay()

    # if restarting scraper, set the rawDirectory
    if options.restart:
        myScraper.setRawDirectory(
            myScraper.generatePath(year=y, month=m, day=d, cleanState='raw')
        )

    outputPath = myScraper.generatePath(year=y, month=m, day=d,
                                        cleanState=u'records')

    output_file = os.path.join(outputPath, myScraper.generateFileName(fileType='tsv'))
    myScraper.addOutputFile('', output_file, noTemp=False)

    # add the seed URL to the scraper
    myScraper.addUrl(
        u'http://list.iqiyi.com/www/2/-------------11-0-1-iqiyi--.html',
        payload=['topUrl']
    )

    # start the scraping job
    try:
        log.info('Starting the scrape \n')

        myScraper.run(
            processPage,
            restart=options.restart,
            badUrlsFile=options.badUrlsFile
        )

        sorted_list = sorted(total_list, key=lambda x: x[2], reverse=True)
        if len(sorted_list) > 1:
            op = OpenFile(output_file, 'a', encoding='utf-8')
            if not options.restart:
                header = [u'epg_title',
                          u'name_actor_csv',
                          u'number_downloads',
                          u'number_rating',
                          u'address',
                          u'name_director',
                          u'category',
                          u'language',
                          u'date_year']
                op.write(u'#scraper01 ' + u'\t'.join(header))
                op.write('\n')
            for i in sorted_list:
                record = '\t'.join([i[0], i[1], str(i[2]), i[3], i[4], i[5], i[6], i[7], i[8]])
                op.write(record)
                op.write('\n')
            op.close()
        else:
            log.warning('Less output')

        log.info('Finished the scrape \n')
    except StandardError, error:
        traceback.print_exc()
        log.error(error)
        if options.debug:
            raise
        sys.exit(2)