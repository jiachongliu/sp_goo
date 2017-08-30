# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
        'scrapy.pipelines.images.ImagesPipeline': 1,
        }

import os
IMAGES_URLS_FIELD='front\_image\_url'
project_dir=os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE=os.path.join(project_dir, '存储图片文件名称')


class SpGooPipeline(object):
    def process_item(self, item, spider):
        return item
