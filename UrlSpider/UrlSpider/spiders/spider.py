# -*- coding: utf-8 -*-
import scrapy

import MySQLdb
from scrapy import Request
from urlparse import *
from UrlSpider.items import UrlspiderItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re
import os

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class UrlSpider(scrapy.Spider):
    name = "Url"

    def __init__(self, category=None, *args, **kwargs):
        super(UrlSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["%s" % category]
        self.conn = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST', '172.29.152.203'),
            db=os.getenv('MYSQL_DB', 'fyspider'),
            user=os.getenv('MYSQL_USER', 'root'),
            passwd=os.getenv('MYSQL_PASSWORD', 'kasiluo203'),
            port=3306,
            charset='utf8'
        )

    def parse(self, response):
        urls_list1 = re.findall(r'href="(https?://[^\[\]\<\>\"\']*?\.[^\[\]\<\>\"\']*?)"', response.body)
        urls_list2 = re.findall(r'href=\'(https?://[^\[\]\<\>\"\']*?\.[^\[\]\<\>\"\']*?)\'', response.body)
        urls_list1.extend(urls_list2)
        urls_list3 = []
        for url in urls_list1:
            netloc = urlparse(url)

            theurl = '%s%s%s' % (netloc.scheme, '://', netloc.hostname)
            urls_list3.append(theurl)
        s1 = list(set(urls_list3))
        for url in s1:
            item = UrlspiderItem()
            item['url'] = url
            item['flag'] = 0
            item['flag2'] = 0
            item['flag3'] = 0
            item['fromWhere'] = response.url

            yield item

        cur = self.conn.cursor()

        cur.execute("select url from biao4 where flag2=0 limit 1")
        willstart = cur.fetchone()[0]
        self.logger.info("willstart = %s" % willstart)

        cur.execute('update biao4 set flag2="1" where url="' + willstart + '"')
        self.conn.commit()

        qstr = 'update biao4 set flag2=1 where url="' + willstart + '"'
        self.logger.info(qstr)
        yield Request(willstart, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
        cur = self.conn.cursor()

        cur.execute("select url from biao4 where flag2=0 limit 1")
        willstart = cur.fetchone()[0]
        self.logger.info("willstart = %s" % willstart)

        cur.execute('update biao4 set flag2="1" where url="' + willstart + '"')
        self.conn.commit()

        str = 'update biao4 set flag2=1 where url="' + willstart + '"'
        self.logger.info(str)
        yield Request(willstart, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)
