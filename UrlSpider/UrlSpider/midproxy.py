# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
import random
import urllib2
import redis
import logging
import os
from scrapy.http import Request

from .settings import STATIC_PROXY


# Start your middleware class
class StaticProxyMiddleware(object):
    # overwrite process request
    proxy_ip = STATIC_PROXY

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        if self.proxy_ip:
            request.meta['proxy'] = self.proxy_ip
            self.logger.info('Current used proxy: %s' % self.proxy_ip)


            # # Start your middleware class
            # class ProxyMiddleware(object):
            #     # overwrite process request
            #     provider = None
            #
            #     def __init__(self):
            #         self.logger = logging.getLogger(__name__)
            #
            #     def process_request(self, request, spider):
            #         if not ProxyMiddleware.provider:
            #             ProxyMiddleware.provider = redis.Redis(host=spider.settings.get('PROXY_PROVIDER_HOST'),
            #                                                    port=spider.settings.get('PROXY_PROVIDER_PORT'))
            #
            #         fetched = ProxyMiddleware.provider.rpop('ip_list')
            #
            #         if fetched:
            #             proxy_ip = "http://%s" % fetched
            #             request.meta['proxy'] = proxy_ip
            #             self.logger.info('Current used proxy: %s' % proxy_ip)
