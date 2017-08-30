# -*- coding: utf-8 -*-
import scrapy

import re
import datetime

from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['python.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        
        posts_nodes = response.xpath("//*[@id="archive"]/div[1]/div[2]/p[1]/a[1]")
        for post_node in post_nodes:
            image_url = post_node.xpath('//*[@id="archive"]/div[1]/div[1]/a/img').extract_first("")
            post_url = post_node.xpath('//*[@id="archive"]/div[1]/div[2]/span/p').extract_first("")

            yield Request(
                    url=parse.urljoin(response.url, post_url), 
                    meta={"front_image_url":image_url}, 
                    callback=self.parse_datail
                    )

        next_url = response.xpath('//*[@id="archive"]/div[21]/a[4]').extract_first("")  ##下一页(next page-numbers)
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)



