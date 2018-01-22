import scrapy
import MySQLdb
from ConSpider.items import ConspiderItem
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re
import os


class contentSpider(scrapy.Spider):
    name = "contentSpider"

    def __init__(self, **kwargs):
        super(contentSpider, self).__init__(**kwargs)
        try:
            self.conn = MySQLdb.connect(
                host=os.getenv('MYSQL_HOST', '172.29.152.203'),
                db=os.getenv('MYSQL_DB', 'fyspider'),
                user=os.getenv('MYSQL_USER', 'root'),
                passwd=os.getenv('MYSQL_PASSWORD', 'kasiluo203'),
                charset='utf8'
            )
            self.logger.info("Connect to db successfully!")
            self.cur = self.conn.cursor()
            self.cur.execute("select url from biao4 where flag3=0 limit 1")
            self.willstart = self.cur.fetchone()[0]
            self.cur.execute('update biao4 set flag3="1" where url="' + self.willstart + '"')

            self.conn.commit()
            self.start_urls.append(self.willstart)
        except Exception as e:
            self.logger.error("Fail to connect to db!, exception '%s'" % e)

    def parse(self, response):
        item = ConspiderItem()
        item['get_url'] = self.willstart
        url = self.willstart

        yield Request(url, meta={'key': item}, callback=self.parse_page1, errback=self.errback_httpbin,
                      dont_filter=True)

    def parse_page1(self, response):

        item = response.meta['key']

        item['title'] = response.xpath('/html/head/title').re(u'[\u4e00-\u9fa5]')
        item['head'] = response.xpath('/html/head').re(u'[\u4e00-\u9fa5]')
        item['body'] = response.xpath('/html/body').re(u'[\u4e00-\u9fa5]')
        item['body'] = ''.join(item['body'])
        item['head'] = ''.join(item['head'])
        item['title'] = ''.join(item['title'])
        item['real_url'] = response.url
        yield item
        cur = self.conn.cursor()

        cur.execute("select url from biao4 where flag3=0 limit 1")
        self.willstart = cur.fetchone()[0]
        self.logger.info("willstart = %s" % self.willstart)

        cur.execute('update biao4 set flag3="1" where url="' + self.willstart + '"')
        self.conn.commit()

        str = 'update biao4 set flag3=1 where url="' + self.willstart + '"'
        self.logger.info(str)
        yield Request(self.willstart, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)

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
        cur.execute("select url from biao4 where flag3=0 limit 1")
        self.willstart = cur.fetchone()[0]
        self.logger.info("willstart = %s" % self.willstart)

        cur.execute('update biao4 set flag3="1" where url="' + self.willstart + '"')
        self.conn.commit()

        str = 'update biao4 set flag3=1 where url="' + self.willstart + '"'
        self.logger.info(str)
        yield Request(self.willstart, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)
