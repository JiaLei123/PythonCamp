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
# v_qq_com_movie.py
#
# Purpose : #81102 Scrape media and app content for Xiaomi
#
# Ticket Link  : https://bn-fbdb01.nuance.com/f/cases/81102
#
# Jeff Jia , for Nuance Corporation, Chengdu, China
#
# Date Started: 1-9-2017
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
import requests
import json
import re

#########################################################################
total_list = []
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
            parse_movie(soup)
            # get next page
            # for debug mode not need get next page data
            if not run_small:
                add_next_page(addUrl, soup, url)


        if urlPayload[0] == "next_page":
            parse_movie(soup)
    except Exception as e:
        print e


def add_next_page(addUrl, soup, url):
    page_num = soup.findAll(attrs={'class': 'page_num'})
    total_page_num = int(page_num[-1].string)
    next_url = '?'.join((url, 'offset='))
    for i in range(30, 30 * total_page_num, 30):
        new_next_url = next_url + str(i)
        addUrl(new_next_url, payload=['next_page'])


def parse_movie(soup):
    movies_soup = soup.findAll(attrs={'class': 'list_item'})
    for movie_soup in movies_soup:
        title = ((movie_soup.find(attrs={'class': 'figure_title'})).find('a')).string.strip()
        title = re.sub(u'（.*?版）', '', title)
        movie_desc = movie_soup.find(attrs={'class': 'figure_desc'})
        if movie_desc:
            actors_list = movie_desc.findAll('a')
            actors = ','.join([actor.string.strip() for actor in actors_list])
        else:
            actors = ''

        movie_figure = movie_soup.find("a", {"class": "figure"})
        data_float = movie_figure.attrMap['data-float']
        movie_year, movie_type = get_movie_detail(data_float)

        movie_score = movie_soup.find(attrs={'class': 'figure_score'})
        if movie_score:
            score_major = movie_score.find("em", {"class": "score_l"})
            score_minor = movie_score.find("em", {"class": "score_s"})
            score = score_major.string + score_minor.string
        else:
            score = ''

        movie_play_count = movie_soup.find(attrs={'class': 'figure_count'})
        if movie_play_count:
            play_count = movie_play_count.find("span", {"class": "num"}).string.strip()
        else:
            play_count = ''

        each_list = list()
        each_list.append(title)
        each_list.append(actors)
        each_list.append(score)

        if not play_count:
            play_count = '0'

        if u'万' in play_count:
            play_count_int = int(play_count[:-1]+'0000')
        elif u'亿' in play_count:
            play_count_int = int(play_count[:-1]+'00000000')
        else:
            play_count_int = int(play_count)
        each_list.append(play_count_int)
        each_list.append(movie_year)
        each_list.append(movie_type)
        total_list.append(each_list)


def get_movie_detail(data_float):
    movie_year = ''
    movie_type = ''
    try:
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) '
                                 'Gecko/20100101 Firefox/22.0'}
        query_url = u"http://node.video.qq.com/x/api/float_vinfo2"
        params = {"cid": data_float}
        print 'get detail data from: ', query_url, 'with parameter ', params
        response = requests.get(query_url, headers=headers, params=params, timeout=20)

        if response.status_code == 200:
            try:
                movie_detail = json.loads(response.text)
            except Exception as e:
                print e
            else:
                movie_year = movie_detail['c']['year']
                if len(movie_detail['typ']) > 0:
                    type_json = movie_detail['typ'][0]
                    if isinstance(type_json, list):
                        movie_type = ','.join(type_json)
                    else:
                        movie_type = type_json
        else:
            print 'fail to get data for: ', data_float
    except Exception as ex:
        print ex
    return movie_year, movie_type

###############################################################################

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
        default='/lm/data2/scrapers/zho-CHN/movies/v.qq.com.movie/log.inc/'
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
        default='/lm/data2/scrapers/zho-CHN/movies/v.qq.com.movie'
                '/log.inc/v.qq.com.movie.badUrls.lst',
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
            topic=u'movies',
            lang=u'zho-CHN',
            name=u'v.qq.com.movie',
            frequency=u'versions'
        )
        myScraper.inputDataBall(options.html)
    else:
        myScraper = WebScraper(
            scraperType=u'scrapers',
            topic=u'movies',
            lang=u'zho-CHN',
            name=u'v.qq.com.movie',
            frequency=u'versions'
        )
        if options.robots:
            # set the robots.txt for the scraper
            myScraper.setRobotsTxt(url='http://v.qq.com/movie/',
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
        u'http://v.qq.com/x/list/movie',
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

        sorted_list = sorted(total_list, key=lambda x: x[3], reverse=True)

        if len(sorted_list) > 1:
            op = OpenFile(output_file, 'a', encoding='utf-8')
            if not options.restart:
                header = [u'title_movie',
                          u'name_actor_csv',
                          u'number_rating',
                          u'number_downloads',
                          u'date_year',
                          u'category']
                op.write(u'#scraper01 ' + u'\t'.join(header))
                op.write('\n')
            for i in sorted_list:
                record = '\t'.join([i[0], i[1], i[2], str(i[3]), i[4], i[5]])
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
