# -*- coding: utf-8 -*-

import logging
import requests
import lxml.html
import pymongo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')



cookies = {
        # cookies has been hidden
        }

headers = {
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2,de;q=0.2,ko;q=0.2,mt;q=0.2',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://movie.douban.com/people/laixintao/collect?start=30&sort=time&rating=all&filter=all&mode=grid',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        }

if __name__ == '__main__':
    for index in range(490, 600, 15):
        params = (
                ('start', index),
                ('sort', 'time'),
                ('rating', 'all'),
                ('filter', 'all'),
                ('mode', 'grid'),
                )

        logging.info(index)
        page = requests.get('https://movie.douban.com/people/laixintao/collect', headers=headers, params=params, cookies=cookies)
        page_lxml = lxml.html.fromstring(page.content)
        movies = page_lxml.xpath("//div[@class='item']")
        mongo = pymongo.MongoClient()
        for movie in movies:
            name = movie.xpath(".//li[@class='title']/a")[0].text_content().strip()
            link = movie.xpath(".//li[@class='title']/a/@href")[0]
            try:
                tags = movie.xpath(".//span[@class='tags']")[0].text
            except:
                tags = ''
            comment = movie.xpath(".//span[@class='comment']")
            if comment:
                comment = comment[0].text
            else:
                comment = ''
            date = movie.xpath(".//span[@class='date']")[0].text
            star = movie.xpath(".//li[3]/span[1]/@class")
            print name, link, tags, comment, date, star
            mongo['douban']['movie'].update_one({'name': name},
                    {'$set': {'name': name,
                              'link': link,
                              'tags': tags,
                              'comment': comment,
                              'date': date,
                              'star': star}
                              },
                    upsert=True)

