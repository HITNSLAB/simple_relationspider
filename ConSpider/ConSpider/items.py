# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConspiderItem(scrapy.Item):
    title = scrapy.Field()
    head = scrapy.Field()
    body = scrapy.Field()
    get_url = scrapy.Field()
    real_url = scrapy.Field()
    pass
