# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import os


class ConspiderPipeline(object):
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
            print "Connect to db successfully!"

        except:
            print "Fail to connect to db!"

    def process_item(self, item, spider):
        # self.dbpool.runInteraction(self.insert_into_table, item)
        sql = "insert into biao6(title,head,body,real_url,get_url) values(%s,%s,%s,%s,%s)"
        param = ([item['title'], item['head'], item['body'], item['real_url'], item['get_url']])
        sql2 = "update biao4 set flag=%s where url=%s"
        param2 = ("1", item['get_url'])
        self.dbpool.runOperation(sql, param)
        self.dbpool.runOperation(sql2, param2)
        return item

        # def insert_into_table(self, conn, item):
        #
        #     sql = "insert into biao6(title,head,body,real_url,get_url) values(%s,%s,%s,%s,%s)"
        #     param = ([item['title'], item['head'], item['body'], item['real_url'], item['get_url']])
        #     conn.execute(sql, param)
        #     sql2 = "update biao4 set flag=%s where url=%s"
        #     param2 = ("1", item['get_url'])
        #     conn.execute(sql2, param2)
        #     # a='UPDATE grabsite set title='+item['title']+',head='+item['head']+',body='+item['body']+' where siteName ='+item['Url']
        #     # conn.execute(a)
