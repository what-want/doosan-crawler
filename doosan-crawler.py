#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = "whatwant"
__date__   = "2017.04.09"


import sys
import json
import requests
from datetime import datetime

from bs4 import BeautifulSoup
from pprint import pprint


DoosanURL = "http://sports.news.naver.com/kbo/news/index.nhn?date=%(target_date)s&type=team&team=OB&page=%(page)s&isphoto=N"

# 긁어 올 URL
#URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055&aid=0000445667'
#URL = "http://sports.news.naver.com/kbo/news/index.nhn?date=20170409&type=team&team=OB&page=1"
 

# 크롤링 함수
def getDoosan( url, target_date ):

    TARGET = {
        'target_date' : target_date,
        'page'        : 1
    }

    ARTICLES = []
    break_flag = False
    raw_new = requests.get( (url % TARGET) )
    for page in range(2, 10):

        TARGET['page'] = page

        raw = raw_new
        raw_new = requests.get( (url % TARGET) )


        # 일반적인 텍스트를 짤라먹는 방식으로 구현... 좀 무식하게!
        rows = raw.text.split( 'newsListModel: {"list":[' )[1]
        rows = rows.split( '],"date":"' )[0].strip()

        if( len(rows) == 0 ):
            break

        rows_new = raw_new.text.split( 'newsListModel: {"list":[' )[1]
        rows_new = rows_new.split( '],"date":"' )[0]

        if( rows_new == rows ):
            break_flag = True

        rows = rows.split("},{")

        for row in rows:
            ARTICLE = {}
            items = row.split(',"')
            for item in items:
                contents = item.split('":')

                if( len(contents) != 2 ):
                    print "[ERROR] Wrong contents :", item
                    continue

                ARTICLE[ contents[0].replace('"', '') ] = unicode(contents[1].replace( '\\"', "'" ).replace('"', '')).encode('utf-8')

            ARTICLES.append( ARTICLE )

        if( break_flag ):
            break

    return ARTICLES
 
 


if __name__ == '__main__':

    today = datetime.now().strftime('%Y%m%d')

    if ( (len(sys.argv) > 1) and (sys.argv[1].isdigit()) ):
        target_date = sys.argv[1]
    else:
        target_date = today


    articles = getDoosan( DoosanURL, target_date )


    print "[INFO] article count =", len(articles)

    #for article in articles:
    #    for key in article.keys():
    #        print key, "=", article[key]
    #    print ""
    #exit()

    NEWSFILENAME = str(target_date) + ".json"

    with open(NEWSFILENAME, "w") as f:
        f.write( json.dumps(articles) )

    exit(0)
