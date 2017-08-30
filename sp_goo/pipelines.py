# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
import pymysql.cursors

from twisted.enterprise import adbapi



class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('192.168.0.106', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        self.cursors = self.conn.cursors()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES(%s, %s, %s, %s)
        """

        self.cursors.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def from_settings(cls, settings):
        dbparms = dict(
                host = settings["MYSQL_HOST"],
                db = settings["MYSQL_DBNAME"],
                user = settings["MYSQL_USER"],
                passwd = settings["MYSQL_PASSWORD"],
                charset = 'utf8',
                cursorclass = pymysql.cursors.DictCursor,
                use_unicode = True,
                )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursors, item):
        insert_sql, params = item.get_insert_sql()
        print(insert_sql, params)
        cursors.execute(insert_sql, params)

"""
class SpGooPipeline(object):
    def process_item(self, item, spider):
        return item
"""
