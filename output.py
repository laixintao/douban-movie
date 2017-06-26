# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import pymongo


mongo = pymongo.MongoClient()
db_coll = mongo['douban']['movie']

counter = 0
for movie in db_coll.find().sort('_id', -1):
    counter += 1
    name = re.sub(r'[\n\t ]+', ' ', movie['name'])
    comment = movie.get('comment') or '无评论'
    try:
        star = re.match(r'rating(\d)-t', movie['star'][0]).group(1)
    except:
        star = '-'
    tags = movie.get('tags') or ''
    print '{}. <a href="{}">《{}》</a>， {}\n{}星: {}({})\n\n'.format(counter, movie['link'], name,
            tags, star, comment, movie['date']).encode('utf-8')
