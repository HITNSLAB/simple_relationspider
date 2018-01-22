# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import time
import MySQLdb
import MySQLdb.cursors
import os
import logging

a = int(time.time())


class UrlspiderPipeline(object):
    logger = logging.getLogger(__name__)

    def __init__(self):

        try:
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                                host=os.getenv('MYSQL_HOST', '172.29.152.203'),
                                                db=os.getenv('MYSQL_DB', 'fyspider'),
                                                user=os.getenv('MYSQL_USER', 'root'),
                                                passwd=os.getenv('MYSQL_PASSWORD', 'kasiluo203'),
                                                cursorclass=MySQLdb.cursors.DictCursor,
                                                charset='utf8',
                                                use_unicode=True
                                                )
            self.logger.info("Connect to db successfully!")

        except Exception as e:
            self.logger.error("Fail to connect to db!, exception '%s'" % e)

    def process_item(self, item, spider):
        sql = "insert ignore into biao4(url,flag,flag2,flag3) values(%s,%s,%s,%s) "
        param = (item['url'], item['flag'], item['flag2'], item['flag3'])

        sql2 = "insert into biao5(fromWhere,toWhere) values(%s,%s) "
        param2 = (item['fromWhere'], item['url'])

        self.dbpool.runOperation(sql, param)
        self.dbpool.runOperation(sql2, param2)
        # self.dbpool.runInteraction(self.insert_into_table, item)
        return item
        #
        # def insert_into_table(self, conn, item):
        #     sql = "insert ignore into biao4(url,flag,flag2,flag3) values(%s,%s,%s,%s) "
        #     param = (item['url'], item['flag'], item['flag2'], item['flag3'])
        #     conn.execute(sql, param)
        #
        #     sql2 = "insert into biao5(fromWhere,toWhere) values(%s,%s) "
        #     param2 = (item['fromWhere'], item['url'])
        #     conn.execute(sql2, param2)
