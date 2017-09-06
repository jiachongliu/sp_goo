# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

def date_convert(value):
    create_date = value.replace('.', '').strip()
    return create_date

def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def return_value(value):
    return value



class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
            input_processor = MapCompose(date_convert)
            )

    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
            output_processor = MapCompose(return_value)
            )
    
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
            input_processor = MapCompose(get_nums)
            )

    comment_nums = scrapy.Field(
            input_processor = MapCompose(get_nums)
            )

    fav_nums = scrapy.Field(
            input_processor = MapCompose(get_nums)
            )

    tags = scrapy.Field(
            input_processor = MapCompose(remove_comment_tags),
            output_processor = Join(",")
            )
    content = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums,
            front_image_url, front_image_path, url_object_id, praise_nums,
            comment_nums, tags, content)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON
            DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """

        fron_image_url = ""
        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["title"], self["url"], self["create_date"],
                  self["fav_nums"], fron_image_url, self["front_image_path"],
                  self["url_object_id"], self["praise_nums"], self["comment_nums"], 
                  self["tags"], self["content"])

        return insert_sql, params
