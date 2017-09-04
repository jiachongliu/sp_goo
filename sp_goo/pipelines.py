# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class ArticleImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        try:
            if "front_image_url" in item:
                for ok, value in results:
                    image_file_path = value["path"]
                item["front_image_path"] = image_file_path
            return item
        except Exception as e:
            print(e)
            item["front_image_path"] = "图片不可用"
            return item



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

        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
       # print(insert_sql, params)
        cursor.execute(insert_sql, params)

"""
class SpGooPipeline(object):
    def process_item(self, item, spider):
        return item
"""
