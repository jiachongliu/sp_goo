# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse


from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from sp_goo.items import JobBoleArticleItem,ArticleItemLoader
from sp_goo.function import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ["python.jobbole.com"]
    start_urls = ['http://python.jobbole.com/all-posts/']


    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))


    def parse(self, response):

        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")
        
        post_nodes = response.xpath('//*[@id="archive"]/div/div[1]/a')
        for post_node in post_nodes:
            image_url = post_node.xpath('img/@src').extract_first('')
            article_url = post_node.xpath('@href').extract_first('')

            yield Request(
                    url=parse.urljoin(response.url, article_url), 
                    meta={"front_image_url":image_url}, 
                    callback=self.parse_datail
                    )

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first('')  ##下一页(next page-numbers)
        if next_page:
            yield Request(url=parse.urljoin(response.url, next_page), callback=self.parse)



    def parse_detail(self, response):
        front_image_url = response.meta.get('front_image_url', '')
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_xpath('create_date', '//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_xpath('praise_nums', '//div[@class="post-adds"]/span/h10/text()')
        item_loader.add_xpath('comment_nums', '//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('fav_nums', '//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_xpath('tags', '//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath('content', '//div[@class="entry"]')

        article_item = item_loader.load_item()
        yield article_item

