# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlspiderItem(scrapy.Item):
    # define the fields for your item here like:
    flag = scrapy.Field()
    url= scrapy.Field()
    fromWhere= scrapy.Field()
    flag2= scrapy.Field()
    flag3= scrapy.Field()
    pass
