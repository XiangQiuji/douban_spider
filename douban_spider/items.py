# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanSpiderItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    summary = scrapy.Field()
    actors = scrapy.Field()
    types = scrapy.Field()
    release_time = scrapy.Field()
    src_url = scrapy.Field()
