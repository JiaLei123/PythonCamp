
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
# justwatch_com_netflix.py
#
# Purpose : #78360 Scrape new VoD streams (2)
#
# Ticket Link  : https://bn-fbdb01.nuance.com/default.asp?78360
#
# Jeff Jia , for Nuance Corporation, Chengdu, China
#
# Date Started: 18-8-2017
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
import time
import re


######################################################################

def preprocessHTML(inputHTML):
    try:
        inputHTML = inputHTML.decode('GB2312', 'ignore')
    except UnicodeDecodeError:
        raise BadHTMLError
    else:
        return inputHTML.encode('utf8')
#########################################################################
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
            title_div_list = soup.findAll("div", {'class': 'title'})
            if title_div_list:
                for title_div in title_div_list:
                    printToFile('', title_div.text)
    except Exception as e:
        print e


def add_next_page(addUrl, soup, url):
    page_num = soup.findAll(attrs={'class': 'page_num'})
    total_page_num = int(page_num[-1].text)
    next_url = '?'.join((url, 'offset='))
    for i in range(30, 30 * total_page_num, 30):
        new_next_url = next_url + str(i)
        addUrl(new_next_url, payload=['next_page'])





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
        default='/lm/data2/scrapers/zho-CHN/epg/zgpingshu.com.top100/log.inc/'
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
        default='/lm/data2/scrapers/zho-CHN/epg/zgpingshu.com.top100/log.inc/zgpingshu.com.top100.badUrls.lst',
        help='Prints unusable URLs to external file instead of halting the scraper.'
    )

    options, args = parser.parse_args()
    log = Logger(options.debug)

    if options.html:
        myScraper = HTMLScraper(
            scraperType=u'scrapers',
            topic=u'epg',
            lang=u'zho-CHN',
            name=u'zgpingshu.com.top100',
            frequency=u'versions'
        )
        myScraper.inputDataBall(options.html)
    else:
        myScraper = WebScraper(
            scraperType=u'scrapers',
            topic=u'epg',
            lang=u'zho-CHN',
            name=u'zgpingshu.com.top100',
            frequency=u'versions'
        )
        if options.robots:
            # set the robots.txt for the scraper
            myScraper.setRobotsTxt(url='http://www.zgpingshu.com/',
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

    myScraper.addOutputFile('', os.path.join(outputPath,
                                             myScraper.generateFileName(fileType='tsv', )),
                            noTemp=False
                            )
    # add the seed URL to the scraper
    myScraper.addUrl(
        u'http://www.zgpingshu.com/top100/',
        payload=['topUrl']
    )

    # start the scraping job
    try:
        log.info('Starting the scrape \n')
        if not options.restart:
            myScraper.printToFile('', u'#scraper01 Title')
        myScraper.run(
            processPage,
            siteEncoding='GB2312',
            HTMLpreprocessor=preprocessHTML,
            restart=options.restart,
            badUrlsFile=options.badUrlsFile
        )
        log.info('Finished the scrape \n')
    except StandardError, error:
        traceback.print_exc()
        log.error(error)
        if options.debug:
            raise
        sys.exit(2)
